#!/bin/bash
# ==============================================================================
# Rupokar Studios — Loupedeck CT Pack 1-Click Installer for DaVinci Resolve
# Double-click this file on macOS to install everything automatically!
# ==============================================================================

cd "$(dirname "$0")"

clear
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3 from https://www.python.org/ or via Homebrew (brew install python)."
    read -p "Press Enter to exit..."
    exit 1
fi

python3 install.py

echo ""
read -p "Press Enter to close this window..."
