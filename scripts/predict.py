#!/usr/bin/env python3
"""
End-to-End Prediction and Optimization Pipeline.
Given an unseen C/C++ program:
1. Generates LLVM IR
2. Extracts static IR features
3. Feeds features to trained ML model
4. Predicts best candidate pass sequence
5. Compiles with predicted sequence
6. Measures resulting code size
7. Compiles with -O2 and -Oz baselines
8. Displays side-by-side performance comparison
"""

import sys
import os
import argparse
import json
import time
from pathlib import Path
import pandas as pd
import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.experiment_runner.compiler import LLVMCompiler
from src.feature_extractor.extractor import LLVMFeatureExtractor, FEATURE_COLUMNS
from src.ml.models import PassSequencePredictor

def parse_args():
    parser = argparse.ArgumentParser(description="End-to-end ML optimization pass prediction")
    parser.add_argument("--source", "-s", required=True, help="Input C/C++ source file")
    parser.add_argument("--model", "-m", default="models/random_forest_pass_predictor.joblib", help="Trained model path")
    parser.add_argument("--candidates", "-c", default="candidates/candidates.json", help="Candidates JSON file")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--output-dir", default="experiments/predictions", help="Directory for prediction artifacts")
    return parser.parse_args()

def main():
    args = parse_args()
    config = {}
    if os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    src_path = Path(args.source)
    if not src_path.is_file():
        print(f"Error: Source file {args.source} not found.", file=sys.stderr)
        sys.exit(1)

    model_path = Path(args.model)
    if not model_path.is_file():
        print(f"Error: Trained model {args.model} not found. Please run scripts/train_model.py first.", file=sys.stderr)
        sys.exit(1)

    cand_path = Path(args.candidates)
    if not cand_path.is_file():
        print(f"Error: Candidates file {args.candidates} not found. Run scripts/generate_candidates.py first.", file=sys.stderr)
        sys.exit(1)

    with open(cand_path, "r", encoding="utf-8") as f:
        candidates_list = json.load(f)
    cand_lookup = {c["id"]: c for c in candidates_list}

    # Setup compiler
    env_cfg = config.get("environment", {})
    compiler = LLVMCompiler(
        clang_path=None if env_cfg.get("clang_path") == "auto" else env_cfg.get("clang_path"),
        opt_path=None if env_cfg.get("opt_path") == "auto" else env_cfg.get("opt_path"),
        llvm_size_path=None if env_cfg.get("llvm_size_path") == "auto" else env_cfg.get("llvm_size_path"),
        extra_clang_flags=env_cfg.get("extra_clang_flags")
    )

    ready, msg = compiler.is_ready()
    if not ready:
        print(f"Error: Compiler environment not ready ({msg}). Run scripts/check_environment.py.", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    prog_name = src_path.stem

    print("\n" + "=" * 65)
    print(f" LLVM ML OPTIMIZATION PREDICTION PIPELINE: {src_path.name}")
    print("=" * 65)

    # 1. Generate LLVM IR
    t_ir_start = time.perf_counter()
    base_ll = out_dir / f"{prog_name}_base.ll"
    ok, err = compiler.compile_to_ir(str(src_path), str(base_ll))
    if not ok:
        print(f"Failed to generate LLVM IR: {err}", file=sys.stderr)
        sys.exit(1)
    ir_time_ms = (time.perf_counter() - t_ir_start) * 1000.0
    print(f"Step 1: Generated LLVM IR -> {base_ll} ({ir_time_ms:.1f} ms)")

    # 2. Extract Features
    t_feat_start = time.perf_counter()
    extractor = LLVMFeatureExtractor()
    feat_dict = extractor.extract_from_file(str(base_ll), prog_name)
    feat_time_ms = (time.perf_counter() - t_feat_start) * 1000.0

    print(f"Step 2: Extracted {len(FEATURE_COLUMNS)} static IR features ({feat_time_ms:.1f} ms)")
    print(f"        Instructions: {feat_dict['instructions']}, Blocks: {feat_dict['basic_blocks']}, Branches: {feat_dict['branches']}, Loads/Stores: {feat_dict['loads']}/{feat_dict['stores']}")

    # 3. Model Inference
    t_inf_start = time.perf_counter()
    predictor = PassSequencePredictor.load(str(model_path))
    X_sample = np.array([[feat_dict.get(c, 0.0) for c in predictor.feature_names_]], dtype=np.float32)
    pred_cand_id = str(predictor.predict(X_sample)[0])
    top3_preds = predictor.predict_top_k(X_sample, k=3)[0]
    inf_time_ms = (time.perf_counter() - t_inf_start) * 1000.0

    pred_cand_info = cand_lookup.get(pred_cand_id, {"pipeline": pred_cand_id})
    print(f"Step 3: ML Model Inference ({inf_time_ms:.2f} ms)")
    print(f"        Predicted Best Sequence : {pred_cand_id} ({pred_cand_info['pipeline']})")
    print(f"        Top-3 Predictions       : {', '.join(top3_preds)}")

    # 4. Compile with Predicted Sequence
    ml_opt_ll = out_dir / f"{prog_name}_ml_{pred_cand_id}.ll"
    ml_obj = out_dir / f"{prog_name}_ml_{pred_cand_id}.o"

    t_ml_start = time.perf_counter()
    opt_ok, opt_time, opt_err = compiler.run_opt_pipeline(str(base_ll), str(ml_opt_ll), pred_cand_info["pipeline"])
    if not opt_ok:
        print(f"Error executing predicted pipeline: {opt_err}", file=sys.stderr)
        sys.exit(1)
    compiler.compile_ir_to_object(str(ml_opt_ll), str(ml_obj))
    ml_size, _ = compiler.measure_code_size(str(ml_obj))
    total_ml_compile_ms = (time.perf_counter() - t_ml_start) * 1000.0

    # 5. Compile with -O2 Baseline
    o2_opt_ll = out_dir / f"{prog_name}_O2.ll"
    o2_obj = out_dir / f"{prog_name}_O2.o"
    t_o2_start = time.perf_counter()
    compiler.run_opt_pipeline(str(base_ll), str(o2_opt_ll), "default<O2>")
    compiler.compile_ir_to_object(str(o2_opt_ll), str(o2_obj))
    o2_size, _ = compiler.measure_code_size(str(o2_obj))
    o2_time_ms = (time.perf_counter() - t_o2_start) * 1000.0

    # 6. Compile with -Oz Baseline
    oz_opt_ll = out_dir / f"{prog_name}_Oz.ll"
    oz_obj = out_dir / f"{prog_name}_Oz.o"
    t_oz_start = time.perf_counter()
    compiler.run_opt_pipeline(str(base_ll), str(oz_opt_ll), "default<Oz>")
    compiler.compile_ir_to_object(str(oz_opt_ll), str(oz_obj))
    oz_size, _ = compiler.measure_code_size(str(oz_obj))
    oz_time_ms = (time.perf_counter() - t_oz_start) * 1000.0

    # 7. Comparison and Metrics
    ml_vs_o2_pct = ((o2_size - ml_size) / o2_size * 100.0) if o2_size else 0.0
    ml_vs_oz_pct = ((oz_size - ml_size) / oz_size * 100.0) if oz_size else 0.0

    print("\n" + "=" * 65)
    print(" EVALUATION RESULTS")
    print("=" * 65)
    print(f"Program                 : {src_path.name}")
    print(f"Predicted Pipeline      : {pred_cand_id} -> [{pred_cand_info['pipeline']}]")
    print(f"ML Code Size            : {ml_size:,} bytes (Compile time: {total_ml_compile_ms:.1f} ms)")
    print(f"LLVM -O2 Baseline       : {o2_size:,} bytes (Compile time: {o2_time_ms:.1f} ms)")
    print(f"LLVM -Oz Baseline       : {oz_size:,} bytes (Compile time: {oz_time_ms:.1f} ms)")
    print("-" * 65)

    o2_symbol = "+" if ml_vs_o2_pct > 0 else ""
    oz_symbol = "+" if ml_vs_oz_pct > 0 else ""
    print(f"ML vs LLVM -O2          : {o2_symbol}{ml_vs_o2_pct:.2f}% size reduction ({o2_size - ml_size:+d} bytes)")
    print(f"ML vs LLVM -Oz          : {oz_symbol}{ml_vs_oz_pct:.2f}% size reduction ({oz_size - ml_size:+d} bytes)")

    if ml_size < o2_size and ml_size < oz_size:
        verdict = "WIN (ML produced smaller code than BOTH -O2 and -Oz!)"
    elif ml_size < o2_size:
        verdict = "WIN vs -O2 (ML produced smaller code than -O2)"
    elif ml_size < oz_size:
        verdict = "WIN vs -Oz (ML produced smaller code than -Oz)"
    elif ml_size == oz_size:
        verdict = "TIE with -Oz (ML matched smallest baseline)"
    else:
        verdict = "BASELINE WON (Standard pipeline achieved smaller size)"
    print(f"Outcome Verdict         : {verdict}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
