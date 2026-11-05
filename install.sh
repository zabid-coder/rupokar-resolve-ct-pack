#!/bin/bash
# ==============================================================================
# Rupokar Studios — Loupedeck CT Pack Terminal Installer for DaVinci Resolve
# Run: bash install.sh
# ==============================================================================

set -e
cd "$(dirname "$0")"

echo "========================================================================"
echo " Rupokar Studios — Loupedeck CT Pack Installer for DaVinci Resolve"
echo "========================================================================"

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

echo "🔍 Detected Python: $(python3 --version)"

echo "🔄 Closing Loupedeck to prevent file conflicts..."
pkill -f "Loupedeck" 2>/dev/null || true
pkill -f "LogiPlugin" 2>/dev/null || true
sleep 2

echo "🎨 [1/4] Building SVG icons..."
python3 scripts/build_icons.py

echo "🖼️  [2/4] Exporting PNG raster icons..."
python3 scripts/export_raster_icons.py

echo "📦 [3/4] Building profile package..."
python3 scripts/build_profile.py

echo "🚀 [4/4] Installing Loupedeck CT profile..."
python3 scripts/install_ct_profile.py

echo "🔄 Restarting Loupedeck..."
open -a "Loupedeck" 2>/dev/null || open "/Applications/Loupedeck.app" 2>/dev/null || true

echo "✅ Loupedeck CT installation complete!"
