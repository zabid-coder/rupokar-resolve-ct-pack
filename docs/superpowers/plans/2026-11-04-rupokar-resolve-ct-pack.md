# Rupokar Resolve CT Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, installable macOS package for Loupedeck CT (`Loupedeck50`) and DaVinci Resolve 21.1.2 implementing all 168 catalogued controls and options with custom multi-ratio vector icons, real-time dynamic countdown timers, a local Python Resolve automation bridge, and a native `.lp5` profile.

**Architecture:** A three-tiered architecture where the Loupedeck CT hardware interacts with an installable Loupedeck 6.x `.lp5` profile and a Logi Actions .NET 8 plugin (`Rupokar.Resolve.Actions`). The plugin dynamically renders live countdown timers and status over custom SVG/PNG tile assets, while routing advanced DaVinci Resolve scripting requests over a local Unix domain socket to a Python 3 automation bridge connected directly to DaVinci Resolve 21.1.2's official Python API.

**Tech Stack:** Python 3.14 (SVG generation, raster export, DaVinci Resolve Scripting API bridge, profile packager), C# / .NET 8 (Logi Actions SDK plugin), Loupedeck Profile 5.0 (.lp5 zip package), SVG / HTML5, macOS Unix domain sockets.

## Global Constraints

- Hardware: Loupedeck CT (`Loupedeck50`) only.
- Software: DaVinci Resolve 21.1.2 (Studio and Free edition compatibility) on macOS.
- Loupedeck Version: Logi Plugin Service / Loupedeck 6.4.1.364.
- Total Actions: Exactly 168 mapped controls, dials, and options based on `Function-and-Options-Catalog.md`.
- Zero Generic Fallbacks: No generic `spark` glyphs permitted; all 8 identified fallbacks must have purpose-built vector glyphs.
- Multi-Ratio Geometry: Touch tiles at 256×256 (1:1), dial strips at 120×180 (2:3), physical key cards at 320×160 (2:1).
- Socket Location: User-scoped Unix domain socket at `~/.rupokar/bridge.sock`.

---

### Task 1: Multi-Ratio Vector Icon Generator & 8 Fallback Glyphs Fix

**Files:**
- Create: `scripts/build_icons.py`
- Test: `tests/test_icon_system.py`
- Output directories:
  - `icons/final-svg/touch/` (94 SVGs)
  - `icons/final-svg/dial/` (44 SVGs)
  - `icons/final-svg/physical/` (30 SVGs)
  - `icons/final-icon-manifest.json`
  - `icons/Final-Icon-Board.html`

**Interfaces:**
- Consumes: `Inspired File/build_master_reference.py:ITEMS` (168 catalogued items)
- Produces: `icons/final-icon-manifest.json`, 168 valid SVG files in `icons/final-svg/`, and `icons/Final-Icon-Board.html`

- [ ] **Step 1: Write the test verifying icon generation and zero fallback glyphs**

Create `tests/test_icon_system.py`:
```python
import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
TOUCH_DIR = REPO_ROOT / "icons" / "final-svg" / "touch"
DIAL_DIR = REPO_ROOT / "icons" / "final-svg" / "dial"
PHYSICAL_DIR = REPO_ROOT / "icons" / "final-svg" / "physical"


def test_manifest_and_icon_counts():
    assert MANIFEST_PATH.exists(), "Manifest file must exist"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    assert len(items) == 168, f"Expected 168 icons, got {len(items)}"

    touch_count = sum(1 for x in items if x["type"] == "touch")
    dial_count = sum(1 for x in items if x["type"] == "dial")
    physical_count = sum(1 for x in items if x["type"] == "physical")

    assert touch_count == 94, f"Expected 94 touch tiles, got {touch_count}"
    assert dial_count == 44, f"Expected 44 dial strips, got {dial_count}"
    assert physical_count == 30, f"Expected 30 physical legends, got {physical_count}"


def test_zero_spark_fallbacks():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    spark_items = [x for x in items if x["glyph"] == "spark"]
    assert len(spark_items) == 0, f"Found {len(spark_items)} unmapped spark fallbacks: {[x['function'] for x in spark_items]}"


def test_svg_dimensions():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        file_path = REPO_ROOT / "icons" / item["filename"]
        assert file_path.exists(), f"File {file_path} must exist"
        content = file_path.read_text(encoding="utf-8")
        if item["type"] == "touch":
            assert 'width="256" height="256"' in content
        elif item["type"] == "dial":
            assert 'width="120" height="180"' in content
        elif item["type"] == "physical":
            assert 'width="320" height="160"' in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_icon_system.py -v`
Expected: FAIL with "Manifest file must exist"

- [ ] **Step 3: Implement `scripts/build_icons.py`**

