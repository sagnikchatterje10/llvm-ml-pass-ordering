"""
Dataset Construction and Leakage-Free Splitting.
Merges static IR features with optimization experiment results to build training,
validation, and test datasets with strict program-level separation.
"""

from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import json
import pandas as pd
import numpy as np

from ..feature_extractor.extractor import FEATURE_COLUMNS

class DatasetBuilder:
    def __init__(self,
                 features_csv: str = "features/ir_features.csv",
                 experiments_csv: str = "experiments/experiments_summary.csv",
                 manifest_json: str = "benchmarks/metadata/manifest.json"):
        self.features_csv = Path(features_csv)
        self.experiments_csv = Path(experiments_csv)
        self.manifest_json = Path(manifest_json)

    def build(self,
              train_out: str = "dataset/dataset_train.csv",
              val_out: str = "dataset/dataset_val.csv",
              test_out: str = "dataset/dataset_test.csv",
              all_out: str = "dataset/dataset_all.csv") -> Dict[str, pd.DataFrame]:
        """
        Merge features and experiment outcomes and split by program.
        """
        if not self.features_csv.is_file():
            raise FileNotFoundError(f"Features file {self.features_csv} not found.")
        if not self.experiments_csv.is_file():
            raise FileNotFoundError(f"Experiments summary {self.experiments_csv} not found.")

        feat_df = pd.read_csv(self.features_csv)
        exp_df = pd.read_csv(self.experiments_csv)

        # Merge on program_id
        merged = pd.merge(feat_df, exp_df, on="program_id", how="inner")
        if merged.empty:
            raise ValueError("Merged dataset is empty. Check program_id values in features and experiments.")

        # Read manifest split assignments if available
        split_map = {}
        if self.manifest_json.is_file():
            with open(self.manifest_json, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            for m in manifest:
                split_map[m["program_id"]] = m.get("split", "train")

        if "split" not in merged.columns:
            merged["split"] = merged["program_id"].map(split_map).fillna("train")

        # Split cleanly by program (never leak programs across splits)
        train_df = merged[merged["split"] == "train"].copy()
        val_df = merged[merged["split"] == "val"].copy()
        test_df = merged[merged["split"] == "test"].copy()

        # If val is empty, reserve 15% from train deterministically
        if val_df.empty and len(train_df) >= 6:
            unique_train_pids = train_df["program_id"].unique()
            val_count = max(1, int(len(unique_train_pids) * 0.15))
            val_pids = unique_train_pids[-val_count:]
            val_df = train_df[train_df["program_id"].isin(val_pids)].copy()
            train_df = train_df[~train_df["program_id"].isin(val_pids)].copy()

        # Verify no program overlap
        train_pids = set(train_df["program_id"].unique())
        test_pids = set(test_df["program_id"].unique())
        val_pids = set(val_df["program_id"].unique())

        assert len(train_pids.intersection(test_pids)) == 0, "Data Leakage: Train and Test share program IDs!"
        assert len(train_pids.intersection(val_pids)) == 0, "Data Leakage: Train and Val share program IDs!"
        assert len(val_pids.intersection(test_pids)) == 0, "Data Leakage: Val and Test share program IDs!"

        # Save files
        for p, df_out in [
            (train_out, train_df),
            (val_out, val_df),
            (test_out, test_df),
            (all_out, merged)
        ]:
            out_p = Path(p)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            df_out.to_csv(out_p, index=False)

        return {
            "train": train_df,
            "val": val_df,
            "test": test_df,
            "all": merged
        }

    @staticmethod
    def get_feature_matrix(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Extract X feature matrix and y target vector."""
        available_cols = [c for c in FEATURE_COLUMNS if c in df.columns]
        X = df[available_cols].values.astype(np.float32)
        # Handle NaN/Inf defensively
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
        y = df["best_candidate"].values.astype(str)
        return X, y, available_cols
