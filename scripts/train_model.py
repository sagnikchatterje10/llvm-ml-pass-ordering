#!/usr/bin/env python3
"""
Train lightweight Machine Learning models for LLVM optimization pass prediction.
Usage:
  python scripts/train_model.py --model rf
  python scripts/train_model.py --model all
"""

import sys
import os
import argparse
import json
from pathlib import Path
import pandas as pd
import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.ml.models import PassSequencePredictor
from src.ml.dataset import DatasetBuilder

def parse_args():
    parser = argparse.ArgumentParser(description="Train ML models for pass selection")
    parser.add_argument("--train-data", default="dataset/dataset_train.csv", help="Training dataset CSV")
    parser.add_argument("--val-data", default="dataset/dataset_val.csv", help="Validation dataset CSV")
    parser.add_argument("--test-data", default="dataset/dataset_test.csv", help="Test dataset CSV")
    parser.add_argument("--model", default="all", choices=["rf", "hgb", "all"], help="Model to train")
    parser.add_argument("--output-dir", default="models", help="Output directory for saved models")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    return parser.parse_args()

def main():
    args = parse_args()
    config = {}
    if os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    ml_cfg = config.get("ml", {})
    random_state = ml_cfg.get("random_state", 42)
    n_estimators = ml_cfg.get("n_estimators", 100)
    max_depth = ml_cfg.get("max_depth", 12)
    top_k = ml_cfg.get("top_k", 3)

    # 1. Load data
    for p in [args.train_data, args.test_data]:
        if not Path(p).is_file():
            print(f"Error: dataset file {p} not found. Run scripts/build_dataset.py first.", file=sys.stderr)
            sys.exit(1)

    train_df = pd.read_csv(args.train_data)
    test_df = pd.read_csv(args.test_data)
    val_df = pd.read_csv(args.val_data) if Path(args.val_data).is_file() else None

    X_train, y_train, feat_cols = DatasetBuilder.get_feature_matrix(train_df)
    X_test, y_test, _ = DatasetBuilder.get_feature_matrix(test_df)

    if val_df is not None and not val_df.empty:
        X_val, y_val, _ = DatasetBuilder.get_feature_matrix(val_df)
    else:
        X_val, y_val = None, None

    print(f"Loaded datasets:")
    print(f"  Train: {X_train.shape[0]} samples, {X_train.shape[1]} features")
    if X_val is not None:
        print(f"  Val:   {X_val.shape[0]} samples")
    print(f"  Test:  {X_test.shape[0]} samples (UNSEEN held-out)")

    models_to_train = []
    if args.model in ["rf", "all"]:
        models_to_train.append(("random_forest", "Random Forest"))
    if args.model in ["hgb", "all"]:
        models_to_train.append(("hist_gradient_boosting", "HistGradientBoosting"))

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results_summary = {}

    for mtype, mname in models_to_train:
        print(f"\nTraining Model: {mname} ({mtype})...")
        predictor = PassSequencePredictor(
            model_type=mtype,
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )
        predictor.fit(X_train, y_train, feat_cols)

        train_metrics = predictor.evaluate(X_train, y_train, k=top_k)
        print(f"  Train Top-1 Accuracy: {train_metrics['top1_accuracy']*100:.1f}%")
        print(f"  Train Top-{top_k} Accuracy: {train_metrics[f'top{top_k}_accuracy']*100:.1f}%")

        if X_val is not None:
            val_metrics = predictor.evaluate(X_val, y_val, k=top_k)
            print(f"  Val   Top-1 Accuracy: {val_metrics['top1_accuracy']*100:.1f}%")
            print(f"  Val   Top-{top_k} Accuracy: {val_metrics[f'top{top_k}_accuracy']*100:.1f}%")
        else:
            val_metrics = None

        test_metrics = predictor.evaluate(X_test, y_test, k=top_k)
        print(f"  Test  Top-1 Accuracy: {test_metrics['top1_accuracy']*100:.1f}%")
        print(f"  Test  Top-{top_k} Accuracy: {test_metrics[f'top{top_k}_accuracy']*100:.1f}%")

        # Save model
        save_path = out_dir / f"{mtype}_pass_predictor.joblib"
        predictor.save(str(save_path))
        print(f"  Model saved -> {save_path}")

        results_summary[mtype] = {
            "name": mname,
            "train": train_metrics,
            "val": val_metrics,
            "test": test_metrics,
            "save_path": str(save_path)
        }

    # Save metrics JSON
    metrics_file = out_dir / "model_metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(results_summary, f, indent=2)
    print(f"\nAll models trained and metrics written -> {metrics_file}")

if __name__ == "__main__":
    main()
