#!/usr/bin/env python3
"""
Full System Evaluation Script.
Evaluates ML-selected optimization pipelines against -O2 and -Oz on held-out test benchmarks.
Usage:
  python scripts/evaluate.py
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
from src.experiment_runner.runner import ExperimentRunner
from src.feature_extractor.extractor import LLVMFeatureExtractor
from src.ml.models import PassSequencePredictor
from src.evaluation.evaluator import EvaluationEngine

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate ML pass predictor on test programs")
    parser.add_argument("--test-dataset", default="dataset/dataset_test.csv", help="Test dataset CSV")
    parser.add_argument("--candidates", default="candidates/candidates.json", help="Candidates JSON file")
    parser.add_argument("--model", default="models/random_forest_pass_predictor.joblib", help="Trained ML model")
    parser.add_argument("--metrics", default="models/model_metrics.json", help="Metrics JSON from training")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    return parser.parse_args()

def main():
    args = parse_args()
    config = {}
    if os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    test_path = Path(args.test_dataset)
    if not test_path.is_file():
        print(f"Error: Test dataset {args.test_dataset} not found. Run scripts/build_dataset.py first.", file=sys.stderr)
        sys.exit(1)

    model_path = Path(args.model)
    if not model_path.is_file():
        print(f"Error: Trained model {args.model} not found. Run scripts/train_model.py first.", file=sys.stderr)
        sys.exit(1)

    cand_path = Path(args.candidates)
    if not cand_path.is_file():
        print(f"Error: Candidates file {args.candidates} not found.", file=sys.stderr)
        sys.exit(1)

    with open(cand_path, "r", encoding="utf-8") as f:
        candidates = json.load(f)
    cand_lookup = {c["id"]: c for c in candidates}

    # Setup compiler & runner
    env_cfg = config.get("environment", {})
    compiler = LLVMCompiler(
        clang_path=None if env_cfg.get("clang_path") == "auto" else env_cfg.get("clang_path"),
        opt_path=None if env_cfg.get("opt_path") == "auto" else env_cfg.get("opt_path"),
        llvm_size_path=None if env_cfg.get("llvm_size_path") == "auto" else env_cfg.get("llvm_size_path"),
        extra_clang_flags=env_cfg.get("extra_clang_flags")
    )
    runner = ExperimentRunner(compiler=compiler)

    # Load test dataset and model
    test_df = pd.read_csv(test_path)
    predictor = PassSequencePredictor.load(str(model_path))

    print("=" * 65)
    print(f" EVALUATING HELD-OUT TEST SUITE ({len(test_df)} UNSEEN PROGRAMS)")
    print("=" * 65)

    test_records = []
    eval_art_dir = Path("experiments/eval_test")
    eval_art_dir.mkdir(parents=True, exist_ok=True)

    for idx, row in test_df.iterrows():
        pid = row["program_id"]
        src = row["source_file"]
        pname = Path(src).stem

        # Extract features and predict
        feat_vals = [row.get(c, 0.0) for c in predictor.feature_names_]
        X_sample = np.array([feat_vals], dtype=np.float32)
        pred_cid = str(predictor.predict(X_sample)[0])
        pred_cand = cand_lookup.get(pred_cid, {"id": pred_cid, "pipeline": pred_cid})

        base_ir = Path("ir") / f"{pid}_{pname}.ll"
        if not base_ir.is_file():
            compiler.compile_to_ir(src, str(base_ir))

        # Evaluate ML predicted sequence
        ml_res = runner.evaluate_candidate(pid, str(base_ir), pred_cand)
        ml_size = ml_res["code_size"]

        # Baseline sizes
        o2_size = int(row["baseline_O2"])
        oz_size = int(row["baseline_Oz"])
        oracle_size = int(row["best_candidate_size"])
        oracle_cand = str(row["best_candidate"])

        print(f"[{pid}] ML: {pred_cid} ({ml_size} B) | O2: {o2_size} B | Oz: {oz_size} B | Oracle: {oracle_cand} ({oracle_size} B)")

        test_records.append({
            "program_id": pid,
            "name": pname,
            "source_file": src,
            "predicted_pass": pred_cid,
            "oracle_pass": oracle_cand,
            "size_O2": o2_size,
            "size_Oz": oz_size,
            "size_ML": ml_size,
            "size_oracle": oracle_size,
            "compile_time_ml_ms": ml_res.get("compile_time_ms", 0.0)
        })

    # Run evaluation engine
    engine = EvaluationEngine()
    summary = engine.evaluate_test_results(test_df, test_records)

    # Plot feature importances and model accuracy if metrics file exists
    if Path(args.metrics).is_file():
        with open(args.metrics, "r", encoding="utf-8") as f:
            metrics_dict = json.load(f)
        engine.generate_accuracy_plot(metrics_dict)
        rf_metrics = metrics_dict.get("random_forest", {})
        feat_imp = rf_metrics.get("train", {}).get("feature_importances", {})
        engine.generate_feature_importance_plot(feat_imp)

    print("\n" + "=" * 65)
    print(" SUMMARY EVALUATION REPORT")
    print("=" * 65)
    print(f"Average Code Size:")
    print(f"  - LLVM -O2          : {summary['avg_size_O2']:.1f} bytes")
    print(f"  - LLVM -Oz          : {summary['avg_size_Oz']:.1f} bytes")
    print(f"  - ML Predicted      : {summary['avg_size_ML']:.1f} bytes")
    print(f"  - Oracle (Best)     : {summary['avg_size_Oracle']:.1f} bytes")
    print(f"Average Size Reduction vs -O2 : {summary['avg_pct_reduction_vs_O2']:+.2f}%")
    print(f"Average Size Reduction vs -Oz : {summary['avg_pct_reduction_vs_Oz']:+.2f}%")
    print(f"Win Rate vs -O2               : {summary['vs_O2']['wins']}/{summary['total_test_programs']} ({summary['vs_O2']['win_rate_pct']}%)")
    print(f"Win Rate vs -Oz               : {summary['vs_Oz']['wins']}/{summary['total_test_programs']} ({summary['vs_Oz']['win_rate_pct']}%)")
    print(f"Average Oracle Gap            : {summary['avg_oracle_gap_pct']:.2f}%")
    print("=" * 65)
    print("Evaluation tables and plots generated:")
    print(f"  Tables: results/tables/evaluation_summary.csv, evaluation_table.md")
    print(f"  Plots:  results/plots/*.png\n")

if __name__ == "__main__":
    main()
