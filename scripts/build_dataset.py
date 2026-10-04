#!/usr/bin/env python3
"""
CLI script to build ML training, validation, and testing datasets from experiment results.
Usage:
  python scripts/build_dataset.py
"""

import sys
import os
import argparse
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.ml.dataset import DatasetBuilder

def parse_args():
    parser = argparse.ArgumentParser(description="Construct ML datasets from IR features and experiment outputs")
    parser.add_argument("--features", default="features/ir_features.csv", help="Path to features CSV")
    parser.add_argument("--experiments", default="experiments/experiments_summary.csv", help="Path to experiments summary CSV")
    parser.add_argument("--manifest", default="benchmarks/metadata/manifest.json", help="Path to manifest JSON")
    parser.add_argument("--output-dir", default="dataset", help="Output directory for CSV files")
    return parser.parse_args()

def main():
    args = parse_args()
    builder = DatasetBuilder(
        features_csv=args.features,
        experiments_csv=args.experiments,
        manifest_json=args.manifest
    )

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    train_file = out_dir / "dataset_train.csv"
    val_file = out_dir / "dataset_val.csv"
    test_file = out_dir / "dataset_test.csv"
    all_file = out_dir / "dataset_all.csv"

    print("Building datasets with program-level separation (zero leakage)...")
    try:
        splits = builder.build(
            train_out=str(train_file),
            val_out=str(val_file),
            test_out=str(test_file),
            all_out=str(all_file)
        )
        print(f"Dataset successfully created:")
        print(f"  Train: {len(splits['train'])} programs -> {train_file}")
        print(f"  Val:   {len(splits['val'])} programs -> {val_file}")
        print(f"  Test:  {len(splits['test'])} programs (UNSEEN) -> {test_file}")
        print(f"  Total: {len(splits['all'])} programs -> {all_file}")
    except Exception as e:
        print(f"Error building dataset: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
