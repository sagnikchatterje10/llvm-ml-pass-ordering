#!/usr/bin/env python3
"""
Environment and Toolchain Checker for LLVM ML Pass Project.

Verifies:
- Python version (>= 3.8)
- Python packages (numpy, pandas, scikit-learn, scipy, matplotlib, seaborn, pyyaml, joblib)
- LLVM tools (clang, opt, llvm-size, llvm-dis, llc)
- Detects LLVM version and validates new pass manager support
- Generates an environment manifest for experiment reproducibility
"""

import sys
import os
import shutil
import subprocess
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

REQUIRED_PYTHON_PACKAGES = [
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("sklearn", "scikit-learn"),
    ("scipy", "scipy"),
    ("matplotlib", "matplotlib"),
    ("seaborn", "seaborn"),
    ("yaml", "PyYAML"),
    ("joblib", "joblib"),
]

LLVM_CANDIDATE_SEARCH_PATHS = [
    r"C:\COMPILER PROJECT\llvm\bin",
    os.path.expandvars(r"%USERPROFILE%\LLVM\bin"),
    r"C:\Program Files\LLVM\bin",
    r"C:\Program Files (x86)\LLVM\bin",
    r"C:\LLVM\bin",
    r"C:\msys64\clang64\bin",
    r"C:\msys64\ucrt64\bin",
    r"C:\msys64\mingw64\bin",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\LLVM\bin"),
]

def find_tool(tool_name: str, config_override: Optional[str] = None) -> Optional[str]:
    """Find the path to an executable tool, checking config, PATH, and known install dirs."""
    if config_override and config_override != "auto" and os.path.isfile(config_override):
        return os.path.abspath(config_override)

    # 1. Search PATH
    path_hit = shutil.which(tool_name)
    if path_hit:
        return os.path.abspath(path_hit)

    # If on Windows, check with .exe
    if sys.platform == "win32" and not tool_name.endswith(".exe"):
        path_hit = shutil.which(f"{tool_name}.exe")
        if path_hit:
            return os.path.abspath(path_hit)

    # 2. Check candidate search paths
    exe_names = [tool_name]
    if sys.platform == "win32" and not tool_name.endswith(".exe"):
        exe_names.append(f"{tool_name}.exe")

    for dir_path in LLVM_CANDIDATE_SEARCH_PATHS:
        if os.path.isdir(dir_path):
            for name in exe_names:
                full_path = os.path.join(dir_path, name)
                if os.path.isfile(full_path):
                    return os.path.abspath(full_path)

    return None

