#!/bin/bash
# ==============================================================================
# Rupokar Studios — Loupedeck CT Pack 1-Click Installer for DaVinci Resolve
# Double-click this file on macOS to install everything automatically!
# ==============================================================================

# Change to the directory where this script is located
cd "$(dirname "$0")"

clear
echo "========================================================================"
echo "   ____  _   _ ____   ___  _  __    _    ____    ____ _____ _   _ ____  "
echo "  |  _ \| | | |  _ \ / _ \| |/ /   / \  |  _ \  / ___|_   _| | | |  _ \ "
echo "  | |_) | | | | |_) | | | | ' /   / _ \ | |_) | \___ \ | | | | | | | | |"
echo "  |  _ <| |_| |  __/| |_| | . \  / ___ \|  _ <   ___) || | | |_| | |_| |"
echo "  |_| \_\\\\___/|_|    \___/|_|\_\/_/   \_\_| \_\ |____/ |_|  \___/|____/ "
echo "                                                                        "
echo "      Loupedeck CT 168-Action Master Pack for DaVinci Resolve Studio     "
echo "========================================================================"
echo ""

# 1. Verify Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3 from https://www.python.org/ or via Homebrew (brew install python)."
    read -p "Press Enter to exit..."
    exit 1
fi

echo "🔍 Detected Python: $(python3 --version)"

# 2. Close Loupedeck cleanly so file writes are never locked
echo "🔄 Closing Loupedeck application to install profile cleanly..."
pkill -f "Loupedeck" 2>/dev/null || true
pkill -f "LogiPlugin" 2>/dev/null || true
sleep 2

# 3. Build SVG icons
echo "🎨 [1/4] Building 168 high-contrast vector icons..."
python3 scripts/build_icons.py
if [ $? -ne 0 ]; then
    echo "❌ Error building SVG icons."
    read -p "Press Enter to exit..."
    exit 1
fi

# 4. Export raster icons
echo "🖼️  [2/4] Exporting crisp high-DPI raster icons for Loupedeck..."
python3 scripts/export_raster_icons.py
if [ $? -ne 0 ]; then
    echo "❌ Error exporting PNG icons."
    read -p "Press Enter to exit..."
    exit 1
fi

# 5. Build LP5 profile archive
echo "📦 [3/4] Building Loupedeck profile package..."
python3 scripts/build_profile.py

# 6. Install CT Profile into Loupedeck20 active configuration
echo "🚀 [4/4] Injecting DaVinci Resolve Rupokar Profile into Loupedeck CT..."
python3 scripts/install_ct_profile.py
if [ $? -ne 0 ]; then
    echo "❌ Error installing Loupedeck CT profile."
    read -p "Press Enter to exit..."
    exit 1
fi

# 7. Relaunch Loupedeck app
echo ""
echo "🔄 Restarting Loupedeck..."
open -a "Loupedeck" 2>/dev/null || open "/Applications/Loupedeck.app" 2>/dev/null || true
sleep 2

echo ""
echo "========================================================================"
echo "🎉 INSTALLATION SUCCESSFUL! / সফলভাবে ইন্সটল সম্পন্ন হয়েছে!"
echo "========================================================================"
echo "✅ All 8 Workspaces fully populated (Zero empty holes / কোনো খালি বাটন নেই):"
echo "   [1] Media & Project (24 buttons: Media Pool + Break Timers)"
echo "   [2] Edit 1 - Timeline & Cuts (24 buttons: Razor, Trims, Ripple, Gaps)"
echo "   [3] Edit 2 - Sync & Colors (12 buttons: Audio Sync & Clip Colors)"
echo "   [4] Edit 3 - Fine Tuning (12 buttons: Precision Nudge & Timing)"
echo "   [5] Color - Nodes & Wheels (12 buttons: Node Tree, Scopes, Still, Compare)"
echo "   [6] Fairlight - Audio & Fades (12 buttons: Audio Level, Zoom, Normalize)"
echo "   [7] Deliver & Render Queue (24 buttons: YouTube, ProRes, Queue, Render)"
echo "   [8] Quick Export & Panels (12 buttons: Quick Export, 7 UI Panels, Bypass)"
echo ""
echo "✅ Round Buttons 1 to 8: Workspace navigation + DaVinci Resolve Page Switch (Shift+2 to Shift+9)"
echo "✅ Dials: 6 active dials per workspace (Shuttle, Zoom, Audio, Colors, Track Height)"
echo "✅ Wheel: Jog/Shuttle rotation + Play/Pause center tap"
echo "✅ Active Profile: 'DaVinci Resolve Rupokar' set as default!"
echo "========================================================================"
echo ""
read -p "Press Enter to close this window..."
