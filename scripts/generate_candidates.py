#!/usr/bin/env python3
"""
Generate and validate candidate optimization pipelines.
Usage:
  python scripts/generate_candidates.py --output candidates/candidates.json
"""

import sys
import os
import argparse
import json
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.experiment_runner.candidate_library import generate_default_candidates, validate_pipeline_with_opt
from src.experiment_runner.compiler import LLVMCompiler

def parse_args():
    parser = argparse.ArgumentParser(description="Generate and validate LLVM optimization candidates")
    parser.add_argument("--output", "-o", type=str, default="candidates/candidates.json", help="Output JSON path")
    parser.add_argument("--config", "-c", type=str, default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--validate", action="store_true", default=True, help="Validate against opt if available")
    return parser.parse_args()

def main():
    args = parse_args()
    config = {}
    if os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    env_cfg = config.get("environment", {})
    compiler = LLVMCompiler(
        opt_path=None if env_cfg.get("opt_path") == "auto" else env_cfg.get("opt_path")
    )

    candidates = generate_default_candidates()
    print(f"Generated {len(candidates)} candidate pipelines (including O2 and Oz).")

    validated_candidates = []
    opt_available = compiler.opt is not None

    if opt_available and args.validate:
        print(f"Validating candidates with opt ({compiler.opt})...")
        valid_cnt = 0
        invalid_cnt = 0
        for cand in candidates:
            ok, msg = validate_pipeline_with_opt(compiler.opt, cand["pipeline"])
            cand["validated"] = ok
            cand["validation_msg"] = msg
            if ok:
                valid_cnt += 1
                validated_candidates.append(cand)
            else:
                invalid_cnt += 1
                print(f"  [INVALID] {cand['id']} ({cand['pipeline']}): {msg}")
        print(f"Validation complete: {valid_cnt} valid, {invalid_cnt} invalid.")
    else:
        print("Note: opt not verified yet; generating definitions with pending validation.")
        for cand in candidates:
            cand["validated"] = None
            cand["validation_msg"] = "Pending LLVM validation"
            validated_candidates.append(cand)

    out_p = Path(args.output)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_p, "w", encoding="utf-8") as f:
        json.dump(validated_candidates, f, indent=2)

    print(f"Saved {len(validated_candidates)} candidates -> {out_p}")

if __name__ == "__main__":
    main()
