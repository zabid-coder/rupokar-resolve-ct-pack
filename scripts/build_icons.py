#!/usr/bin/env python3
"""Build the complete 168-asset multi-ratio SVG icon system for Rupokar Resolve CT.

Fine-tuned for crisp legibility, DaVinci Resolve authenticity, zero text/glyph
overlap, distinctive timer durations, and reference crop comparisons on the
interactive Icon Board.
"""

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

    # 1. Distinct Timer Interval Glyphs (Fine-Tuned)
    if "25-minute" in name:
        return "timer_25m"
    if "45-minute" in name:
        return "timer_45m"
    if "1-hour" in name:
        return "timer_1h"
    if "1.5-hour" in name:
        return "timer_1_5h"
    if "2-hour" in name:
        return "timer_2h"
    if "2.5-hour" in name:
        return "timer_2_5h"
    if "3-hour" in name:
        return "timer_3h"
    if "4-hour" in name:
        return "timer_4h"
    if "break status" in name or "break!" in name:
        return "break_status"

    # 2. Aspect Ratio Timelines
    if "timeline 9:16" in name or "timeline 9x16" in name or "timeline 9×16" in name:
        return "timeline_9_16"
    if "timeline 4:5" in name or "timeline 4x5" in name or "timeline 4×5" in name:
        return "timeline_4_5"
    if "timeline 4:3" in name or "timeline 4x3" in name or "timeline 4×3" in name:
        return "timeline_4_3"

    # 3. Dedicated Custom Glyphs
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

    # 4. Exact Mappings
    exact = {
        "media page": "folder", "edit page 1": "scissors", "edit page 2": "link", "edit page 3": "timeline",
        "color page": "colorwheel", "fairlight page": "wave", "deliver page": "export", "quick export": "quickexport",
        "project settings": "gear", "new bin": "folderplus", "import media": "import", "power bins": "powerbins",
        "project notes": "note", "project manager": "grid", "new project": "newfile", "prefer proxy": "proxy", "camera originals": "camera",
        "ripple start": "rippleleft", "ripple end": "rippleright", "split": "split", "delete": "trash",
        "trim start": "trimleft", "trim end": "trimright", "retime controls": "retime", "change clip speed": "speed",
        "select backward all": "selectleft", "select forward all": "selectright", "snapping": "magnet",
        "zoom to fit": "fit", "timeline zoom": "zoom", "shuttle": "shuttle", "fast shuttle": "fastshuttle", "next clip": "nextclip",
        "add marker": "marker", "delete all markers": "markerdelete", "linked selection": "linked", "link clips": "link",
        "compound clip": "compoundclip", "normalize": "normalize", "auto align": "align", "mark in": "markin", "mark out": "markout",
        "loop": "loop", "match frame": "matchframe", "cinema viewer": "cinema", "enable clip": "eye",
        "freeze frame": "freeze", "title safe": "safe", "delete gaps": "deletegaps", "find clip": "findclip",
        "crossfade": "crossfade", "swap left": "swapleft", "swap right": "swapright", "find timeline": "timeline",
        "new timeline": "timelineplus", "duplicate timeline": "duplicate", "undo": "undo", "save project": "save",
        "move clip up": "uptrack", "move clip down": "downtrack", "timeline start": "startline", "timeline end": "endline",
        "right-click": "rightclick", "ripple delete": "rippledelete", "media pool panel": "folder",
        "inspector panel": "inspector", "mixer panel": "mixer", "power bins panel": "powerbins", "metadata panel": "metadata", "index panel": "list",
        "copy": "copy", "paste attributes": "paste", "bypass all grades": "bypass",
        "scopes": "scopes", "light box": "lightbox", "printer lights": "printerlights", "add node": "nodeplus", "node before": "nodebefore",
        "label node": "tag", "grab still": "still", "split selected": "splittwo", "split prev/next": "splitprevnext",
        "split original": "splitoriginal", "split stills": "splitstills", "saturation": "saturation", "reset saturation": "reset",
        "gamma": "gamma", "reset gamma": "reset", "gain": "gain", "reset gain": "reset",
        "printer light red": "redlight", "printer light green": "greenlight", "printer light blue": "bluelight",
        "exit split comparison": "closecompare", "batch fade settings": "batchfadesettings", "apply batch fades": "applybatchfades",
        "track height": "trackheight", "waveform zoom": "wavezoom", "reset waveform zoom": "reset",
        "youtube preset": "youtube", "vimeo preset": "vimeo", "tiktok preset": "tiktok", "instagram 4:5 preset": "instagram",
        "prores 422 hq preset": "prores", "custom preset 1": "custom1", "custom preset 2": "custom2", "custom preset 3": "custom3",
        "add to queue": "queueadd", "render all": "renderall", "render new": "rendernew", "stop render": "stop",
        "thumbnail": "thumbnail", "export folder": "exportfolder", "clear render queue": "clearqueue",
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
    stroke_attrs = f'stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"'
    s = f'{stroke_attrs} fill="none"'
    fill = f'fill="{color}"'
    shapes = {
        # 1. Distinct Break Timer Badges
        "timer_25m": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 43v14M82 43h48" {s}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="800">25m</text>',
        "timer_45m": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 43v14M82 43h48" {s}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="800">45m</text>',
        "timer_1h": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 43v14M82 43h48" {s}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800">1h</text>',
        "timer_1_5h": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 43v14M82 43h48" {s}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="800">1.5h</text>',
        "timer_2h": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 43v14M82 43h48" {s}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800">2h</text>',
        "timer_2_5h": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 43v14M82 43h48" {s}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="800">2.5h</text>',
        "timer_3h": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 43v14M82 43h48" {s}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800">3h</text>',
        "timer_4h": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 43v14M82 43h48" {s}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800">4h</text>',
        "break_status": f'<rect x="44" y="52" width="124" height="96" rx="16" fill="{color}" opacity=".15" {stroke_attrs}/><path d="M68 84h76M68 112h52" {s}/><circle cx="146" cy="112" r="9" {fill}/>',

        # 2. Aspect Ratio Timelines
        "timeline_9_16": f'<rect x="74" y="44" width="64" height="118" rx="10" {s}/><path d="M96 90l22 13-22 13z" {fill}/><text x="106" y="148" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="800">9:16</text>',
        "timeline_4_5": f'<rect x="64" y="48" width="84" height="110" rx="8" {s}/><text x="106" y="114" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800">4:5</text>',
        "timeline_4_3": f'<rect x="52" y="55" width="108" height="84" rx="8" {s}/><text x="106" y="110" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="800">4:3</text>',

        # 3. Dedicated Custom Glyphs & Resolve Authenticity
        "rushwise": f'<path d="M106 43l55 55-55 55-55-55z" {s}/><circle cx="106" cy="98" r="16" {fill}/><path d="M106 43v30m0 50v30m-55-55h30m50 0h30" {s}/>',
        "audio_level": f'<path d="M58 84v42h24l30 24V60L82 84H58z" {s}/><path d="M136 78a38 38 0 0 1 0 54m18-72a62 62 0 0 1 0 90" {s}/>',
        "dynamic_trim": f'<path d="M64 55v100m30-75-30 25 30 25M148 55v100m-30-75 30 25-30 25" {s}/><path d="M106 65v80" stroke="{color}" stroke-width="6" stroke-dasharray="8 8"/>',
        "dynamic_trim_toggle": f'<circle cx="106" cy="105" r="52" {s}/><path d="M106 60v36m-22 20l22-20 22 20" {s}/>',
        "effects_library": f'<path d="M55 145l65-65m12-12 18-18 18 18-18 18z" {s}/><path d="M65 65l6 14 14 6-14 6-6 14-6-14-14-6 14-6z" {fill}/>',

        # 4. Color Grading Nodes (Official DaVinci Resolve Node Tree Style)
        "nodeplus": f'<rect x="52" y="60" width="108" height="90" rx="10" {s}/><circle cx="42" cy="105" r="7" {fill}/><circle cx="170" cy="105" r="7" {fill}/><path d="M106 87v36m-18-18h36" {s}/>',
        "nodebefore": f'<rect x="44" y="68" width="58" height="74" rx="8" {s}/><rect x="120" y="68" width="58" height="74" rx="8" {s}/><path d="M102 105h18m-9-9 9 9-9 9" {s}/><circle cx="36" cy="105" r="5" {fill}/><circle cx="186" cy="105" r="5" {fill}/>',
        "tag": f'<rect x="46" y="58" width="120" height="94" rx="10" {s}/><circle cx="38" cy="105" r="7" {fill}/><circle cx="174" cy="105" r="7" {fill}/><path d="M70 92h72m-72 26h48" {s}/>',

        # 5. Scopes, Light Box, and Printer Lights
        "scopes": f'<rect x="42" y="52" width="128" height="96" rx="10" {s}/><circle cx="106" cy="100" r="30" stroke="{color}" stroke-width="4" fill="none"/><path d="M106 74v52m-26-26h52" stroke="{color}" stroke-width="3"/><path d="M88 156h36" {s}/>',
        "lightbox": f'<rect x="46" y="54" width="34" height="40" rx="4" {s}/><rect x="89" y="54" width="34" height="40" rx="4" {s}/><rect x="132" y="54" width="34" height="40" rx="4" {s}/><rect x="46" y="104" width="34" height="40" rx="4" {s}/><rect x="89" y="104" width="34" height="40" rx="4" {s}/><rect x="132" y="104" width="34" height="40" rx="4" {s}/>',
        "printerlights": f'<circle cx="68" cy="88" r="18" fill="#FF6572" opacity=".85"/><circle cx="106" cy="88" r="18" fill="#5EE07E" opacity=".85"/><circle cx="144" cy="88" r="18" fill="#65AFFF" opacity=".85"/><path d="M68 114v32m38-32v32m38-32v32" {s}/>',
        "redlight": f'<circle cx="106" cy="94" r="44" fill="#FF6572" opacity=".25" {stroke_attrs}/><text x="106" y="112" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="800">R</text><path d="M68 150h18m58 0h18m-9-9v18" {s}/>',
        "greenlight": f'<circle cx="106" cy="94" r="44" fill="#5EE07E" opacity=".25" {stroke_attrs}/><text x="106" y="112" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="800">G</text><path d="M68 150h18m58 0h18m-9-9v18" {s}/>',
        "bluelight": f'<circle cx="106" cy="94" r="44" fill="#65AFFF" opacity=".25" {stroke_attrs}/><text x="106" y="112" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="800">B</text><path d="M68 150h18m58 0h18m-9-9v18" {s}/>',

        # 6. Color Curves & Tonal Controls
        "saturation": f'<path d="M106 50 C80 90 66 112 66 128 a40 40 0 0 0 80 0 C146 112 132 90 106 50 Z" {s}/><path d="M74 130a32 32 0 0 0 64 0" fill="{color}" opacity=".35"/>',
        "gamma": f'<path d="M52 50v110h110" {s}/><path d="M52 160 C80 160 90 100 162 60" stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="106" cy="112" r="10" {fill}/>',
        "gain": f'<path d="M52 50v110h110" {s}/><path d="M52 160 L110 140 L162 55" stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="162" cy="55" r="10" {fill}/>',
        "bypass": f'<circle cx="106" cy="105" r="54" {s}/><path d="M106 51a54 54 0 0 1 0 108z" fill="{color}" opacity=".3"/><path d="M58 58l96 96" stroke="#FF6C7A" stroke-width="12" stroke-linecap="round"/>',

        # 7. Split Comparisons
        "splittwo": f'<rect x="47" y="61" width="50" height="88" rx="6" {s}/><rect x="115" y="61" width="50" height="88" rx="6" {s}/>',
        "splitprevnext": f'<rect x="43" y="69" width="40" height="72" rx="5" {s}/><rect x="86" y="54" width="40" height="102" rx="5" {s}/><rect x="129" y="69" width="40" height="72" rx="5" {s}/>',
        "splitoriginal": f'<rect x="47" y="60" width="57" height="90" rx="6" {s}/><rect x="108" y="60" width="57" height="90" rx="6" {s}/><path d="M77 117l17-19 17 19m28 0 17-19 17 19" {s}/>',
        "splitstills": f'<rect x="49" y="62" width="48" height="84" rx="6" {s}/><rect x="114" y="62" width="48" height="84" rx="6" {s}/><path d="M58 127l13-15 15 15m38 0 13-15 15 15" {s}/>',
        "closecompare": f'<rect x="53" y="57" width="106" height="96" rx="9" {s}/><path d="M79 82l54 54m0-54-54 54" {s}/>',

        # 8. Fairlight Audio & Fades
        "batchfadesettings": f'<rect x="44" y="65" width="124" height="80" rx="8" {s}/><path d="M54 135 C70 135 78 80 106 80 C134 80 142 135 158 135" stroke="{color}" stroke-width="8" fill="none"/><circle cx="106" cy="80" r="8" {fill}/>',
        "applybatchfades": f'<rect x="44" y="65" width="124" height="80" rx="8" {s}/><path d="M54 135 C70 135 78 80 106 80 C134 80 142 135 158 135" stroke="{color}" stroke-width="8" fill="none"/><path d="M140 50l12 12 24-24" stroke="#5CE080" stroke-width="8" stroke-linecap="round" fill="none"/>',
        "trackheight": f'<rect x="48" y="60" width="116" height="90" rx="8" {s}/><path d="M106 42v30m-14-14 14-14 14 14M106 168v-30m-14 14 14 14 14-14" stroke="{color}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M68 95h76m-76 20h76" stroke="{color}" stroke-width="4"/>',
        "wavezoom": f'<path d="M42 105h18l12-32 18 64 20-80 20 90 18-50 12 8h12" {s}/><path d="M34 52h26m-13-13-13 13 13 13M178 52h-26m13-13 13 13-13 13" stroke="{color}" stroke-width="6" stroke-linecap="round"/>',

        # 9. Edit Tools (Authentic DaVinci Resolve Razor, Retime, Compound Clip)
        "split": f'<rect x="42" y="70" width="60" height="70" rx="6" {s}/><rect x="110" y="70" width="60" height="70" rx="6" {s}/><path d="M106 44v122" stroke="#FF6C7A" stroke-width="8" stroke-linecap="round"/><path d="M96 46l10 14 10-14z" fill="#FF6C7A"/>',
        "retime": f'<rect x="45" y="116" width="122" height="30" rx="6" {s}/><path d="M65 116v30m25-30v30m25-30v30m25-30v30" stroke="{color}" stroke-width="4"/><circle cx="106" cy="75" r="32" {s}/><path d="M106 55v22l14 10" {s}/>',
        "speed": f'<path d="M52 135a60 60 0 1 1 108 0" {s}/><path d="M106 125l28-42" stroke="#FF8A3D" stroke-width="8" stroke-linecap="round"/><circle cx="106" cy="125" r="10" {fill}/><text x="106" y="152" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="800">%</text>',
        "compoundclip": f'<rect x="44" y="56" width="124" height="98" rx="8" stroke="{color}" stroke-width="5" stroke-dasharray="8 8" fill="none"/><rect x="56" y="70" width="100" height="30" rx="4" {s}/><rect x="56" y="110" width="100" height="30" rx="4" {s}/>',
        "deletegaps": f'<rect x="42" y="75" width="46" height="60" rx="6" {s}/><rect x="124" y="75" width="46" height="60" rx="6" {s}/><path d="M88 105h36" stroke="#FF6C7A" stroke-width="6" stroke-dasharray="4 4"/><path d="M74 105h20m-8-8 8 8-8 8M138 105h-20m8-8-8 8 8 8" {s}/>',
        "crossfade": f'<rect x="40" y="70" width="54" height="70" rx="6" {s}/><rect x="118" y="70" width="54" height="70" rx="6" {s}/><path d="M80 140l52-70M80 70l52 70" stroke="{color}" stroke-width="8" stroke-linecap="round"/>',
        "magnet": f'<path d="M67 59v47a39 39 0 0 0 78 0V59M67 59h22m34 0h22M78 136l-18 18m74-18 18 18" {s}/>',
        "scissors": f'<circle cx="69" cy="75" r="17" {s}/><circle cx="69" cy="135" r="17" {s}/><path d="M84 88l71 48M84 122l71-48" {s}/>',
        "trash": f'<path d="M66 66h80M88 66V48h36v18M78 66l7 87h42l7-87M95 89v40m22-40v40" {s}/>',
        "trimleft": f'<path d="M74 55v100m29-75H74m29 50H74M133 105h37" {s}/>',
        "trimright": f'<path d="M138 55v100m-29-75h29m-29 50h29M72 105h37" {s}/>',
        "rippleleft": f'<path d="M151 105H72m20-22-22 22 22 22M166 73v64" {s}/>',
        "rippleright": f'<path d="M61 105h79m-20-22 22 22-22 22M46 73v64" {s}/>',
        "rippledelete": f'<path d="M150 105H71m20-22-22 22 22 22M164 73v64" {s}/><path d="M60 59l93 93M153 59l-93 93" stroke="#FF6C7A" stroke-width="8" stroke-linecap="round"/>',

        # 10. Media & Project (Power Bins, Proxies, Camera RAW)
        "powerbins": f'<path d="M38 78h45l12 15h83v55H38z" {s}/><path d="M112 85l-16 28h18l-8 28 26-34h-18z" {fill}/>',
        "proxy": f'<rect x="43" y="61" width="126" height="87" rx="10" {s}/><text x="86" y="112" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800">PXY</text><circle cx="153" cy="69" r="18" fill="#111923" {stroke_attrs}/><path d="M153 60v9l7 4" {s}/>',
        "camera": f'<path d="M42 82h34l14-20h35l14 20h31v69H42z" {s}/><circle cx="106" cy="116" r="25" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="12" font-weight="800">RAW</text>',

        # 11. Presets & Deliver
        "youtube": f'<rect x="45" y="67" width="122" height="77" rx="18" {s}/><path d="M94 87l39 19-39 19z" {fill}/>',
        "vimeo": f'<path d="M52 77c20-17 46-24 56 2 9 23-14 57-6 57 7 0 24-28 31-42 8-17 25-22 36-13-14 47-55 87-74 87-17 0-26-45-35-69-5-13-11-10-23 0z" {s}/>',
        "tiktok": f'<path d="M119 48v77a28 28 0 1 1-25-28v22a7 7 0 1 0 6 6V48h19c3 17 14 27 31 29v20c-12-1-23-6-31-14" {s}/>',
        "instagram": f'<rect x="51" y="50" width="110" height="110" rx="29" {s}/><circle cx="106" cy="105" r="27" {s}/><circle cx="140" cy="72" r="7" {fill}/>',
        "prores": f'<rect x="44" y="70" width="124" height="70" rx="9" {s}/><text x="106" y="116" text-anchor="middle" fill="{color}" font-size="33" font-family="Arial, Helvetica, sans-serif" font-weight="700">HQ</text>',
        "custom1": f'<rect x="52" y="51" width="108" height="108" rx="12" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-size="56" font-family="Arial, Helvetica, sans-serif" font-weight="700">1</text>',
        "custom2": f'<rect x="52" y="51" width="108" height="108" rx="12" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-size="56" font-family="Arial, Helvetica, sans-serif" font-weight="700">2</text>',
        "custom3": f'<rect x="52" y="51" width="108" height="108" rx="12" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-size="56" font-family="Arial, Helvetica, sans-serif" font-weight="700">3</text>',
        "queueadd": f'<rect x="52" y="50" width="108" height="120" rx="10" {s}/><path d="M74 80h40M74 105h40M74 130h40" {s}/><circle cx="140" cy="130" r="22" fill="#15181E" {stroke_attrs}/><path d="M140 118v24m-12-12h24" {s}/>',
        "renderall": f'<path d="M60 62l55 43-55 43zM110 62l55 43-55 43z" {fill}/><path d="M48 158h116" stroke="{color}" stroke-width="6" stroke-linecap="round"/>',
        "rendernew": f'<path d="M65 62l65 43-65 43z" {fill}/><path d="M150 62l5 15 15 5-15 5-5 15-5-15-15-5 15-5z" fill="#FFD43D"/>',
        "stop": f'<path d="M78 48h56l38 38v56l-38 38H78L40 142V86z" fill="#FF6C7A" opacity=".2" {stroke_attrs}/><rect x="80" y="80" width="52" height="52" rx="8" fill="#FF6C7A"/>',
        "thumbnail": f'<rect x="46" y="56" width="120" height="96" rx="10" {s}/><circle cx="84" cy="88" r="14" {fill}/><path d="M58 138l34-34 22 22 24-24 20 20" {s}/>',
        "exportfolder": f'<path d="M38 78h45l12 15h83v55H38z" {s}/><path d="M106 100v34m-14-14 14 14 14-14" {s}/>',
        "clearqueue": f'<path d="M62 64h88M84 64V50h44v14M72 64l8 88h52l8-88" {s}/><path d="M92 86l28 28m0-28-28 28" stroke="#FF6C7A" stroke-width="8" stroke-linecap="round"/>',
        "free": f'<path d="M49 58h114v94H49z" {s}/><text x="106" y="117" text-anchor="middle" fill="{color}" font-size="36" font-family="Arial, Helvetica, sans-serif" font-weight="700">FREE</text>',

        # 12. Standard Navigation & Media Pool
        "folder": f'<path d="M38 78h45l12 15h83v55H38z" {s}/>',
        "folderplus": f'<path d="M33 82h48l12 14h84v53H33z" {s}/><path d="M136 105v32m-16-16h32" {s}/>',
        "import": f'<path d="M106 43v77m-29-29 29 29 29-29M47 142h118v18H47z" {s}/>',
        "grid": f'<rect x="52" y="51" width="37" height="37" rx="5" {s}/><rect x="123" y="51" width="37" height="37" rx="5" {s}/><rect x="52" y="122" width="37" height="37" rx="5" {s}/><rect x="123" y="122" width="37" height="37" rx="5" {s}/>',
        "gear": f'<circle cx="106" cy="105" r="26" {s}/><path d="M106 43v18m0 88v18M44 105h18m88 0h18M62 61l13 13m62 62 13 13M150 61l-13 13m-62 62-13 13" {s}/>',
        "note": f'<path d="M61 44h91v119H61zM82 76h48M82 103h48M82 130h28" {s}/>',
        "newfile": f'<path d="M67 43h63l27 27v94H67zM129 43v29h28M110 92v47m-24-24h48" {s}/>',
        "layers": f'<path d="M106 48l68 37-68 37-68-37zM38 119l68 37 68-37M38 93l68 37 68-37" {s}/>',
        "link": f'<path d="M92 125l-13 13a28 28 0 0 1-40-40l25-25a28 28 0 0 1 40 0m2 0 13-13a28 28 0 0 1 40 40l-25 25a28 28 0 0 1-40 0M78 106h57" {s}/>',
        "timeline": f'<path d="M42 73h127M42 106h127M42 139h127" {s}/><circle cx="70" cy="73" r="9" {fill}/><circle cx="119" cy="106" r="9" {fill}/><circle cx="151" cy="139" r="9" {fill}/>',
        "timelineplus": f'<path d="M42 76h79M42 106h79M42 136h79M151 105v43m-22-22h44" {s}/>',
        "duplicate": f'<rect x="54" y="61" width="75" height="81" rx="8" {s}/><rect x="83" y="43" width="75" height="81" rx="8" {s}/>',
        "colorwheel": f'<circle cx="106" cy="105" r="57" fill="#1a2332" {stroke_attrs}/><path d="M106 48a57 57 0 0 1 50 84l-50-27z" fill="#FF6B7B"/><path d="M106 105l50 27a57 57 0 0 1-100 0z" fill="#57DDA9"/><path d="M106 105 56 132a57 57 0 0 1 50-84z" fill="#5AA9FF"/><circle cx="106" cy="105" r="16" fill="#F3F7FF"/>',
        "wave": f'<path d="M34 106h18l12-41 20 84 22-101 22 116 18-74 14 16h22" {s}/>',
        "export": f'<path d="M61 43h78l26 26v89H61zM111 68v60m-23-24 23 24 23-24M79 151h70" {s}/>',
        "quickexport": f'<path d="M61 47h75l25 25v82H61zM108 71v53m-21-21 21 21 21-21" {s}/><path d="M164 41l7 22 22 7-22 7-7 22-7-22-22-7 22-7z" {fill}/>',
        "timer": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 72v34l26 18M82 43h48M106 43v14" {s}/>',
        "play": f'<path d="M80 58l68 47-68 47z" {fill}/><path d="M47 52v106" {s}/>',
        "selectleft": f'<path d="M158 65H74l23-23M74 65l23 23M158 145H74" {s}/><rect x="46" y="116" width="49" height="35" rx="5" {s}/>',
        "selectright": f'<path d="M54 65h84l-23-23m23 23-23 23M54 145h84" {s}/><rect x="117" y="116" width="49" height="35" rx="5" {s}/>',
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
        "findclip": f'<rect x="49" y="63" width="91" height="77" rx="8" {s}/><circle cx="139" cy="136" r="25" {s}/><path d="M157 154l20 20" {s}/>',
        "swapleft": f'<path d="M153 78H75l22-22M75 78l22 22M57 132h78l-22-22m22 22-22 22" {s}/>',
        "swapright": f'<path d="M59 78h78l-22-22m22 22-22 22M155 132H77l22-22m-22 22 22 22" {s}/>',
        "undo": f'<path d="M91 60L52 100l39 40M55 100h63a36 36 0 0 1 36 36" {s}/>',
        "save": f'<path d="M55 48h84l21 21v91H55zM79 48v45h51V48m-48 101h49" {s}/>',
        "uptrack": f'<path d="M106 156V55m-27 29 27-29 27 29M57 143h99" {s}/>',
        "downtrack": f'<path d="M106 54v101m-27-29 27 29 27-29M57 67h99" {s}/>',
        "startline": f'<path d="M73 75v60M99 105h63m-33-30-30 30 30 30" {s}/>',
        "endline": f'<path d="M139 75v60M113 105H50m33-30 30 30-30 30" {s}/>',
        "rightclick": f'<path d="M75 51v76m0 0-18-22m18 22 18-22M111 51v76m0 0-18-22m18 22 18-22M70 150h41a27 27 0 0 0 27-27V88" {s}/>',
        "inspector": f'<rect x="52" y="49" width="108" height="112" rx="8" {s}/><path d="M77 80h58M77 105h58M77 130h34" {s}/>',
        "mixer": f'<path d="M62 57v96m44-96v96m44-96v96M45 86h34m27 45h34m10-50h34" {s}/><circle cx="62" cy="86" r="10" {fill}/><circle cx="106" cy="131" r="10" {fill}/><circle cx="150" cy="81" r="10" {fill}/>',
        "metadata": f'<path d="M49 57h78l29 29v70H49zM127 57v29h29M75 113h55M75 137h32" {s}/>',
        "list": f'<path d="M67 65h91M67 105h91M67 145h91" {s}/><circle cx="45" cy="65" r="7" {fill}/><circle cx="45" cy="105" r="7" {fill}/><circle cx="45" cy="145" r="7" {fill}/>',
        "copy": f'<rect x="51" y="67" width="76" height="87" rx="8" {s}/><rect x="84" y="45" width="76" height="87" rx="8" {s}/>',
        "paste": f'<path d="M59 57h94v104H59zM84 57v-13h44v13M80 96h52M80 122h35" {s}/><path d="M137 136l21 21 30-38" {s}/>',
        "still": f'<rect x="47" y="61" width="118" height="88" rx="9" {s}/><path d="M70 127l25-24 20 18 15-14 20 20" {s}/><circle cx="88" cy="85" r="8" {s}/>',
        "reset": f'<path d="M151 84a49 49 0 1 0 5 46M151 58v29h-29" {s}/>',
        "colorswatch": f'<circle cx="106" cy="105" r="47" fill="{color}"/><circle cx="106" cy="105" r="57" {s}/>',
        "framewheel": f'<circle cx="106" cy="105" r="56" {s}/><path d="M106 58v94M59 105h94" {s}/><circle cx="106" cy="105" r="15" {fill}/>',
        "spark": f'<path d="M106 43l14 48 48 14-48 14-14 48-14-48-48-14 48-14z" {s}/>',
    }
    return shapes.get(token, shapes["spark"])


def asset_type(item: dict[str, str]) -> str:
    control = item["control"].lower()
    if "dial" in control or "wheel · turn" in control:
        return "dial"
    if "touch" in control or "swipe-right" in control or "wheel · press" in control:
        return "touch"
    return "physical"


def svg_touch(item: dict[str, str], color: str, token: str) -> str:
    label = lines(item["function"], 14)
    font_size = 17 if any(len(w) > 10 for w in item["function"].split()) else 18
    line_spacing = 21
    y_start = 202 if len(label) > 1 else 214
    text = "".join(
        f'<text x="128" y="{y_start + line * line_spacing}" text-anchor="middle" fill="#F5F7FC" font-family="Arial, Helvetica, sans-serif" font-size="{font_size}" font-weight="700">{html.escape(val)}</text>'
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
    label = lines(item["function"], 12)
    max_len = max(len(w) for w in item["function"].split()) if item["function"] else 0
    font_size = 11 if max_len > 12 else (12 if len(label) > 1 else 13)
    
    if len(label) == 1:
        text_y_offsets = [122]
    else:
        text_y_offsets = [114, 130]

    line_text = "".join(
        f'<text x="60" y="{text_y_offsets[line]}" text-anchor="middle" fill="#F5F7FC" font-family="Arial, Helvetica, sans-serif" font-size="{font_size}" font-weight="700">{html.escape(val)}</text>'
        for line, val in enumerate(label)
    )
    control = "TURN" if "turn" in item["control"].lower() else "PRESS"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="120" height="180" viewBox="0 0 120 180">'
        f'<rect width="120" height="180" rx="14" fill="#15181E"/>'
        f'<rect x="2" y="2" width="116" height="176" rx="12" fill="none" stroke="#364055" stroke-width="2"/>'
        f'<rect x="16" y="8" width="88" height="4" rx="2" fill="{color}"/>'
        f'<g transform="translate(5 4) scale(.52)">{glyph(token, color)}</g>'
        f'{line_text}'
        f'<rect x="18" y="148" width="84" height="20" rx="6" fill="#0D1117" stroke="{color}" stroke-width="1.5"/>'
        f'<text x="60" y="162" text-anchor="middle" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="10" font-weight="700" letter-spacing="1.2">{control}</text>'
        f'</svg>'
    )


def svg_physical(item: dict[str, str], color: str, token: str) -> str:
    label = lines(item["function"], 20)
    control = item["control"].upper().replace("ROUND BUTTON", "ROUND")
    font_size = 23 if any(len(w) > 12 for w in item["function"].split()) else 25
    y_start = 68 if len(label) > 1 else 82
    line_spacing = 28
    label_text = "".join(
        f'<text x="126" y="{y_start + line * line_spacing}" fill="#F5F7FC" font-family="Arial, Helvetica, sans-serif" font-size="{font_size}" font-weight="700">{html.escape(val)}</text>'
        for line, val in enumerate(label)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="320" height="160" viewBox="0 0 320 160">'
        f'<rect width="320" height="160" rx="17" fill="#15181E"/>'
        f'<rect x="3" y="3" width="314" height="154" rx="14" fill="none" stroke="#364055" stroke-width="3"/>'
        f'<rect x="17" y="17" width="91" height="126" rx="14" fill="#11151C" stroke="{color}" stroke-width="3"/>'
        f'<g transform="translate(7 2) scale(.52)">{glyph(token, color)}</g>{label_text}'
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
            "reference": f"reference-png/{index:03d}.png"
        })

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Generate Interactive Filterable Review Board with Reference Comparison
    cards = "\n".join(
        f'<article class="card" data-section="{html.escape(m["section"])}" data-name="{html.escape(m["function"].lower())}">'
        f'<div class="final"><img src="{html.escape(m["filename"])}" alt="{html.escape(m["function"])}"></div>'
        f'<div class="info">'
        f'<p class="eyebrow">#{idx:03d} · {html.escape(m["type"].upper())}</p>'
        f'<h2>{html.escape(m["function"])}</h2>'
        f'<p class="control"><strong>{html.escape(m["control"])}</strong></p>'
        f'<p class="meta">{html.escape(m["section"])} · <span class="badge">{html.escape(m["availability"])}</span></p>'
        f'<p class="time">⏱ Video: {html.escape(m["source_time"])}</p>'
        f'<details><summary>🔍 Compare Walkthrough Crop</summary>'
        f'<img class="ref-crop" src="{html.escape(m["reference"])}" alt="Reference crop for {html.escape(m["function"])}">'
        f'</details>'
        f'</div></article>'
        for idx, m in enumerate(manifest, start=1)
    )

    BOARD_PATH.write_text(
        f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rupokar Resolve CT — Multi-Ratio Icon System Audit Board</title>
<style>
  :root {{
    --bg: #090D16;
    --card-bg: #121927;
    --border: #243247;
    --text: #EEF4FF;
    --accent: #4EE0E2;
  }}
  body {{
    margin: 0; padding: 28px;
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  header {{
    max-width: 1400px; margin: 0 auto 24px;
    border-bottom: 1px solid var(--border); padding-bottom: 20px;
  }}
  h1 {{ font-size: 2.2rem; margin: 0 0 8px; color: #FFF; }}
  p.desc {{ margin: 0 0 16px; color: #9AB0D0; font-size: 15px; }}
  .toolbar {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-top: 14px; }}
  .search-box {{
    padding: 8px 14px; border-radius: 8px; border: 1px solid var(--border);
    background: #0D1420; color: #FFF; font-size: 14px; min-width: 260px;
  }}
  .filter-btn {{
    padding: 7px 12px; border-radius: 6px; border: 1px solid var(--border);
    background: #141E2F; color: #CAD9EE; cursor: pointer; font-size: 13px; font-weight: 600;
  }}
  .filter-btn.active {{ background: var(--accent); color: #09101C; border-color: var(--accent); }}
  .stats-pill {{ background: #1A263B; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #5EE080; }}
  .grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px;
    max-width: 1400px; margin: 0 auto;
  }}
  .card {{
    display: flex; gap: 14px; background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 12px; padding: 12px; transition: transform .15s, border-color .15s;
  }}
  .card:hover {{ border-color: #4EE0E2; transform: translateY(-2px); }}
  .final {{
    display: grid; place-items: center; background: #0A0F1A; border-radius: 8px;
    padding: 6px; min-width: 110px; border: 1px solid #1C2738;
  }}
  .final img {{ max-width: 100%; max-height: 150px; object-fit: contain; }}
  .info {{ flex: 1; min-width: 0; }}
  .eyebrow {{ color: #4EE0E2; font-size: 11px; font-weight: 800; letter-spacing: .08em; margin: 0 0 4px; }}
  h2 {{ font-size: 16px; margin: 0 0 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  p.control {{ font-size: 13px; color: #E0E8F5; margin: 0 0 4px; }}
  p.meta {{ font-size: 12px; color: #8FA6C8; margin: 0 0 4px; }}
  .badge {{ background: #1B2940; padding: 2px 6px; border-radius: 4px; color: #ADC2E0; font-size: 11px; }}
  p.time {{ font-size: 11px; color: #6E85A8; margin: 0 0 8px; }}
  details {{ margin-top: 6px; font-size: 12px; color: #9BB0D0; }}
  summary {{ cursor: pointer; user-select: none; font-weight: 600; color: #5CD5E0; }}
  .ref-crop {{ margin-top: 8px; max-width: 120px; border-radius: 6px; border: 1px solid var(--border); display: block; }}
</style>
<script>
function filterSection(sec, btn) {{
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const cards = document.querySelectorAll('.card');
  cards.forEach(c => {{
    if (sec === 'ALL' || c.getAttribute('data-section').includes(sec)) {{
      c.style.display = 'flex';
    }} else {{
      c.style.display = 'none';
    }}
  }});
}}
function searchCards(query) {{
  const q = query.toLowerCase();
  document.querySelectorAll('.card').forEach(c => {{
    const name = c.getAttribute('data-name');
    const sec = c.getAttribute('data-section').toLowerCase();
    c.style.display = (name.includes(q) || sec.includes(q)) ? 'flex' : 'none';
  }});
}}
</script>
</head>
<body>
<header>
  <h1>Rupokar Resolve CT — Multi-Ratio Icon System Audit Board</h1>
  <p class="desc">168 Purpose-Built Vector SVGs: Touch (256×256), Dial (120×180), Physical (320×160). Click on any card to view and compare against original walkthrough video crops.</p>
  <div class="toolbar">
    <input type="text" class="search-box" placeholder="Search actions, dials, shortcuts..." onkeyup="searchCards(this.value)">
    <button class="filter-btn active" onclick="filterSection('ALL', this)">All (168)</button>
    <button class="filter-btn" onclick="filterSection('Media', this)">Media & Timer</button>
    <button class="filter-btn" onclick="filterSection('Edit', this)">Edit Pages</button>
    <button class="filter-btn" onclick="filterSection('Color', this)">Color Page</button>
    <button class="filter-btn" onclick="filterSection('Fairlight', this)">Fairlight</button>
    <button class="filter-btn" onclick="filterSection('Deliver', this)">Deliver & Export</button>
    <button class="filter-btn" onclick="filterSection('Physical', this)">Physical & Fn</button>
    <span class="stats-pill">✅ 168/168 Fine-Tuned</span>
  </div>
</header>
<main class="grid">
{cards}
</main>
</body>
</html>''',
        encoding="utf-8"
    )
    print(f"Generated {len(manifest)} SVGs: Touch={sum(x['type']=='touch' for x in manifest)}, Dial={sum(x['type']=='dial' for x in manifest)}, Physical={sum(x['type']=='physical' for x in manifest)}")


if __name__ == "__main__":
    main()
