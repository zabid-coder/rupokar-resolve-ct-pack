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
    "Navigation": "#38BDF8",           # Electric Sky Blue / Cyan
    "Media / Project": "#A855F7",      # Vibrant Purple
    "Media / Break Timer": "#2DD4BF",  # Bright Teal / Aqua
    "Edit 1": "#3B82F6",               # Vivid Royal Blue
    "Edit 2": "#60A5FA",               # Crisp Electric Blue
    "Edit 3": "#818CF8",               # Indigo / Lavender Blue
    "Physical keys & Fn layer": "#94A3B8", # Sleek Cool Silver
    "Color": "#F59E0B",                # Luminous Golden Amber
    "Fairlight": "#10B981",            # Vivid Emerald Green
    "Deliver / Render Queue": "#EC4899", # Bright Magenta / Hot Pink
    "Quick Export": "#EC4899",         # Bright Magenta
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


def lines(text: str, max_chars: int = 18) -> list[str]:
    text = text.replace(" / ", " ").replace(" · ", " ")
    if len(text) <= max_chars:
        return [text]
    words = text.split()
    candidates = []
    for index in range(1, len(words)):
        first, second = " ".join(words[:index]), " ".join(words[index:])
        candidates.append((max(len(first), len(second)), abs(len(first) - len(second)), first, second))
    _, _, first, second = min(candidates)
    return [first[:20], second[:20]]


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
        "color page": "colorwheel", "fairlight page": "wave", "deliver page": "export",
        "quick export": "quickexport_touch",
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
        "right-click": "rightclick", "ripple delete": "rippledelete",
        "media pool panel": "mediapool_panel",
        "effects library panel": "effects_panel",
        "inspector panel": "inspector_panel",
        "mixer panel": "mixer_panel",
        "power bins panel": "powerbins_panel",
        "metadata panel": "metadata_panel",
        "index panel": "index_panel",
        "copy": "copy", "paste attributes": "paste",
        "bypass all grades": "bypass_panel",
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
        "thumbnail": "thumbnail_touch", "export folder": "exportfolder_touch", "clear render queue": "clearqueue",
        "mark in for export": "markin", "mark out for export": "markout", "free deliver controls": "freedeliver_touch",
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
    stroke_attrs = f'stroke="{color}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"'
    s = f'{stroke_attrs} fill="none"'
    fill = f'fill="{color}"'
    subtle = f'fill="{color}" opacity=".16"'
    shapes = {
        # 1. Distinct Break Timer Badges (Wide 140px stopwatch with huge bold text)
        "timer_25m": f'<circle cx="106" cy="108" r="62" {subtle} {stroke_attrs}/><path d="M106 36v18M78 36h56" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="42" font-weight="900">25m</text>',
        "timer_45m": f'<circle cx="106" cy="108" r="62" {subtle} {stroke_attrs}/><path d="M106 36v18M78 36h56" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="42" font-weight="900">45m</text>',
        "timer_1h": f'<circle cx="106" cy="108" r="62" {subtle} {stroke_attrs}/><path d="M106 36v18M78 36h56" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="46" font-weight="900">1h</text>',
        "timer_1_5h": f'<circle cx="106" cy="108" r="62" {subtle} {stroke_attrs}/><path d="M106 36v18M78 36h56" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="34" font-weight="900">1.5h</text>',
        "timer_2h": f'<circle cx="106" cy="108" r="62" {subtle} {stroke_attrs}/><path d="M106 36v18M78 36h56" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="46" font-weight="900">2h</text>',
        "timer_2_5h": f'<circle cx="106" cy="108" r="62" {subtle} {stroke_attrs}/><path d="M106 36v18M78 36h56" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="34" font-weight="900">2.5h</text>',
        "timer_3h": f'<circle cx="106" cy="108" r="62" {subtle} {stroke_attrs}/><path d="M106 36v18M78 36h56" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="46" font-weight="900">3h</text>',
        "timer_4h": f'<circle cx="106" cy="108" r="62" {subtle} {stroke_attrs}/><path d="M106 36v18M78 36h56" {s}/><text x="106" y="122" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="46" font-weight="900">4h</text>',
        "break_status": f'<rect x="28" y="52" width="156" height="102" rx="16" {subtle} {stroke_attrs}/><path d="M56 86h100M56 118h64" {s}/><circle cx="156" cy="118" r="10" {fill}/>',

        # 2. Aspect Ratio Timelines (Wide cards with large bold numbers)
        "timeline_9_16": f'<rect x="66" y="42" width="80" height="126" rx="16" {subtle} {stroke_attrs}/><text x="106" y="116" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="28" font-weight="900">9:16</text><circle cx="106" cy="150" r="5" {fill}/>',
        "timeline_4_5": f'<rect x="52" y="46" width="108" height="118" rx="14" {subtle} {stroke_attrs}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="36" font-weight="900">4:5</text>',
        "timeline_4_3": f'<rect x="36" y="52" width="140" height="106" rx="12" {subtle} {stroke_attrs}/><text x="106" y="116" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="38" font-weight="900">4:3</text>',

        # 3. Dedicated Custom Glyphs & Resolve Authenticity
        "rushwise": f'<path d="M106 38l64 64-64 64-64-64z" {subtle} {stroke_attrs}/><circle cx="106" cy="102" r="18" {fill}/><path d="M106 38v34m0 60v34m-64-64h34m60 0h34" {s}/>',
        "audio_level": f'<path d="M42 80v48h28l36 30V50L70 80H42z" {subtle} {stroke_attrs}/><path d="M136 74a44 44 0 0 1 0 60m22-82a72 72 0 0 1 0 104" {s}/>',
        "dynamic_trim": f'<path d="M48 54v102M84 76l-36 27 36 27M164 54v102M128 76l36 27-36 27" {s}/><path d="M106 62v86" stroke="{color}" stroke-width="6" stroke-dasharray="8 8"/>',
        "dynamic_trim_toggle": f'<circle cx="106" cy="105" r="58" {subtle} {stroke_attrs}/><path d="M106 58v40m-26 22l26-22 26 22" {s}/>',
        "effects_library": f'<path d="M48 144l72-72 18 18-72 72z" {s}/><path d="M152 50l6 14 14 6-14 6-6 14-6-14-14-6 14-6z" {fill}/><path d="M72 58l4 10 10 4-10 4-4 10-4-10-10-4 10-4z" {fill} opacity=".7"/>',

        # 4. Color Grading Nodes (Wide Resolve Node Tree Style)
        "nodeplus": f'<rect x="36" y="56" width="140" height="96" rx="12" {subtle} {stroke_attrs}/><circle cx="22" cy="104" r="9" {fill}/><circle cx="190" cy="104" r="9" {fill}/><path d="M22 104h14M176 104h14M106 82v44m-22-22h44" {s}/>',
        "nodebefore": f'<rect x="32" y="66" width="62" height="78" rx="10" {subtle} {stroke_attrs}/><rect x="118" y="66" width="62" height="78" rx="10" {subtle} {stroke_attrs}/><path d="M94 105h24m-12-12 12 12-12 12" {s}/><circle cx="20" cy="105" r="7" {fill}/><circle cx="192" cy="105" r="7" {fill}/>',
        "tag": f'<rect x="34" y="56" width="144" height="98" rx="12" {subtle} {stroke_attrs}/><circle cx="22" cy="105" r="8" {fill}/><circle cx="190" cy="105" r="8" {fill}/><path d="M64 92h84M64 120h56" {s}/>',

        # 5. Scopes, Light Box, and Printer Lights
        "scopes": f'<rect x="24" y="48" width="164" height="104" rx="12" {subtle} {stroke_attrs}/><circle cx="106" cy="100" r="34" stroke="{color}" stroke-width="4" fill="none"/><path d="M106 72v56M78 100h56" stroke="{color}" stroke-width="3"/><path d="M84 152h44" {s}/>',
        "lightbox": f'<rect x="30" y="50" width="40" height="46" rx="6" {subtle} {stroke_attrs}/><rect x="86" y="50" width="40" height="46" rx="6" {subtle} {stroke_attrs}/><rect x="142" y="50" width="40" height="46" rx="6" {subtle} {stroke_attrs}/><rect x="30" y="108" width="40" height="46" rx="6" {subtle} {stroke_attrs}/><rect x="86" y="108" width="40" height="46" rx="6" {subtle} {stroke_attrs}/><rect x="142" y="108" width="40" height="46" rx="6" {subtle} {stroke_attrs}/>',
        "printerlights": f'<circle cx="56" cy="88" r="22" fill="#FF6572" opacity=".9"/><circle cx="106" cy="88" r="22" fill="#5EE07E" opacity=".9"/><circle cx="156" cy="88" r="22" fill="#65AFFF" opacity=".9"/><path d="M56 118v34m50-34v34m50-34v34" {s}/>',
        "redlight": f'<circle cx="106" cy="94" r="48" fill="#FF6572" opacity=".25" {stroke_attrs}/><text x="106" y="114" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="52" font-weight="900">R</text><path d="M60 152h24m68 0h24m-12-12v24" {s}/>',
        "greenlight": f'<circle cx="106" cy="94" r="48" fill="#5EE07E" opacity=".25" {stroke_attrs}/><text x="106" y="114" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="52" font-weight="900">G</text><path d="M60 152h24m68 0h24m-12-12v24" {s}/>',
        "bluelight": f'<circle cx="106" cy="94" r="48" fill="#65AFFF" opacity=".25" {stroke_attrs}/><text x="106" y="114" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="52" font-weight="900">B</text><path d="M60 152h24m68 0h24m-12-12v24" {s}/>',

        # 6. Color Curves & Tonal Controls
        "saturation": f'<path d="M106 44 C72 90 54 116 54 136 a52 52 0 0 0 104 0 C158 116 140 90 106 44 Z" {subtle} {stroke_attrs}/><path d="M64 136a42 42 0 0 0 84 0" fill="{color}" opacity=".4"/>',
        "gamma": f'<path d="M36 46v116h140" {s}/><path d="M36 162 C74 162 90 94 176 54" stroke="{color}" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="106" cy="112" r="12" {fill}/>',
        "gain": f'<path d="M36 46v116h140" {s}/><path d="M36 162 L108 136 L176 52" stroke="{color}" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="176" cy="52" r="12" {fill}/>',
        "bypass": f'<circle cx="106" cy="105" r="58" {subtle} {stroke_attrs}/><path d="M106 47a58 58 0 0 1 0 116z" fill="{color}" opacity=".35"/><path d="M50 50l112 112" stroke="#FF6C7A" stroke-width="14" stroke-linecap="round"/>',

        # 7. Split Comparisons
        "splittwo": f'<rect x="36" y="58" width="62" height="94" rx="8" {subtle} {stroke_attrs}/><rect x="114" y="58" width="62" height="94" rx="8" {subtle} {stroke_attrs}/>',
        "splitprevnext": f'<rect x="28" y="68" width="44" height="74" rx="6" {subtle} {stroke_attrs}/><rect x="84" y="50" width="44" height="110" rx="6" {subtle} {stroke_attrs}/><rect x="140" y="68" width="44" height="74" rx="6" {subtle} {stroke_attrs}/>',
        "splitoriginal": f'<rect x="34" y="58" width="66" height="94" rx="8" {subtle} {stroke_attrs}/><rect x="112" y="58" width="66" height="94" rx="8" {subtle} {stroke_attrs}/><path d="M67 116l18-18 18 18M130 116l18-18 18 18" {s}/>',
        "splitstills": f'<rect x="36" y="60" width="58" height="90" rx="8" {subtle} {stroke_attrs}/><rect x="118" y="60" width="58" height="90" rx="8" {subtle} {stroke_attrs}/><path d="M48 128l16-16 16 16M130 128l16-16 16 16" {s}/>',
        "closecompare": f'<rect x="38" y="54" width="136" height="102" rx="12" {subtle} {stroke_attrs}/><path d="M72 80l68 68m0-68-68 68" stroke="#FF6C7A" stroke-width="14" stroke-linecap="round"/>',

        # 8. Fairlight Audio & Fades
        "batchfadesettings": f'<rect x="32" y="62" width="148" height="86" rx="10" {subtle} {stroke_attrs}/><path d="M44 136 C64 136 76 76 106 76 C136 76 148 136 168 136" stroke="{color}" stroke-width="10" fill="none"/><circle cx="106" cy="76" r="10" {fill}/>',
        "applybatchfades": f'<rect x="32" y="62" width="148" height="86" rx="10" {subtle} {stroke_attrs}/><path d="M44 136 C64 136 76 76 106 76 C136 76 148 136 168 136" stroke="{color}" stroke-width="10" fill="none"/><path d="M148 48l14 14 28-28" stroke="#5CE080" stroke-width="10" stroke-linecap="round" fill="none"/>',
        "trackheight": f'<rect x="36" y="56" width="140" height="98" rx="10" {subtle} {stroke_attrs}/><path d="M106 38v34m-16-16 16-16 16 16M106 172v-34m-16 16 16 16 16-16" stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="M60 94h92m-92 22h92" stroke="{color}" stroke-width="5"/>',
        "wavezoom": f'<path d="M22 105h18l14-48 22 96 24-118 24 130 22-86 16 26h30" {s}/><path d="M24 50h30m-15-15-15 15 15 15M188 50h-30m15-15 15 15-15 15" stroke="{color}" stroke-width="7" stroke-linecap="round"/>',

        # 9. Edit Tools (Wide Razor, Scissors, Retime, Compound Clip)
        "split": f'<rect x="24" y="64" width="70" height="82" rx="8" {subtle} {stroke_attrs}/><rect x="118" y="64" width="70" height="82" rx="8" {subtle} {stroke_attrs}/><path d="M106 36v138" stroke="#FF6C7A" stroke-width="10" stroke-linecap="round"/><path d="M94 38l12 18 12-18z" fill="#FF6C7A"/>',
        "retime": f'<circle cx="70" cy="105" r="38" {subtle} {stroke_attrs}/><path d="M70 78v27h24" {s}/><path d="M126 75h52M126 105h52M126 135h52" stroke="{color}" stroke-width="12" stroke-linecap="round"/>',
        "speed": f'<path d="M34 135 A72 72 0 1 1 178 135" {s}/><path d="M106 125 L152 75" stroke="#FF8A3D" stroke-width="12" stroke-linecap="round"/><circle cx="106" cy="125" r="12" {fill}/><text x="106" y="156" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="22" font-weight="900">%</text>',
        "compoundclip": f'<rect x="28" y="52" width="156" height="106" rx="12" stroke="{color}" stroke-width="5" stroke-dasharray="10 8" fill="none"/><rect x="44" y="68" width="124" height="32" rx="6" {subtle} {stroke_attrs}/><rect x="44" y="112" width="124" height="32" rx="6" {subtle} {stroke_attrs}/>',
        "deletegaps": f'<rect x="28" y="72" width="56" height="66" rx="8" {subtle} {stroke_attrs}/><rect x="128" y="72" width="56" height="66" rx="8" {subtle} {stroke_attrs}/><path d="M84 105h44" stroke="#FF6C7A" stroke-width="8" stroke-dasharray="6 6"/><path d="M70 105h22m-10-10 10 10-10 10M142 105h-22m10-10-10 10 10 10" {s}/>',
        "crossfade": f'<rect x="30" y="64" width="66" height="82" rx="8" {subtle} {stroke_attrs}/><rect x="116" y="64" width="66" height="82" rx="8" {subtle} {stroke_attrs}/><path d="M80 146l52-82M80 64l52 82" stroke="{color}" stroke-width="10" stroke-linecap="round"/>',
        "magnet": f'<path d="M42 56v54a64 64 0 0 0 128 0V56" {s}/><rect x="34" y="52" width="28" height="22" rx="4" {fill}/><rect x="150" y="52" width="28" height="22" rx="4" {fill}/><path d="M82 136l-16 16m60-16 16 16" {s}/>',
        "scissors": f'<circle cx="48" cy="70" r="20" {s}/><circle cx="48" cy="140" r="20" {s}/><path d="M66 84l114 62M66 126l114-62" {s}/><circle cx="106" cy="105" r="7" {fill}/>',
        "trash": f'<path d="M34 64h144M84 64V44h44v20" {s}/><path d="M50 64l10 96h92l10-96z" {subtle} {stroke_attrs}/><path d="M84 90v46m44-46v46" {s}/>',
        "trimleft": f'<path d="M54 52v106M90 76H54m36 58H54M126 105h56" {s}/>',
        "trimright": f'<path d="M158 52v106M122 76h36m-36 58h36M30 105h56" {s}/>',
        "rippleleft": f'<path d="M172 105H44m28-28-28 28 28 28M186 68v74" {s}/>',
        "rippleright": f'<path d="M40 105h128m-28-28 28 28-28 28M26 68v74" {s}/>',
        "rippledelete": f'<path d="M172 105H44m28-28-28 28 28 28M186 68v74" {s}/><path d="M46 54l120 102M166 54L46 156" stroke="#FF6C7A" stroke-width="10" stroke-linecap="round"/>',

        # 10. Media & Project (Wide Folders, Proxies, Camera RAW)
        "powerbins": f'<path d="M24 66h52l16 16h96v84H24z" {subtle} {stroke_attrs}/><path d="M114 84l-20 34h22l-12 36 34-44h-22z" {fill}/>',
        "proxy": f'<rect x="28" y="58" width="156" height="94" rx="12" {subtle} {stroke_attrs}/><text x="82" y="118" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="34" font-weight="900">PXY</text><circle cx="152" cy="74" r="20" fill="#0A0D14" {stroke_attrs}/><path d="M152 64v10l8 4" {s}/>',
        "camera": f'<path d="M30 78h42l16-24h36l16 24h42v76H30z" {subtle} {stroke_attrs}/><circle cx="106" cy="116" r="28" {s}/><text x="106" y="123" text-anchor="middle" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="14" font-weight="900">RAW</text>',

        # 11. Presets & Deliver (Wide Cards)
        "youtube": f'<rect x="30" y="62" width="152" height="86" rx="22" {subtle} {stroke_attrs}/><path d="M92 85l44 20-44 20z" {fill}/>',
        "vimeo": f'<path d="M44 76c22-18 50-24 62 2 10 24-15 62-6 62 8 0 28-30 36-46 9-18 28-24 40-14-15 50-60 92-80 92-18 0-28-48-38-74-6-14-12-10-24 0z" {s}/>',
        "tiktok": f'<path d="M118 46v80a30 30 0 1 1-26-30v24a8 8 0 1 0 7 7V46h22c3 18 16 30 34 32v22c-14-1-26-8-37-17" {s}/>',
        "instagram": f'<rect x="42" y="46" width="128" height="118" rx="32" {subtle} {stroke_attrs}/><circle cx="106" cy="105" r="30" {s}/><circle cx="144" cy="68" r="8" {fill}/>',
        "prores": f'<rect x="28" y="64" width="156" height="82" rx="12" {subtle} {stroke_attrs}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-size="40" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-weight="900">HQ</text>',
        "custom1": f'<rect x="36" y="48" width="140" height="114" rx="14" {subtle} {stroke_attrs}/><text x="106" y="128" text-anchor="middle" fill="{color}" font-size="64" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-weight="900">1</text>',
        "custom2": f'<rect x="36" y="48" width="140" height="114" rx="14" {subtle} {stroke_attrs}/><text x="106" y="128" text-anchor="middle" fill="{color}" font-size="64" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-weight="900">2</text>',
        "custom3": f'<rect x="36" y="48" width="140" height="114" rx="14" {subtle} {stroke_attrs}/><text x="106" y="128" text-anchor="middle" fill="{color}" font-size="64" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-weight="900">3</text>',
        "queueadd": f'<rect x="40" y="48" width="132" height="114" rx="12" {subtle} {stroke_attrs}/><path d="M64 80h48M64 105h48M64 130h48" {s}/><circle cx="148" cy="130" r="24" fill="#0A0D14" {stroke_attrs}/><path d="M148 116v28m-14-14h28" {s}/>',
        "renderall": f'<path d="M54 58l62 47-62 47zM108 58l62 47-62 47z" {fill}/><path d="M38 162h136" stroke="{color}" stroke-width="8" stroke-linecap="round"/>',
        "rendernew": f'<path d="M58 58l74 47-74 47z" {fill}/><path d="M156 58l6 16 16 6-16 6-6 16-6-16-16-6 16-6z" fill="#FFD43D"/>',
        "stop": f'<path d="M72 46h68l42 42v68l-42 42H72L30 156V88z" fill="#FF6C7A" opacity=".2" {stroke_attrs}/><rect x="76" y="76" width="60" height="60" rx="10" fill="#FF6C7A"/>',
        "thumbnail": f'<rect x="32" y="54" width="148" height="102" rx="12" {subtle} {stroke_attrs}/><circle cx="74" cy="88" r="16" {fill}/><path d="M46 144l42-38 28 24 30-28 22 22" {s}/>',
        "exportfolder": f'<path d="M24 66h52l16 16h96v84H24z" {subtle} {stroke_attrs}/><path d="M106 102v38m-16-16 16 16 16-16" {s}/>',
        "clearqueue": f'<path d="M38 64h136M84 64V46h44v18" {s}/><path d="M52 64l8 94h92l8-94z" {subtle} {stroke_attrs}/><path d="M88 92l36 36m0-36-36 36" stroke="#FF6C7A" stroke-width="10" stroke-linecap="round"/>',
        "free": f'<rect x="34" y="56" width="144" height="98" rx="12" {subtle} {stroke_attrs}/><text x="106" y="118" text-anchor="middle" fill="{color}" font-size="42" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-weight="900">FREE</text>',

        # 12. Standard Navigation & Media Pool (Wide Format)
        "folder": f'<path d="M24 66h52l16 16h96v84H24z" {subtle} {stroke_attrs}/>',
        "folderplus": f'<path d="M24 66h52l16 16h96v84H24z" {subtle} {stroke_attrs}/><path d="M136 108v36m-18-18h36" {s}/>',
        "import": f'<path d="M106 38v86m-34-34 34 34 34-34M28 136v24h156v-24" {s}/>',
        "grid": f'<rect x="36" y="48" width="56" height="50" rx="8" {subtle} {stroke_attrs}/><rect x="120" y="48" width="56" height="50" rx="8" {subtle} {stroke_attrs}/><rect x="36" y="112" width="56" height="50" rx="8" {subtle} {stroke_attrs}/><rect x="120" y="112" width="56" height="50" rx="8" {subtle} {stroke_attrs}/>',
        "gear": f'<circle cx="106" cy="105" r="32" {subtle} {stroke_attrs}/><path d="M106 36v20m0 98v20M37 105h20m98 0h20M57 56l15 15m68 68 15 15M155 56l-15 15m-68 68-15 15" {s}/>',
        "note": f'<path d="M46 42h120v126H46z" {subtle} {stroke_attrs}/><path d="M72 76h68M72 106h68M72 136h44" {s}/>',
        "newfile": f'<path d="M52 40h74l32 32v100H52z" {subtle} {stroke_attrs}/><path d="M126 40v32h32M106 96v46m-23-23h46" {s}/>',
        "layers": f'<path d="M106 46l74 38-74 38-74-38z" {subtle} {stroke_attrs}/><path d="M32 118l74 38 74-38M32 92l74 38 74-38" {s}/>',
        "link": f'<path d="M88 126l-16 16a32 32 0 0 1-46-46l30-30a32 32 0 0 1 46 0m8 0 16-16a32 32 0 0 1 46 46l-30 30a32 32 0 0 1-46 0M72 105h68" {s}/>',
        "timeline": f'<path d="M28 68h156M28 105h156M28 142h156" {s}/><circle cx="64" cy="68" r="10" {fill}/><circle cx="124" cy="105" r="10" {fill}/><circle cx="160" cy="142" r="10" {fill}/>',
        "timelineplus": f'<path d="M28 72h96M28 105h96M28 138h96M156 105v44m-22-22h44" {s}/>',
        "duplicate": f'<rect x="38" y="64" width="90" height="94" rx="10" {subtle} {stroke_attrs}/><rect x="84" y="42" width="90" height="94" rx="10" {subtle} {stroke_attrs}/>',
        "colorwheel": f'<circle cx="106" cy="105" r="62" fill="#121824" {stroke_attrs}/><path d="M106 43a62 62 0 0 1 54 92l-54-30z" fill="#FF6B7B"/><path d="M106 105l54 30a62 62 0 0 1-108 0z" fill="#57DDA9"/><path d="M106 105 52 135a62 62 0 0 1 54-92z" fill="#5AA9FF"/><circle cx="106" cy="105" r="18" fill="#F3F7FF"/>',
        "wave": f'<path d="M20 105h18l14-48 22 96 24-118 24 130 22-86 16 26h30" {s}/>',
        "export": f'<path d="M48 42h84l28 28v98H48z" {subtle} {stroke_attrs}/><path d="M106 68v64m-26-26 26 26 26-26M68 154h76" {s}/>',
        "quickexport": f'<path d="M48 44h80l28 28v94H48z" {subtle} {stroke_attrs}/><path d="M106 72v56m-24-24 24 24 24-24" {s}/><path d="M168 38l8 24 24 8-24 8-8 24-8-24-24-8 24-8z" {fill}/>',
        "timer": f'<circle cx="106" cy="108" r="62" {subtle} {stroke_attrs}/><path d="M106 72v36l28 18M78 36h56M106 36v18" {s}/>',
        "play": f'<path d="M72 56l72 49-72 49z" {fill}/><path d="M32 56v98m148-98v98" {s}/>',
        "selectleft": f'<rect x="110" y="68" width="76" height="74" rx="8" {subtle} {stroke_attrs}/><path d="M176 105H36m32-32L36 105l32 32" {s}/>',
        "selectright": f'<rect x="26" y="68" width="76" height="74" rx="8" {subtle} {stroke_attrs}/><path d="M36 105h140m-32-32 32 32-32 32" {s}/>',
        "fit": f'<path d="M36 78V50h28M176 78V50h-28M36 132v28h28M176 132v28h-28" {s}/><rect x="68" y="74" width="76" height="62" rx="8" {subtle} {stroke_attrs}/>',
        "zoom": f'<circle cx="94" cy="94" r="44" {subtle} {stroke_attrs}/><path d="M128 128l46 46M94 72v44m-22-22h44" {s}/>',
        "shuttle": f'<path d="M26 105h160M54 74l-30 31 30 31M158 74l30 31-30 31" {s}/>',
        "fastshuttle": f'<path d="M24 105h164M50 74l-28 31 28 31M80 74l-28 31 28 31M132 74l28 31-28 31M162 74l28 31-28 31" {s}/>',
        "nextclip": f'<path d="M32 64v82M72 105h84m-28-28 28 28-28 28M180 64v82" {s}/>',
        "marker": f'<path d="M52 48h108v64l-54 50-54-50z" {subtle} {stroke_attrs}/><path d="M74 82h64" {s}/>',
        "markerdelete": f'<path d="M52 48h108v64l-54 50-54-50z" {subtle} {stroke_attrs}/><path d="M74 76l64 64m0-64-64 64" stroke="#FF6C7A" stroke-width="12" stroke-linecap="round"/>',
        "linked": f'<path d="M38 80h136M38 130h136" {s}/><path d="M68 60l-22 20 22 20M144 110l22 20-22 20" {s}/>',
        "normalize": f'<path d="M20 126h20l14-34 20 64 22-98 24 112 22-68 14 24h36" {s}/><path d="M24 50h164" stroke="#5CE080" stroke-width="8" stroke-linecap="round"/>',
        "align": f'<path d="M38 56v98m136-98v98M66 82h80M66 128h80M86 56v98m40-98v98" {s}/>',
        "markin": f'<path d="M56 50v110m34-78H56m34 46H56M112 105h68" {s}/>',
        "markout": f'<path d="M156 50v110m-34-78h34m-34 46h34M32 105h68" {s}/>',
        "loop": f'<path d="M156 74a58 58 0 1 0 10 68" {s}/><path d="M154 48v32h-32" {s}/>',
        "matchframe": f'<rect x="34" y="54" width="144" height="102" rx="10" {subtle} {stroke_attrs}/><path d="M64 130l28-28 24 20 20-20 26 28" {s}/><path d="M162 64v36h-36" {s}/>',
        "cinema": f'<rect x="28" y="58" width="156" height="96" rx="12" {subtle} {stroke_attrs}/><path d="M66 166h80" {s}/>',
        "eye": f'<path d="M24 105s32-52 82-52 82 52 82 52-32 52-82 52-82-52-82-52z" {subtle} {stroke_attrs}/><circle cx="106" cy="105" r="24" {s}/>',
        "freeze": f'<rect x="46" y="46" width="120" height="118" rx="12" {subtle} {stroke_attrs}/><path d="M72 78h68M72 105h68M72 132h68" {s}/><path d="M34 58l144 94" stroke="#82C8FF" stroke-width="10" stroke-linecap="round"/>',
        "safe": f'<rect x="34" y="46" width="144" height="118" rx="10" {s}/><rect x="62" y="68" width="88" height="74" rx="6" {subtle} {stroke_attrs}/>',
        "findclip": f'<rect x="34" y="58" width="112" height="92" rx="10" {subtle} {stroke_attrs}/><circle cx="148" cy="138" r="28" fill="#0A0D14" {stroke_attrs}/><path d="M168 158l22 22" {s}/>',
        "swapleft": f'<path d="M172 74H40m28-28L40 74l28 28M40 136h132m-28-28 28 28-28 28" {s}/>',
        "swapright": f'<path d="M40 74h132m-28-28 28 28-28 28M172 136H40m28-28L40 136l28 28" {s}/>',
        "undo": f'<path d="M88 56L42 102l46 46" {s}/><path d="M46 102h76a44 44 0 0 1 44 44" {s}/>',
        "save": f'<path d="M42 44h96l32 32v90H42z" {subtle} {stroke_attrs}/><path d="M70 44v48h60V44M64 148h84" {s}/>',
        "uptrack": f'<path d="M106 166V44m-34 34 34-34 34 34M44 154h124" {s}/>',
        "downtrack": f'<path d="M106 44v122m-34-34 34 34 34-34M44 56h124" {s}/>',
        "startline": f'<path d="M52 68v74M82 105h96m-40-36-36 36 36 36" {s}/>',
        "endline": f'<path d="M160 68v74M130 105H34m40-36 36 36-36 36" {s}/>',
        "rightclick": f'<path d="M64 48v86m0 0-22-26m22 26 22-26M108 48v86m0 0-22-26m22 26 22-26M64 156h56a32 32 0 0 0 32-32V88" {s}/>',
        "inspector": f'<rect x="36" y="48" width="140" height="114" rx="10" {subtle} {stroke_attrs}/><path d="M66 80h80M66 106h80M66 132h46" {s}/>',
        "mixer": f'<path d="M48 54v102M86 54v102M126 54v102M164 54v102" {s}/><rect x="38" y="90" width="20" height="18" rx="4" {fill}/><rect x="76" y="120" width="20" height="18" rx="4" {fill}/><rect x="116" y="72" width="20" height="18" rx="4" {fill}/><rect x="154" y="102" width="20" height="18" rx="4" {fill}/>',
        "metadata": f'<path d="M36 52h96l36 36v76H36z" {subtle} {stroke_attrs}/><path d="M132 52v36h36M64 116h76M64 142h44" {s}/>',
        "list": f'<path d="M66 66h114M66 106h114M66 146h114" {s}/><circle cx="40" cy="66" r="9" {fill}/><circle cx="40" cy="106" r="9" {fill}/><circle cx="40" cy="146" r="9" {fill}/>',
        "copy": f'<rect x="36" y="62" width="94" height="100" rx="10" {subtle} {stroke_attrs}/><rect x="82" y="44" width="94" height="100" rx="10" {subtle} {stroke_attrs}/>',
        "paste": f'<rect x="42" y="54" width="128" height="114" rx="12" {subtle} {stroke_attrs}/><rect x="74" y="40" width="64" height="24" rx="6" {fill}/><path d="M68 98h76M68 126h50" {s}/>',
        "still": f'<rect x="32" y="56" width="148" height="98" rx="12" {subtle} {stroke_attrs}/><circle cx="74" cy="88" r="14" {fill}/><path d="M50 144l38-34 26 22 28-26 26 26" {s}/>',
        "reset": f'<path d="M164 78a62 62 0 1 0 8 72" {s}/><path d="M162 48v34h-34" {s}/>',
        "colorswatch": f'<circle cx="106" cy="105" r="54" fill="{color}"/><circle cx="106" cy="105" r="64" {s}/>',
        "framewheel": f'<circle cx="106" cy="105" r="64" {subtle} {stroke_attrs}/><path d="M106 50v110M51 105h110" {s}/><circle cx="106" cy="105" r="20" {fill}/>',
        "spark": f'<path d="M106 38l16 52 52 16-52 16-16 52-16-52-52-16 52-16z" {fill}/>',

        # 13. Dedicated Workspace 8 Touch Panels (Zero letterboxing, wide square format)
        "mediapool_panel": f'<path d="M24 66h52l16 16h96v84H24z" {subtle} {stroke_attrs}/><rect x="44" y="98" width="34" height="26" rx="4" {fill} opacity=".7"/><rect x="88" y="98" width="34" height="26" rx="4" {fill} opacity=".7"/><rect x="132" y="98" width="34" height="26" rx="4" {fill} opacity=".7"/>',
        "effects_panel": f'<path d="M42 144l72-72 18 18-72 72z" {s}/><path d="M152 48l6 16 16 6-16 6-6 16-6-16-16-6 16-6z" {fill}/><path d="M72 56l4 10 10 4-10 4-4 10-4-10-10-4 10-4z" {fill} opacity=".7"/>',
        "inspector_panel": f'<rect x="28" y="52" width="156" height="106" rx="12" {subtle} {stroke_attrs}/><path d="M50 78h112M50 105h112M50 132h112" {s}/><rect x="80" y="70" width="24" height="16" rx="4" {fill}/><rect x="126" y="97" width="24" height="16" rx="4" {fill}/><rect x="70" y="124" width="24" height="16" rx="4" {fill}/>',
        "mixer_panel": f'<rect x="28" y="52" width="156" height="106" rx="12" {subtle} {stroke_attrs}/><path d="M54 62v86M88 62v86M124 62v86M158 62v86" {s}/><rect x="46" y="94" width="16" height="16" rx="4" {fill}/><rect x="80" y="118" width="16" height="16" rx="4" {fill}/><rect x="116" y="78" width="16" height="16" rx="4" {fill}/><rect x="150" y="104" width="16" height="16" rx="4" {fill}/>',
        "powerbins_panel": f'<path d="M24 66h52l16 16h96v84H24z" {subtle} {stroke_attrs}/><path d="M114 84l-20 34h22l-12 36 34-44h-22z" {fill}/>',
        "metadata_panel": f'<rect x="30" y="52" width="152" height="106" rx="12" {subtle} {stroke_attrs}/><path d="M52 78h64M52 105h96M52 132h76" {s}/>',
        "index_panel": f'<rect x="28" y="52" width="156" height="106" rx="12" {subtle} {stroke_attrs}/><path d="M68 76h98M68 105h98M68 134h98" {s}/><circle cx="48" cy="76" r="6" {fill}/><circle cx="48" cy="105" r="6" {fill}/><circle cx="48" cy="134" r="6" {fill}/>',
        "bypass_panel": f'<circle cx="106" cy="105" r="58" {subtle} {stroke_attrs}/><path d="M106 47a58 58 0 0 1 0 116z" fill="{color}" opacity=".35"/><path d="M50 50l112 112" stroke="#FF6C7A" stroke-width="14" stroke-linecap="round"/>',
        "quickexport_touch": f'<path d="M106 34l34 44h-24v46h-20V78H72z" {fill}/><path d="M68 136l38-16 38 16-38-42z" fill="{color}" opacity=".4"/><path d="M36 156h140" stroke="{color}" stroke-width="8" stroke-linecap="round"/>',
        "exportfolder_touch": f'<path d="M24 66h52l16 16h96v84H24z" {subtle} {stroke_attrs}/><path d="M106 98v44m-18-18 18 18 18-18" {s}/>',
        "thumbnail_touch": f'<rect x="28" y="54" width="156" height="102" rx="12" {subtle} {stroke_attrs}/><circle cx="70" cy="88" r="16" {fill}/><path d="M44 144l42-38 28 24 32-28 26 26" {s}/>',
        "freedeliver_touch": f'<rect x="28" y="54" width="156" height="102" rx="12" {subtle} {stroke_attrs}/><path d="M28 86h156M68 54l-16 32M112 54l-16 32M156 54l-16 32" {s}/><path d="M96 100l32 18-32 18z" {fill}/>',
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
    """Touch button: 256×256. Deep OLED dark canvas, vibrant top accent pill, large centered bold glyph, punchy white label."""
    label = lines(item["function"], 18)
    n_lines = len(label)
    max_word = max((len(w) for w in item["function"].split()), default=0)
    if n_lines == 1:
        font_size = 23 if max_word > 13 else (25 if max_word > 10 else 27)
        y_positions = [226]
    else:
        font_size = 19 if max_word > 9 else 22
        y_positions = [208, 232]
    text = "".join(
        f'<text x="128" y="{y}" text-anchor="middle" fill="#FFFFFF" '
        f'font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="{font_size}" font-weight="900">'
        f'{html.escape(val)}</text>'
        for y, val in zip(y_positions, label)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
        f'<rect width="256" height="256" rx="24" fill="#0C0F17"/>'
        f'<rect x="2" y="2" width="252" height="252" rx="22" fill="none" stroke="#222A3B" stroke-width="2.5"/>'
        f'<rect x="28" y="10" width="200" height="6" rx="3" fill="{color}"/>'
        f'<g transform="translate(22, 14) scale(1.0)">{glyph(token, color)}</g>'
        f'{text}'
        f'</svg>'
    )


def svg_dial(item: dict[str, str], color: str, token: str) -> str:
    """Dial/Turn: 120×180 OLED strip. Text-primary inverted hierarchy."""
    label = lines(item["function"], 11)
    n_lines = len(label)
    max_word = max((len(w) for w in item["function"].split()), default=0)
    if n_lines == 1:
        font_size = 17 if max_word > 8 else 20
        y_positions = [108]
    else:
        font_size = 14 if max_word > 7 else 17
        y_positions = [96, 118]
    line_text = "".join(
        f'<text x="60" y="{y}" text-anchor="middle" fill="#FFFFFF" '
        f'font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="{font_size}" font-weight="900">'
        f'{html.escape(val)}</text>'
        for y, val in zip(y_positions, label)
    )
    control_badge = "TURN ↻" if "turn" in item["control"].lower() else "PRESS ●"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="120" height="180" viewBox="0 0 120 180">'
        f'<rect width="120" height="180" rx="16" fill="#0C0F17"/>'
        f'<rect x="2" y="2" width="116" height="176" rx="14" fill="none" stroke="#222A3B" stroke-width="2"/>'
        f'<rect x="18" y="8" width="84" height="4" rx="2" fill="{color}"/>'
        f'<g transform="translate(38, 16) scale(0.21)">{glyph(token, color)}</g>'
        f'<line x1="28" y1="64" x2="92" y2="64" stroke="{color}" stroke-width="2" stroke-linecap="round" opacity="0.6"/>'
        f'{line_text}'
        f'<rect x="14" y="146" width="92" height="24" rx="12" fill="#182030" stroke="{color}" stroke-width="1.5"/>'
        f'<text x="60" y="162" text-anchor="middle" fill="{color}" '
        f'font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="11" font-weight="900" letter-spacing="1.2">'
        f'{control_badge}</text>'
        f'</svg>'
    )


