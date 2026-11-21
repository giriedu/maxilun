#!/usr/bin/env python3
"""Root entrypoint for slopscan - mechanical check for machine-averaged UI.
Delegates directly to skills/maxilun-craft/scripts/slopscan.py.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "skills", "maxilun-craft", "scripts", "slopscan.py")

if not os.path.exists(TARGET):
    HOME = os.path.expanduser("~")
    TARGET = os.path.join(HOME, ".agents", "skills", "maxilun-craft", "scripts", "slopscan.py")

if os.path.exists(TARGET):
    import importlib.util
    spec = importlib.util.spec_from_file_location("slopscan_craft", TARGET)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.exit(mod.main(sys.argv[1:]))
else:
    print(f"Error: slopscan.py not found at {TARGET}", file=sys.stderr)
    sys.exit(1)

