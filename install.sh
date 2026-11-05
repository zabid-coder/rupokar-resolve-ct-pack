#!/bin/bash
# ==============================================================================
# Rupokar Studios — Loupedeck CT Pack Terminal Installer for DaVinci Resolve
# Run: bash install.sh
# ==============================================================================

set -e
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3 from https://www.python.org/ or via Homebrew (brew install python)."
    exit 1
fi

python3 install.py