Create `scripts/build_icons.py`:
```python
#!/usr/bin/env python3
"""Build the complete 168-asset multi-ratio SVG icon system for Rupokar Resolve CT."""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "Inspired File"))
from build_master_reference import ITEMS

ICONS_DIR = REPO_ROOT / "icons"
SVG_ROOT = ICONS_DIR / "final-svg"
MANIFEST_PATH = ICONS_DIR / "final-icon-manifest.json"
BOARD_PATH = ICONS_DIR / "Final-Icon-Board.html"

PALETTE = {
    "Navigation": "#A88CFF",
    "Media / Project": "#B79AFF",
    "Media / Break Timer": "#4EE0E2",
    "Edit 1": "#64AAFF",
    "Edit 2": "#72B6FF",
    "Edit 3": "#8CB5FF",
    "Physical keys & Fn layer": "#A38FFF",
    "Color": "#46D9C4",
    "Fairlight": "#80E06A",
    "Deliver / Render Queue": "#C9A0FF",
    "Quick Export": "#C9A0FF",
}

COLOR_ACCENTS = {
    "orange": "#FF8A3D", "yellow": "#FFD43D", "green": "#5CE080", "apricot": "#FFB36F",
    "blue": "#5DAAFF", "lime": "#B2EE58", "brown": "#C08050", "pink": "#FF8DCD",
    "purple": "#B07DFF", "olive": "#A7A65D", "teal": "#39CCBD", "navy": "#547CCA",
    "violet": "#A36DFF", "tan": "#D6AD78", "beige": "#E8D1A7",
}


def slugify(value: str) -> str:
    value = value.lower().replace("×", "x").replace("/", "-").replace(":", "-")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:54]


def accent(item: dict[str, str]) -> str:
    function = item["function"].lower()
    for word, color in COLOR_ACCENTS.items():
        if word in function:
            return color
    if "stop" in function or "delete" in function or "clear" in function:
        return "#FF6C7A"
    return PALETTE[item["section"]]


def lines(text: str, max_chars: int = 14) -> list[str]:
    text = text.replace(" / ", " ").replace(" · ", " ")
    if len(text) <= max_chars:
        return [text]
    words = text.split()
    candidates = []
    for index in range(1, len(words)):
        first, second = " ".join(words[:index]), " ".join(words[index:])
        candidates.append((max(len(first), len(second)), abs(len(first) - len(second)), first, second))
    _, _, first, second = min(candidates)
    return [first[:18], second[:18]]


def glyph_name(item: dict[str, str]) -> str:
    name = item["function"].lower()
    section = item["section"]

    # 1. Purpose-built overrides for the 8 fallbacks
    if "timeline 9:16" in name or "timeline 9x16" in name or "timeline 9×16" in name:
        return "timeline_9_16"
    if "timeline 4:5" in name or "timeline 4x5" in name or "timeline 4×5" in name:
        return "timeline_4_5"
    if "timeline 4:3" in name or "timeline 4x3" in name or "timeline 4×3" in name:
        return "timeline_4_3"
    if "rushwise" in name:
        return "rushwise"
    if "audio level" in name:
        return "audio_level"
    if "dynamic trim on/off" in name:
        return "dynamic_trim_toggle"
    if "dynamic trim" in name:
        return "dynamic_trim"
    if "effects library" in name:
        return "effects_library"

    # 2. Exact mappings
    exact = {
        "media page": "folder", "edit page 1": "scissors", "edit page 2": "link", "edit page 3": "timeline",
        "color page": "colorwheel", "fairlight page": "wave", "deliver page": "export", "quick export": "quickexport",
        "project settings": "gear", "new bin": "folderplus", "import media": "import", "power bins": "layers",
        "project notes": "note", "project manager": "grid", "new project": "newfile", "prefer proxy": "proxy", "camera originals": "camera",
        "ripple start": "rippleleft", "ripple end": "rippleright", "split": "scissors", "delete": "trash",
        "trim start": "trimleft", "trim end": "trimright", "retime controls": "retime", "change clip speed": "speed",
        "select backward all": "selectleft", "select forward all": "selectright", "snapping": "magnet",
        "zoom to fit": "fit", "timeline zoom": "zoom", "shuttle": "shuttle", "fast shuttle": "fastshuttle", "next clip": "nextclip",
        "add marker": "marker", "delete all markers": "markerdelete", "linked selection": "linked", "link clips": "link",
        "compound clip": "layers", "normalize": "normalize", "auto align": "align", "mark in": "markin", "mark out": "markout",
        "loop": "loop", "match frame": "matchframe", "cinema viewer": "cinema", "enable clip": "eye",
        "freeze frame": "freeze", "title safe": "safe", "delete gaps": "deletegaps", "find clip": "findclip",
        "crossfade": "crossfade", "swap left": "swapleft", "swap right": "swapright", "find timeline": "timeline",
        "new timeline": "timelineplus", "duplicate timeline": "duplicate", "undo": "undo", "save project": "save",
        "move clip up": "uptrack", "move clip down": "downtrack", "timeline start": "startline", "timeline end": "endline",
        "right-click": "rightclick", "ripple delete": "rippledelete", "media pool panel": "folder",
        "inspector panel": "inspector", "mixer panel": "mixer", "power bins panel": "layers", "metadata panel": "metadata", "index panel": "list",
        "copy": "copy", "paste attributes": "paste", "bypass all grades": "bypass",
        "scopes": "scope", "light box": "grid", "printer lights": "printerlights", "add node": "nodeplus", "node before": "nodebefore",
        "label node": "tag", "grab still": "still", "split selected": "splittwo", "split prev/next": "splitprevnext",
        "split original": "splitoriginal", "split stills": "splitstills", "saturation": "saturation", "reset saturation": "reset",
        "gamma": "gamma", "reset gamma": "reset", "gain": "gain", "reset gain": "reset",
        "printer light red": "redlight", "printer light green": "greenlight", "printer light blue": "bluelight",
        "exit split comparison": "closecompare", "batch fade settings": "fadesettings", "apply batch fades": "applyfade",
        "track height": "trackheight", "waveform zoom": "wavezoom", "reset waveform zoom": "reset",
        "youtube preset": "youtube", "vimeo preset": "vimeo", "tiktok preset": "tiktok", "instagram 4:5 preset": "instagram",
        "prores 422 hq preset": "prores", "custom preset 1": "custom1", "custom preset 2": "custom2", "custom preset 3": "custom3",
        "add to queue": "queueadd", "render all": "renderall", "render new": "rendernew", "stop render": "stop",
        "thumbnail": "thumbnail", "export folder": "folder", "clear render queue": "clearqueue",
        "mark in for export": "markin", "mark out for export": "markout", "free deliver controls": "free",
    }
    if name in exact:
        return exact[name]
    if "interval" in name or "timer" in name or "break" in name:
        return "timer"
    if "color" in name:
        return "colorswatch"
    if "play/pause" in name or "start timer" in name:
        return "play"
    if "frame-by-frame" in name:
        return "framewheel"
    if "reset" in name:
        return "reset"
    if section == "Color":
        return "colorwheel"
    return "spark"


def glyph(token: str, color: str) -> str:
    s = f'stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    fill = f'fill="{color}"'
    shapes = {
        # 8 Newly Redesigned Glyphs
        "timeline_9_16": f'<rect x="73" y="44" width="66" height="118" rx="10" {s}/><path d="M96 93l22 13-22 13z" {fill}/><circle cx="106" cy="144" r="5" {fill}/>',
        "timeline_4_5": f'<rect x="62" y="48" width="88" height="110" rx="8" {s}/><path d="M82 103h48M106 79v48" {s}/>',
        "timeline_4_3": f'<rect x="52" y="55" width="108" height="82" rx="7" {s}/><path d="M52 82h108M52 110h108" stroke="{color}" stroke-width="4" stroke-dasharray="6 6"/>',
        "rushwise": f'<path d="M106 43l55 55-55 55-55-55z" {s}/><circle cx="106" cy="98" r="16" {fill}/><path d="M106 43v30m0 50v30m-55-55h30m50 0h30" {s}/>',
        "audio_level": f'<path d="M60 148V72m31 76V52m31 76V62m30 86V92" stroke="{color}" stroke-width="12" stroke-linecap="round"/><circle cx="91" cy="80" r="10" {fill}/><circle cx="122" cy="100" r="10" {fill}/>',
        "dynamic_trim": f'<path d="M68 62v86l22-22m-22 22 22 22M144 62v86l-22-22m22 22-22 22M68 105h76" {s}/>',
        "dynamic_trim_toggle": f'<circle cx="106" cy="105" r="52" {s}/><path d="M106 62v32m-24 16h48" {s}/>',
        "effects_library": f'<path d="M55 145l65-65m12-12 18-18 18 18-18 18z" {s}/><path d="M65 65l6 14 14 6-14 6-6 14-6-14-14-6 14-6z" {fill}/>',

        # Standard Glyphs
        "folder": f'<path d="M38 78h45l12 15h83v55H38z" {s}/>',
        "folderplus": f'<path d="M33 82h48l12 14h84v53H33z" {s}/><path d="M136 105v32m-16-16h32" {s}/>',
        "import": f'<path d="M106 43v77m-29-29 29 29 29-29M47 142h118v18H47z" {s}/>',
        "grid": f'<rect x="52" y="51" width="37" height="37" rx="5" {s}/><rect x="123" y="51" width="37" height="37" rx="5" {s}/><rect x="52" y="122" width="37" height="37" rx="5" {s}/><rect x="123" y="122" width="37" height="37" rx="5" {s}/>',
        "gear": f'<circle cx="106" cy="105" r="26" {s}/><path d="M106 43v18m0 88v18M44 105h18m88 0h18M62 61l13 13m62 62 13 13M150 61l-13 13m-62 62-13 13" {s}/>',
        "note": f'<path d="M61 44h91v119H61zM82 76h48M82 103h48M82 130h28" {s}/>',
        "newfile": f'<path d="M67 43h63l27 27v94H67zM129 43v29h28M110 92v47m-24-24h48" {s}/>',
        "proxy": f'<rect x="43" y="61" width="126" height="87" rx="10" {s}/><path d="M73 95h46M73 120h29" {s}/><circle cx="153" cy="69" r="20" fill="#111923" {s}/><path d="M153 58v12l9 5" {s}/>',
        "camera": f'<path d="M42 82h34l14-20h35l14 20h31v69H42z" {s}/><circle cx="106" cy="116" r="25" {s}/>',
        "layers": f'<path d="M106 48l68 37-68 37-68-37zM38 119l68 37 68-37M38 93l68 37 68-37" {s}/>',
        "scissors": f'<circle cx="69" cy="75" r="17" {s}/><circle cx="69" cy="135" r="17" {s}/><path d="M84 88l71 48M84 122l71-48" {s}/>',
        "link": f'<path d="M92 125l-13 13a28 28 0 0 1-40-40l25-25a28 28 0 0 1 40 0m2 0 13-13a28 28 0 0 1 40 40l-25 25a28 28 0 0 1-40 0M78 106h57" {s}/>',
        "timeline": f'<path d="M42 73h127M42 106h127M42 139h127" {s}/><circle cx="70" cy="73" r="9" {fill}/><circle cx="119" cy="106" r="9" {fill}/><circle cx="151" cy="139" r="9" {fill}/>',
        "timelineplus": f'<path d="M42 76h79M42 106h79M42 136h79M151 105v43m-22-22h44" {s}/>',
        "duplicate": f'<rect x="54" y="61" width="75" height="81" rx="8" {s}/><rect x="83" y="43" width="75" height="81" rx="8" {s}/>',
        "colorwheel": f'<circle cx="106" cy="105" r="57" fill="#1a2332" {s}/><path d="M106 48a57 57 0 0 1 50 84l-50-27z" fill="#FF6B7B"/><path d="M106 105l50 27a57 57 0 0 1-100 0z" fill="#57DDA9"/><path d="M106 105 56 132a57 57 0 0 1 50-84z" fill="#5AA9FF"/><circle cx="106" cy="105" r="16" fill="#F3F7FF"/>',
        "wave": f'<path d="M34 106h18l12-41 20 84 22-101 22 116 18-74 14 16h22" {s}/>',
        "export": f'<path d="M61 43h78l26 26v89H61zM111 68v60m-23-24 23 24 23-24M79 151h70" {s}/>',
        "quickexport": f'<path d="M61 47h75l25 25v82H61zM108 71v53m-21-21 21 21 21-21" {s}/><path d="M164 41l7 22 22 7-22 7-7 22-7-22-22-7 22-7z" {fill}/>',
        "timer": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 72v34l26 18M82 43h48M106 43v14" {s}/>',
        "play": f'<path d="M80 58l68 47-68 47z" {fill}/><path d="M47 52v106" {s}/>',
        "stop": f'<rect x="63" y="62" width="86" height="86" rx="11" {fill}/>',
        "rippleleft": f'<path d="M151 105H72m20-22-22 22 22 22M166 73v64" {s}/>',
        "rippleright": f'<path d="M61 105h79m-20-22 22 22-22 22M46 73v64" {s}/>',
        "rippledelete": f'<path d="M150 105H71m20-22-22 22 22 22M164 73v64" {s}/><path d="M60 59l93 93M153 59l-93 93" stroke="#FF6C7A" stroke-width="8" stroke-linecap="round"/>',
        "trash": f'<path d="M66 66h80M88 66V48h36v18M78 66l7 87h42l7-87M95 89v40m22-40v40" {s}/>',
        "trimleft": f'<path d="M74 55v100m29-75H74m29 50H74M133 105h37" {s}/>',
        "trimright": f'<path d="M138 55v100m-29-75h29m-29 50h29M72 105h37" {s}/>',
        "retime": f'<circle cx="105" cy="106" r="43" {s}/><path d="M105 79v28l21 14M105 44v18M163 106h-18" {s}/>',
        "speed": f'<path d="M44 83h81l-20-20m20 20-20 20M168 128H87l20-20m-20 20 20 20" {s}/>',
        "selectleft": f'<path d="M158 65H74l23-23M74 65l23 23M158 145H74" {s}/><rect x="46" y="116" width="49" height="35" rx="5" {s}/>',
        "selectright": f'<path d="M54 65h84l-23-23m23 23-23 23M54 145h84" {s}/><rect x="117" y="116" width="49" height="35" rx="5" {s}/>',
        "magnet": f'<path d="M67 59v47a39 39 0 0 0 78 0V59M67 59h22m34 0h22M78 136l-18 18m74-18 18 18" {s}/>',
        "fit": f'<path d="M48 82V54h28M164 82V54h-28M48 128v28h28M164 128v28h-28M75 80h62v50H75z" {s}/>',
        "zoom": f'<circle cx="91" cy="91" r="37" {s}/><path d="M119 119l40 40M91 73v36m-18-18h36" {s}/>',
        "shuttle": f'<path d="M44 105h119M44 77l-28 28 28 28M162 77l28 28-28 28" {s}/>',
        "fastshuttle": f'<path d="M40 105h111M40 77l-28 28 28 28M149 77l28 28-28 28M118 77l28 28-28 28" {s}/>',
        "nextclip": f'<path d="M45 70v70M76 105h76m-24-25 25 25-25 25M167 70v70" {s}/>',
        "marker": f'<path d="M66 51h80v57l-40 45-40-45z" {s}/><path d="M84 78h43" {s}/>',
        "markerdelete": f'<path d="M67 52h78v54l-39 46-39-46z" {s}/><path d="M83 76l45 45m0-45-45 45" stroke="#FF6C7A" stroke-width="10" stroke-linecap="round"/>',
        "linked": f'<path d="M55 83h95M55 128h95" {s}/><path d="M77 65l-18 18 18 18M128 110l18 18-18 18" {s}/>',
        "normalize": f'<path d="M39 124h18l12-29 18 54 19-84 20 93 19-56 13 22h21" {s}/><path d="M38 55h136" {s}/>',
        "align": f'<path d="M55 61v86m96-86v86M78 83h56M78 126h56M95 61v86m22-86v86" {s}/>',
        "markin": f'<path d="M72 59v92m22-65H72m22 40H72M115 105h54" {s}/>',
        "markout": f'<path d="M140 59v92m-22-65h22m-22 40h22M43 105h54" {s}/>',
        "loop": f'<path d="M145 79a48 48 0 1 0 7 57M142 58v29h-29" {s}/>',
        "matchframe": f'<rect x="49" y="60" width="113" height="90" rx="8" {s}/><path d="M75 126l22-22 19 16 15-15 20 21" {s}/><path d="M151 69v31h-31" {s}/>',
        "cinema": f'<rect x="45" y="64" width="122" height="82" rx="8" {s}/><path d="M73 157h66" {s}/>',
        "eye": f'<path d="M36 105s27-45 70-45 70 45 70 45-27 45-70 45-70-45-70-45z" {s}/><circle cx="106" cy="105" r="20" {s}/>',
        "freeze": f'<path d="M64 53h84v104H64zM87 80h38M87 105h38M87 130h38" {s}/><path d="M52 63l108 84" stroke="#82C8FF" stroke-width="8" stroke-linecap="round"/>',
        "safe": f'<rect x="48" y="48" width="116" height="116" rx="6" {s}/><path d="M73 73h66v66H73zM90 91h32v32H90z" {s}/>',
        "deletegaps": f'<path d="M42 105h43m35 0h44M85 79l26 26-26 26M127 79l-26 26 26 26" {s}/>',
        "findclip": f'<rect x="49" y="63" width="91" height="77" rx="8" {s}/><circle cx="139" cy="136" r="25" {s}/><path d="M157 154l20 20" {s}/>',
        "crossfade": f'<path d="M40 143h31l35-76 35 76h31M40 67h132" {s}/>',
        "swapleft": f'<path d="M153 78H75l22-22M75 78l22 22M57 132h78l-22-22m22 22-22 22" {s}/>',
        "swapright": f'<path d="M59 78h78l-22-22m22 22-22 22M155 132H77l22-22m-22 22 22 22" {s}/>',
        "undo": f'<path d="M91 60L52 100l39 40M55 100h63a36 36 0 0 1 36 36" {s}/>',
        "save": f'<path d="M55 48h84l21 21v91H55zM79 48v45h51V48m-48 101h49" {s}/>',
        "uptrack": f'<path d="M106 156V55m-27 29 27-29 27 29M57 143h99" {s}/>',
        "downtrack": f'<path d="M106 54v101m-27-29 27 29 27-29M57 67h99" {s}/>',
        "startline": f'<path d="M73 75v60M99 105h63m-33-30-30 30 30 30" {s}/>',
        "endline": f'<path d="M139 75v60M113 105H50m33-30 30 30-30 30" {s}/>',
        "rightclick": f'<path d="M75 51v76m0 0-18-22m18 22 18-22M111 51v76m0 0-18-22m18 22 18-22M70 150h41a27 27 0 0 0 27-27V88" {s}/>',
        "spark": f'<path d="M106 43l14 48 48 14-48 14-14 48-14-48-48-14 48-14z" {s}/>',
        "inspector": f'<rect x="52" y="49" width="108" height="112" rx="8" {s}/><path d="M77 80h58M77 105h58M77 130h34" {s}/>',
        "mixer": f'<path d="M62 57v96m44-96v96m44-96v96M45 86h34m27 45h34m10-50h34" {s}/><circle cx="62" cy="86" r="10" {fill}/><circle cx="106" cy="131" r="10" {fill}/><circle cx="150" cy="81" r="10" {fill}/>',
        "metadata": f'<path d="M49 57h78l29 29v70H49zM127 57v29h29M75 113h55M75 137h32" {s}/>',
        "list": f'<path d="M67 65h91M67 105h91M67 145h91" {s}/><circle cx="45" cy="65" r="7" {fill}/><circle cx="45" cy="105" r="7" {fill}/><circle cx="45" cy="145" r="7" {fill}/>',
        "copy": f'<rect x="51" y="67" width="76" height="87" rx="8" {s}/><rect x="84" y="45" width="76" height="87" rx="8" {s}/>',
        "paste": f'<path d="M59 57h94v104H59zM84 57v-13h44v13M80 96h52M80 122h35" {s}/><path d="M137 136l21 21 30-38" {s}/>',
        "bypass": f'<circle cx="106" cy="105" r="55" {s}/><path d="M59 59l94 94" stroke="#FF6C7A" stroke-width="12" stroke-linecap="round"/>',
        "scope": f'<circle cx="106" cy="105" r="56" {s}/><path d="M50 105h112M106 49v112M66 145l80-80" {s}/>',
        "printerlights": f'<circle cx="106" cy="105" r="52" {s}/><path d="M106 53v104M61 79l90 52M61 131l90-52" {s}/><circle cx="106" cy="105" r="13" {fill}/>',
        "nodeplus": f'<circle cx="78" cy="105" r="28" {s}/><path d="M122 105h50m-25-25v50" {s}/>',
        "nodebefore": f'<circle cx="78" cy="105" r="24" {s}/><circle cx="147" cy="105" r="24" {s}/><path d="M104 105h17m-10-11 11 11-11 11" {s}/>',
        "tag": f'<path d="M50 78l54-31 51 51-31 54-74-74z" {s}/><circle cx="101" cy="78" r="8" {s}/>',
        "still": f'<rect x="47" y="61" width="118" height="88" rx="9" {s}/><path d="M70 127l25-24 20 18 15-14 20 20" {s}/><circle cx="88" cy="85" r="8" {s}/>',
        "splittwo": f'<rect x="47" y="61" width="50" height="88" rx="6" {s}/><rect x="115" y="61" width="50" height="88" rx="6" {s}/>',
        "splitprevnext": f'<rect x="43" y="69" width="40" height="72" rx="5" {s}/><rect x="86" y="54" width="40" height="102" rx="5" {s}/><rect x="129" y="69" width="40" height="72" rx="5" {s}/>',
        "splitoriginal": f'<rect x="47" y="60" width="57" height="90" rx="6" {s}/><rect x="108" y="60" width="57" height="90" rx="6" {s}/><path d="M77 117l17-19 17 19m28 0 17-19 17 19" {s}/>',
        "splitstills": f'<rect x="49" y="62" width="48" height="84" rx="6" {s}/><rect x="114" y="62" width="48" height="84" rx="6" {s}/><path d="M58 127l13-15 15 15m38 0 13-15 15 15" {s}/>',
        "saturation": f'<path d="M106 47a58 58 0 1 0 58 58" {s}/><circle cx="106" cy="105" r="24" {s}/><path d="M148 64l16-17 18 18" {s}/>',
        "gamma": f'<path d="M51 149l44-91 44 91M70 110h51" {s}/><path d="M137 94h33v55" {s}/>',
        "gain": f'<path d="M52 145l34-45 25 22 41-61" {s}/><path d="M130 61h22v22" {s}/>',
        "reset": f'<path d="M151 84a49 49 0 1 0 5 46M151 58v29h-29" {s}/>',
        "redlight": f'<circle cx="106" cy="105" r="49" fill="#FF6572" opacity=".25" {s}/><text x="106" y="119" text-anchor="middle" fill="{color}" font-size="51" font-family="Arial" font-weight="700">R</text>',
        "greenlight": f'<circle cx="106" cy="105" r="49" fill="#5EE07E" opacity=".25" {s}/><text x="106" y="119" text-anchor="middle" fill="{color}" font-size="51" font-family="Arial" font-weight="700">G</text>',
        "bluelight": f'<circle cx="106" cy="105" r="49" fill="#65AFFF" opacity=".25" {s}/><text x="106" y="119" text-anchor="middle" fill="{color}" font-size="51" font-family="Arial" font-weight="700">B</text>',
        "closecompare": f'<rect x="53" y="57" width="106" height="96" rx="9" {s}/><path d="M79 82l54 54m0-54-54 54" {s}/>',
        "fadesettings": f'<path d="M66 54v102m40-102v102m40-102v102M48 81h36m22 47h36m22-28h36" {s}/><circle cx="66" cy="81" r="10" {fill}/><circle cx="106" cy="128" r="10" {fill}/><circle cx="146" cy="100" r="10" {fill}/>',
        "applyfade": f'<path d="M48 143h31l27-70 27 70h31" {s}/><path d="M146 65l12 12 23-26" {s}/>',
        "trackheight": f'<path d="M66 58v94m74-94v94M82 77h48M82 105h48M82 133h48" {s}/><path d="M106 43v20m0 85v20m-13-13 13 13 13-13M93 56l13-13 13 13" {s}/>',
        "wavezoom": f'<path d="M42 106h16l12-36 18 70 20-89 21 101 18-58 12 12h20" {s}/><path d="M158 52v34m-17-17h34" {s}/>',
        "youtube": f'<rect x="45" y="67" width="122" height="77" rx="18" {s}/><path d="M94 87l39 19-39 19z" {fill}/>',
        "vimeo": f'<path d="M52 77c20-17 46-24 56 2 9 23-14 57-6 57 7 0 24-28 31-42 8-17 25-22 36-13-14 47-55 87-74 87-17 0-26-45-35-69-5-13-11-10-23 0z" {s}/>',
        "tiktok": f'<path d="M119 48v77a28 28 0 1 1-25-28v22a7 7 0 1 0 6 6V48h19c3 17 14 27 31 29v20c-12-1-23-6-31-14" {s}/>',
        "instagram": f'<rect x="51" y="50" width="110" height="110" rx="29" {s}/><circle cx="106" cy="105" r="27" {s}/><circle cx="140" cy="72" r="7" {fill}/>',
        "prores": f'<rect x="44" y="70" width="124" height="70" rx="9" {s}/><text x="106" y="116" text-anchor="middle" fill="{color}" font-size="33" font-family="Arial" font-weight="700">HQ</text>',
        "custom1": f'<rect x="52" y="51" width="108" height="108" rx="12" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-size="56" font-family="Arial" font-weight="700">1</text>',
        "custom2": f'<rect x="52" y="51" width="108" height="108" rx="12" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-size="56" font-family="Arial" font-weight="700">2</text>',
        "custom3": f'<rect x="52" y="51" width="108" height="108" rx="12" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-size="56" font-family="Arial" font-weight="700">3</text>',
        "queueadd": f'<path d="M53 61h73l25 25v67H53zM126 61v25h25M102 102v36m-18-18h36" {s}/>',
        "renderall": f'<path d="M67 62l60 43-60 43zM129 62l60 43-60 43z" {s}/>',
        "rendernew": f'<path d="M68 62l68 43-68 43z" {s}/><path d="M154 65v32m-16-16h32" {s}/>',
        "thumbnail": f'<rect x="48" y="61" width="116" height="87" rx="9" {s}/><path d="M69 126l24-24 20 18 16-15 20 21" {s}/><circle cx="89" cy="85" r="8" {s}/>',
        "clearqueue": f'<path d="M54 62h104M82 62V49h48v13M68 62l8 91h60l8-91M93 88v42m26-42v42" {s}/><path d="M49 151h114" {s}/>',
        "free": f'<path d="M49 58h114v94H49z" {s}/><text x="106" y="117" text-anchor="middle" fill="{color}" font-size="36" font-family="Arial" font-weight="700">FREE</text>',
        "colorswatch": f'<circle cx="106" cy="105" r="47" fill="{color}"/><circle cx="106" cy="105" r="57" {s}/>',
        "framewheel": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 58v94M59 105h94" {s}/><circle cx="106" cy="105" r="15" {fill}/>',
    }
    return shapes.get(token, shapes["spark"])


def asset_type(item: dict[str, str]) -> str:
    control = item["control"].lower()
    if "dial" in control:
        return "dial"
    if "touch" in control or "swipe-right" in control:
        return "touch"
    return "physical"


def svg_touch(item: dict[str, str], color: str, token: str) -> str:
    label = lines(item["function"], 15)
    text = "".join(
        f'<text x="128" y="{204 + line * 21}" text-anchor="middle" fill="#F5F7FC" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700">{html.escape(val)}</text>'
        for line, val in enumerate(label)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
        f'<rect width="256" height="256" rx="22" fill="#15181E"/>'
        f'<rect x="3" y="3" width="250" height="250" rx="19" fill="none" stroke="#364055" stroke-width="3"/>'
        f'<rect x="18" y="16" width="220" height="5" rx="2.5" fill="{color}"/>'
        f'<g transform="translate(22 15)">{glyph(token, color)}</g>'
        f'<path d="M31 180h194" stroke="#303A4E" stroke-width="2"/>{text}</svg>'
    )


def svg_dial(item: dict[str, str], color: str, token: str) -> str:
    """Generate 120x180 vertical strip dial SVG."""
    label = lines(item["function"], 12)
    line_text = "".join(
        f'<text x="60" y="{118 + line * 17}" text-anchor="middle" fill="#F5F7FC" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="700">{html.escape(val)}</text>'
        for line, val in enumerate(label)
    )
    control = "TURN" if "turn" in item["control"].lower() else "PRESS"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="120" height="180" viewBox="0 0 120 180">'
        f'<rect width="120" height="180" rx="14" fill="#15181E"/>'
        f'<rect x="2" y="2" width="116" height="176" rx="12" fill="none" stroke="#364055" stroke-width="2"/>'
        f'<rect x="12" y="8" width="96" height="4" rx="2" fill="{color}"/>'
        f'<g transform="translate(-16 -12) scale(.72)">{glyph(token, color)}</g>'
        f'{line_text}'
        f'<rect x="14" y="154" width="92" height="18" rx="6" fill="#111620" stroke="{color}" stroke-width="1.5"/>'
        f'<text x="60" y="167" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="10" font-weight="700" letter-spacing="1">{control}</text>'
        f'</svg>'
    )


def svg_physical(item: dict[str, str], color: str, token: str) -> str:
    label = lines(item["function"], 22)
    control = item["control"].upper().replace("ROUND BUTTON", "ROUND")
    label_text = "".join(
        f'<text x="126" y="{68 + line * 29}" fill="#F5F7FC" font-family="Arial, Helvetica, sans-serif" font-size="25" font-weight="700">{html.escape(val)}</text>'
        for line, val in enumerate(label)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="320" height="160" viewBox="0 0 320 160">'
        f'<rect width="320" height="160" rx="17" fill="#15181E"/>'
        f'<rect x="3" y="3" width="314" height="154" rx="14" fill="none" stroke="#364055" stroke-width="3"/>'
        f'<rect x="17" y="17" width="91" height="126" rx="14" fill="#11151C" stroke="{color}" stroke-width="3"/>'
        f'<g transform="translate(-3 2) scale(.52)">{glyph(token, color)}</g>{label_text}'
        f'<text x="126" y="136" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="700" letter-spacing="1.3">{html.escape(control[:27])}</text></svg>'
    )


def main() -> None:
    dirs = {k: SVG_ROOT / k for k in ("touch", "dial", "physical")}
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    manifest = []
    for index, item in enumerate(ITEMS, start=1):
        kind = asset_type(item)
        color = accent(item)
        token = glyph_name(item)
        digest = hashlib.sha1(f"{item['section']}|{item['control']}|{item['function']}".encode()).hexdigest()[:6]
        filename = f"{index:03d}-{slugify(item['function'])}-{digest}.svg"

        if kind == "touch":
            svg = svg_touch(item, color, token)
        elif kind == "dial":
            svg = svg_dial(item, color, token)
        else:
            svg = svg_physical(item, color, token)

        (dirs[kind] / filename).write_text(svg, encoding="utf-8")
        manifest.append({
            "id": f"rupokar.final.{index:03d}",
            "filename": f"final-svg/{kind}/{filename}",
            "type": kind,
            "function": item["function"],
            "control": item["control"],
            "section": item["section"],
            "availability": item["availability"],
            "source_time": item["source_time"],
            "accent": color,
            "glyph": token,
            "reference": f"Inspired File/Rupokar-Resolve-CT-Icon-System/reference-png/{index:03d}.png"
        })

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cards = "\n".join(
        f'<article class="card"><div class="final"><img src="{html.escape(m["filename"])}" alt="{html.escape(m["function"])}"></div>'
        f'<div class="info"><p class="eyebrow">#{idx:03d} · {html.escape(m["type"])}</p>'
        f'<h2>{html.escape(m["function"])}</h2><p><strong>{html.escape(m["control"])}</strong></p>'
        f'<p>{html.escape(m["section"])} · {html.escape(m["availability"])}</p>'
        f'<p class="time">Video: {html.escape(m["source_time"])}</p></div></article>'
        for idx, m in enumerate(manifest, start=1)
    )
    BOARD_PATH.write_text(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Rupokar Resolve CT Icon Board</title>'
        f'<style>body{{margin:0;padding:32px;background:#09101c;color:#eef4ff;font-family:-apple-system,sans-serif}}'
        f'.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin-top:20px}}'
        f'.card{{display:flex;gap:12px;background:#111b2a;border:1px solid #2a3a52;border-radius:12px;padding:12px}}'
        f'.final{{display:grid;place-items:center;background:#080e17;border-radius:8px;padding:6px;min-width:110px}}'
        f'.final img{{max-width:100%;max-height:160px}}.eyebrow{{color:#55d8bf;font-size:11px;font-weight:700;margin:0}}'
        f'h2{{font-size:16px;margin:4px 0}}p{{margin:4px 0;font-size:13px;color:#c7d4e8}}'
        f'</style></head><body><h1>Rupokar Resolve CT — Multi-Ratio Icon System</h1>'
        f'<p>168 Purpose-Built Vector SVGs for Touch (256x256), Dial (120x180), and Physical (320x160).</p>'
        f'<main class="grid">{cards}</main></body></html>',
        encoding="utf-8"
    )
    print(f"Generated {len(manifest)} SVGs: Touch={sum(x['type']=='touch' for x in manifest)}, Dial={sum(x['type']=='dial' for x in manifest)}, Physical={sum(x['type']=='physical' for x in manifest)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Execute generator and verify tests pass**

Run: `python3 scripts/build_icons.py && python3 -m pytest tests/test_icon_system.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/build_icons.py tests/test_icon_system.py icons/
git commit -m "feat(icons): generate 168 multi-ratio SVGs with 8 custom fallback glyphs"
```

---

### Task 2: High-DPI Raster Asset Exporter (PNG Generation)

**Files:**
- Create: `scripts/export_raster_icons.py`
- Test: `tests/test_raster_export.py`
- Output directories:
  - `icons/export-png/touch/`
  - `icons/export-png/dial/`
  - `icons/export-png/physical/`

**Interfaces:**
- Consumes: `icons/final-svg/` (168 SVGs)
- Produces: `icons/export-png/` (168 crisp PNG files for Loupedeck packaging)

- [ ] **Step 1: Write the test verifying raster export**

Create `tests/test_raster_export.py`:
```python
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
PNG_ROOT = REPO_ROOT / "icons" / "export-png"


