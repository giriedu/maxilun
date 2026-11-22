#!/usr/bin/env python3
"""Root entrypoint for component_lookup - CLI tool to search the 220+ component & 84 registry ecosystem.
Delegates directly to skills/maxilun-craft/scripts/component_lookup.py.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "skills", "maxilun-craft", "scripts", "component_lookup.py")

if not os.path.exists(TARGET):
    HOME = os.path.expanduser("~")
    TARGET = os.path.join(HOME, ".agents", "skills", "maxilun-craft", "scripts", "component_lookup.py")

if os.path.exists(TARGET):
    import importlib.util
    spec = importlib.util.spec_from_file_location("comp_lookup", TARGET)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.exit(mod.main())
else:
    print(f"Error: component_lookup.py not found at {TARGET}", file=sys.stderr)
    sys.exit(1)