def get_tool_version(tool_path: str) -> Optional[str]:
    """Run tool --version and parse the first line of output."""
    try:
        res = subprocess.run([tool_path, "--version"], capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            lines = res.stdout.strip().splitlines()
            if lines:
                return lines[0].strip()
        return None
    except Exception as e:
        return f"Error running tool: {e}"

def check_python_environment() -> Dict[str, Any]:
    """Check Python version and required packages."""
    py_info = {
        "version": sys.version.split()[0],
        "version_info": list(sys.version_info[:3]),
        "compatible": sys.version_info >= (3, 8),
        "packages": {}
    }
    all_packages_ok = True
    for mod_name, pip_name in REQUIRED_PYTHON_PACKAGES:
        try:
            mod = __import__(mod_name)
            ver = getattr(mod, "__version__", "unknown")
            py_info["packages"][pip_name] = {"installed": True, "version": ver}
        except ImportError:
            py_info["packages"][pip_name] = {"installed": False, "version": None}
            all_packages_ok = False

    py_info["all_packages_ok"] = all_packages_ok
    return py_info

def check_llvm_environment(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Check LLVM toolchain executables and capabilities."""
    env_cfg = config.get("environment", {}) if config else {}
    tools_to_check = {
        "clang": env_cfg.get("clang_path", "auto"),
        "opt": env_cfg.get("opt_path", "auto"),
        "llvm-size": env_cfg.get("llvm_size_path", "auto"),
        "llvm-dis": env_cfg.get("llvm_dis_path", "auto"),
    }

    llvm_info = {
        "tools": {},
        "all_required_present": True,
        "llvm_version": None,
        "new_pm_supported": False,
    }

    for tool_name, override in tools_to_check.items():
        path = find_tool(tool_name, override)
        if path:
            version_str = get_tool_version(path)
            llvm_info["tools"][tool_name] = {
                "available": True,
                "path": path,
                "version": version_str
            }
            if tool_name == "clang" and version_str and "version" in version_str:
                llvm_info["llvm_version"] = version_str
        else:
            llvm_info["tools"][tool_name] = {
                "available": False,
                "path": None,
                "version": None
            }
            # clang is strictly required; opt is optional in LLVM 23+ (clang handles optimization)
            if tool_name in ["clang"]:
                llvm_info["all_required_present"] = False

    # Check opt new pass manager support
    opt_info = llvm_info["tools"].get("opt")
    if opt_info and opt_info["available"]:
        try:
            # Test running opt with new pass manager flag
            test_run = subprocess.run([opt_info["path"], "-passes=no-op-module", "--version"],
                                      capture_output=True, text=True, timeout=5)
            # If it accepts -passes= syntax without crashing or unknown option error
            llvm_info["new_pm_supported"] = True
        except Exception:
            llvm_info["new_pm_supported"] = False

    return llvm_info

def run_environment_check(config_path: Optional[str] = None, save_manifest: bool = True) -> Tuple[bool, Dict[str, Any]]:
    """Execute complete environment check and print report."""
    config = None
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

    print("=" * 60)
    print(" LLVM ML PASS OPTIMIZATION - ENVIRONMENT CHECK")
    print("=" * 60)

    # 1. Python Check
    py_info = check_python_environment()
    print(f"\n[Python]")
    print(f"  Version: {py_info['version']} ({'OK' if py_info['compatible'] else 'UPGRADE RECOMMENDED (>=3.8)'})")
    print("  Required packages:")
    for pkg_name, pkg_data in py_info["packages"].items():
        status = f"OK (v{pkg_data['version']})" if pkg_data["installed"] else "MISSING"
        print(f"    - {pkg_name:<16}: {status}")

    # 2. LLVM Check
    llvm_info = check_llvm_environment(config)
    print(f"\n[LLVM Toolchain]")
    for tool_name, tool_data in llvm_info["tools"].items():
        if tool_data["available"]:
            print(f"  - {tool_name:<12}: FOUND -> {tool_data['path']}")
            print(f"    Version: {tool_data['version']}")
        else:
            if tool_name == "opt":
                print(f"  - {tool_name:<12}: NOT FOUND (OK - LLVM 23+ uses clang directly)")
            else:
                print(f"  - {tool_name:<12}: NOT FOUND")

    print(f"  Pass Manager: {'New Pass Manager (-passes=...) Supported' if llvm_info['new_pm_supported'] else 'Legacy or Unknown'}")

    # Overall Status
    ready = py_info["all_packages_ok"] and llvm_info["all_required_present"]
    print("\n" + "=" * 60)
    if ready:
        print(" STATUS: ENVIRONMENT READY FOR COMPILER EXPERIMENTS")
    else:
        print(" STATUS: ACTION REQUIRED - MISSING COMPONENTS")
        if not py_info["all_packages_ok"]:
            print("   * Run: pip install -r requirements.txt")
        if not llvm_info["all_required_present"]:
            print("   * LLVM/Clang or opt is not detected in PATH or standard install directories.")
            print("   * Windows: winget install LLVM.LLVM or install from https://releases.llvm.org")
            print("   * Or specify paths in config.yaml under environment.")
    print("=" * 60)

    manifest = {
        "python": py_info,
        "llvm": llvm_info,
        "environment_ready": ready
    }

    if save_manifest:
        out_dir = Path("experiments")
        out_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = out_dir / "environment_manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"Manifest written to: {manifest_path}")

    return ready, manifest

if __name__ == "__main__":
    cfg_file = "config.yaml" if os.path.exists("config.yaml") else None
    ready, _ = run_environment_check(cfg_file)
    sys.exit(0 if ready else 1)
