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
    if "dial" in control or "wheel · turn" in control:
        return "dial"
    if "touch" in control or "swipe-right" in control or "wheel · press" in control:
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
