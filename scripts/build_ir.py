#!/usr/bin/env python3
"""
Build LLVM IR from benchmark C/C++ source programs.
Usage:
  python scripts/build_ir.py                   # Process all benchmarks in manifest
  python scripts/build_ir.py --source file.c   # Process single file
  python scripts/build_ir.py --force           # Force rebuild even if exists
"""

import sys
import os
import argparse
import json
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.experiment_runner.compiler import LLVMCompiler

def parse_args():
    parser = argparse.ArgumentParser(description="Generate LLVM IR (.ll) from benchmark C source files")
    parser.add_argument("--source", "-s", type=str, default=None, help="Single source file to compile to IR")
    parser.add_argument("--manifest", "-m", type=str, default="benchmarks/metadata/manifest.json", help="Path to manifest JSON")
    parser.add_argument("--output-dir", "-o", type=str, default="ir", help="Output directory for .ll files")
    parser.add_argument("--config", "-c", type=str, default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--force", action="store_true", help="Force rebuild existing IR files")
    return parser.parse_args()

def main():
    args = parse_args()
    config = {}
    if os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    env_cfg = config.get("environment", {})
    compiler = LLVMCompiler(
        clang_path=None if env_cfg.get("clang_path") == "auto" else env_cfg.get("clang_path"),
        opt_path=None if env_cfg.get("opt_path") == "auto" else env_cfg.get("opt_path"),
        llvm_size_path=None if env_cfg.get("llvm_size_path") == "auto" else env_cfg.get("llvm_size_path"),
        extra_clang_flags=env_cfg.get("extra_clang_flags")
    )

    ready, msg = compiler.is_ready()
    if not ready:
        print(f"Error: Toolchain not ready ({msg}).", file=sys.stderr)
        print("Please check your environment using: python scripts/check_environment.py", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    items = []
    if args.source:
        src = Path(args.source)
        if not src.is_file():
            print(f"Error: Source file {args.source} not found.", file=sys.stderr)
            sys.exit(1)
        pid = src.stem.split("_")[0] if "_" in src.stem else src.stem
        out_ll = out_dir / f"{src.stem}.ll"
        items.append({"program_id": pid, "source_file": str(src), "output_ll": str(out_ll)})
    else:
        manifest_path = Path(args.manifest)
        if not manifest_path.is_file():
            print(f"Error: Manifest {args.manifest} not found.", file=sys.stderr)
            sys.exit(1)
        with open(manifest_path, "r", encoding="utf-8") as f:
            benchmarks = json.load(f)
        for b in benchmarks:
            src = Path(b["source_file"])
            out_ll = out_dir / f"{b['program_id']}_{b['name']}.ll"
            items.append({"program_id": b["program_id"], "source_file": str(src), "output_ll": str(out_ll)})

    print(f"Generating LLVM IR for {len(items)} program(s)...")
    successes = 0
    failures = 0

    for it in items:
        out_p = Path(it["output_ll"])
        if out_p.is_file() and not args.force:
            print(f"  [CACHED] {it['program_id']} -> {it['output_ll']}")
            successes += 1
            continue

        ok, err = compiler.compile_to_ir(it["source_file"], it["output_ll"])
        if ok:
            print(f"  [OK]     {it['program_id']} -> {it['output_ll']}")
            successes += 1
        else:
            print(f"  [FAIL]   {it['program_id']} -> {err}", file=sys.stderr)
            failures += 1

    print(f"\nIR Generation Complete: {successes} succeeded, {failures} failed.")
    if failures > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
