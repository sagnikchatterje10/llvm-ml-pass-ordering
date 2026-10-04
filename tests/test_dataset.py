"""
Unit tests for Dataset Builder and Leakage Prevention.
"""

import pandas as pd
from pathlib import Path
from src.ml.dataset import DatasetBuilder

def test_leakage_prevention(tmp_path):
    # Create mock features
    feat_data = {
        "program_id": [f"PG{i:03d}" for i in range(1, 11)],
        "instructions": [50 + i * 5 for i in range(1, 11)],
        "basic_blocks": [5 + i for i in range(1, 11)],
        "branches": [4 + i for i in range(1, 11)],
    }
    feat_df = pd.DataFrame(feat_data)
    feat_file = tmp_path / "features.csv"
    feat_df.to_csv(feat_file, index=False)

    # Create mock experiment results
    exp_data = {
        "program_id": [f"PG{i:03d}" for i in range(1, 11)],
        "baseline_O2": [1000 + i * 20 for i in range(1, 11)],
        "baseline_Oz": [980 + i * 20 for i in range(1, 11)],
        "best_candidate": ["S01", "S02", "S03", "S01", "S05", "S02", "S04", "S01", "S03", "S02"],
        "best_candidate_size": [960 + i * 20 for i in range(1, 11)]
    }
    exp_df = pd.DataFrame(exp_data)
    exp_file = tmp_path / "experiments.csv"
    exp_df.to_csv(exp_file, index=False)

    builder = DatasetBuilder(
        features_csv=str(feat_file),
        experiments_csv=str(exp_file),
        manifest_json="non_existent.json"
    )

    splits = builder.build(
        train_out=str(tmp_path / "train.csv"),
        val_out=str(tmp_path / "val.csv"),
        test_out=str(tmp_path / "test.csv"),
        all_out=str(tmp_path / "all.csv")
    )

    train_pids = set(splits["train"]["program_id"])
    val_pids = set(splits["val"]["program_id"])

    # Strict program-level isolation: zero overlap
    assert len(train_pids.intersection(val_pids)) == 0
    assert len(splits["train"]) + len(splits["val"]) == 10
