# Rupokar Studios LoupeDeck CT Pack for DaVinci Resolve

<div align="center">

![DaVinci Resolve](https://img.shields.io/badge/DaVinci%20Resolve-18%20%26%2019%20Studio%20%2F%20Free-black?style=for-the-badge&logo=davinciresolve)
![Loupedeck Hardware](https://img.shields.io/badge/Loupedeck-CT%20(Loupedeck50)-5B4EE4?style=for-the-badge&logo=logitech)
![Platform](https://img.shields.io/badge/Platforms-macOS%20%7C%20Windows-0078D4?style=for-the-badge&logo=apple&logoColor=white)
![Actions](https://img.shields.io/badge/Actions-168%20Audited-success?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-28%20%2F%2028%20Passing-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

**The complete, production-grade 168-action control system for Loupedeck CT and DaVinci Resolve Studio / Free on macOS & Windows.**

[Quick Start](#-quick-start--auto-installation) • [Hardware Layout](#-hardware-layout--8-workspaces) • [Icon System](#-multi-ratio-vector-icon-suite) • [Keyboard Shortcuts](#-keyboard-shortcuts-auto-setup) • [Cross-Platform Guide](#-cross-platform-support-macos--windows)

</div>

---

## ⚡ What Makes This Pack Exceptional?

- 🎯 **168 Purpose-Built Actions**: Zero generic placeholders, zero spark fallbacks. Every single dial turn, dial press, touch button, wheel rotation, and physical key has an explicit, tested function.
- 📐 **Edge-to-Edge Wide Icon System**: Clean-sheet SVG vector geometry spanning `190–210px` across the 256×256 canvas. Eliminates dead black side margins with high-contrast dual-tone depth.
- 🎛️ **Text-Primary Inverted Dials**: Dials flip the visual hierarchy! Parameter names (`SHUTTLE`, `ZOOM`, `AUDIO LEVEL`, `GAMMA`) are displayed in **bold, 21px white typography** in the center for instant legibility at arm's length.
- 🚀 **1-Click Auto-Installer for macOS & Windows**:
  - Automatically closes Loupedeck to prevent file locking.
  - Generates 336 high-DPI raster icons (native 512×512 retina touch squares & 240×360 dial OLED strips).
  - Injects the profile directly into Loupedeck's active profile storage.
  - Auto-copies `Rupokar_Resolve_Keys.txt` directly into DaVinci Resolve's keyboard shortcut presets folder!
  - Restarts Loupedeck ready to edit in under 5 seconds.
- 🔘 **Workspace 8 Dedicated Touch Suite**: Quick Export, 7 UI Panel Toggles, and Bypass All Grades rendered as native 256×256 touch buttons with zero letterboxing or squashing.
- 🔄 **Jog/Shuttle Center Wheel**: Ultra-smooth frame-by-frame timeline scrubbing with center playhead Play/Pause toggle.

---

## 🚀 Quick Start / Auto-Installation

### 🍎 On macOS (Apple Silicon & Intel)
Double-click **`install.command`** in Finder (or run in Terminal):
```bash
bash install.sh
```
*That's it! Loupedeck and DaVinci Resolve are configured automatically.*

---

### 🪟 On Windows 10 & 11
Double-click **`install.bat`** in File Explorer!
- If Python is installed, it runs the full auto-injector and installs the profile & shortcuts.
- If Python is not installed, it automatically copies the keyboard preset to `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Keyboard Shortcuts\` and opens `Rupokar-Resolve-CT.lp5` directly in Loupedeck!

---

### 🐍 Universal Python Installer (Cross-Platform)
From terminal or command prompt:
```bash
python3 install.py      # macOS / Linux
python install.py       # Windows
```

---

## 📦 What's in the Box?

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| **1-Click macOS Installer** | [`install.command`](install.command) / [`install.sh`](install.sh) | Automated script configuring Loupedeck CT & DaVinci Resolve on macOS. |
| **1-Click Windows Installer** | [`install.bat`](install.bat) | Native Windows batch installer with auto keyboard preset placement. |
| **Universal Python Installer** | [`install.py`](install.py) | Cross-platform Python runner supporting both OS environments. |
| **Loupedeck CT Profile Package** | [`profile/Rupokar-Resolve-CT.lp5`](profile/Rupokar-Resolve-CT.lp5) | Double-clickable importable Loupedeck `.lp5` package (168 actions, 8 workspaces). |
| **Keyboard Preset** | [`keyboard-preset/Rupokar_Resolve_Keys.txt`](keyboard-preset/Rupokar_Resolve_Keys.txt) | Conflict-free keyboard shortcuts file auto-installed into DaVinci Resolve. |
| **High-DPI Vector Icons** | [`icons/final-svg/`](icons/final-svg/) & [`icons/export-png/`](icons/export-png/) | 168 SVGs and 336 high-DPI PNGs across Touch (256×256), Dial (120×180), and Physical (320×160). |
| **Automated Test Suite** | [`tests/`](tests/) | 28 automated pytest unit and integration tests verifying integrity. |
| **Interactive Review Board** | [`icons/Final-Icon-Board.html`](icons/Final-Icon-Board.html) | Filterable web review gallery comparing final icons with reference crops. |

---

## 🕹️ Hardware Layout & 8 Workspaces

Loupedeck CT's 8 round buttons provide instant 1-touch navigation between all 8 DaVinci Resolve pages and custom workspaces:

```
+-----------------------------------------------------------------------------------+
|                                   LOUPEDECK CT                                    |
|                                                                                   |
|   [1] Media    [2] Edit 1   [3] Edit 2   [4] Edit 3   [5] Color   [6] Fairlight   [7] Deliver   [8] QuickExp
|   (Shift+2)    (Shift+4)    (Shift+4)    (Shift+4)    (Shift+6)   (Shift+7)       (Shift+8)     (Shift+9)  |
|                                                                                   |
|   [Dial 1]     +-----------------------------------------------+     [Dial 4]     |
|   [Dial 2]     |                12 TOUCH TILES                 |     [Dial 5]     |
|   [Dial 3]     |             (3 rows x 4 columns)              |     [Dial 6]     |
|                +-----------------------------------------------+                  |
|                                                                                   |
|   [Undo] [Save]                ( CENTER WHEEL )                [A] [B] [C] [D]    |
|                                   Jog/Shuttle                     [E]   [Fn]      |
+-----------------------------------------------------------------------------------+
```

### Workspace Matrix

| # | Workspace Name | Navigation Button | Touch Screen Controls (12 Tiles) | Dials (6 Knobs: Turn & Press) |
| :-: | :--- | :-: | :--- | :--- |
| **1** | **Media & Project** | **Round 1** | Import Media, New Bin, Project Notes, Project Manager, Prefer Proxy, Camera Originals, Project Settings, New Project, Power Bins, 9:16, 4:5, 4:3 *(+ 12 Break Timer Tiles on Swipe)* | Shuttle, Zoom, Fast Shuttle, Clip Navigation |
| **2** | **Edit 1 — Timeline & Cuts** | **Round 2** | Select Backward All, Select Forward All, Snapping, Delete, Trim Start, Trim End, Retime Controls, Change Clip Speed, Ripple Start, Razor Split, Ripple End, Play/Pause | **Dial 1:** Shuttle / Orange Color<br>**Dial 2:** Audio ±1dB / Yellow Color<br>**Dial 3:** Dynamic Trim / Toggle<br>**Dial 4:** Fast Shuttle / Green Color<br>**Dial 5:** Timeline Zoom / Zoom Fit<br>**Dial 6:** Next Clip / Add Marker |
| **3** | **Edit 2 — Sync & Colors** | **Round 3** | Delete All Markers, Linked Selection, Link Clips, Compound Clip, Normalize Audio, Auto Align Audio, Mark In, Mark Out, Match Frame, Cinema Viewer, Loop, Play/Pause | **Bank 1:** Apricot, Blue, Lime, Brown, Pink, Purple<br>**Bank 2:** Olive, Teal, Navy, Violet, Tan, Beige |
| **4** | **Edit 3 — Fine Tuning** | **Round 4** | Enable/Disable Clip, Freeze Frame, Title Safe, Delete Gaps, Find in Pool, Crossfade, Swap Left, Swap Right, Find Timeline, New Timeline, Duplicate Timeline, Play/Pause | Track Heights, Fine Nudge, Timeline Navigation |
| **5** | **Color — Nodes & Wheels** | **Round 5** | Scopes, Light Box, Cinema Viewer, Printer Lights, Add Serial Node, Node Before, Label Node, Grab Still, Split Selected, Split Prev/Next, Split Original, Split Stills | **Dial 1:** Saturation / Reset<br>**Dial 2:** Gamma / Reset<br>**Dial 3:** Gain / Reset<br>**Dial 4:** Printer Red / Exit Split<br>**Dial 5:** Printer Green<br>**Dial 6:** Printer Blue |
| **6** | **Fairlight — Audio & Fades** | **Round 6** | Batch Fade Settings, Apply Batch Fades, Loop, Mark In, Mark Out, Play/Pause, Track Height, Waveform Zoom, Reset Zoom, Audio Level, Normalize, Mixer Panel | Shuttle, Fast Shuttle, Track Height, Waveform Zoom, Zoom to Fit, Next Clip |
| **7** | **Deliver & Render Queue** | **Round 7** | YouTube, Vimeo, TikTok, Instagram 4:5, ProRes 422 HQ, Custom #1, Custom #2, Custom #3, Add to Queue, Render All, Render New, Stop Render *(+ Thumbnail, Export Folder on Swipe)* | Mark In for Export, Mark Out for Export, Queue Controls |
| **8** | **Quick Export & Panels** | **Round 8** | Quick Export, Export Folder, Save Thumbnail, Free Deliver Controls, Media Pool, Effects Library, Inspector, Mixer, Power Bins, Metadata, Edit Index, Bypass All Grades | Shuttle, Zoom, Audio Level, Timeline Navigation |

---

## 🎨 Multi-Ratio Vector Icon Suite

Every icon is built as a mathematical vector SVG tailored specifically to the hardware OLED screen geometry:

```
+---------------------------+   +-------------------+   +------------------------------------+
|        TOUCH TILE         |   |    DIAL STRIP     |   |          PHYSICAL LEGEND           |
|          256x256          |   |      120x180      |   |              320x160               |
|                           |   |                   |   |                                    |
|   +===================+   |   |    [Accent Bar]   |   |   +------------+                   |
|   |    Accent Bar     |   |   |     (Icon 38px)   |   |   |   Glyph    |   Action Name     |
|   +===================+   |   |   -------------   |   |   |   Badge    |   (Bold White)    |
|                           |   |    PARAMETER      |   |   +------------+                   |
|       WIDE GLYPH          |   |      NAME         |   |                                    |
|      (190–210px)          |   |  (Bold 21px W900) |   |   KEY: ROUND / SQUARE / FN         |
|                           |   |   +-----------+   |   +------------------------------------+
|     Action Title          |   |   |  TURN ↻   |   |
|   (Bold 27px W900)        |   |   +-----------+   |
+---------------------------+   +-------------------+
```

### Key Visual Innovations
1. **Edge-to-Edge Fill**: Touch glyphs span `x=24` to `x=188` (over 200px wide on canvas), eliminating dead margins.
2. **Text-Primary Dials**: The parameter name is placed front-and-center in crisp white, high-contrast typography so editors don't have to squint.
3. **Zero Stroke Collisions**: Minimum 30px distance between adjacent geometry lines ensures sharp rendering even on small OLEDs.
4. **Dual-Tone Depth**: Subtle translucent fills (`opacity="0.18"`) paired with 14px bold outline strokes.

---

## ⌨️ Keyboard Shortcuts Auto-Setup

Our installers **automatically copy** `Rupokar_Resolve_Keys.txt` to the appropriate system directory:

| Operating System | Auto-Install Target Directory |
| :--- | :--- |
| **macOS** | `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Keyboard Shortcuts/` |
| **Windows** | `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Keyboard Shortcuts\` |

### To verify or activate manually in DaVinci Resolve:
1. Open **DaVinci Resolve**.
2. Press `Option+Command+K` (macOS) or `Ctrl+Alt+K` (Windows) to open **Keyboard Customization**.
3. In the top-right preset dropdown, select **`Rupokar Loupedeck CT`** (or click `...` -> **Import Preset** and choose `keyboard-preset/Rupokar_Resolve_Keys.txt`).
4. Click **Save** and close.

---

## 💻 Cross-Platform Support: macOS & Windows

This package is engineered from the ground up for 100% feature parity on macOS and Windows:

| Feature | macOS Support | Windows Support |
| :--- | :---: | :---: |
| **Loupedeck CT Profile (`.lp5`)** | ✅ Fully Supported | ✅ Fully Supported |
| **Loupedeck 2.0 / Logi Plugin Service Profile** | ✅ Auto-Injected | ✅ Auto-Injected |
| **All 8 Workspaces & 168 Actions** | ✅ Identical Layout | ✅ Identical Layout |
| **Jog / Shuttle Wheel Scrubbing** | ✅ Native | ✅ Native |
| **Keyboard Shortcut Preset** | ✅ Auto-Installed | ✅ Auto-Installed |
| **1-Click Installer** | `install.command` / `install.sh` | `install.bat` |
| **Automated Test Suite** | 28 / 28 Passed | 28 / 28 Passed |

---

## 🧪 Verification & Automated Testing

The entire repository is backed by automated tests:

```bash
# Run pytest verification suite
PYTHONPATH=. pytest tests/ -v
```

```
tests/test_ct_profile_installer.py::test_profile_basic_metadata PASSED
tests/test_ct_profile_installer.py::test_eight_workspaces_exist PASSED
tests/test_ct_profile_installer.py::test_zero_empty_touch_buttons PASSED
tests/test_ct_profile_installer.py::test_all_dials_active PASSED
tests/test_ct_profile_installer.py::test_round_navigation_macros PASSED
tests/test_ct_profile_installer.py::test_wheel_page_configured PASSED
tests/test_icon_system.py::test_manifest_and_icon_counts PASSED
tests/test_icon_system.py::test_zero_spark_fallbacks PASSED
tests/test_icon_system.py::test_svg_dimensions_and_xml_validity PASSED
tests/test_keyboard_preset.py::test_keyboard_preset_exists PASSED
tests/test_keyboard_preset.py::test_keyboard_preset_no_duplicate_shortcuts PASSED
tests/test_keyboard_preset.py::test_keyboard_preset_structure PASSED
tests/test_keyboard_preset.py::test_docs_keyboard_preset_map_exists PASSED
tests/test_plugin_structure.py::test_plugin_files_exist PASSED
tests/test_profile_lp5.py::test_profile_lp5_is_valid_zip PASSED
tests/test_profile_lp5.py::test_profile_lp5_action_icons PASSED
tests/test_profile_lp5.py::test_profile_lp5_workspaces_and_actions PASSED
tests/test_raster_export.py::test_png_files_exist PASSED
...
======================== 28 passed, 0 failed ========================
```

---

## 📄 License & Credits

- **Author**: Rupokar Studios / Zabid
- **Hardware**: Designed exclusively for **Loupedeck CT** by Logitech / Loupedeck
- **Target Software**: **Blackmagic DaVinci Resolve Studio & Free** (v18 & v19+)
- **License**: [MIT License](LICENSE) — free for personal and commercial editing workflows.
