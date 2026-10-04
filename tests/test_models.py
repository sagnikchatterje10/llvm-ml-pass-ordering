"""
Unit tests for ML models and evaluation metrics.
"""

import numpy as np
from src.ml.models import PassSequencePredictor

def test_random_forest_fit_predict(tmp_path):
    X = np.random.randn(20, 5).astype(np.float32)
    y = np.array(["S01"] * 5 + ["S02"] * 5 + ["S03"] * 5 + ["S04"] * 5)
    fnames = ["f1", "f2", "f3", "f4", "f5"]

    predictor = PassSequencePredictor(model_type="random_forest", n_estimators=10, random_state=42)
    predictor.fit(X, y, fnames)

    preds = predictor.predict(X[:3])
    assert len(preds) == 3

    top2 = predictor.predict_top_k(X[:3], k=2)
    assert len(top2) == 3
    assert len(top2[0]) == 2

    metrics = predictor.evaluate(X, y, k=2)
    assert "top1_accuracy" in metrics
    assert "top2_accuracy" in metrics
    assert "feature_importances" in metrics

    # Save and reload
    model_file = tmp_path / "rf.joblib"
    predictor.save(str(model_file))
    loaded = PassSequencePredictor.load(str(model_file))
    preds_loaded = loaded.predict(X[:3])
    assert np.array_equal(preds, preds_loaded)
