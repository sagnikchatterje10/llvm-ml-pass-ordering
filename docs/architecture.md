# LLVM ML Pass Ordering / Selection - Architecture Specification

## 1. System Overview

The **ML-Based LLVM Optimization Pass Ordering / Selection** system predicts a useful LLVM optimization pass sequence from static features extracted from a program's unoptimized LLVM IR, and evaluates the ML-selected sequence against LLVM standard baselines (`-O2` and `-Oz`) under a strictly constrained compilation budget.

```
+-----------------------------------------------------------------------------------+
|                               SYSTEM ARCHITECTURE                                 |
+-----------------------------------------------------------------------------------+

   +------------------------+
   | Benchmark C Source     |  (40 Diverse Programs across 9 Behavioral Categories)
   +------------------------+
               |
               v [clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone]
   +------------------------+
   | Unoptimized LLVM IR    |  (.ll text representation)
   +------------------------+
        |              \
        |               \
        v                v
   +--------------+   +-------------------------------------------------------+
   | IR Feature   |   | Candidate Library (S01..S40, baselines O2, Oz)       |
   | Extractor    |   +-------------------------------------------------------+
   +--------------+                              |
        |                                        v
        |                          +------------------------------------------+
        |                          | Limited-Budget Compilation Experiments   |
        |                          | (Budget <= 30 pipelines per program)     |
        |                          +------------------------------------------+
        |                                        |
        |                                        v
        |                          +------------------------------------------+
        |                          | Code Size Measurement                    |
        |                          | (llvm-size .text section bytes)          |
        |                          +------------------------------------------+
        |                                        |
        +-------------------+--------------------+
                            |
                            v
   +-------------------------------------------------------+
   | Dataset Builder                                       |
   | (Strict Program-Level Split: Train 70%, Val 15%, Test 15%)
   +-------------------------------------------------------+
                            |
                            v
   +-------------------------------------------------------+
   | ML Model Training                                     |
   | (Random Forest Classifier & HistGradientBoosting)     |
   +-------------------------------------------------------+
                            |
                            v
   +-------------------------------------------------------+
   | End-to-End Predictor & Evaluator                      |
   | (Inference -> Apply Pipeline -> Measure -> Compare)   |
   +-------------------------------------------------------+
```

---

## 2. Core Architectural Components

### 2.1 Benchmark Suite Manager (`benchmarks/`)
- Contains 40 distinct C benchmarks spanning loops, recursion, bitwise logic, memory structures, nested branches, and algorithms.
- Programs are assigned unique IDs (`PG001` - `PG040`).
- Strict train/validation/test assignment stored in `benchmarks/metadata/manifest.json`.

### 2.2 LLVM Toolchain Interface (`src/experiment_runner/compiler.py`)
- Standardizes compiler flags across all experiments.
- `clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone`:
  - Crucial: By default, Clang adds `optnone` to functions compiled at `-O0`, which prevents `opt` from performing optimization. Emitting IR with `-disable-O0-optnone` allows `opt` to run pass sequences on the base IR.
- Invokes `opt -passes=...` using LLVM's New Pass Manager.
- Compiles optimized IR to native object code (`.o`) and invokes `llvm-size` to measure `.text` section bytes.

### 2.3 IR Feature Extractor (`src/feature_extractor/extractor.py`)
- Deterministic static analysis on LLVM IR text files.
- Computes 30 features across 8 dimensions:
  1. **Program Size**: instruction count, function count, basic block count.
  2. **Control Flow**: total branches, conditional branches, unconditional branches, switch instructions, indirect branches.
  3. **Memory**: loads, stores, stack allocations (`alloca`), pointer arithmetic (`getelementptr`).
  4. **Computation**: integer arithmetic operations, floating-point operations, comparisons (`icmp`, `fcmp`), type conversions/casts.
  5. **Calls**: direct calls, indirect calls.
  6. **SSA Structures**: PHI nodes, select instructions.
  7. **Loops / CFG Signals**: back-edges detected from CFG successor traversal.
  8. **Normalized Ratios**: instructions/basic-block, branch ratio, memory ratio, call ratio, phi ratio.

### 2.4 Candidate Pass Library (`candidates/`)
- Replaces the intractable combinatorial space (\(>10^{20}\) permutations) with a curated, safe candidate library of 40 short pipelines (lengths 2 to 4).
- Passes included: `instcombine`, `simplifycfg`, `sroa`, `dce`, `adce`, `bdce`, `gvn`, `early-cse`, `sccp`, `jump-threading`, `reassociate`, `loop-simplify`, `loop-rotate`, `licm`, `mem2reg`, `globaldce`, `constmerge`.
- Candidate validation: Every pass is dynamically validated against `opt` to guarantee version compatibility before running experiments.

### 2.5 Limited-Budget Experiment Runner (`src/experiment_runner/runner.py`)
- Enforces hard limit `MAX_CANDIDATES_PER_PROGRAM = 30`.
- Evaluates candidate sequences and baseline pipelines (`-O2`, `-Oz`).
- Persistent cache (`experiments/results_cache.json`) eliminates redundant compilations.
- Fault-tolerant: candidate failures are isolated and logged without crashing the batch run.

### 2.6 Dataset Construction & Leakage Isolation (`src/ml/dataset.py`)
- Merges static IR feature vectors \(X\) with optimal candidate IDs \(y = \arg\min (\text{code\_size})\).
- **Program-Level Separation**: Train, validation, and test splits partition programs by `program_id`. Rows belonging to the same benchmark never appear across multiple splits.

### 2.7 ML Prediction Engine (`src/ml/models.py`)
- Baseline Model: **Random Forest Classifier** (`n_estimators=100`, `max_depth=12`, `random_state=42`).
- Alternative Model: **HistGradientBoosting Classifier**.
- Evaluates Top-1 accuracy, Top-3 accuracy, and Gini feature importances.

### 2.8 Evaluation and Visualization (`src/evaluation/evaluator.py`)
- Evaluates unseen test programs.
- Compiles each test program with ML-selected pipeline, -O2, -Oz, and Oracle.
- Calculates:
  $$\text{Size Reduction vs } O2 = \frac{\text{Size}_{O2} - \text{Size}_{ML}}{\text{Size}_{O2}} \times 100\%$$
  $$\text{Size Reduction vs } Oz = \frac{\text{Size}_{Oz} - \text{Size}_{ML}}{\text{Size}_{Oz}} \times 100\%$$
  $$\text{Oracle Gap} = \frac{\text{Size}_{ML} - \text{Size}_{Oracle}}{\text{Size}_{Oracle}} \times 100\%$$
- Outputs high-resolution plots (`results/plots/`) and summary tables (`results/tables/`).