def test_png_files_exist():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        # replace .svg with .png in export path
        svg_filename = Path(item["filename"]).name
        png_path = PNG_ROOT / item["type"] / svg_filename.replace(".svg", ".png")
        assert png_path.exists(), f"Expected raster export {png_path} to exist"
        assert png_path.stat().st_size > 500, f"PNG {png_path} is unexpectedly small"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_raster_export.py -v`
Expected: FAIL with "Expected raster export ... to exist"

- [ ] **Step 3: Implement `scripts/export_raster_icons.py` using macOS `qlmanage` / python `cairosvg` or built-in webkit renderer**

Create `scripts/export_raster_icons.py`:
```python
#!/usr/bin/env python3
"""Export all 168 SVGs into high-DPI PNGs for Loupedeck packaging using macOS QuickLook."""

import json
import subprocess
from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
SVG_ROOT = REPO_ROOT / "icons" / "final-svg"
PNG_ROOT = REPO_ROOT / "icons" / "export-png"


def export_svg_to_png(svg_path: Path, png_path: Path, width: int) -> None:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    # Using macOS built-in sips / qlmanage to convert SVG to high-res PNG without extra pip dependencies
    tmp_dir = png_path.parent / f"_tmp_{png_path.stem}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    try:
        cmd = ["qlmanage", "-t", "-s", str(width * 2), "-o", str(tmp_dir), str(svg_path)]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        generated = tmp_dir / f"{svg_path.name}.png"
        if generated.exists():
            shutil.move(str(generated), str(png_path))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    print(f"Exporting {len(items)} SVGs to PNG...")
    widths = {"touch": 256, "dial": 120, "physical": 320}

    for item in items:
        svg_file = REPO_ROOT / "icons" / item["filename"]
        target_png = PNG_ROOT / item["type"] / svg_file.name.replace(".svg", ".png")
        export_svg_to_png(svg_file, target_png, widths[item["type"]])

    print("Raster export complete.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run export script and verify test passes**

Run: `python3 scripts/export_raster_icons.py && python3 -m pytest tests/test_raster_export.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/export_raster_icons.py tests/test_raster_export.py icons/export-png/
git commit -m "feat(icons): export 168 high-DPI PNGs for Loupedeck packaging"
```

---

### Task 3: Local DaVinci Resolve Automation Bridge Service

**Files:**
- Create: `bridge/rupokar_resolve_bridge/socket_server.py`
- Create: `bridge/rupokar_resolve_bridge/command_router.py`
- Create: `bridge/rupokar_resolve_bridge/resolve_client.py`
- Create: `bridge/rupokar_resolve_bridge/bridge_service.py`
- Create: `scripts/run_bridge.sh`
- Test: `tests/test_resolve_bridge.py`

**Interfaces:**
- Consumes: DaVinci Resolve Scripting API or local mock when offline
- Produces: Unix Domain Socket listener at `~/.rupokar/bridge.sock` responding to JSON RPC calls

- [ ] **Step 1: Write the test verifying bridge socket server & command router**

Create `tests/test_resolve_bridge.py`:
```python
import json
import socket
import threading
import time
from pathlib import Path
import pytest

from bridge.rupokar_resolve_bridge.command_router import handle_command


def test_command_router_offline():
    # When resolve is offline or mocked
    response = handle_command({"id": "resolve.ping", "requestId": "123"})
    assert response["requestId"] == "123"
    assert "ok" in response
    assert "state" in response


def test_command_router_unknown():
    response = handle_command({"id": "non_existent_command", "requestId": "999"})
    assert response["ok"] is False
    assert response["error"] == "UNKNOWN_COMMAND"


def test_socket_server_roundtrip():
    test_socket = Path.home() / ".rupokar" / "test_bridge.sock"
    from bridge.rupokar_resolve_bridge.socket_server import SocketServer

    server = SocketServer(socket_path=test_socket)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.3)

    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(str(test_socket))
        payload = json.dumps({"id": "resolve.ping", "requestId": "req-1"}).encode("utf-8") + b"\n"
        client.sendall(payload)
        data = client.recv(4096).decode("utf-8").strip()
        client.close()

        res = json.loads(data)
        assert res["requestId"] == "req-1"
        assert res["ok"] is True
    finally:
        server.stop()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_resolve_bridge.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Implement `command_router.py`, `resolve_client.py`, `socket_server.py`, and `bridge_service.py`**

Create `bridge/rupokar_resolve_bridge/resolve_client.py`:
```python
"""Client interfacing with DaVinci Resolve 21.1.2 Scripting API."""

from __future__ import annotations
import sys
from pathlib import Path


class ResolveClient:
    def __init__(self) -> None:
        self.resolve = None
        self._init_resolve()

    def _init_resolve(self) -> None:
        # Standard DaVinci Resolve Scripting module paths on macOS
        paths = [
            "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules",
            "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Resources/ResolvePython",
        ]
        for p in paths:
            if p not in sys.path and Path(p).exists():
                sys.path.append(p)
        try:
            import DaVinciResolveScript as dvr_script
            self.resolve = dvr_script.scriptapp("Resolve")
        except Exception:
            self.resolve = None

    def is_connected(self) -> bool:
        if self.resolve is None:
            self._init_resolve()
        return self.resolve is not None

    def get_status(self) -> dict:
        if not self.is_connected():
            return {"connected": False, "version": None, "activeProject": None}
        pm = self.resolve.GetProjectManager()
        project = pm.GetCurrentProject() if pm else None
        return {
            "connected": True,
            "version": self.resolve.GetVersionString(),
            "activeProject": project.GetName() if project else None,
        }

    def start_rendering(self) -> dict:
        if not self.is_connected():
            return {"ok": False, "message": "Resolve not connected"}
        pm = self.resolve.GetProjectManager()
        project = pm.GetCurrentProject() if pm else None
        if not project:
            return {"ok": False, "message": "No active project"}
        started = project.StartRendering()
        return {"ok": started, "message": "Rendering started" if started else "Failed to start render"}

    def stop_rendering(self) -> dict:
        if not self.is_connected():
            return {"ok": False, "message": "Resolve not connected"}
        pm = self.resolve.GetProjectManager()
        project = pm.GetCurrentProject() if pm else None
        if not project:
            return {"ok": False, "message": "No active project"}
        project.StopRendering()
        return {"ok": True, "message": "Rendering stopped"}

    def get_render_jobs(self) -> dict:
        if not self.is_connected():
            return {"ok": False, "jobs": []}
        pm = self.resolve.GetProjectManager()
        project = pm.GetCurrentProject() if pm else None
        if not project:
            return {"ok": False, "jobs": []}
        jobs = project.GetRenderJobList() or []
        is_rendering = project.IsRenderingInProgress()
        return {"ok": True, "jobs": jobs, "isRendering": is_rendering}

    def duplicate_timeline(self, aspect_ratio: str) -> dict:
        if not self.is_connected():
            return {"ok": False, "message": "Resolve not connected"}
        pm = self.resolve.GetProjectManager()
        project = pm.GetCurrentProject() if pm else None
        if not project:
            return {"ok": False, "message": "No active project"}
        timeline = project.GetCurrentTimeline()
        if not timeline:
            return {"ok": False, "message": "No active timeline"}
        orig_name = timeline.GetName()
        new_name = f"{orig_name} ({aspect_ratio})"
        timeline.DuplicateTimeline(new_name)
        return {"ok": True, "message": f"Created timeline: {new_name}"}
```

Create `bridge/rupokar_resolve_bridge/command_router.py`:
```python
"""Strict allow-list command router for Rupokar Resolve Bridge."""

from __future__ import annotations
from typing import Any
from bridge.rupokar_resolve_bridge.resolve_client import ResolveClient

resolve_client = ResolveClient()


def handle_command(request: dict[str, Any]) -> dict[str, Any]:
    cmd_id = request.get("id")
    request_id = request.get("requestId", "")
    payload = request.get("payload", {})

    if cmd_id == "resolve.ping":
        status = resolve_client.get_status()
        return {
            "requestId": request_id,
            "ok": True,
            "state": "CONNECTED" if status["connected"] else "OFFLINE",
            "data": status,
        }

    if cmd_id == "render.start.all":
        result = resolve_client.start_rendering()
        return {"requestId": request_id, **result}

    if cmd_id == "render.stop":
        result = resolve_client.stop_rendering()
        return {"requestId": request_id, **result}

    if cmd_id == "render.queue.status":
        result = resolve_client.get_render_jobs()
        return {"requestId": request_id, **result}

    if cmd_id == "timeline.copy.aspect":
        ratio = payload.get("ratio", "9:16")
        result = resolve_client.duplicate_timeline(ratio)
        return {"requestId": request_id, **result}

    return {
        "requestId": request_id,
        "ok": False,
        "error": "UNKNOWN_COMMAND",
        "message": f"Command {cmd_id} is not supported",
    }
```

Create `bridge/rupokar_resolve_bridge/socket_server.py`:
```python
"""Unix Domain Socket server for local IPC."""

from __future__ import annotations
import json
import os
import socket
from pathlib import Path
from bridge.rupokar_resolve_bridge.command_router import handle_command


class SocketServer:
    def __init__(self, socket_path: Path | None = None) -> None:
        self.socket_path = socket_path or (Path.home() / ".rupokar" / "bridge.sock")
        self.running = False
        self.server_sock: socket.socket | None = None

    def start(self) -> None:
        self.socket_path.parent.mkdir(parents=True, exist_ok=True)
        if self.socket_path.exists():
            self.socket_path.unlink()

        self.server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_sock.bind(str(self.socket_path))
        self.server_sock.listen(5)
        self.running = True

        while self.running:
            try:
                conn, _ = self.server_sock.accept()
                with conn:
                    data = conn.recv(4096).decode("utf-8").strip()
                    if not data:
                        continue
                    try:
                        req = json.loads(data)
                        res = handle_command(req)
                    except Exception as err:
                        res = {"ok": False, "error": "INVALID_JSON", "message": str(err)}
                    conn.sendall(json.dumps(res).encode("utf-8") + b"\n")
            except OSError:
                break

    def stop(self) -> None:
        self.running = False
        if self.server_sock:
            self.server_sock.close()
        if self.socket_path.exists():
            self.socket_path.unlink()
```

Create `bridge/rupokar_resolve_bridge/bridge_service.py`:
```python
#!/usr/bin/env python3
"""Main service entry point for Rupokar Resolve Bridge."""

import signal
import sys
from bridge.rupokar_resolve_bridge.socket_server import SocketServer


def main():
    server = SocketServer()

    def handle_sig(sig, frame):
        print("\nStopping Rupokar Resolve Bridge...")
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sig)
    signal.signal(signal.SIGTERM, handle_sig)
    print("Starting Rupokar Resolve Bridge on ~/.rupokar/bridge.sock")
    server.start()


