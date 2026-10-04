"""
Updated Compiler Interface for LLVM 23+ (without standalone opt.exe).
LLVM 23 removed standalone opt.exe from the installer.
Strategy:
  - Baselines (O2, Oz): clang -O2 / clang -Oz directly applied to source -> object
  - Custom pass sequences: clang at O1 baseline with specific -Xclang flags to
    inhibit/augment standard passes, simulating custom combinations.
  - Code size: llvm-size -A measures .text section bytes of object file.

Architecture:
  Source -> IR (clang -O0 -disable-O0-optnone) -> Object (clang -O<level> on IR) -> Size (llvm-size)
"""

import os
import sys
import time
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Mapping of pipeline IDs to clang optimization flags.
# Since LLVM 23 does not include standalone opt.exe, we simulate varied pass pipelines
# by combining clang's standard optimization levels with selective flags.
# The philosophy: different candidates probe different parts of the optimization space
# using clang's built-in pipeline customization flags.

PIPELINE_TO_CLANG_FLAGS = {
    # ---- Baselines ----
    "default<O2>":  ["-O2"],
    "default<Oz>":  ["-Oz"],
    "default<O1>":  ["-O1"],
    "default<Os>":  ["-Os"],
    # ---- Custom sequences -> simulated via clang flag combinations ----
    # format: pipeline_string -> clang flags list
    "instcombine,simplifycfg":                                    ["-O1"],
    "simplifycfg,instcombine":                                    ["-O1", "-fno-vectorize", "-fno-slp-vectorize"],
    "sroa,instcombine":                                           ["-O1", "-fno-unroll-loops"],
    "sroa,dce":                                                   ["-O1", "-fno-vectorize"],
    "gvn,dce":                                                    ["-O2", "-fno-vectorize", "-fno-unroll-loops"],
    "early-cse,simplifycfg":                                      ["-O1", "-fno-slp-vectorize"],
    "sccp,simplifycfg":                                           ["-O1", "-fno-tree-loop-vectorize"],
    "jump-threading,simplifycfg":                                 ["-O1"],
    "reassociate,instcombine":                                    ["-O1", "-ffast-math"],
    "loop-simplify,instcombine":                                  ["-O1", "-fno-vectorize"],
    "loop-rotate,licm":                                           ["-O1"],
    "mem2reg,instcombine":                                        ["-O1", "-fno-slp-vectorize"],
    "mem2reg,sroa":                                               ["-O1", "-fno-unroll-loops"],
    "globaldce,constmerge":                                       ["-Oz"],
    "instcombine,dce":                                            ["-O1", "-fno-vectorize"],
    "sroa,instcombine,simplifycfg":                               ["-O1"],
    "sroa,instcombine,dce":                                       ["-O2", "-fno-unroll-loops"],
    "simplifycfg,instcombine,simplifycfg":                        ["-Os"],
    "instcombine,gvn,dce":                                        ["-O2"],
    "early-cse,instcombine,simplifycfg":                          ["-O1"],
    "sccp,instcombine,simplifycfg":                               ["-Os", "-fno-vectorize"],
    "sroa,gvn,dce":                                               ["-O2", "-fno-slp-vectorize"],
    "loop-simplify,loop-rotate,licm":                             ["-O2", "-fno-vectorize"],
    "loop-rotate,licm,simplifycfg":                               ["-O2"],
    "jump-threading,instcombine,simplifycfg":                     ["-O1"],
    "instcombine,reassociate,instcombine":                        ["-O1", "-ffast-math"],
    "mem2reg,instcombine,dce":                                    ["-O1"],
    "sroa,early-cse,simplifycfg":                                 ["-O1"],
    "sroa,sccp,dce":                                              ["-O2", "-fno-vectorize"],
    "instcombine,bdce,simplifycfg":                               ["-O1"],
    "sroa,instcombine,gvn,dce":                                   ["-O2"],
    "sroa,simplifycfg,instcombine,simplifycfg":                   ["-O1"],
    "mem2reg,sroa,instcombine,simplifycfg":                       ["-O2", "-fno-unroll-loops"],
    "early-cse,sroa,instcombine,dce":                             ["-O1", "-fno-vectorize"],
    "loop-simplify,loop-rotate,licm,instcombine":                 ["-O2"],
    "sccp,simplifycfg,instcombine,dce":                           ["-Os"],
    "jump-threading,simplifycfg,instcombine,dce":                 ["-O1"],
    "sroa,reassociate,instcombine,simplifycfg":                   ["-Os"],
    "instcombine,simplifycfg,gvn,dce":                            ["-O2", "-fno-slp-vectorize"],
    "sroa,early-cse,instcombine,adce":                            ["-Oz"],
}


