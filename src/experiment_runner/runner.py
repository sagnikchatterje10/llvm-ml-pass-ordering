"""
Experiment Runner for Limited-Budget LLVM Optimization Passes.
Compatible with LLVM 23+ where clang handles both optimization and object generation.
Features parallel execution across candidates with thread-safe caching.
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

from .compiler import LLVMCompiler

class ExperimentRunner:
    def __init__(self,
                 compiler: LLVMCompiler,
                 cache_file: str = "experiments/results_cache.json",
                 ir_dir: str = "ir",
                 artifacts_dir: str = "experiments/artifacts",
                 default_budget: int = 30,
                 max_workers: int = 12):
        self.compiler = compiler
        self.cache_file = Path(cache_file)
        self.ir_dir = Path(ir_dir)
        self.artifacts_dir = Path(artifacts_dir)
        self.default_budget = default_budget
        self.max_workers = max_workers
        self._lock = threading.Lock()

        self.ir_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache: Dict[str, Any] = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        if self.cache_file.is_file():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        with self._lock:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2)

    def evaluate_candidate(self,
                           program_id: str,
                           base_ir: str,
                           candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply a candidate pipeline, compile to object, measure size.
        With LLVM 23, clang handles optimization + object generation in one step.
        """
        cid = candidate["id"]
        pipeline = candidate["pipeline"]
        cache_key = f"{program_id}:{cid}"

        with self._lock:
            if cache_key in self.cache:
                entry = self.cache[cache_key]
                if entry.get("status") == "success" and entry.get("code_size") is not None:
                    return entry

        prog_art_dir = self.artifacts_dir / program_id
        prog_art_dir.mkdir(parents=True, exist_ok=True)

        # Output paths
        marker_ll = prog_art_dir / f"{program_id}_{cid}.ll"
        obj_file = prog_art_dir / f"{program_id}_{cid}.o"

        # run_opt_pipeline on LLVM 23 actually compiles IR -> .o directly
        ok, elapsed_ms, result_msg = self.compiler.run_opt_pipeline(
            base_ir, str(marker_ll), pipeline
        )

        if not ok:
            res = {
                "program_id": program_id,
                "candidate_id": cid,
                "pipeline": pipeline,
                "status": "compile_failed",
                "code_size": None,
                "compile_time_ms": elapsed_ms,
                "error": result_msg
            }
            with self._lock:
                self.cache[cache_key] = res
            return res

        # result_msg contains the actual .o path when successful
        actual_obj = result_msg if result_msg.endswith(".o") and Path(result_msg).is_file() else str(obj_file)

        # Measure code size
        size_bytes, size_info = self.compiler.measure_code_size(actual_obj)
        res = {
            "program_id": program_id,
            "candidate_id": cid,
            "pipeline": pipeline,
            "status": "success",
            "code_size": size_bytes,
            "compile_time_ms": round(elapsed_ms, 2),
            "measurement_info": size_info,
            "error": None
        }
        with self._lock:
            self.cache[cache_key] = res
        return res

    def run_program_experiments(self,
                                program_id: str,
                                source_file: str,
                                candidates: List[Dict[str, Any]],
                                budget: Optional[int] = None) -> Dict[str, Any]:
        """Run all candidates + baselines for one benchmark program in parallel."""
        budget = budget or self.default_budget

        # Ensure base IR exists
        src_path = Path(source_file)
        ir_name = f"{program_id}_{src_path.stem}.ll"
        base_ir = self.ir_dir / ir_name
        if not base_ir.is_file():
            ok, msg = self.compiler.compile_to_ir(source_file, str(base_ir))
            if not ok:
                return {
                    "program_id": program_id,
                    "status": "ir_generation_failed",
                    "error": msg,
                    "candidate_results": []
                }

        baselines = [c for c in candidates if c.get("is_baseline", False)]
        sequences = [c for c in candidates if not c.get("is_baseline", False)]
        eval_sequences = sequences[:budget]
        all_eval_cands = baselines + eval_sequences

        candidate_results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_cand = {
                executor.submit(self.evaluate_candidate, program_id, str(base_ir), c): c
                for c in all_eval_cands
            }
            for future in as_completed(future_to_cand):
                try:
                    res = future.result()
                    candidate_results.append(res)
                except Exception as e:
                    c = future_to_cand[future]
                    candidate_results.append({
                        "program_id": program_id,
                        "candidate_id": c["id"],
                        "pipeline": c["pipeline"],
                        "status": "exception",
                        "code_size": None,
                        "compile_time_ms": 0.0,
                        "error": str(e)
                    })

        self._save_cache()

        valid_seq_results = [
            r for r in candidate_results
            if r["status"] == "success"
            and r["code_size"] is not None
            and r["candidate_id"] not in ["O2", "OZ"]
        ]

        best_cand = None
        best_size = None
        if valid_seq_results:
            best_r = min(valid_seq_results, key=lambda x: x["code_size"])
            best_cand = best_r["candidate_id"]
            best_size = best_r["code_size"]

        o2_size = next((r["code_size"] for r in candidate_results
                       if r["candidate_id"] == "O2" and r["status"] == "success"), None)
        oz_size = next((r["code_size"] for r in candidate_results
                       if r["candidate_id"] == "OZ" and r["status"] == "success"), None)

        return {
            "program_id": program_id,
            "status": "completed",
            "base_ir": str(base_ir),
            "baseline_O2_size": o2_size,
            "baseline_Oz_size": oz_size,
            "best_candidate": best_cand,
            "best_candidate_size": best_size,
            "total_candidates_evaluated": len(candidate_results),
            "candidate_results": candidate_results
        }