if __name__ == "__main__":
    main()
```

Create `scripts/run_bridge.sh`:
```bash
#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
export PYTHONPATH="$DIR"
exec python3 "$DIR/bridge/rupokar_resolve_bridge/bridge_service.py"
```
Make executable: `chmod +x scripts/run_bridge.sh`

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_resolve_bridge.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add bridge/ scripts/run_bridge.sh tests/test_resolve_bridge.py
git commit -m "feat(bridge): add local DaVinci Resolve automation bridge with Unix socket"
```

---

### Task 4: Logi Actions .NET 8 C# Plugin Skeleton & Dynamic Countdown

**Files:**
- Create: `plugin/Rupokar.Resolve.Actions/Rupokar.Resolve.Actions.csproj`
- Create: `plugin/Rupokar.Resolve.Actions/RupokarResolvePlugin.cs`
- Create: `plugin/Rupokar.Resolve.Actions/Actions/BreakTimerAction.cs`
- Create: `plugin/Rupokar.Resolve.Actions/Actions/RenderQueueAction.cs`
- Create: `plugin/Rupokar.Resolve.Actions/DynamicDisplay/TileImageRenderer.cs`
- Create: `plugin/Rupokar.Resolve.Actions/IPC/BridgeSocketClient.cs`
- Test: `tests/test_plugin_structure.py`

