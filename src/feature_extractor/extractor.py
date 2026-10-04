"""
Deterministic LLVM IR Feature Extractor.
Parses LLVM text IR (.ll) files and extracts compiler-relevant features:
- Program Size (instructions, functions, basic blocks)
- Control Flow (branches, conditional branches, switches, ratios)
- Memory (loads, stores, allocas, GEPs, ratios)
- Computation (integer arithmetic, FP arithmetic, comparisons, casts)
- Function/Calls (direct calls, indirect calls)
- SSA / IR (PHI nodes, select instructions)
- Loop / CFG signals (detected back-edges, loop header candidates)
- Normalized ratios
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import pandas as pd

# Regular expressions for LLVM IR instructions
RE_FUNC_DEF = re.compile(r"^define\s+.*@([a-zA-Z0-9_$.]+)\s*\(")
RE_FUNC_DECL = re.compile(r"^declare\s+.*@([a-zA-Z0-9_$.]+)\s*\(")
RE_BB_LABEL = re.compile(r"^([a-zA-Z0-9_$.]+):\s*(;.*)?$")

# Opcodes
INT_ARITH_OPCODES = {
    "add", "sub", "mul", "udiv", "sdiv", "urem", "srem",
    "shl", "lshr", "ashr", "and", "or", "xor"
}
FP_ARITH_OPCODES = {"fadd", "fsub", "fmul", "fdiv", "frem", "fneg"}
CMP_OPCODES = {"icmp", "fcmp"}
CAST_OPCODES = {
    "trunc", "zext", "sext", "fptrunc", "fpext",
    "fptoui", "fptosi", "uitofp", "sitofp",
    "ptrtoint", "inttoptr", "bitcast", "addrspacecast"
}

FEATURE_COLUMNS = [
    # Size
    "instructions", "functions", "basic_blocks",
    # Control flow
    "branches", "cond_branches", "uncond_branches", "switches", "indirect_branches",
    # Memory
    "loads", "stores", "allocas", "geps",
    # Computation
    "int_arith", "fp_arith", "comparisons", "casts",
    # Calls
    "calls", "indirect_calls",
    # SSA / IR
    "phis", "selects",
    # Loops
    "loop_backedges",
    # Normalized ratios
    "instr_per_bb", "branch_ratio", "cond_branch_ratio",
    "load_ratio", "store_ratio", "mem_ratio",
    "arith_ratio", "call_ratio", "phi_ratio"
]

class LLVMFeatureExtractor:
    """Extracts deterministic static features from an LLVM IR (.ll) text file."""

    def __init__(self):
        pass

    def extract_from_file(self, filepath: str, program_id: Optional[str] = None) -> Dict[str, Any]:
        """Extract features from a .ll file on disk."""
        path = Path(filepath)
        if not path.is_file():
            raise FileNotFoundError(f"LLVM IR file not found: {filepath}")

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        pid = program_id or path.stem
        return self.extract_from_text(content, pid)

    def extract_from_text(self, ir_text: str, program_id: str) -> Dict[str, Any]:
        """Parse LLVM IR string and compute feature dictionary."""
        lines = ir_text.splitlines()

        num_functions = 0
        num_blocks = 0
        num_instructions = 0

        branches = 0
        cond_branches = 0
        uncond_branches = 0
        switches = 0
        indirect_branches = 0

        loads = 0
        stores = 0
        allocas = 0
        geps = 0

        int_arith = 0
        fp_arith = 0
        comparisons = 0
        casts = 0

        calls = 0
        indirect_calls = 0
        phis = 0
        selects = 0

        # CFG tracking for loops: list of (block_name, [successors]) per function
        current_func: Optional[str] = None
        current_bb: Optional[str] = None
        func_bbs: Dict[str, List[str]] = {}
        func_cfg: Dict[str, Dict[str, List[str]]] = {}

        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith(";"):
                continue

            # Check function definition
            m_def = RE_FUNC_DEF.match(line)
            if m_def:
                current_func = m_def.group(1)
                num_functions += 1
                func_bbs[current_func] = []
                func_cfg[current_func] = {}
                # The entry block has implicit or explicit label
                current_bb = "entry"
                func_bbs[current_func].append(current_bb)
                func_cfg[current_func][current_bb] = []
                continue

            # Check function end
            if line == "}":
                current_func = None
                current_bb = None
                continue

            # Only parse inside function definitions
            if current_func is None:
                continue

            # Check basic block label
            m_bb = RE_BB_LABEL.match(line)
            if m_bb:
                current_bb = m_bb.group(1)
                num_blocks += 1
                if current_bb not in func_bbs[current_func]:
                    func_bbs[current_func].append(current_bb)
                if current_bb not in func_cfg[current_func]:
                    func_cfg[current_func][current_bb] = []
                continue

            # Instruction parsing
            # Format usually: %dest = opcode ... OR opcode ...
            tokens = line.split()
            if not tokens:
                continue

            opcode = None
            if len(tokens) >= 3 and tokens[1] == "=":
                # %res = opcode ...
                opcode = tokens[2]
                # Handle possible decorators like "tail call", "musttail call"
                if opcode in ["tail", "musttail", "notail"] and len(tokens) >= 4:
                    opcode = tokens[3]
            else:
                opcode = tokens[0]

            # Strip atomic or fast-math or call qualifiers
            if opcode in ["tail", "musttail", "notail"] and len(tokens) > 1:
                opcode = tokens[1]

            num_instructions += 1

            # Count by category
            if opcode == "br":
                branches += 1
                # Format: br i1 %cond, label %b1, label %b2 OR br label %dest
                if "label" in line:
                    labels = re.findall(r"label\s+%([a-zA-Z0-9_$.]+)", line)
                    if len(labels) > 1:
                        cond_branches += 1
                    else:
                        uncond_branches += 1
                    if current_func and current_bb:
                        func_cfg[current_func][current_bb].extend(labels)
                else:
                    uncond_branches += 1

            elif opcode == "switch":
                switches += 1
                labels = re.findall(r"label\s+%([a-zA-Z0-9_$.]+)", line)
                if current_func and current_bb:
                    func_cfg[current_func][current_bb].extend(labels)

            elif opcode == "indirectbr":
                indirect_branches += 1

            elif opcode == "load":
                loads += 1
            elif opcode == "store":
                stores += 1
            elif opcode == "alloca":
                allocas += 1
            elif opcode == "getelementptr":
                geps += 1

            elif opcode in INT_ARITH_OPCODES:
                int_arith += 1
            elif opcode in FP_ARITH_OPCODES:
                fp_arith += 1
            elif opcode in CMP_OPCODES:
                comparisons += 1
            elif opcode in CAST_OPCODES:
                casts += 1

            elif opcode in ["call", "invoke"]:
                calls += 1
                # Check direct (@func) vs indirect (%func or pointer)
                if "@" not in line and "%" in line:
                    indirect_calls += 1

            elif opcode == "phi":
                phis += 1
            elif opcode == "select":
                selects += 1

        # Fallback if entry block wasn't counted as an explicit label
        if num_functions > 0 and num_blocks < num_functions:
            num_blocks = max(num_blocks, num_functions)

        # Calculate simple CFG loop back-edges
        # A back-edge in structured CFG goes to an earlier block or itself
        loop_backedges = 0
        for f_name, cfg in func_cfg.items():
            order = {bb: idx for idx, bb in enumerate(func_bbs.get(f_name, []))}
            for src_bb, successors in cfg.items():
                src_idx = order.get(src_bb, 999999)
                for succ in successors:
                    succ_idx = order.get(succ, 999999)
                    if succ_idx <= src_idx and succ_idx != 999999:
                        loop_backedges += 1

        # Normalized Ratios (safe division)
        inst_safe = max(num_instructions, 1)
        bb_safe = max(num_blocks, 1)

        instr_per_bb = round(num_instructions / bb_safe, 4)
        branch_ratio = round(branches / inst_safe, 4)
        cond_branch_ratio = round(cond_branches / inst_safe, 4)
        load_ratio = round(loads / inst_safe, 4)
        store_ratio = round(stores / inst_safe, 4)
        mem_ratio = round((loads + stores + allocas + geps) / inst_safe, 4)
        arith_ratio = round((int_arith + fp_arith) / inst_safe, 4)
        call_ratio = round(calls / inst_safe, 4)
        phi_ratio = round(phis / inst_safe, 4)

        result = {
            "program_id": program_id,
            "instructions": num_instructions,
            "functions": num_functions,
            "basic_blocks": num_blocks,
            "branches": branches,
            "cond_branches": cond_branches,
            "uncond_branches": uncond_branches,
            "switches": switches,
            "indirect_branches": indirect_branches,
            "loads": loads,
            "stores": stores,
            "allocas": allocas,
            "geps": geps,
            "int_arith": int_arith,
            "fp_arith": fp_arith,
            "comparisons": comparisons,
            "casts": casts,
            "calls": calls,
            "indirect_calls": indirect_calls,
            "phis": phis,
            "selects": selects,
            "loop_backedges": loop_backedges,
            "instr_per_bb": instr_per_bb,
            "branch_ratio": branch_ratio,
            "cond_branch_ratio": cond_branch_ratio,
            "load_ratio": load_ratio,
            "store_ratio": store_ratio,
            "mem_ratio": mem_ratio,
            "arith_ratio": arith_ratio,
            "call_ratio": call_ratio,
            "phi_ratio": phi_ratio,
        }
        return result

    def extract_batch(self, files: List[Tuple[str, str]]) -> pd.DataFrame:
        """Extract features for multiple files [(file_path, program_id)]. Returns DataFrame."""
        rows = []
        for fpath, pid in files:
            row = self.extract_from_file(fpath, pid)
            rows.append(row)
        df = pd.DataFrame(rows)
        # Ensure deterministic column ordering
        cols = ["program_id"] + [c for c in FEATURE_COLUMNS if c in df.columns]
        return df[cols]
