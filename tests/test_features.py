"""
Unit tests for LLVM IR Feature Extractor.
"""

import pandas as pd
import numpy as np
from src.feature_extractor.extractor import LLVMFeatureExtractor, FEATURE_COLUMNS

SYNTHETIC_LLVM_IR = """
; ModuleID = 'sample.c'
source_filename = "sample.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc"

define i32 @calc(i32 %a, i32 %b) {
entry:
  %cmp = icmp sgt i32 %a, 0
  br i1 %cmp, label %if.then, label %if.else

if.then:
  %sum = add nsw i32 %a, %b
  %mul = mul nsw i32 %sum, 2
  br label %if.end

if.else:
  %sub = sub nsw i32 %b, %a
  br label %if.end

if.end:
  %res = phi i32 [ %mul, %if.then ], [ %sub, %if.else ]
  ret i32 %res
}

define i32 @main() {
entry:
  %call = call i32 @calc(i32 5, i32 10)
  ret i32 %call
}
"""

def test_feature_extractor_synthetic():
    extractor = LLVMFeatureExtractor()
    features = extractor.extract_from_text(SYNTHETIC_LLVM_IR, "PG_TEST")

    assert features["program_id"] == "PG_TEST"
    assert features["functions"] == 2
    assert features["basic_blocks"] >= 4
    assert features["phis"] == 1
    assert features["int_arith"] == 3  # add, mul, sub
    assert features["comparisons"] == 1 # icmp
    assert features["calls"] == 1 # call @calc
    assert features["cond_branches"] == 1 # br i1 %cmp
    assert features["uncond_branches"] >= 2 # br label ...

    # Normalized ratios
    assert 0.0 <= features["branch_ratio"] <= 1.0
    assert 0.0 <= features["phi_ratio"] <= 1.0
    assert features["instr_per_bb"] > 0

def test_batch_extraction():
    extractor = LLVMFeatureExtractor()
    feat1 = extractor.extract_from_text(SYNTHETIC_LLVM_IR, "PG001")
    feat2 = extractor.extract_from_text(SYNTHETIC_LLVM_IR, "PG002")

    df = pd.DataFrame([feat1, feat2])
    assert len(df) == 2
    assert "instructions" in df.columns
    assert "branch_ratio" in df.columns
    assert df["program_id"].tolist() == ["PG001", "PG002"]
