"""
Comprehensive Evaluation Engine for LLVM ML Pass Selection.
Calculates:
- Code size comparisons (ML vs -O2, -Oz, Oracle)
- Win/tie/loss frequencies
- Relative percentage improvements
- Generates publication-ready tables and matplotlib visualization figures
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg") # Non-interactive headless backend
import matplotlib.pyplot as plt
import seaborn as sns

class EvaluationEngine:
    def __init__(self,
                 tables_dir: str = "results/tables",
                 plots_dir: str = "results/plots"):
        self.tables_dir = Path(tables_dir)
        self.plots_dir = Path(plots_dir)
        self.tables_dir.mkdir(parents=True, exist_ok=True)
        self.plots_dir.mkdir(parents=True, exist_ok=True)

    def evaluate_test_results(self, test_df: pd.DataFrame, test_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute comprehensive evaluation statistics on test programs.
        test_records format per program:
        {
          "program_id": str,
          "name": str,
          "size_O2": int,
          "size_Oz": int,
          "size_ML": int,
          "size_oracle": int,
          "predicted_pass": str,
          "oracle_pass": str,
          "compile_time_ml_ms": float,
          "compile_time_oz_ms": float
        }
        """
        df = pd.DataFrame(test_records)
        if df.empty:
            raise ValueError("No test evaluation records provided.")

        n_progs = len(df)

        # Computations
        df["diff_vs_O2"] = df["size_O2"] - df["size_ML"]
        df["pct_vs_O2"] = (df["diff_vs_O2"] / df["size_O2"]) * 100.0

        df["diff_vs_Oz"] = df["size_Oz"] - df["size_ML"]
        df["pct_vs_Oz"] = (df["diff_vs_Oz"] / df["size_Oz"]) * 100.0

        df["oracle_gap"] = df["size_ML"] - df["size_oracle"]
        df["oracle_gap_pct"] = (df["oracle_gap"] / df["size_oracle"]) * 100.0

        # Wins, ties, losses vs O2
        wins_o2 = int((df["size_ML"] < df["size_O2"]).sum())
        ties_o2 = int((df["size_ML"] == df["size_O2"]).sum())
        losses_o2 = int((df["size_ML"] > df["size_O2"]).sum())

        # Wins, ties, losses vs Oz
        wins_oz = int((df["size_ML"] < df["size_Oz"]).sum())
        ties_oz = int((df["size_ML"] == df["size_Oz"]).sum())
        losses_oz = int((df["size_ML"] > df["size_Oz"]).sum())

        avg_o2 = float(df["size_O2"].mean())
        avg_oz = float(df["size_Oz"].mean())
        avg_ml = float(df["size_ML"].mean())
        avg_oracle = float(df["size_oracle"].mean())

        avg_pct_vs_o2 = float(df["pct_vs_O2"].mean())
        avg_pct_vs_oz = float(df["pct_vs_Oz"].mean())
        avg_oracle_gap = float(df["oracle_gap_pct"].mean())

        # Save CSV table
        csv_path = self.tables_dir / "evaluation_summary.csv"
        df.to_csv(csv_path, index=False)

        # Save Markdown table
        md_path = self.tables_dir / "evaluation_table.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# LLVM ML Pass Selection - Evaluation Results\n\n")
            f.write("| Program | O2 (B) | Oz (B) | ML (B) | Oracle (B) | Pred Pass | ML vs O2 (%) | ML vs Oz (%) |\n")
            f.write("|---------|--------|--------|--------|------------|-----------|--------------|--------------|\n")
            for _, r in df.iterrows():
                f.write(f"| {r['program_id']} | {r['size_O2']:,} | {r['size_Oz']:,} | {r['size_ML']:,} | {r['size_oracle']:,} | {r['predicted_pass']} | {r['pct_vs_O2']:+.2f}% | {r['pct_vs_Oz']:+.2f}% |\n")
            f.write(f"\n**Averages:** O2: {avg_o2:.1f} B | Oz: {avg_oz:.1f} B | ML: {avg_ml:.1f} B | Oracle: {avg_oracle:.1f} B\n")
            f.write(f"**Win rate vs O2:** {wins_o2}/{n_progs} ({wins_o2/n_progs*100:.1f}%) | **vs Oz:** {wins_oz}/{n_progs} ({wins_oz/n_progs*100:.1f}%)\n")

        summary = {
            "total_test_programs": n_progs,
            "avg_size_O2": round(avg_o2, 2),
            "avg_size_Oz": round(avg_oz, 2),
            "avg_size_ML": round(avg_ml, 2),
            "avg_size_Oracle": round(avg_oracle, 2),
            "avg_pct_reduction_vs_O2": round(avg_pct_vs_o2, 2),
            "avg_pct_reduction_vs_Oz": round(avg_pct_vs_oz, 2),
            "avg_oracle_gap_pct": round(avg_oracle_gap, 2),
            "vs_O2": {"wins": wins_o2, "ties": ties_o2, "losses": losses_o2, "win_rate_pct": round(wins_o2/n_progs*100, 2)},
            "vs_Oz": {"wins": wins_oz, "ties": ties_oz, "losses": losses_oz, "win_rate_pct": round(wins_oz/n_progs*100, 2)},
            "dataframe": df
        }

        # Generate plots
        self.generate_plots(df, summary)

        return summary

    def generate_plots(self, df: pd.DataFrame, summary: Dict[str, Any]):
        """Generate all required evaluation graphs."""
        sns.set_theme(style="whitegrid", palette="muted")

        # 1. Average Code Size Comparison
        plt.figure(figsize=(7, 5))
        bars = plt.bar(
            ["-O2", "-Oz", "ML Predicted", "Oracle"],
            [summary["avg_size_O2"], summary["avg_size_Oz"], summary["avg_size_ML"], summary["avg_size_Oracle"]],
            color=["#4A90E2", "#50E3C2", "#F5A623", "#7ED321"],
            edgecolor="black",
            linewidth=1.2
        )
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + (yval*0.01), f"{yval:.1f} B", ha='center', va='bottom', fontweight='bold')
        plt.title("Average Code Size Comparison Across Optimization Strategies", fontsize=12, fontweight='bold', pad=15)
        plt.ylabel("Code Size (Bytes)", fontsize=10)
        plt.ylim(0, max(summary["avg_size_O2"], summary["avg_size_Oz"]) * 1.18)
        plt.tight_layout()
        plt.savefig(self.plots_dir / "average_code_size_comparison.png", dpi=300)
        plt.close()

        # 2. Per-Program Comparison Bar Chart
        plt.figure(figsize=(10, 5))
        x = np.arange(len(df))
        width = 0.20
        plt.bar(x - 1.5*width, df["size_O2"], width, label="LLVM -O2", color="#4A90E2", edgecolor="black")
        plt.bar(x - 0.5*width, df["size_Oz"], width, label="LLVM -Oz", color="#50E3C2", edgecolor="black")
        plt.bar(x + 0.5*width, df["size_ML"], width, label="ML-Predicted", color="#F5A623", edgecolor="black")
        plt.bar(x + 1.5*width, df["size_oracle"], width, label="Oracle (Best Offline)", color="#7ED321", edgecolor="black")
        plt.xlabel("Held-Out Test Benchmark Programs", fontsize=10)
        plt.ylabel("Code Size (Bytes)", fontsize=10)
        plt.title("Per-Program Code Size by Optimization Pipeline", fontsize=12, fontweight='bold', pad=15)
        plt.xticks(x, df["program_id"], rotation=0)
        plt.legend(frameon=True)
        plt.tight_layout()
        plt.savefig(self.plots_dir / "per_program_comparison.png", dpi=300)
        plt.close()

        # 3. ML Wins/Draws/Losses
        plt.figure(figsize=(8, 4.5))
        categories = ["vs LLVM -O2", "vs LLVM -Oz"]
        wins = [summary["vs_O2"]["wins"], summary["vs_Oz"]["wins"]]
        ties = [summary["vs_O2"]["ties"], summary["vs_Oz"]["ties"]]
        losses = [summary["vs_O2"]["losses"], summary["vs_Oz"]["losses"]]

        x_cat = np.arange(len(categories))
        w = 0.25
        plt.bar(x_cat - w, wins, w, label="ML Wins (Smaller)", color="#7ED321", edgecolor="black")
        plt.bar(x_cat, ties, w, label="Ties (Equal)", color="#F5A623", edgecolor="black")
        plt.bar(x_cat + w, losses, w, label="Losses (Larger)", color="#D0021B", edgecolor="black")
        plt.xticks(x_cat, categories, fontsize=11, fontweight='bold')
        plt.ylabel("Number of Programs", fontsize=10)
        plt.title("ML-Selected Pipeline Head-to-Head Outcomes", fontsize=12, fontweight='bold', pad=15)
        plt.legend(frameon=True)
        plt.tight_layout()
        plt.savefig(self.plots_dir / "ml_wins_breakdown.png", dpi=300)
        plt.close()

    def generate_feature_importance_plot(self, feature_importances: Dict[str, float], top_n: int = 12):
        """Plot top feature importances for Random Forest."""
        if not feature_importances:
            return
        top_items = list(feature_importances.items())[:top_n]
        names = [k for k, _ in top_items][::-1]
        vals = [v for _, v in top_items][::-1]

        plt.figure(figsize=(8, 5))
        plt.barh(names, vals, color="#4A90E2", edgecolor="black")
        plt.xlabel("Gini Importance Score", fontsize=10)
        plt.title(f"Top {top_n} Static LLVM IR Features (Random Forest)", fontsize=12, fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(self.plots_dir / "feature_importance.png", dpi=300)
        plt.close()

    def generate_accuracy_plot(self, metrics_dict: Dict[str, Any]):
        """Plot Top-1 vs Top-3 accuracy comparison."""
        models = []
        top1_scores = []
        top3_scores = []
        for mkey, mdata in metrics_dict.items():
            models.append(mdata.get("name", mkey))
            t_data = mdata.get("test", {})
            top1_scores.append(t_data.get("top1_accuracy", 0.0) * 100)
            top3_scores.append(t_data.get("top3_accuracy", 0.0) * 100)

        plt.figure(figsize=(7, 4.5))
        x = np.arange(len(models))
        w = 0.3
        plt.bar(x - w/2, top1_scores, w, label="Top-1 Accuracy", color="#4A90E2", edgecolor="black")
        plt.bar(x + w/2, top3_scores, w, label="Top-3 Accuracy", color="#7ED321", edgecolor="black")
        plt.xticks(x, models, fontsize=10, fontweight='bold')
        plt.ylabel("Accuracy (%)", fontsize=10)
        plt.ylim(0, 105)
        plt.title("Model Prediction Accuracy on Held-Out Test Suite", fontsize=12, fontweight='bold', pad=15)
        plt.legend(frameon=True)
        plt.tight_layout()
        plt.savefig(self.plots_dir / "model_accuracy.png", dpi=300)
        plt.close()
