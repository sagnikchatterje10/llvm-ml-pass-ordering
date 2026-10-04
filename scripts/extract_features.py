#!/usr/bin/env python3
"""
Command-line feature extraction script.
Usage:
  python scripts/extract_features.py --input ir/ --output features/ir_features.csv
  python scripts/extract_features.py --file ir/PG001_vec_dot.ll --output features/single.csv
"""

import sys
import os
import argparse
from pathlib import Path
import pandas as pd
import yaml

# Add src to python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.feature_extractor.extractor import LLVMFeatureExtractor, FEATURE_COLUMNS

def parse_args():
    parser = argparse.ArgumentParser(description="Extract features from LLVM IR files")
    parser.add_argument("--input", "-i", type=str, default="ir", help="Input directory of .ll files")
    parser.add_argument("--file", "-f", type=str, default=None, help="Extract for a single .ll file")
    parser.add_argument("--output", "-o", type=str, default="features/ir_features.csv", help="Output CSV path")
    parser.add_argument("--config", "-c", type=str, default="config.yaml", help="Configuration file path")
    return parser.parse_args()

def main():
    args = parse_args()
    extractor = LLVMFeatureExtractor()

    if args.file:
        fpath = Path(args.file)
        if not fpath.is_file():
            print(f"Error: file {args.file} not found.", file=sys.stderr)
            sys.exit(1)
        pid = fpath.stem.split("_")[0] if "_" in fpath.stem else fpath.stem
        feat = extractor.extract_from_file(str(fpath), pid)
        df = pd.DataFrame([feat])
    else:
        in_dir = Path(args.input)
        if not in_dir.is_dir():
            print(f"Error: directory {args.input} not found.", file=sys.stderr)
            sys.exit(1)
        ll_files = sorted(list(in_dir.glob("*.ll")))
        if not ll_files:
            print(f"Warning: no .ll files found in {args.input}.")
            sys.exit(0)

        pairs = []
        for p in ll_files:
            pid = p.stem.split("_")[0] if "_" in p.stem else p.stem
            pairs.append((str(p), pid))

        df = extractor.extract_batch(pairs)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Extracted features for {len(df)} program(s) -> {out_path}")
    print(f"Feature columns ({len(FEATURE_COLUMNS)}): {', '.join(FEATURE_COLUMNS[:8])} ...")

if __name__ == "__main__":
    main()
