#!/usr/bin/env python3
"""Rupokar Studios — Loupedeck CT Pack Cross-Platform Installer for DaVinci Resolve.

Works seamlessly on macOS and Windows.
Run: python3 install.py (macOS) or python install.py (Windows)
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

# Add scripts directory to path
sys.path.insert(0, str(REPO_ROOT / "scripts"))

try:
    import build_icons
    import export_raster_icons
    import build_profile
    import install_ct_profile
except ImportError as e:
    print(f"❌ Failed to import installer modules: {e}", file=sys.stderr)
    sys.exit(1)


def close_loupedeck():
    print("🔄 Closing Loupedeck to prevent file conflicts...")
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/IM", "Loupedeck.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["taskkill", "/F", "/IM", "LogiPluginService.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(["pkill", "-f", "Loupedeck"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "LogiPlugin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def restart_loupedeck():
    print("🔄 Restarting Loupedeck application...")
    if sys.platform == "win32":
        exe_path = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Loupedeck" / "Loupedeck.exe"
        if exe_path.exists():
            subprocess.Popen([str(exe_path)])
        else:
            try:
                os.startfile("loupedeck:")
            except Exception:
                pass
    else:
        subprocess.Popen(["open", "-a", "Loupedeck"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    print("=" * 72)
    print(" Rupokar Studios — Loupedeck CT Pack Installer for DaVinci Resolve")
    print(f" Platform: {sys.platform.upper()} | Python: {sys.version.split()[0]}")
    print("=" * 72)

    close_loupedeck()

    print("\n🎨 [1/4] Building SVG icons...")
    build_icons.main()

    print("\n🖼️  [2/4] Exporting PNG raster icons...")
    export_raster_icons.main()

    print("\n📦 [3/4] Building profile package (.lp5)...")
    build_profile.main()

    print("\n🚀 [4/4] Installing Loupedeck CT profile & shortcuts...")
    install_ct_profile.main()

    restart_loupedeck()

    print("\n" + "=" * 72)
    print("🎉 ALL SYSTEMS READY! DaVinci Resolve Rupokar CT Pack Installed Successfully!")
    print("=" * 72)


if __name__ == "__main__":
    main()
