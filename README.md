# Rupokar Studios LoupeDeck CT Pack for DaVinci Resolve

[![DaVinci Resolve](https://img.shields.io/badge/DaVinci%20Resolve-21.1.2%20Studio%20%2F%20Free-black?logo=davinciresolve)](https://www.blackmagicdesign.com/products/davinciresolve)
[![Loupedeck Hardware](https://img.shields.io/badge/Loupedeck-CT%20(Loupedeck50)-5B4EE4?logo=logitech)](https://loupedeck.com/en/products/loupedeck-ct)
[![Platform](https://img.shields.io/badge/Platform-macOS%20(Apple%20Silicon%20%26%20Intel)-grey?logo=apple)](https://apple.com)
[![Actions](https://img.shields.io/badge/Audited%20Actions-168%20Total-success)](#hardware-layout--8-workspaces)
[![Tests](https://img.shields.io/badge/Tests-22%20Passed-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![.NET](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet)](https://dotnet.microsoft.com/)

A complete, precision-engineered control suite for **Loupedeck CT (`Loupedeck50`)** tailored for **DaVinci Resolve 21.1.2** on macOS. 

This pack delivers an audited **168-action system** across 8 dedicated workspaces, featuring a multi-ratio vector icon suite, an importable native Loupedeck profile (`.lp5`), a conflict-free DaVinci Resolve keyboard shortcut preset, a local Python automation bridge daemon connecting to Resolve's Scripting API, a .NET 8 Logi Actions C# plugin with real-time countdown timer rendering, and an interactive side-by-side visual audit board.

---

## Table of Contents

- [Core Deliverables & Highlights](#core-deliverables--highlights)
- [Hardware Layout & 8 Workspaces](#hardware-layout--8-workspaces)
- [Multi-Ratio Vector Icon Suite](#multi-ratio-vector-icon-suite)
- [Installation & Setup Guide](#installation--setup-guide)
  - [1. Import Loupedeck Profile](#1-import-loupedeck-profile-lp5)
  - [2. Import DaVinci Resolve Keyboard Shortcut Preset](#2-import-davinci-resolve-keyboard-shortcut-preset)
  - [3. Configure DaVinci Resolve Studio External Scripting](#3-configure-davinci-resolve-studio-external-scripting)
  - [4. Launch the Local Automation Bridge](#4-launch-the-local-automation-bridge)
  - [5. (Optional) Compile .NET 8 Logi Actions Plugin](#5-optional-compile-net-8-logi-actions-plugin)
- [Interactive Visual Audit Board](#interactive-visual-audit-board)
- [Repository Structure](#repository-structure)
- [Bridge IPC Socket Protocol](#bridge-ipc-socket-protocol)
- [Testing & Quality Verification](#testing--quality-verification)
- [License & Credits](#license--credits)

---

## Core Deliverables & Highlights

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| **Loupedeck CT Profile** | [`profile/Rupokar-Resolve-CT.lp5`](profile/Rupokar-Resolve-CT.lp5) | Native `.lp5` zip bundle for Loupedeck 6.4+, containing all 8 workspaces, 168 mapped controls, and 168 embedded action icons. |
| **Keyboard Preset** | [`keyboard-preset/Rupokar_Resolve_Keys.txt`](keyboard-preset/Rupokar_Resolve_Keys.txt) | Conflict-free shortcut mapping file ready for import into DaVinci Resolve Keyboard Customization. |
| **Multi-Ratio Icon Suite** | [`icons/final-svg/`](icons/final-svg/) & [`icons/export-png/`](icons/export-png/) | 168 custom vector icons across Touch (256×256), Dial (120×180 vertical strips), and Physical Key legends (320×160). |
| **Python Automation Bridge** | [`bridge/rupokar_resolve_bridge/`](bridge/rupokar_resolve_bridge/) | Unix domain socket (`~/.rupokar/bridge.sock`) daemon talking directly to Resolve Studio 21.1.2 Scripting API. |
| **Logi Actions C# Plugin** | [`plugin/Rupokar.Resolve.Actions/`](plugin/Rupokar.Resolve.Actions/) | C# / .NET 8 plugin implementing real-time countdown timer tiles with macOS notifications. |
| **Interactive Audit Board** | [`icons/Final-Icon-Board.html`](icons/Final-Icon-Board.html) | Searchable and filterable HTML inspection gallery with side-by-side walkthrough crop comparisons. |
| **Documentation & Guides** | [`docs/`](docs/) | Complete architecture specs, setup instructions, shortcut tables, and validation checklist. |

---

## Hardware Layout & 8 Workspaces

Loupedeck CT's 8 round navigation buttons seamlessly switch between 8 custom workspaces:

```
+-------------------------------------------------------------------------+
|                              LOUPEDECK CT                               |
|                                                                         |
|  [Round 1] [Round 2] [Round 3] [Round 4] [Round 5] [Round 6] [Round 7] [Round 8]
|   Media      Edit 1    Edit 2    Edit 3    Color    Fairlight  Deliver   QuickExp
|                                                                         |
|  [Dial 1]     +-----------------------------------------+     [Dial 4]  |
|  [Dial 2]     |            12 TOUCH TILES               |     [Dial 5]  |
|  [Dial 3]     |         (3 rows x 4 columns)            |     [Dial 6]  |
|               +-----------------------------------------+               |
|                                                                         |
|  [Undo] [Save]            ( CENTER WHEEL )            [A] [B] [C] [D]   |
|                              (Display)                  [E]   [Fn]      |
+-------------------------------------------------------------------------+
```

### 1. Workspace 1 — Media & Project Manager (`Round 1`)
- **Touch Tiles (1-12):** Import Media, New Bin, Project Notes, Project Manager, Prefer Proxy, Camera Originals, Project Settings, New Project, Power Bins, Timeline 9:16, Timeline 4:5, Timeline 4:3.
- **Alternate Free Edition:** Duplicate Timeline, New Timeline.
- **Sub-page (Swipe Right):** Break Timer suite with 8 interval choices (25m, 45m, 1h, 1.5h, 2h, 2.5h, 3h, 4h), Rushwise project manager launcher, Break! status tile, Start timer, and Stop timer.

### 2. Workspace 2 — Edit 1: Timeline & Cuts (`Round 2`)
- **Touch Tiles (1-12):** Select Backward All, Select Forward All, Magnetic Snapping, Delete (with gap), Trim Start, Trim End, Retime Controls, Change Clip Speed, Ripple Start, Razor Split, Ripple End, Play/Pause.
- **Left Dials:** Dial 1 Turn (Shuttle) / Press (Orange clip color); Dial 2 Turn (Audio Level ±1dB) / Press (Yellow clip color); Dial 3 Turn (Dynamic Trim frame-by-frame) / Press (Dynamic Trim on/off).
- **Right Dials:** Dial 4 Turn (Fast Shuttle 1s/click) / Press (Green clip color); Dial 5 Turn (Timeline Zoom) / Press (Zoom to Fit); Dial 6 Turn (Next Clip) / Press (Add Marker).
- **Center Wheel:** Turn (Frame-by-frame playhead scrub) / Press (Play/Pause).

### 3. Workspace 3 — Edit 2: Sync & Colors (`Round 3`)
- **Touch Tiles (1-12):** Delete All Markers, Linked Selection toggle, Link Clips, Compound Clip, Normalize Audio, Auto Align by waveform, Mark In, Mark Out, Match Frame, Cinema Viewer full screen, Loop playback, Play/Pause.
- **Dial Banks (15 Clip Colors):** Bank 1 (Apricot, Blue, Lime, Brown, Pink, Purple); Bank 2 (Olive, Teal, Navy, Violet, Tan, Beige).

### 4. Workspace 4 — Edit 3: Fine Tuning (`Round 4`)
- **Touch Tiles (1-12):** Enable/Disable Clip, Freeze Frame, Title Safe guides, Delete Gaps (close all timeline voids), Find Clip in Media Pool, Crossfade transition, Swap Left, Swap Right, Find Timeline, New Timeline, Duplicate Timeline, Play/Pause.

### 5. Workspace 5 — Color Page: Nodes & Grading (`Round 5`)
- **Touch Tiles (1-12):** Scopes monitor, Light Box multi-clip gallery, Cinema Viewer, Printer Lights toggle, Add Serial Node, Node Before, Label Node, Grab Still to gallery, Split Selected clips, Split Prev/Next, Split Original (grade vs raw), Split Stills.
- **Left Dials (Node Adjustments):** Dial 1 Turn (Saturation) / Press (Reset Saturation); Dial 2 Turn (Gamma midtones) / Press (Reset Gamma); Dial 3 Turn (Gain highlights) / Press (Reset Gain).
- **Right Dials (Printer Lights):** Dial 4 (Printer Light Red); Dial 5 (Printer Light Green); Dial 6 (Printer Light Blue); Dial 4 Press (Exit split comparison).

### 6. Workspace 6 — Fairlight Page: Audio & Fades (`Round 6`)
- **Touch Tiles:** Batch Fade Settings dialog, Apply Batch Fades, Loop playback, Mark In, Mark Out, Play/Pause.
- **Dials:** Dial 1 Turn (Shuttle); Dial 2 Turn (Track Height expansion); Dial 3 Turn (Waveform Zoom) / Press (Reset Waveform Zoom); Dial 4 Turn (Fast Shuttle); Dial 5 Turn (Timeline Zoom); Dial 6 Turn (Next Clip).

### 7. Workspace 7 — Deliver & Render Queue (`Round 7`)
- **Presets Touch Tiles:** YouTube, Vimeo, TikTok, Instagram 4:5, ProRes 422 HQ, Custom Preset #1, Custom Preset #2, Custom Preset #3.
- **Render Queue Actions:** Add to Queue, Render All, Render New, Stop Render.
- **Extras (Swipe Right):** Save Thumbnail, Open Export Folder, Clear Render Queue.
- **Dials:** Dial 1 Press (Mark In for export); Dial 4 Press (Mark Out for export).

### 8. Workspace 8 — Quick Export (`Round 8`)
- **Round Button 8:** Instant trigger for DaVinci Resolve Quick Export overlay.

### Physical Keys & Fn Modifier Layer
- **Dedicated Keys:** `Undo`, `Save Project`.
- **Square Keys:** `Square A` (Move clip up track), `Square B` (Move clip down track), `Square C` (Jump to timeline start), `Square D` (Jump to timeline end), `Square E` (Right-click at mouse location).
- **Fn Combinations:**
  - `Fn + B`: Ripple Delete (delete clip and close gap)
  - `Fn + C`: Copy selected clip
  - `Fn + A`: Paste Attributes dialog
  - `Fn + D`: Bypass All Grades (grade comparison)
  - `Fn + Round 1-7`: Toggle UI Panels (Media Pool, Effects Library, Inspector, Fairlight Mixer, Power Bins, Metadata, Edit Index).

---

## Multi-Ratio Vector Icon Suite

Every icon is built from pure SVG vectors without pixel stretching or generic fallbacks:

```
+--------------------+   +--------------+   +-------------------------------+
|     TOUCH TILE     |   |  DIAL STRIP  |   |        PHYSICAL LEGEND        |
|      256x256       |   |   120x180    |   |            320x160            |
|                    |   |              |   |                               |
|   [ Accent Bar ]   |   | [Accent Bar] |   | +----------+                  |
|                    |   |              |   | |  Glyph   |  Function Label  |
|      (Glyph)       |   |   (Glyph)    |   | |  Badge   |                  |
|                    |   |              |   | +----------+  KEY / CONTROL   |
|   --------------   |   | Function Lbl |   +-------------------------------+
|    Function Lbl    |   | [TURN/PRESS] |
+--------------------+   +--------------+
```

### Icon Design Highlights
- **Serial Nodes:** Detailed Resolve serial node geometry with input/output connection pins and active `+` badges.
- **Razor Tool:** Slicing blade dividing playhead video clips instead of generic scissors.
- **Videoscopes:** Curved studio monitor with circular vectorscope graticule and crosshair grid.
- **Light Box:** 3×2 filmstrip clip matrix matching Resolve's Light Box view.
- **Printer Lights:** Lab timing optical lamps with `[-]`/`[+]` step trim controls.
- **Color Curves:** Logarithmic S-curves (Gamma midtones) and dynamic highlight slopes (Gain).
- **Power Bins:** Media folder bearing an unmistakable lightning bolt (`⚡`) emblem.
- **Aspect Ratio Timelines:** Clean smartphone/portrait cards with bold `9:16`, `4:5`, `4:3` typography.
- **Timer Badges:** Stopwatch bezels with high-contrast duration badges (`25m` to `4h`).

---

## Installation & Setup Guide

### 1. Import Loupedeck Profile (`.lp5`)
1. Open the **Loupedeck** software (v6.4 or later).
2. Ensure your **Loupedeck CT** is connected via USB-C.
3. Click the profile dropdown menu in the upper header -> select **Import Profile...**
4. Browse to and select [`profile/Rupokar-Resolve-CT.lp5`](profile/Rupokar-Resolve-CT.lp5).
5. The **Rupokar DaVinci Resolve CT** profile will load automatically, configuring all 8 workspaces and embedding all 168 raster action icons.

### 2. Import DaVinci Resolve Keyboard Shortcut Preset
1. Launch **DaVinci Resolve**.
2. Go to **DaVinci Resolve** menu -> **Keyboard Customization...** (`Option+Command+K` on macOS, `Ctrl+Alt+K` on Windows).
3. In the top-right corner, click the three-dot menu `...` -> select **Import Preset**.
4. Select [`keyboard-preset/Rupokar_Resolve_Keys.txt`](keyboard-preset/Rupokar_Resolve_Keys.txt).
5. Name the preset `Rupokar Loupedeck CT` and click **Save**.
6. Confirm that `Rupokar Loupedeck CT` is the active preset in the dropdown.

### 3. Configure DaVinci Resolve Studio External Scripting
For the Python automation bridge to communicate with Resolve:
1. In DaVinci Resolve Studio, open **Preferences** (`Command+,`).
2. Navigate to **System** -> **General**.
3. Under **External scripting using**, select **Local**.
4. Click **Save** and restart DaVinci Resolve.

### 4. Launch the Local Automation Bridge
The bridge daemon manages background automation (timeline duplication, render queue control, non-blocking timers with macOS notifications):

```bash
# Make sure the script is executable
chmod +x scripts/run_bridge.sh

# Run the bridge daemon in foreground or as a background service
./scripts/run_bridge.sh
```

The bridge creates a secure Unix socket at `~/.rupokar/bridge.sock` with user-only permissions (`0o600`).

### 5. (Optional) Compile .NET 8 Logi Actions Plugin
If using the Loupedeck Developer Plugin ecosystem:

```bash
cd plugin/Rupokar.Resolve.Actions
dotnet restore
dotnet build -c Release
```

Copy the compiled output into `~/Library/Application Support/Logi/LogiPluginService/Plugins/` and restart Loupedeck.

---

## Interactive Visual Audit Board

An interactive HTML review board is included for side-by-side inspection of all 168 final vector icons against the original walkthrough video crops:

Open [`icons/Final-Icon-Board.html`](icons/Final-Icon-Board.html) in your browser:

```bash
open icons/Final-Icon-Board.html
```

**Features:**
- **Real-time Search:** Filter instantly by action name, control type, or keyword.
- **Workspace Category Pills:** Filter by Media, Edit, Color, Fairlight, Deliver, or Physical.
- **Crop Comparison:** Expand `<details> 🔍 Compare Walkthrough Crop</details>` on any card to compare against original walkthrough video frames.

---

## Repository Structure

```
.
├── Inspired File/                   # Master reference, transcripts & source catalog
│   ├── Function-and-Options-Catalog.md
│   ├── Rupokar-Resolve-CT-Architecture-Plan.md
│   ├── build_master_reference.py
│   └── full-audio-transcript.txt
├── bridge/                          # Local Python automation bridge
│   └── rupokar_resolve_bridge/
│       ├── bridge_service.py        # Background service & timer scheduler
│       ├── command_router.py        # IPC message handler
│       ├── resolve_client.py        # DaVinci Resolve 21.1.2 Scripting API client
│       └── socket_server.py         # Unix domain socket IPC server
├── docs/                            # Specifications, guides & checklists
│   ├── install-guide.md             # Complete installation instructions
│   ├── keyboard-preset-map.md       # Comprehensive shortcut map table
│   ├── validation-checklist.md      # Hardware and software sign-off checklist
│   └── superpowers/                 # Architecture design specs & implementation plans
├── icons/                           # 168-asset multi-ratio icon suite
│   ├── Final-Icon-Board.html        # Interactive filterable audit board
│   ├── export-png/                  # High-resolution raster icons (touch, dial, physical)
│   ├── final-icon-manifest.json     # Machine-readable metadata catalog
│   ├── final-svg/                   # Source SVG vector files
│   └── reference-png/               # Audited walkthrough video reference crops
├── keyboard-preset/                 # DaVinci Resolve shortcut preset
│   └── Rupokar_Resolve_Keys.txt
├── plugin/                          # Logi Actions C# / .NET 8 plugin
│   └── Rupokar.Resolve.Actions/
│       ├── Actions/                 # BreakTimerAction & RenderQueueAction
│       ├── DynamicDisplay/          # Real-time countdown timer tile renderer
│       ├── IPC/                     # Unix socket IPC client with exception guards
│       ├── Rupokar.Resolve.Actions.csproj
│       └── RupokarResolvePlugin.cs
├── profile/                         # Loupedeck CT profile archive
│   └── Rupokar-Resolve-CT.lp5       # 8-workspace Loupedeck50 package
├── scripts/                         # Build, export, verification & bridge scripts
│   ├── build_icons.py               # Generates 168 SVGs and audit board
│   ├── build_profile.py             # Assembles Loupedeck CT .lp5 package
│   ├── export_raster_icons.py       # High-speed rasterizer (PyQt6 / cairosvg)
│   ├── run_bridge.sh                # Automation bridge launcher
│   └── verify_pack.py               # End-to-end integrity verifier
└── tests/                           # Complete automated test suite
    ├── test_icon_system.py          # SVG dimensions, XML validity, zero spark assertions
    ├── test_keyboard_preset.py      # No duplicate shortcuts check
    ├── test_plugin_structure.py     # C# plugin contracts, intervals, csproj validation
    ├── test_profile_lp5.py          # LP5 zip integrity, 8 workspaces, 168 action icons
    ├── test_raster_export.py        # PNG file existence & dimensions
    └── test_resolve_bridge.py       # IPC socket roundtrips & Resolve client fallbacks
```

---

## Bridge IPC Socket Protocol

The bridge communicates over a Unix domain socket at `~/.rupokar/bridge.sock` using newline-delimited JSON.

### Example Request:
```json
{
  "id": "timeline.copy.aspect",
  "requestId": "req-001",
  "payload": {
    "ratio": "9:16"
  }
}
```

### Example Response:
```json
{
  "requestId": "req-001",
  "ok": true,
  "message": "Created timeline: Timeline 1 (9:16)"
}
```

### Supported Commands:
- `resolve.ping`: Check DaVinci Resolve connection status and active project.
- `timeline.copy.aspect`: Duplicate active timeline into `9:16`, `4:5`, or `4:3` formats.
- `render.start.all`: Start rendering all jobs in the Resolve Render Queue.
- `render.stop`: Abort active rendering.
- `render.queue.status`: Query queued jobs and rendering status.
- `timer.set`: Set non-blocking break interval (e.g. 25m, 45m, 1h, 2h).
- `timer.status`: Query remaining break timer seconds.

---

## Testing & Quality Verification

Run the full pytest suite:

```bash
python3 -m pytest tests/ -v
```

Run the end-to-end pack verifier:

```bash
python3 scripts/verify_pack.py
```

All 22 automated tests verify:
- ✅ Zero generic `spark` icon fallbacks.
- ✅ Exact dimensions: Touch 256×256, Dial 120×180, Physical 320×160.
- ✅ Valid XML parsing for all 168 SVG files (no duplicate XML attributes).
- ✅ Conflict-free keyboard shortcut preset with zero duplicate keybindings.
- ✅ Profile `.lp5` zip contains valid `ProfileInfo.json`, 8 workspaces, and 168 embedded action icons.
- ✅ Bridge socket server roundtrip, graceful offline fallback, and command routing.
- ✅ C# plugin .NET 8 target, timer intervals, and exception-shielded socket client.

---

## License & Credits

- **Author:** Zabid / Rupokar Studios
- **Compatibility:** DaVinci Resolve 21.1.2 (Studio & Free) / Loupedeck Software 6.4+
- **Hardware:** Loupedeck CT (`Loupedeck50`)
- **License:** MIT License