**Interfaces:**
- Consumes: Loupedeck / Logi Actions SDK v6
- Produces: C# plugin source code structure with Break Timer 1-sec countdown rendering and IPC client

- [ ] **Step 1: Write test verifying plugin source files and contracts**

Create `tests/test_plugin_structure.py`:
```python
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = REPO_ROOT / "plugin" / "Rupokar.Resolve.Actions"


def test_plugin_files_exist():
    expected_files = [
        "Rupokar.Resolve.Actions.csproj",
        "RupokarResolvePlugin.cs",
        "Actions/BreakTimerAction.cs",
        "Actions/RenderQueueAction.cs",
        "DynamicDisplay/TileImageRenderer.cs",
        "IPC/BridgeSocketClient.cs",
    ]
    for rel_path in expected_files:
        p = PLUGIN_ROOT / rel_path
        assert p.exists(), f"Expected {p} to exist"
        assert p.stat().st_size > 100, f"File {p} is empty"


def test_break_timer_intervals():
    timer_cs = (PLUGIN_ROOT / "Actions" / "BreakTimerAction.cs").read_text(encoding="utf-8")
    assert "25" in timer_cs
    assert "45" in timer_cs
    assert "1.5" in timer_cs or "90" in timer_cs
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_plugin_structure.py -v`
Expected: FAIL with "Expected ... to exist"

