"""
Candidate Optimization Pass and Pipeline Library.
Defines meaningful, safe optimization pass sequences of length 2-4 for code size reduction.
Supports validation against opt with the New Pass Manager.
"""

from typing import List, Dict, Any, Optional, Tuple
import subprocess
import json
from pathlib import Path

# Core safe passes compatible across LLVM releases with the New Pass Manager
SAFE_PASSES = [
    "instcombine",
    "simplifycfg",
    "sroa",
    "dce",
    "adce",
    "gvn",
    "early-cse",
    "sccp",
    "ipsccp",
    "jump-threading",
    "reassociate",
    "loop-simplify",
    "loop-rotate",
    "licm",
    "mem2reg",
    "globaldce",
    "constmerge",
    "bdce",
]

# Curated seed sequences designed to expose code-size optimization opportunities
DEFAULT_CANDIDATE_SEQUENCES = [
    # Length 2 combinations
    ["instcombine", "simplifycfg"],
    ["simplifycfg", "instcombine"],
    ["sroa", "instcombine"],
    ["sroa", "dce"],
    ["gvn", "dce"],
    ["early-cse", "simplifycfg"],
    ["sccp", "simplifycfg"],
    ["jump-threading", "simplifycfg"],
    ["reassociate", "instcombine"],
    ["loop-simplify", "instcombine"],
    ["loop-rotate", "licm"],
    ["mem2reg", "instcombine"],
    ["mem2reg", "sroa"],
    ["globaldce", "constmerge"],
    ["instcombine", "dce"],

    # Length 3 combinations
    ["sroa", "instcombine", "simplifycfg"],
    ["sroa", "instcombine", "dce"],
    ["simplifycfg", "instcombine", "simplifycfg"],
    ["instcombine", "gvn", "dce"],
    ["early-cse", "instcombine", "simplifycfg"],
    ["sccp", "instcombine", "simplifycfg"],
    ["sroa", "gvn", "dce"],
    ["loop-simplify", "loop-rotate", "licm"],
    ["loop-rotate", "licm", "simplifycfg"],
    ["jump-threading", "instcombine", "simplifycfg"],
    ["instcombine", "reassociate", "instcombine"],
    ["mem2reg", "instcombine", "dce"],
    ["sroa", "early-cse", "simplifycfg"],
    ["sroa", "sccp", "dce"],
    ["instcombine", "bdce", "simplifycfg"],

    # Length 4 combinations
    ["sroa", "instcombine", "gvn", "dce"],
    ["sroa", "simplifycfg", "instcombine", "simplifycfg"],
    ["mem2reg", "sroa", "instcombine", "simplifycfg"],
    ["early-cse", "sroa", "instcombine", "dce"],
    ["loop-simplify", "loop-rotate", "licm", "instcombine"],
    ["sccp", "simplifycfg", "instcombine", "dce"],
    ["jump-threading", "simplifycfg", "instcombine", "dce"],
    ["sroa", "reassociate", "instcombine", "simplifycfg"],
    ["instcombine", "simplifycfg", "gvn", "dce"],
    ["sroa", "early-cse", "instcombine", "adce"],
]

def generate_default_candidates() -> List[Dict[str, Any]]:
    """Build list of candidate dictionary objects with stable IDs."""
    candidates = []

    # Baselines
    candidates.append({
        "id": "O2",
        "pipeline": "default<O2>",
        "passes": ["default<O2>"],
        "length": 1,
        "is_baseline": True,
        "description": "LLVM Standard Optimization Pipeline (-O2)"
    })
    candidates.append({
        "id": "OZ",
        "pipeline": "default<Oz>",
        "passes": ["default<Oz>"],
        "length": 1,
        "is_baseline": True,
        "description": "LLVM Code Size Optimization Pipeline (-Oz)"
    })

    # Sequence candidates S01..S40
    for idx, seq in enumerate(DEFAULT_CANDIDATE_SEQUENCES, start=1):
        cid = f"S{idx:02d}"
        pipeline_str = ",".join(seq)
        candidates.append({
            "id": cid,
            "pipeline": pipeline_str,
            "passes": seq,
            "length": len(seq),
            "is_baseline": False,
            "description": f"Custom pipeline: {pipeline_str}"
        })

    return candidates

def validate_pipeline_with_opt(opt_path: str, pipeline_str: str) -> Tuple[bool, str]:
    """Test whether opt accepts a pass pipeline without error."""
    # A minimal valid LLVM IR module
    test_ir = "define i32 @test() { ret i32 0 }\n"
    pass_arg = f"-passes={pipeline_str}"

    try:
        res = subprocess.run(
            [opt_path, pass_arg, "-S", "-o", "-"],
            input=test_ir,
            capture_output=True,
            text=True,
            timeout=5
        )
        if res.returncode == 0:
            return True, "Valid"
        return False, res.stderr.strip().splitlines()[0] if res.stderr else "Unknown opt error"
    except Exception as e:
        return False, str(e)
