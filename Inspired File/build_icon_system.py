#!/usr/bin/env python3
"""Generate one deterministic SVG source icon for every audited CT mapping."""

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path

from build_master_reference import ITEMS


ROOT = Path(__file__).resolve().parent / "Rupokar-Resolve-CT-Icon-System"
SVG_DIR = ROOT / "svg"
MANIFEST = ROOT / "icon-manifest.json"
BOARD = ROOT / "Icon-Board.html"

SECTION_COLORS = {
    "Navigation": "#A98BFF",
    "Media / Project": "#B99AFF",
    "Media / Break Timer": "#4DE2E1",
    "Edit 1": "#5AA9FF",
    "Edit 2": "#65B4FF",
    "Edit 3": "#7EAEFF",
    "Physical keys & Fn layer": "#9C8CFF",
    "Color": "#43D7C5",
    "Fairlight": "#7FE36C",
    "Deliver / Render Queue": "#C99AFF",
    "Quick Export": "#C99AFF",
}

COLOR_OVERRIDES = {
    "orange": "#FF8A3D", "yellow": "#FFD43D", "green": "#59DD7A",
    "apricot": "#FFB071", "blue": "#54A9FF", "lime": "#A8E84A",
    "brown": "#B87D4E", "pink": "#FF83C8", "purple": "#AE79FF",
    "olive": "#A2A35B", "teal": "#31C7B7", "navy": "#4F79C7",
    "violet": "#A36BFF", "tan": "#D2A977", "beige": "#E7CFA1",
    "red": "#FF5D68", "cyan": "#4DE2E1",
}


def slugify(value: str) -> str:
    value = value.lower().replace("×", "x").replace("/", "-")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:54]