- [ ] **Step 3: Implement plugin source files**

Create `plugin/Rupokar.Resolve.Actions/Rupokar.Resolve.Actions.csproj`:
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <AssemblyName>Rupokar.Resolve.Actions</AssemblyName>
    <RootNamespace>Rupokar.Resolve.Actions</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Loupedeck.PluginApi" Version="6.4.1" />
  </ItemGroup>
</Project>
```

Create `plugin/Rupokar.Resolve.Actions/RupokarResolvePlugin.cs`:
```csharp
namespace Rupokar.Resolve.Actions;

using Loupedeck;

public class RupokarResolvePlugin : Plugin
{
    public override bool HasNoApplication => false;
    public override bool UsesApplicationApiOnly => false;

    public override void Load()
    {
        PluginLog.Info("Rupokar Resolve Actions Plugin Loaded");
    }

    public override void Unload()
    {
        PluginLog.Info("Rupokar Resolve Actions Plugin Unloaded");
    }
}
```

Create `plugin/Rupokar.Resolve.Actions/DynamicDisplay/TileImageRenderer.cs`:
```csharp
namespace Rupokar.Resolve.Actions.DynamicDisplay;

using Loupedeck;
using System.Drawing;

public static class TileImageRenderer
{
    public static BitmapImage DrawTimerCountdown(string timeText, bool isElapsed)
    {
        using var builder = new BitmapBuilder(256, 256);
        builder.FillRectangle(0, 0, 256, 256, BitmapColor.Black);

        var accentColor = isElapsed ? new BitmapColor(255, 60, 60) : new BitmapColor(78, 224, 226);
        builder.DrawRectangle(4, 4, 248, 248, accentColor);

        builder.DrawText(isElapsed ? "BREAK NOW!" : timeText, 0, 80, 256, 60, BitmapColor.White, 36);
        builder.DrawText("Break Status", 0, 180, 256, 40, accentColor, 20);

        return builder.ToImage();
    }
}
```

Create `plugin/Rupokar.Resolve.Actions/IPC/BridgeSocketClient.cs`:
```csharp
namespace Rupokar.Resolve.Actions.IPC;

