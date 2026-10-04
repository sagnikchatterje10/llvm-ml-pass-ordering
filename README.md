# ML-Based LLVM Optimization Pass Ordering / Selection

An intelligent, lightweight machine learning system that predicts effective LLVM optimization pass sequences from static program features extracted directly from LLVM IR, evaluated against standard LLVM `-O2` and `-Oz` baselines on code size under a limited compilation budget.

---

## 1. Problem Statement

Standard compiler optimization levels such as LLVM `-O2` and `-Oz` rely on fixed, hand-tuned heuristic pass sequences designed for general-purpose code. However, different software workloads exhibit widely diverging structural characteristics:
- Some programs are dominated by deeply nested loop structures with invariant memory access patterns.
- Others are dominated by pointer indirection, complex branching state machines, or extensive stack allocations.

Applying a one-size-fits-all optimization sequence frequently misses compacting opportunities or introduces pass overhead. Furthermore, searching the full permutation space of optimization passes for every target program is computationally intractable ($>10^{20}$ combinations).

### Research Question
> **Can a lightweight ML model use static LLVM IR features to select a useful optimization pass sequence that achieves lower code size than fixed baselines (-O2 / -Oz) for previously unseen programs, without exhaustively trying every possible sequence?**

---

## 2. Why LLVM?

- **Industry Standard Intermediate Representation (IR)**: LLVM IR provides a clean, well-defined Single Static Assignment (SSA) based representation with strongly typed operations and explicit control flow graphs (CFGs).
- **Modular Pass Infrastructure**: The LLVM New Pass Manager allows arbitrary, composable optimization pass pipelines to be specified directly via textual strings (e.g., `-passes='sroa,instcombine,simplifycfg'`).
- **Precision in Measurement**: LLVM provides native tools (`clang`, `opt`, `llvm-size`, `llvm-dis`) that allow precise tracking of intermediate representations, transformation costs, and binary `.text` code size.

---

## 3. Why Machine Learning?

Instead of running an expensive iterative search or genetic algorithm every time a program is compiled, a supervised machine learning model (such as a Random Forest) learns the non-linear mapping:

$$\text{Static IR Features } (X) \longrightarrow \text{Optimal Pass Pipeline } (y)$$

Once trained, **inference takes less than 2 milliseconds**, enabling instantaneous recommendation of compacting pass sequences with zero iterative compilation search overhead.

---

## 4. System Architecture

```
Source Program (.c)
       │
       ▼ [clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone]
Unoptimized LLVM IR (.ll)
       │
       ├─────────────────────────────────────────┐
       ▼                                         ▼
IR Feature Extraction (30 Features)     Candidate Optimization Library
       │                                (S01..S40, Baselines O2/Oz)
       │                                         │
       │                                         ▼
       │                                Limited-Budget Experiments
       │                                (Budget <= 30 compilations)
       │                                         │
       │                                         ▼
       │                                Code Size Measurement
       │                                (llvm-size .text section)
       │                                         │
       └───────────────────┬─────────────────────┘
                           ▼
               Leakage-Free Dataset
         (Train: 67.5% | Val: 15% | Test: 17.5%)
                           │
                           ▼
                  ML Model Training
               (Random Forest & HGB)
                           │
                           ▼
               End-to-End Prediction
        (Unseen Program -> Predict -> Compile)
                           │
                           ▼
             Evaluation vs -O2 and -Oz
```

---

## 5. Environment & Installation

### Prerequisites
- **Python**: >= 3.8 (Tested on Python 3.12)
- **LLVM / Clang**: Version 15+ with New Pass Manager support (`clang`, `opt`, `llvm-size`)
- **OS**: Windows, Linux, or macOS

### Python Dependencies
Install required packages using pip:
```bash
pip install -r requirements.txt
```

Verify your environment with the automated diagnostic tool:
```bash
python scripts/check_environment.py
```

---

## 6. Project Structure

```
llvm-ml-pass-project/
├── benchmarks/              # 40 diverse C programs (train, val, test)
│   ├── train/               # 27 training programs
│   ├── val/                 # 6 validation programs
│   ├── test/                # 7 held-out test programs
│   └── metadata/            # manifest.json
├── candidates/              # 42 validated candidate pass pipelines
├── dataset/                 # Leakage-isolated training/test datasets
├── docs/                    # Architecture and implementation design docs
├── experiments/             # Intermediate artifacts and persistent cache
├── features/                # Static IR feature tables
├── ir/                      # Generated unoptimized LLVM IR (.ll)
├── models/                  # Trained ML models and metric JSONs
├── results/                 # Evaluation output tables and plots
│   ├── plots/
│   └── tables/
├── scripts/                 # CLI pipeline execution scripts
├── src/                     # Core Python modules
├── tests/                   # Pytest and unittest suites
├── config.yaml              # Central configuration
└── requirements.txt         # Package requirements
```

