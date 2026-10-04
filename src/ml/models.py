"""
Machine Learning Models for LLVM Optimization Pass Prediction.
Supports:
1. Random Forest Classifier (Primary baseline)
2. HistGradientBoosting Classifier (Alternative tree model)
Calculates Top-1 accuracy, Top-k accuracy, confusion matrix, and feature importances.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

class PassSequencePredictor:
    def __init__(self,
                 model_type: str = "random_forest",
                 n_estimators: int = 100,
                 max_depth: Optional[int] = 12,
                 random_state: int = 42):
        self.model_type = model_type
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state

        if model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state,
                class_weight="balanced"
            )
        elif model_type in ["hist_gradient_boosting", "gradient_boosting"]:
            self.model = HistGradientBoostingClassifier(
                max_iter=n_estimators,
                max_depth=max_depth,
                random_state=random_state
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        self.classes_: Optional[np.ndarray] = None
        self.feature_names_: List[str] = []
        self.is_fitted: bool = False

    def fit(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]):
        """Train the classifier."""
        self.feature_names_ = feature_names
        self.model.fit(X, y)
        self.classes_ = np.array(self.model.classes_)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict top-1 candidate pass sequence ID."""
        if not self.is_fitted:
            raise RuntimeError("Model is not fitted yet.")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        if not self.is_fitted:
            raise RuntimeError("Model is not fitted yet.")
        return self.model.predict_proba(X)

    def predict_top_k(self, X: np.ndarray, k: int = 3) -> List[List[str]]:
        """Predict top-k candidate pass sequence IDs ordered by probability."""
        probs = self.predict_proba(X)
        top_k_preds = []
        for p in probs:
            # Sort indices descending by probability
            top_idx = np.argsort(p)[::-1][:k]
            top_k_preds.append([str(self.classes_[i]) for i in top_idx])
        return top_k_preds

    def evaluate(self, X: np.ndarray, y: np.ndarray, k: int = 3) -> Dict[str, Any]:
        """Compute evaluation metrics including top-1 and top-k accuracy."""
        y_pred = self.predict(X)
        top_k_preds = self.predict_top_k(X, k=k)

        top1_acc = accuracy_score(y, y_pred)

        # Top-k accuracy: true label is in top-k predicted candidates
        top_k_correct = sum(1 for true_lbl, preds in zip(y, top_k_preds) if true_lbl in preds)
        top_k_acc = top_k_correct / len(y) if len(y) > 0 else 0.0

        labels = sorted(list(set(y).union(set(y_pred))))
        cm = confusion_matrix(y, y_pred, labels=labels).tolist()

        feature_importances = {}
        if hasattr(self.model, "feature_importances_"):
            for fname, imp in zip(self.feature_names_, self.model.feature_importances_):
                feature_importances[fname] = round(float(imp), 4)
            # Sort descending
            feature_importances = dict(sorted(feature_importances.items(), key=lambda item: item[1], reverse=True))

        return {
            "model_type": self.model_type,
            "samples": len(y),
            "top1_accuracy": round(float(top1_acc), 4),
            f"top{k}_accuracy": round(float(top_k_acc), 4),
            "labels": labels,
            "confusion_matrix": cm,
            "feature_importances": feature_importances
        }

    def save(self, filepath: str):
        """Save model object to disk."""
        out_p = Path(filepath)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, out_p)

    @classmethod
    def load(cls, filepath: str) -> "PassSequencePredictor":
        """Load model object from disk."""
        return joblib.load(filepath)