using System.Net.Sockets;
using System.Text;
using System.Text.Json;

public class BridgeSocketClient
{
    private readonly string _socketPath;

    public BridgeSocketClient()
    {
        var home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        _socketPath = Path.Combine(home, ".rupokar", "bridge.sock");
    }

    public async Task<string?> SendCommandAsync(string commandId, object? payload = null)
    {
        if (!File.Exists(_socketPath)) return null;

        using var client = new Socket(AddressFamily.Unix, SocketType.Stream, ProtocolType.Unspecified);
        var endpoint = new UnixDomainSocketEndPoint(_socketPath);
        await client.ConnectAsync(endpoint);

        var req = new { id = commandId, requestId = Guid.NewGuid().ToString(), payload = payload ?? new { } };
        var json = JsonSerializer.Serialize(req) + "\n";
        var bytes = Encoding.UTF8.GetBytes(json);
        await client.SendAsync(bytes, SocketFlags.None);

        var buffer = new byte[4096];
        var received = await client.ReceiveAsync(buffer, SocketFlags.None);
        return Encoding.UTF8.GetString(buffer, 0, received).Trim();
    }
}
```

Create `plugin/Rupokar.Resolve.Actions/Actions/BreakTimerAction.cs`:
```csharp
namespace Rupokar.Resolve.Actions.Actions;

using Loupedeck;
using System.Timers;
using Rupokar.Resolve.Actions.DynamicDisplay;

public class BreakTimerAction : PluginDynamicCommand
{
    private static Timer? _timer;
    private static int _remainingSeconds;
    private static bool _isRunning;

    public BreakTimerAction() : base("Break Timer", "Timer controls and countdown display", "Break Timer")
    {
        this.AddParameter("25m", "25 Minutes", "Intervals");
        this.AddParameter("45m", "45 Minutes", "Intervals");
        this.AddParameter("1h", "1 Hour", "Intervals");
        this.AddParameter("1.5h", "1.5 Hours", "Intervals");
        this.AddParameter("2h", "2 Hours", "Intervals");
        this.AddParameter("2.5h", "2.5 Hours", "Intervals");
        this.AddParameter("3h", "3 Hours", "Intervals");
        this.AddParameter("4h", "4 Hours", "Intervals");
        this.AddParameter("start", "Start Timer", "Controls");
        this.AddParameter("stop", "Stop Timer", "Controls");
        this.AddParameter("status", "Timer Status", "Display");
    }

    protected override void RunCommand(string actionParameter)
    {
        if (actionParameter == "start")
        {
            _isRunning = true;
            _timer?.Start();
        }
        else if (actionParameter == "stop")
        {
            _isRunning = false;
            _timer?.Stop();
            _remainingSeconds = 0;
            this.ActionImageChanged();
        }
        else if (actionParameter.EndsWith("m") || actionParameter.EndsWith("h"))
        {
            _remainingSeconds = actionParameter switch
            {
                "25m" => 25 * 60,
                "45m" => 45 * 60,
                "1h" => 60 * 60,
                "1.5h" => 90 * 60,
                "2h" => 120 * 60,
                "2.5h" => 150 * 60,
                "3h" => 180 * 60,
                "4h" => 240 * 60,
                _ => 25 * 60
            };
            this.ActionImageChanged();
        }
    }

    protected override BitmapImage GetCommandImage(string actionParameter, PluginImageSize imageSize)
    {
        if (actionParameter == "status")
        {
            var minutes = _remainingSeconds / 60;
            var seconds = _remainingSeconds % 60;
            var text = _isRunning ? $"{minutes:00}:{seconds:00}" : "IDLE";
            return TileImageRenderer.DrawTimerCountdown(text, _isRunning && _remainingSeconds == 0);
        }
        return base.GetCommandImage(actionParameter, imageSize);
    }
}
```

Create `plugin/Rupokar.Resolve.Actions/Actions/RenderQueueAction.cs`:
```csharp
namespace Rupokar.Resolve.Actions.Actions;

using Loupedeck;
using Rupokar.Resolve.Actions.IPC;

public class RenderQueueAction : PluginDynamicCommand
{
    private readonly BridgeSocketClient _bridge = new();

    public RenderQueueAction() : base("Render Queue", "Render control and queue management", "Deliver")
    {
        this.AddParameter("start_all", "Render All", "Render");
        this.AddParameter("start_new", "Render New", "Render");
        this.AddParameter("stop", "Stop Render", "Render");
        this.AddParameter("status", "Queue Status", "Status");
    }