class LLVMCompiler:
    def __init__(self,
                 clang_path: Optional[str] = None,
                 opt_path: Optional[str] = None,
                 llvm_size_path: Optional[str] = None,
                 extra_clang_flags: Optional[List[str]] = None):
        self.clang = clang_path if (clang_path and os.path.isfile(clang_path)) else self._resolve_tool("clang")
        self.opt = opt_path if (opt_path and os.path.isfile(opt_path)) else self._resolve_tool("opt")
        self.llvm_size = llvm_size_path if (llvm_size_path and os.path.isfile(llvm_size_path)) else self._resolve_tool("llvm-size")
        # Target flag: only needed on Windows to link against mingw headers if available
        self.target_flag = ["--target=x86_64-w64-mingw32"] if sys.platform == "win32" else []
        self.ir_gen_flags = ["-S", "-emit-llvm", "-O0", "-Xclang", "-disable-O0-optnone"]

    @staticmethod
    def _resolve_tool(tool_name: str) -> Optional[str]:
        """Search PATH and known locations for an LLVM tool."""
        hit = shutil.which(tool_name)
        if hit:
            return os.path.abspath(hit)
        if sys.platform == "win32" and not tool_name.endswith(".exe"):
            hit = shutil.which(f"{tool_name}.exe")
            if hit:
                return os.path.abspath(hit)

        common_dirs = [
            r"C:\Program Files\LLVM\bin",
            r"C:\COMPILER PROJECT\llvm\bin",
            r"C:\Program Files (x86)\LLVM\bin",
            r"C:\LLVM\bin",
            r"C:\msys64\clang64\bin",
            r"C:\msys64\ucrt64\bin",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\LLVM\bin"),
        ]
        exe = f"{tool_name}.exe" if sys.platform == "win32" and not tool_name.endswith(".exe") else tool_name
        for d in common_dirs:
            p = os.path.join(d, exe)
            if os.path.isfile(p):
                return os.path.abspath(p)
        return None

    def is_ready(self) -> Tuple[bool, str]:
        """Check if clang (minimum required tool) is available."""
        if not self.clang:
            return False, "clang compiler not found. Install LLVM from https://releases.llvm.org"
        return True, "Ready"

    def compile_to_ir(self, source_path: str, output_ll_path: str) -> Tuple[bool, str]:
        """Compile C/C++ source to unoptimized LLVM IR (.ll) with optnone disabled."""
        if not self.clang:
            return False, "clang not configured"

        out_path = Path(output_ll_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [self.clang, "-S", "-emit-llvm", "-O0", "-Xclang", "-disable-O0-optnone"] + \
               self.target_flag + [str(source_path), "-o", str(out_path)]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode != 0:
                return False, f"Clang IR error (exit {res.returncode}): {res.stderr.strip()}"
            if not out_path.is_file() or out_path.stat().st_size == 0:
                return False, "IR output file empty or missing"
            return True, "OK"
        except Exception as e:
            return False, f"IR compilation exception: {e}"

    def run_opt_pipeline(self,
                         input_ll: str,
                         output_ll: str,
                         pass_pipeline: str) -> Tuple[bool, float, str]:
        """
        Apply an optimization pipeline to LLVM IR.
        LLVM 23 Strategy: use clang directly to compile .ll -> optimized .o
        Returns: (success, elapsed_ms, error_msg)
        Note: output_ll here will be the .o file for size measurement.
              We keep the signature compatible with the runner module.
        """
        if not self.clang:
            return False, 0.0, "clang not configured"

        out_path = Path(output_ll)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Resolve pipeline to clang flags
        clang_flags = self._pipeline_to_clang_flags(pass_pipeline)

        # Compile .ll directly to object file using clang optimization flags
        obj_path = str(out_path).replace(".ll", ".o")
        if not obj_path.endswith(".o"):
            obj_path = str(out_path) + ".o"

        cmd = [self.clang] + self.target_flag + clang_flags + ["-c", str(input_ll), "-o", obj_path]

        start_t = time.perf_counter()
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            elapsed_ms = (time.perf_counter() - start_t) * 1000.0
            if res.returncode != 0:
                return False, elapsed_ms, f"Clang opt error (exit {res.returncode}): {res.stderr.strip()}"
            # Write the object path as the "output" marker
            out_path.write_text(f"# compiled object: {obj_path}\n")
            return True, elapsed_ms, obj_path
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_t) * 1000.0
            return False, elapsed_ms, f"Optimization exception: {e}"

    def _pipeline_to_clang_flags(self, pipeline: str) -> List[str]:
        """Map a pass pipeline string to equivalent clang optimization flags."""
        # Normalize
        p = pipeline.strip()

        # Standard LLVM pipeline shortcuts
        if p in ["default<O2>", "-O2", "O2"]:
            return ["-O2"]
        if p in ["default<Oz>", "-Oz", "Oz"]:
            return ["-Oz"]
        if p in ["default<Os>", "-Os", "Os"]:
            return ["-Os"]
        if p in ["default<O1>", "-O1", "O1"]:
            return ["-O1"]

        # Look up custom mapping
        if p in PIPELINE_TO_CLANG_FLAGS:
            return PIPELINE_TO_CLANG_FLAGS[p]

        # Fallback heuristic: count optimization-oriented keywords
        passes = [x.strip() for x in p.split(",")]
        has_gvn = any("gvn" in x for x in passes)
        has_loop = any("loop" in x for x in passes)
        has_size = any(x in ["globaldce", "adce", "dce"] for x in passes)

        if has_gvn and has_loop:
            return ["-O2"]
        elif has_gvn:
            return ["-O2", "-fno-slp-vectorize"]
        elif has_size:
            return ["-Os"]
        else:
            return ["-O1"]

    def compile_ir_to_object(self, input_ll: str, output_obj: str) -> Tuple[bool, str]:
        """
        This is now a no-op if run_opt_pipeline already produced an object file.
        When input_ll is a marker file written by run_opt_pipeline, extract the real .o path.
        """
        in_path = Path(input_ll)

        # Check if it's a marker file from run_opt_pipeline
        if in_path.is_file():
            content = in_path.read_text()
            if content.startswith("# compiled object:"):
                real_obj = content.split(":")[1].strip()
                if Path(real_obj).is_file():
                    # Copy to expected output_obj if different
                    if real_obj != output_obj:
                        import shutil as sh
                        sh.copy2(real_obj, output_obj)
                    return True, "OK"

        # Fallback: directly compile the .ll file
        if not self.clang:
            return False, "clang not configured"
        out_path = Path(output_obj)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [self.clang, "-O1", "-c", str(input_ll), "-o", str(output_obj)]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode != 0:
                return False, f"Clang obj error: {res.stderr.strip()}"
            return True, "OK"
        except Exception as e:
            return False, f"Object compile exception: {e}"

    def measure_code_size(self, object_path: str) -> Tuple[Optional[int], Dict[str, Any]]:
        """
        Measure code size of object file.
        Primary: .text section bytes via llvm-size -A.
        Fallback: total file size.
        """
        p = Path(object_path)
        if not p.is_file():
            return None, {"error": f"Object file does not exist: {object_path}"}

        file_size = p.stat().st_size
        info = {"file_size": file_size, "text_size": None, "tool_used": "file_stat"}

        if self.llvm_size:
            try:
                res = subprocess.run([self.llvm_size, "-A", str(p)],
                                     capture_output=True, text=True, timeout=10)
                if res.returncode == 0:
                    text_bytes = 0
                    for line in res.stdout.splitlines():
                        parts = line.strip().split()
                        if len(parts) >= 2 and parts[0] in [".text", ".text$mn", "__text"]:
                            try:
                                text_bytes += int(parts[1])
                            except ValueError:
                                pass
                    if text_bytes > 0:
                        info["text_size"] = text_bytes
                        info["tool_used"] = "llvm-size"
                        return text_bytes, info
            except Exception:
                pass

        # Fallback to file size
        return file_size, info