def display_lines(name: str) -> list[str]:
    """Break CT labels into two compact lines without truncating semantic words."""
    normalized = name.replace(" / ", " ").replace(" · ", " ").replace(" for ", " ")
    words = normalized.split()
    if len(normalized) <= 14:
        return [normalized]
    midpoint = max(1, len(words) // 2)
    candidates = []
    for cut in range(1, len(words)):
        a, b = " ".join(words[:cut]), " ".join(words[cut:])
        candidates.append((max(len(a), len(b)), abs(cut - midpoint), a, b))
    _, _, first, second = min(candidates)
    return [first[:18], second[:18]]


def glyph_token(name: str, control: str, section: str) -> str:
    value = f"{name} {control}".lower()
    if "color" in value or any(word in value for word in COLOR_OVERRIDES): return "color"
    if "timer" in value or "interval" in value or "break" in value: return "timer"
    if "start" in value and "ripple" not in value: return "play"
    if "stop" in value: return "stop"
    if "play/pause" in value: return "play"
    if "import" in value: return "import"
    if "bin" in value or "folder" in value: return "folder"
    if "project" in value or "manager" in value: return "grid"
    if "note" in value: return "note"
    if "proxy" in value: return "proxy"
    if "camera" in value: return "camera"
    if "setting" in value or "preset" in value: return "gear"
    if "export" in value or "render" in value or "queue" in value or "youtube" in value or "vimeo" in value or "tiktok" in value or "instagram" in value or "prores" in value: return "export"
    if "timeline" in value or "find" in value: return "timeline"
    if "select backward" in value or "swap left" in value or "left" in value: return "left"
    if "select forward" in value or "swap right" in value or "right" in value: return "right"
    if "snapping" in value: return "magnet"
    if "delete" in value or "clear" in value or "remove" in value: return "delete"
    if "trim" in value: return "trim"
    if "retime" in value or "speed" in value: return "speed"
    if "ripple" in value: return "ripple"
    if "split" in value and section != "Color": return "scissors"
    if "zoom" in value: return "zoom"
    if "marker" in value or "mark in" in value or "mark out" in value: return "marker"
    if "link" in value: return "link"
    if "compound" in value: return "layers"
    if "normalize" in value or "audio level" in value: return "wave"
    if "align" in value: return "align"
    if "loop" in value: return "loop"
    if "viewer" in value or "frame" in value or "thumbnail" in value or "still" in value: return "frame"
    if "enable" in value: return "eye"
    if "title safe" in value: return "safe"
    if "crossfade" in value or "fade" in value: return "fade"
    if "shuttle" in value or "next clip" in value or "navigation" in section: return "transport"
    if "undo" in value: return "undo"
    if "save" in value: return "save"
    if "copy" in value or "paste" in value: return "copy"
    if "right-click" in value or "fn" in control: return "key"
    if "scope" in value: return "scope"
    if "node" in value: return "node"
    if "printer" in value or "saturation" in value or "gamma" in value or "gain" in value: return "color"
    if "waveform" in value or "track" in value or "fairlight" in section: return "wave"
    return "spark"


def symbol(token: str, color: str) -> str:
    stroke = f'stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    filled = f'fill="{color}"'
    shapes = {
        "import": f'<path d="M68 55v53m-25-25 25 25 25-25M42 118h84v24H42z" {stroke}/>',
        "folder": f'<path d="M38 74h42l12 14h88v58H38z" {stroke}/><path d="M119 109v32m-16-16h32" {stroke}/>',
        "note": f'<path d="M62 47h86v108H62zM84 78h42M84 101h42M84 124h28" {stroke}/>',
        "grid": f'<rect x="49" y="49" width="36" height="36" rx="5" {stroke}/><rect x="111" y="49" width="36" height="36" rx="5" {stroke}/><rect x="49" y="111" width="36" height="36" rx="5" {stroke}/><rect x="111" y="111" width="36" height="36" rx="5" {stroke}/>',
        "proxy": f'<rect x="44" y="61" width="122" height="87" rx="10" {stroke}/><path d="M76 105h58M76 125h37" {stroke}/><circle cx="154" cy="67" r="20" fill="#172235" {stroke}/><path d="M154 57v11l8 5" {stroke}/>',
        "camera": f'<path d="M43 79h32l13-18h38l13 18h31v72H43z" {stroke}/><circle cx="106" cy="115" r="26" {stroke}/>',
        "gear": f'<circle cx="106" cy="104" r="25" {stroke}/><path d="M106 45v17m0 84v17M47 104h17m84 0h17M65 63l12 12m58 58 12 12M147 63l-12 12m-58 58-12 12" {stroke}/>',
        "timer": f'<circle cx="106" cy="105" r="57" {stroke}/><path d="M106 72v35l25 17M83 42h46M106 42v15" {stroke}/>',
        "play": f'<path d="M78 59l67 46-67 46z" {filled}/><path d="M47 52v106" {stroke}/>',
        "stop": f'<rect x="65" y="64" width="82" height="82" rx="10" {filled}/>',
        "left": f'<path d="M150 60l-47 45 47 45M109 105h65" {stroke}/>',
        "right": f'<path d="M62 60l47 45-47 45M103 105H38" {stroke}/>',
        "magnet": f'<path d="M67 58v48a39 39 0 0 0 78 0V58M67 58h22m34 0h22M78 136l-18 18m74-18 18 18" {stroke}/>',
        "delete": f'<path d="M66 65h80M87 65V49h38v16M78 65l7 88h43l7-88M94 88v42m24-42v42" {stroke}/>',
        "trim": f'<path d="M70 61v88m68-88v88M91 80H70m65 0h-21M91 130H70m65 0h-21" {stroke}/>',
        "speed": f'<path d="M52 79h70l-18-18m18 18-18 18M160 129H90l18-18m-18 18 18 18" {stroke}/>',
        "ripple": f'<path d="M44 105h38m-18-20 20 20-20 20M168 105h-38m18-20-20 20 20 20" {stroke}/><path d="M94 73v64m18-64v64" {stroke}/>',
        "scissors": f'<circle cx="69" cy="132" r="18" {stroke}/><circle cx="69" cy="76" r="18" {stroke}/><path d="M85 88l71 49M85 120l71-49" {stroke}/>',
        "zoom": f'<circle cx="91" cy="91" r="37" {stroke}/><path d="M119 119l40 40M91 73v36m-18-18h36" {stroke}/>',
        "marker": f'<path d="M67 51h82v58l-41 45-41-45z" {stroke}/><path d="M87 78h42" {stroke}/>',
        "link": f'<path d="M94 127l-13 13a28 28 0 0 1-40-40l24-24a28 28 0 0 1 40 0m1-1 13-13a28 28 0 0 1 40 40l-24 24a28 28 0 0 1-40 0M78 106h57" {stroke}/>',
        "layers": f'<path d="M106 49l69 37-69 37-69-37zM37 118l69 37 69-37M37 92l69 37 69-37" {stroke}/>',
        "wave": f'<path d="M35 106h18l12-42 20 85 22-102 22 118 18-76 13 17h21" {stroke}/>',
        "align": f'<path d="M55 61v86m96-86v86M78 83h56M78 126h56M95 61v86m22-86v86" {stroke}/>',
        "loop": f'<path d="M145 79a48 48 0 1 0 7 57M142 58v29h-29" {stroke}/>',
        "frame": f'<rect x="48" y="58" width="116" height="94" rx="8" {stroke}/><path d="M77 126l22-23 19 17 14-13 19 19" {stroke}/><circle cx="91" cy="84" r="8" {stroke}/>',
        "eye": f'<path d="M36 105s27-45 70-45 70 45 70 45-27 45-70 45-70-45-70-45z" {stroke}/><circle cx="106" cy="105" r="20" {stroke}/>',
        "safe": f'<rect x="48" y="48" width="116" height="116" rx="6" {stroke}/><path d="M73 73h66v66H73zM90 91h32v32H90z" {stroke}/>',
        "fade": f'<path d="M43 142h32l30-70 30 70h34M42 72h124" {stroke}/>',
        "transport": f'<path d="M45 105h104M45 80l-24 25 24 25M151 80l24 25-24 25M95 79v52m18-52v52" {stroke}/>',
        "undo": f'<path d="M91 61L52 100l39 39M55 100h62a36 36 0 0 1 36 36" {stroke}/>',
        "save": f'<path d="M55 48h85l20 20v92H55zM78 48v44h52V48m-49 102h50" {stroke}/>',
        "copy": f'<rect x="78" y="49" width="77" height="91" rx="7" {stroke}/><path d="M59 75H47v91h76v-12" {stroke}/>',
        "key": f'<rect x="44" y="77" width="124" height="58" rx="10" {stroke}/><path d="M69 97h12m14 0h12m14 0h12M68 116h54m11 0h16" {stroke}/>',
        "scope": f'<circle cx="106" cy="105" r="56" {stroke}/><path d="M51 105h110M106 50v110M66 145l80-80" {stroke}/>',
        "node": f'<circle cx="54" cy="105" r="14" {stroke}/><circle cx="107" cy="61" r="14" {stroke}/><circle cx="107" cy="149" r="14" {stroke}/><circle cx="160" cy="105" r="14" {stroke}/><path d="M68 96l25-25m0 68-25-25m28-53v88m28-78 25 25m0 18-25 25" {stroke}/>',
        "color": f'<circle cx="106" cy="105" r="55" fill="#172235" {stroke}/><path d="M106 50a55 55 0 0 1 48 82l-48-27z" fill="#FF6C7A" opacity=".85"/><path d="M106 105l48 27a55 55 0 0 1-96 0z" fill="#55DDA7" opacity=".85"/><path d="M106 105L58 132A55 55 0 0 1 106 50z" fill="#5AA9FF" opacity=".85"/><circle cx="106" cy="105" r="15" fill="#f7fbff"/>',
        "export": f'<path d="M61 54h80l24 24v78H61zM113 71v54m-22-22 22 22 22-22M79 151h69" {stroke}/>',
        "spark": f'<path d="M106 45l13 45 45 15-45 13-13 45-13-45-45-13 45-15z" {stroke}/>',
    }
    return shapes.get(token, shapes["spark"])


def accent_for(item: dict[str, str]) -> str:
    name = item["function"].lower()
    for color_name, color in COLOR_OVERRIDES.items():
        if color_name in name:
            return color
    return SECTION_COLORS[item["section"]]


def render_svg(item: dict[str, str], index: int, filename: str) -> str:
    accent = accent_for(item)
    glyph = glyph_token(item["function"], item["control"], item["section"])
    label = display_lines(item["function"])
    label_svg = "".join(
        f'<text x="128" y="{204 + (line_index * 21)}" text-anchor="middle" fill="#F4F7FC" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700">{html.escape(line)}</text>'
        for line_index, line in enumerate(label)
    )
    section = html.escape(item["section"])
    function = html.escape(item["function"])
    control = html.escape(item["control"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" role="img" aria-labelledby="title-{index} desc-{index}">
  <title id="title-{index}">{function}</title>
  <desc id="desc-{index}">{control}; {section}</desc>
  <rect width="256" height="256" rx="24" fill="#101826"/>
  <rect x="3" y="3" width="250" height="250" rx="21" fill="none" stroke="#2A3A52" stroke-width="3"/>
  <rect x="22" y="20" width="212" height="5" rx="2.5" fill="{accent}"/>
  <g transform="translate(22 13)">{symbol(glyph, accent)}</g>
  <path d="M34 181h188" stroke="#2A3A52" stroke-width="2"/>
  {label_svg}
  <text x="128" y="245" text-anchor="middle" fill="{accent}" font-family="Arial, Helvetica, sans-serif" font-size="9" font-weight="700" letter-spacing="1.4">{html.escape(item["section"].upper()[:26])}</text>
</svg>'''


def main() -> None:
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for index, item in enumerate(ITEMS, start=1):
        slug = slugify(item["function"])
        digest = hashlib.sha1(f"{item['section']}|{item['control']}|{item['function']}".encode()).hexdigest()[:6]
        filename = f"{index:03d}-{slug}-{digest}.svg"
        icon_id = f"rupokar.{index:03d}.{slug}.{digest}"
        (SVG_DIR / filename).write_text(render_svg(item, index, filename), encoding="utf-8")
        manifest.append({
            "id": icon_id,
            "filename": f"svg/{filename}",
            "function": item["function"],
            "control": item["control"],
            "section": item["section"],
            "availability": item["availability"],
            "source_time": item["source_time"],
            "glyph": glyph_token(item["function"], item["control"], item["section"]),
            "accent": accent_for(item),
        })
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tiles = "\n".join(
        f'''<article class="tile"><img src="{html.escape(record['filename'])}" alt="{html.escape(record['function'])}"><h2>{index:03d}. {html.escape(record['function'])}</h2><p>{html.escape(record['control'])}</p><small>{html.escape(record['availability'])} · {html.escape(record['source_time'])}</small></article>'''
        for index, record in enumerate(manifest, start=1)
    )
    BOARD.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rupokar Resolve CT — Icon Board</title><style>body{{margin:0;padding:38px;background:#09101c;color:#eef4ff;font:15px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}h1{{font-size:clamp(2rem,5vw,4rem);line-height:1;margin:0}}.lead{{max-width:800px;color:#b9c8df}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;margin-top:28px}}.tile{{padding:12px;border:1px solid #2a3a52;border-radius:12px;background:#111b2a}}img{{width:100%;height:auto;border-radius:8px;background:#101826}}h2{{font-size:1rem;margin:10px 0 4px}}p,small{{margin:0;color:#b9c8df}}small{{display:block;margin-top:7px;font-size:.75rem}}</style></head><body><h1>Rupokar Resolve CT<br>Icon Board</h1><p class="lead">{len(manifest)} individual SVG source icons generated directly from the audited mapping catalog. Each source is editable and carries its matching function, control, edition, and walkthrough timestamp in the manifest.</p><main class="grid">{tiles}</main></body></html>''', encoding="utf-8")
    print(f"Generated {len(manifest)} SVG icons in {SVG_DIR}")
    print(f"Manifest: {MANIFEST}")
    print(f"Preview: {BOARD}")


if __name__ == "__main__":
    main()