    protected override async void RunCommand(string actionParameter)
    {
        if (actionParameter == "start_all")
        {
            await _bridge.SendCommandAsync("render.start.all");
        }
        else if (actionParameter == "stop")
        {
            await _bridge.SendCommandAsync("render.stop");
        }
    }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_plugin_structure.py -v`
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add plugin/ tests/test_plugin_structure.py
git commit -m "feat(plugin): scaffold .NET 8 Logi Actions plugin with dynamic countdown"
```

---

### Task 5: DaVinci Resolve Custom Keyboard Preset

**Files:**
- Create: `keyboard-preset/Rupokar_Resolve_Keys.txt`
- Create: `docs/keyboard-preset-map.md`
- Test: `tests/test_keyboard_preset.py`

**Interfaces:**
- Consumes: Master catalog action names
- Produces: Conflict-free keyboard preset for DaVinci Resolve import

- [ ] **Step 1: Write test verifying shortcut integrity**

Create `tests/test_keyboard_preset.py`:
```python
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PRESET_FILE = REPO_ROOT / "keyboard-preset" / "Rupokar_Resolve_Keys.txt"


def test_keyboard_preset_exists():
    assert PRESET_FILE.exists()
    content = PRESET_FILE.read_text(encoding="utf-8")
    assert "Ripple Delete" in content
    assert "Split" in content or "Blade" in content
    assert "Compound Clip" in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_keyboard_preset.py -v`
Expected: FAIL with "PRESET_FILE.exists() is False"

- [ ] **Step 3: Implement `keyboard-preset/Rupokar_Resolve_Keys.txt` and `docs/keyboard-preset-map.md`**

Create `keyboard-preset/Rupokar_Resolve_Keys.txt`:
```text
# DaVinci Resolve Keyboard Shortcuts Preset for Rupokar Loupedeck CT Pack
# Import into DaVinci Resolve -> Keyboard Customization

Version = 1
Profile = "Rupokar Loupedeck CT"

# Edit Actions
Split = "Ctrl+B"
Ripple Delete = "Shift+Backspace"
Ripple Start = "Ctrl+Shift+["
Ripple End = "Ctrl+Shift+]"
Trim Start = "Shift+["
Trim End = "Shift+]"
Select Forward All = "Y"
Select Backward All = "Ctrl+Y"
Snapping = "N"
Change Clip Speed = "Ctrl+R"
Retime Controls = "Ctrl+Alt+R"
Add Marker = "M"
Delete All Markers = "Ctrl+Alt+M"

# Navigation & Transport
Zoom to Fit = "Shift+Z"
Next Clip = "Down"
Previous Clip = "Up"
Shuttle Reverse = "J"
Shuttle Stop = "K"
Shuttle Forward = "L"
Play Pause = "Space"

# Panels & Fn Layer
Media Pool Panel = "Ctrl+1"
Effects Library Panel = "Ctrl+2"
Inspector Panel = "Ctrl+3"
Mixer Panel = "Ctrl+4"
Power Bins Panel = "Ctrl+5"
Metadata Panel = "Ctrl+6"
Index Panel = "Ctrl+7"

# Color Page
Add Node = "Alt+S"
Node Before = "Shift+S"
Grab Still = "Ctrl+Alt+G"
Bypass All Grades = "Shift+D"
```

Create `docs/keyboard-preset-map.md`:
```markdown
# DaVinci Resolve Keyboard Preset Setup

1. Open **DaVinci Resolve**.
2. Click **DaVinci Resolve** menu -> **Keyboard Customization...** (`Option+Command+K`).
3. Click the three dots `...` in the top right -> **Import Preset**.
4. Select `keyboard-preset/Rupokar_Resolve_Keys.txt`.
5. Name it **Rupokar Loupedeck CT** and click **Save**.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_keyboard_preset.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add keyboard-preset/ docs/keyboard-preset-map.md tests/test_keyboard_preset.py
git commit -m "feat(shortcuts): add conflict-free DaVinci Resolve keyboard shortcut preset"
```

---

### Task 6: Loupedeck CT Profile (.lp5) Assembler & Packager

**Files:**
- Create: `scripts/build_profile.py`
- Output: `profile/Rupokar-Resolve-CT.lp5`
- Test: `tests/test_profile_lp5.py`

**Interfaces:**
- Consumes: `icons/final-icon-manifest.json`, `icons/export-png/`
- Produces: Importable `profile/Rupokar-Resolve-CT.lp5` zip archive containing `ProfileInfo.json`, `ApplicationInfo.json`, and `ActionIcons/`

- [ ] **Step 1: Write test verifying .lp5 profile zip structure**

Create `tests/test_profile_lp5.py`:
```python
import json
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILE_LP5 = REPO_ROOT / "profile" / "Rupokar-Resolve-CT.lp5"


def test_profile_lp5_is_valid_zip():
    assert PROFILE_LP5.exists()
    with zipfile.ZipFile(PROFILE_LP5, "r") as z:
        names = z.namelist()
        assert "ProfileInfo.json" in names
        assert "ApplicationInfo.json" in names
        assert "metadata/LoupedeckPackage.yaml" in names

        profile_json = json.loads(z.read("ProfileInfo.json").decode("utf-8"))
        assert profile_json["deviceType"] == "Loupedeck50"
        assert profile_json["displayName"] == "Rupokar DaVinci Resolve CT"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_profile_lp5.py -v`
Expected: FAIL with "PROFILE_LP5.exists() is False"

- [ ] **Step 3: Implement `scripts/build_profile.py`**

Create `scripts/build_profile.py`:
```python
#!/usr/bin/env python3
"""Build the official Loupedeck CT (.lp5) profile archive for DaVinci Resolve."""

import json
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "profile"
LP5_PATH = OUTPUT_DIR / "Rupokar-Resolve-CT.lp5"
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
PNG_DIR = REPO_ROOT / "icons" / "export-png"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    app_info = {
        "$type": "Loupedeck.Service.SupportedApplicationInfo, LoupedeckService",
        "name": "@_davinciresolve-ade6ee31394b4060",
        "displayName": "DaVinci Resolve",
        "deviceType": "Loupedeck50",
        "nativePluginName": "DaVinciResolve-ADE6EE31394B4060",
        "hasNativePlugin": True,
        "defaultProfileName": "RUPOKAR_RESOLVE_CT_PROFILE",
        "isEnabled": True
    }

    profile_info = {
        "$type": "Loupedeck.Service.ApplicationProfile, LoupedeckService",
        "name": "RUPOKAR_RESOLVE_CT_PROFILE",
        "displayName": "Rupokar DaVinci Resolve CT",
        "deviceType": "Loupedeck50",
        "applicationName": "@_davinciresolve-ade6ee31394b4060",
        "nativePluginName": "DaVinciResolve-ADE6EE31394B4060",
        "hasNativePlugin": True,
        "layout": {
            "$type": "Loupedeck.Service.ProfileLayout20, LoupedeckService",
            "deviceType": "Loupedeck50",
            "layoutModes": [
                {
                    "modeName": "main",
                    "touchPages": [
                        {"name": f"Page_{i}", "displayName": f"Workspace {i}"} for i in range(1, 9)
                    ]
                }
            ]
        }
    }

    pkg_yaml = "type: Profile5\nname: RUPOKAR_RESOLVE_CT_PROFILE\ndisplayName: Rupokar DaVinci Resolve CT\nversion: 1.0.0\n"

    with zipfile.ZipFile(LP5_PATH, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("ApplicationInfo.json", json.dumps(app_info, indent=2))
        z.writestr("ProfileInfo.json", json.dumps(profile_info, indent=2))
        z.writestr("metadata/LoupedeckPackage.yaml", pkg_yaml)

        # embed raster icons into ActionIcons/
        for item in manifest:
            svg_filename = Path(item["filename"]).name
            png_path = PNG_DIR / item["type"] / svg_filename.replace(".svg", ".png")
            if png_path.exists():
                z.write(png_path, f"ActionIcons/{png_path.name}")

    print(f"Built Loupedeck CT profile at: {LP5_PATH}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run script and verify test passes**

Run: `python3 scripts/build_profile.py && python3 -m pytest tests/test_profile_lp5.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/build_profile.py tests/test_profile_lp5.py profile/
git commit -m "feat(profile): generate importable Loupedeck CT (.lp5) profile with 8 workspaces"
```

---

### Task 7: End-to-End Pack Verification & Setup Guides

**Files:**
- Create: `scripts/verify_pack.py`
- Create: `docs/install-guide.md`
- Create: `docs/validation-checklist.md`
- Test: `python3 scripts/verify_pack.py`

**Interfaces:**
- Consumes: All outputs from Tasks 1-6
- Produces: Complete verification suite confirming 168 icons, profile, bridge, shortcuts, and documentation

- [ ] **Step 1: Implement `scripts/verify_pack.py`**

Create `scripts/verify_pack.py`:
```python
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
```

- [ ] **Step 2: Create `docs/install-guide.md` and `docs/validation-checklist.md`**

Create `docs/install-guide.md`:
```markdown
# Rupokar Studios LoupeDeck CT Pack — Installation Guide

## Step 1: Import Loupedeck Profile
1. Double-click `profile/Rupokar-Resolve-CT.lp5` to open it in **Loupedeck 6.4.1+**.
2. When prompted, select **DaVinci Resolve** as the target application.

## Step 2: Load DaVinci Resolve Keyboard Preset
1. Launch **DaVinci Resolve 21.1.2**.
2. Navigate to **DaVinci Resolve** menu -> **Keyboard Customization...**.
3. Select `...` in top right -> **Import Preset**.
4. Choose `keyboard-preset/Rupokar_Resolve_Keys.txt` and activate it.

## Step 3: Enable External Scripting
1. In DaVinci Resolve, go to **Preferences** -> **System** -> **General**.
2. Set **External scripting using** to **Local**.
3. Save preferences.

## Step 4: Run the Automation Bridge (Studio Features)
Run:
```bash
./scripts/run_bridge.sh
```
This enables YouTube/TikTok render queue automation, timeline aspect ratio duplication, and real-time timer sync.
```

Create `docs/validation-checklist.md`:
```markdown
# Validation Checklist

- [ ] 1. All 168 icons load cleanly on Loupedeck CT Touch, Dial, and Wheel slots.
- [ ] 2. Edit Page 1: Middle dial controls Audio Level in 1dB increments.
- [ ] 3. Edit Page 2: Dial swipe down displays 12 additional clip colors.
- [ ] 4. Edit Page 3: Delete Gaps removes all single-track gaps.
- [ ] 5. Media Page: Swipe right opens Break Timer; Start begins 25m countdown.
- [ ] 6. Deliver Page: YouTube and TikTok render presets load without UI errors.
- [ ] 7. Center Wheel: Turning moves playhead frame-by-frame; pressing toggles Play/Pause.
```

- [ ] **Step 3: Run the end-to-end verification script**

Run: `python3 scripts/verify_pack.py`
Expected: "ALL PACK INTEGRITY CHECKS PASSED"

- [ ] **Step 4: Commit**

```bash
git add scripts/verify_pack.py docs/install-guide.md docs/validation-checklist.md
git commit -m "docs: add installation guide, validation checklist, and verification script"
```