---

## 7. Step-by-Step Reproduction Guide

### Step 1: Initialize Benchmarks
Generate the 40 distinct C benchmark programs across 9 categories:
```bash
python scripts/init_benchmarks.py
```

### Step 2: Build Unoptimized LLVM IR
Compile source benchmarks to unoptimized IR with `optnone` disabled:
```bash
python scripts/build_ir.py
```

### Step 3: Extract Static IR Features
Extract 30 deterministic structural features (size, memory, CFG, calls, SSA, loops, ratios):
```bash
python scripts/extract_features.py --input ir/ --output features/ir_features.csv
```

### Step 4: Generate & Validate Candidate Pass Pipelines
Generate 42 candidate pass sequences (lengths 2-4) and validate against `opt`:
```bash
python scripts/generate_candidates.py
```

### Step 5: Execute Limited-Budget Experiments
Compile programs under a strict compilation budget (e.g. 30 candidates per program):
```bash
python scripts/run_experiments.py --split all --budget 30
```

### Step 6: Build Training & Testing Datasets
Merge static features with optimal labels enforcing strict program-level separation:
```bash
python scripts/build_dataset.py
```

### Step 7: Train Machine Learning Models
Train Random Forest and HistGradientBoosting classifiers:
```bash
python scripts/train_model.py --model all
```

### Step 8: Run End-to-End Prediction on an Unseen Program
Predict and optimize any C source file in a single step:
```bash
python scripts/predict.py --source benchmarks/test/PG005_conv2d.c
```

### Step 9: Evaluate Test Suite and Generate Visualizations
Evaluate on held-out test programs and generate figures and Markdown tables:
```bash
python scripts/evaluate.py
```

### Step 10: Run Unit Tests
Verify all core components:
```bash
python scripts/run_tests.py
```

---

## 8. Example Output

Running end-to-end prediction on an unseen program:
```
=================================================================
 LLVM ML OPTIMIZATION PREDICTION PIPELINE: PG005_conv2d.c
=================================================================
Step 1: Generated LLVM IR -> ir/PG005_conv2d.ll (14.2 ms)
Step 2: Extracted 30 static IR features (2.1 ms)
        Instructions: 168, Blocks: 18, Branches: 17, Loads/Stores: 26/18
Step 3: ML Model Inference (1.10 ms)
        Predicted Best Sequence : S01 (instcombine,simplifycfg)
        Top-3 Predictions       : S01, S03, S17

=================================================================
 EVALUATION RESULTS
=================================================================
Program                 : PG005_conv2d.c
Predicted Pipeline      : S01 -> [instcombine,simplifycfg]
ML Code Size            : 960 bytes (Compile time: 18.4 ms)
LLVM -O2 Baseline       : 1,024 bytes (Compile time: 42.1 ms)
LLVM -Oz Baseline       : 976 bytes (Compile time: 39.8 ms)
-----------------------------------------------------------------
ML vs LLVM -O2          : +6.25% size reduction (-64 bytes)
ML vs LLVM -Oz          : +1.64% size reduction (-16 bytes)
Outcome Verdict         : WIN (ML produced smaller code than BOTH -O2 and -Oz!)
=================================================================
```

---

## 9. Current 70% Scope vs Remaining 30%

### Completed in 70% Scope:
- Fully automated LLVM IR generation and validation pipeline.
- Deterministic 30-feature IR parser (instruction classes, memory, control flow, loops, ratios).
- Controlled candidate pass library (40 short sequences + baselines).
- Budget-constrained compilation runner with persistent caching.
- Zero-leakage program-level train/validation/test dataset construction.
- Supervised ML models (Random Forest, HistGradientBoosting) with Top-1, Top-3, and feature importance analysis.
- End-to-end single command prediction workflow (`predict.py`).
- Evaluation against `-O2` and `-Oz` with automated publication plots and markdown tables.

### Reserved for Final 30%:
- Evolutionary pass sequence search and Monte Carlo tree search.
- Value ranking / regression formulation ($P(\text{size\_delta} \mid \text{pipeline})$).
- Graph Neural Network (GNN) embeddings on LLVM Control Flow Graphs.
- Scaled benchmarks (e.g., SPEC CPU, PolyBench, cBench).
- Cross-architecture binary size evaluation (x86_64, AArch64, RISC-V).
