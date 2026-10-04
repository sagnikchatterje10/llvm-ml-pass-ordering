"""
Unit tests for Candidate Pass Library.
"""

from src.experiment_runner.candidate_library import generate_default_candidates

def test_candidate_generation():
    candidates = generate_default_candidates()
    assert len(candidates) >= 40

    c_ids = [c["id"] for c in candidates]
    assert "O2" in c_ids
    assert "OZ" in c_ids
    assert "S01" in c_ids
    assert "S10" in c_ids

    # Sequence lengths must be between 1 and 4
    for c in candidates:
        assert 1 <= c["length"] <= 4
        assert len(c["pipeline"]) > 0
        assert isinstance(c["passes"], list)
