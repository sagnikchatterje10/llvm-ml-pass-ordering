#!/usr/bin/env python3
"""
CLI Script to execute limited-budget LLVM pass experiments.
Usage:
  python scripts/run_experiments.py --split train --budget 30
  python scripts/run_experiments.py --program benchmarks/train/PG001_vec_dot.c
"""

import sys
import os
import argparse
import json
from pathlib import Path
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.experiment_runner.compiler import LLVMCompiler
from src.experiment_runner.runner import ExperimentRunner

def parse_args():
    parser = argparse.ArgumentParser(description="Run optimization experiments on benchmark programs")
    parser.add_argument("--manifest", "-m", type=str, default="benchmarks/metadata/manifest.json", help="Path to manifest JSON")
    parser.add_argument("--candidates", "-c", type=str, default="candidates/candidates.json", help="Candidates JSON file")
    parser.add_argument("--program", "-p", type=str, default=None, help="Run on single source file")
    parser.add_argument("--split", "-s", type=str, default="all", choices=["train", "val", "test", "all"], help="Filter by split")
    parser.add_argument("--budget", "-b", type=int, default=30, help="Max candidate sequences per program")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to config.yaml")
    return parser.parse_args()

def main():
    args = parse_args()
    config = {}
    if os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    env_cfg = config.get("environment", {})
    compiler = LLVMCompiler(
        clang_path=None if env_cfg.get("clang_path") == "auto" else env_cfg.get("clang_path"),
        opt_path=None if env_cfg.get("opt_path") == "auto" else env_cfg.get("opt_path"),
        llvm_size_path=None if env_cfg.get("llvm_size_path") == "auto" else env_cfg.get("llvm_size_path"),
        extra_clang_flags=env_cfg.get("extra_clang_flags")
    )

    ready, msg = compiler.is_ready()
    if not ready:
        print(f"Error: Toolchain not ready ({msg}). Run python scripts/check_environment.py", file=sys.stderr)
        sys.exit(1)

    runner = ExperimentRunner(compiler=compiler, default_budget=args.budget)

    # Load candidates
    cand_path = Path(args.candidates)
    if not cand_path.is_file():
        print(f"Error: Candidates file {args.candidates} not found. Run scripts/generate_candidates.py first.", file=sys.stderr)
        sys.exit(1)

    with open(cand_path, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    # Filter invalid candidates if validated
    valid_candidates = [c for c in candidates if c.get("validated", True) is not False]
    print(f"Loaded {len(valid_candidates)} usable candidate pipelines.")

    programs_to_run = []
    if args.program:
        p_path = Path(args.program)
        if not p_path.is_file():
            print(f"Error: Program file {args.program} not found.", file=sys.stderr)
            sys.exit(1)
        pid = p_path.stem.split("_")[0] if "_" in p_path.stem else p_path.stem
        programs_to_run.append({"program_id": pid, "source_file": str(p_path), "name": p_path.stem})
    else:
        man_path = Path(args.manifest)
        if not man_path.is_file():
            print(f"Error: Manifest {args.manifest} not found. Run scripts/init_benchmarks.py first.", file=sys.stderr)
            sys.exit(1)
        with open(man_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for b in manifest:
            if args.split == "all" or b["split"] == args.split:
                programs_to_run.append(b)

    print(f"Executing experiments for {len(programs_to_run)} program(s) (Budget: {args.budget} sequences/program)...")

    all_summaries = []
    all_raw_rows = []

    for idx, prog in enumerate(programs_to_run, start=1):
        pid = prog["program_id"]
        src = prog["source_file"]
        print(f"[{idx}/{len(programs_to_run)}] Evaluating {pid} ({Path(src).name})...", flush=True)
        res = runner.run_program_experiments(pid, src, valid_candidates, budget=args.budget)

        if res["status"] != "completed":
            print(f"    Failed: {res.get('error')}", file=sys.stderr, flush=True)
            continue

        best_c = res["best_candidate"]
        best_sz = res["best_candidate_size"]
        o2_sz = res["baseline_O2_size"]
        oz_sz = res["baseline_Oz_size"]

        print(f"    -> Best: {best_c} ({best_sz} B) | O2: {o2_sz} B | Oz: {oz_sz} B", flush=True)

        all_summaries.append({
            "program_id": pid,
            "source_file": src,
            "baseline_O2": o2_sz,
            "baseline_Oz": oz_sz,
            "best_candidate": best_c,
            "best_candidate_size": best_sz,
            "total_candidates": res["total_candidates_evaluated"]
        })

        for cr in res["candidate_results"]:
            all_raw_rows.append(cr)

    # Save summary and raw experiments
    exp_dir = Path("experiments")
    exp_dir.mkdir(parents=True, exist_ok=True)

    summary_df = pd.DataFrame(all_summaries)
    summary_csv = exp_dir / "experiments_summary.csv"
    summary_df.to_csv(summary_csv, index=False)

    raw_df = pd.DataFrame(all_raw_rows)
    raw_csv = exp_dir / "experiments_raw.csv"
    raw_df.to_csv(raw_csv, index=False)

    print(f"\nExperiments finished! Results recorded:")
    print(f"  Summary table: {summary_csv}")
    print(f"  Raw measurements: {raw_csv}")

if __name__ == "__main__":
    main()
