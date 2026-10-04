# LLVM ML Pass Ordering / Selection - Implementation Details

## 1. Environment & Setup

- **Language Support**: C99 / C11 / C++
- **Python Version**: Python 3.12+ (compatible with Python >= 3.8)
- **Compiler Suite**: LLVM Clang, opt, llvm-size (LLVM 15+ compatible with New Pass Manager)
- **Key Python Libraries**: `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`, `pyyaml`, `joblib`

## 2. Directory Structure

```
llvm-ml-pass-project/
├── benchmarks/
│   ├── train/                  # 27 training benchmark C programs (PG001..PG028, PG036..PG039)
│   ├── val/                    # 6 validation benchmark C programs (PG029..PG034)
│   ├── test/                   # 7 held-out test programs (PG005, PG010, PG015, PG020, PG026, PG035, PG040)
│   └── metadata/
│       └── manifest.json       # Benchmark program catalog and split assignments
├── candidates/
│   └── candidates.json         # 42 validated candidate pipelines (S01..S40, O2, OZ)
├── dataset/
│   ├── dataset_train.csv       # Training feature-label matrix
│   ├── dataset_val.csv         # Validation feature-label matrix
│   ├── dataset_test.csv        # Held-out test matrix
│   └── dataset_all.csv         # Consolidated dataset
├── docs/
│   ├── architecture.md         # System architecture specification
│   └── implementation.md       # Implementation details & methodology
├── experiments/
│   ├── artifacts/              # Intermediate .ll and .o files per program
│   ├── results_cache.json      # Persistent experiment cache
│   ├── experiments_summary.csv # Per-program summary of candidates
│   └── experiments_raw.csv     # Raw measurements per candidate run
├── features/
│   └── ir_features.csv         # Extracted static IR features for all programs
├── ir/                         # Base unoptimized LLVM IR files
├── models/
│   ├── random_forest_pass_predictor.joblib
│   ├── hist_gradient_boosting_pass_predictor.joblib
│   └── model_metrics.json      # Training and validation metric records
├── results/
│   ├── plots/                  # Visualizations (code size, wins, accuracy, feature importance)
│   └── tables/                 # Evaluation summary tables (CSV and Markdown)
├── scripts/
│   ├── check_environment.py    # Toolchain and package verification
│   ├── init_benchmarks.py      # Benchmark code generator
│   ├── build_ir.py             # Clang IR generation script
│   ├── extract_features.py     # IR feature extraction CLI
│   ├── generate_candidates.py  # Candidate library generator & opt validator
│   ├── run_experiments.py      # Budget-constrained compilation runner
│   ├── build_dataset.py        # Dataset construction & leakage isolation
│   ├── train_model.py          # ML model trainer
│   ├── predict.py              # End-to-end single program predictor
│   ├── evaluate.py             # Test suite evaluator & graph generator
│   └── run_tests.py            # Unit test suite runner
├── src/
│   ├── feature_extractor/      # Feature extraction module
│   ├── experiment_runner/      # Compiler interface, candidate library, runner
│   ├── ml/                     # Dataset builder, ML predictor models
│   └── evaluation/             # Evaluator and plotting engine
├── tests/                      # Pytest and unittest test cases
├── config.yaml                 # Central configuration file
├── requirements.txt            # Python dependencies
└── README.md                   # Comprehensive guide
```

---

## 3. Methodological Design Decisions

### 3.1 Unoptimized IR Generation Without `optnone`
Standard Clang compilation at `-O0` attaches the function attribute `optnone`:
```llvm
define i32 @func() #0 { ... }
attributes #0 = { noinline optnone ... }
```
When `opt` encounters `optnone`, it silently skips optimization passes. To ensure that `opt` can transform the unoptimized IR, we invoke:
```bash
clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone benchmark.c -o program.ll
```
This produces pure, unoptimized IR representing standard memory-heavy code without artificial pass-blocking attributes.

### 3.2 Candidate Pass Library Design
Searching the full permutation space of LLVM optimization passes is computationally intractable (\(N!\) with thousands of valid pass combinations). To remain within a practical student project compilation budget while capturing real compiler dynamics, we construct 40 short, ordered pass sequences of lengths 2 to 4.

Key optimization interactions included:
- **`sroa` (Scalar Replacement of Aggregates) + `instcombine`**: Promotes stack alloca variables to SSA registers, allowing instruction combining to fold constants and algebraic simplifications.
- **`simplifycfg` + `instcombine` + `dce`**: Merges redundant basic blocks, cleans up empty jumps, and purges dead instructions.
- **`gvn` (Global Value Numbering) + `dce`**: Eliminates redundant load operations across basic blocks.
- **`loop-simplify` + `loop-rotate` + `licm`**: Normalizes loops and hoists invariant expressions out of loop bodies.

### 3.3 Strict Zero-Leakage Protocol
Unlike traditional tabular ML where rows can be shuffled randomly, each program produces multiple candidate experiment rows. If rows from the same program appeared in both training and test sets, the model would memorize the static IR features of the program, causing catastrophic data leakage and unrealistic accuracy scores.

Our protocol:
1. Benchmark splitting occurs strictly by **`program_id`**.
2. 27 programs in Training (67.5%), 6 in Validation (15.0%), 7 in Test (17.5%).
3. Test programs (`PG005`, `PG010`, `PG015`, `PG020`, `PG026`, `PG035`, `PG040`) are held out completely during feature scaling, model fitting, and hyperparameter tuning.

### 3.4 Primary Code Size Metric
Object file `.text` section byte size measured via `llvm-size -A <file.o>`. This accurately isolates executable machine code from debugging symbols and metadata.
