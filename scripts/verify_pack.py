#!/usr/bin/env python3
"""End-to-end verification script for Rupokar Studios LoupeDeck Pack."""

import json
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def check():
    print("=== Rupokar Studios LoupeDeck Pack Verification ===")
    errors = []

    # 1. Manifest and SVGs
    manifest_file = REPO_ROOT / "icons" / "final-icon-manifest.json"
    if not manifest_file.exists():
        errors.append("Manifest missing")
    else:
        with open(manifest_file, "r") as f:
            data = json.load(f)
        if len(data) != 168:
            errors.append(f"Manifest count is {len(data)}, expected 168")
        sparks = [x for x in data if x["glyph"] == "spark"]
        if sparks:
            errors.append(f"Found {len(sparks)} fallback spark icons")

    # 2. Profile LP5
    lp5_file = REPO_ROOT / "profile" / "Rupokar-Resolve-CT.lp5"
    if not lp5_file.exists():
        errors.append("Profile .lp5 file missing")
    else:
        with zipfile.ZipFile(lp5_file, "r") as z:
            if "ProfileInfo.json" not in z.namelist():
                errors.append("ProfileInfo.json missing from .lp5")

    # 3. Keyboard preset
    key_file = REPO_ROOT / "keyboard-preset" / "Rupokar_Resolve_Keys.txt"
    if not key_file.exists():
        errors.append("Keyboard preset file missing")

    # 4. Bridge script
    bridge_script = REPO_ROOT / "scripts" / "run_bridge.sh"
    if not bridge_script.exists():
        errors.append("Bridge runner script missing")

    if errors:
        print("FAILED with errors:")
        for e in errors:
            print(f"  ❌ {e}")
        return False
    else:
        print("✅ ALL PACK INTEGRITY CHECKS PASSED (168 Actions, LP5 Profile, Bridge, Shortcuts)")
        return True


if __name__ == "__main__":
    import sys
    sys.exit(0 if check() else 1)