def svg_physical(item: dict[str, str], color: str, token: str) -> str:
    """Physical key: 320×160."""
    label = lines(item["function"], 16)
    n_lines = len(label)
    control = item["control"].upper().replace("ROUND BUTTON", "ROUND")
    max_word = max((len(w) for w in item["function"].split()), default=0)
    font_size = 20 if max_word > 12 else (22 if n_lines > 1 else 25)
    y_start = 66 if n_lines > 1 else 78
    line_spacing = 26
    label_text = "".join(
        f'<text x="216" y="{y_start + i * line_spacing}" text-anchor="middle" '
        f'fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" '
        f'font-size="{font_size}" font-weight="900">'
        f'{html.escape(val)}</text>'
        for i, val in enumerate(label)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="320" height="160" viewBox="0 0 320 160">'
        f'<rect width="320" height="160" rx="18" fill="#0C0F17"/>'
        f'<rect x="3" y="3" width="314" height="154" rx="15" fill="none" stroke="#222A3B" stroke-width="3"/>'
        f'<rect x="16" y="16" width="102" height="128" rx="12" fill="#141822" stroke="{color}" stroke-width="2"/>'
        f'<g transform="translate(14, 28) scale(0.50)">{glyph(token, color)}</g>'
        f'{label_text}'
        f'<text x="216" y="136" text-anchor="middle" fill="{color}" '
        f'font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-size="12" font-weight="900" letter-spacing="1.4">'
        f'{html.escape(control[:30])}</text>'
        f'</svg>'
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
        if kind != "touch":
            (dirs["touch"] / filename).write_text(svg_touch(item, color, token), encoding="utf-8")
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
