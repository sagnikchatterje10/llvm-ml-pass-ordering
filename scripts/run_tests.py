#!/usr/bin/env python3
"""
Test runner using standard library unittest.
"""

import sys
import unittest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tests.test_features import test_feature_extractor_synthetic, test_batch_extraction
from tests.test_candidates import test_candidate_generation
from tests.test_dataset import test_leakage_prevention
from tests.test_models import test_random_forest_fit_predict

class LLVMMLProjectTests(unittest.TestCase):
    def test_features_synthetic(self):
        test_feature_extractor_synthetic()

    def test_features_batch(self):
        test_batch_extraction()

    def test_candidates(self):
        test_candidate_generation()

    def test_dataset_leakage(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            test_leakage_prevention(Path(tmpdir))

    def test_models(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            test_random_forest_fit_predict(Path(tmpdir))

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LLVMMLProjectTests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
