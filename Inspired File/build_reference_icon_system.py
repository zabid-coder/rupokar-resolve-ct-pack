#!/usr/bin/env python3
"""Extract the exact CT control art from the supplied walkthrough for every mapping.

The resulting PNGs deliberately reuse the source walkthrough's own icon and label
art. They replace generic concept icons with visual evidence of the real mapping.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
from pathlib import Path

from build_master_reference import ITEMS


SOURCE_DIR = Path(__file__).resolve().parent
SOURCE_FRAMES = SOURCE_DIR / "Loupedeck-CT-Master-Reference" / "images"
VIDEO = SOURCE_DIR / "Loupedeck CT for Davinci Resolve Every Button Explained (Full Walkthrough)-1920x1080-avc1-mp4a.mp4"
ROOT = SOURCE_DIR / "Rupokar-Resolve-CT-Icon-System"
PNG_DIR = ROOT / "reference-png"
MANIFEST = ROOT / "reference-icon-manifest.json"
BOARD = ROOT / "Icon-Board.html"

TOUCH_ORIGIN = (1436, 191)
TOUCH_SIZE = (86, 87)
TOUCH_STEP = (96, 96)
DIALS = {
    "top-left": (1413, 227), "middle-left": (1413, 334), "bottom-left": (1413, 438),
    "top-right": (1847, 227), "middle-right": (1847, 334), "bottom-right": (1847, 438),
}
ROUND_CENTERS = {1: (1395, 502), 2: (1457, 502), 3: (1519, 502), 4: (1582, 502), 5: (1644, 502), 6: (1707, 502), 7: (1769, 502), 8: (1832, 502)}
KEY_CENTERS = {"a": (1747, 591), "b": (1793, 591), "c": (1747, 638), "d": (1793, 638), "e": (1793, 685), "fn": (1747, 685), "undo": (1433, 638), "save": (1479, 638)}
TOUCH_POSITION = {
    "top-left": (0, 0), "top row": (1, 0), "top-right": (3, 0),
    "middle-left": (0, 1), "middle row": (1, 1), "middle-right": (3, 1),
    "bottom-left": (0, 2), "bottom row": (1, 2), "bottom-right": (3, 2),
}


def crop_for(item: dict[str, str]) -> tuple[int, int, int, int]:
    control = item["control"].lower()
    function = item["function"].lower()
    if control == "alternate bottom row":
        # Exact same action labels are visible on Edit 3 in the supplied video.
        column = 2 if function == "duplicate timeline" else 1
        return TOUCH_ORIGIN[0] + column * TOUCH_STEP[0], TOUCH_ORIGIN[1] + 2 * TOUCH_STEP[1], *TOUCH_SIZE
    if control == "free edition deliver":
        # The walkthrough shows the Free Deliver page as a complete layout.
        return 1425, 190, 336, 270
    position_match = re.search(r"· (top-left|top row|top-right|middle-left|middle row|middle-right|bottom-left|bottom row|bottom-right)", control)
    # Fairlight intentionally uses only the lower two rows, so its labels—not
    # its serial action numbers—are the reliable control coordinates.
    if position_match and item["section"] == "Fairlight":
        column, row = TOUCH_POSITION[position_match.group(1)]
        x = TOUCH_ORIGIN[0] + column * TOUCH_STEP[0]
        y = TOUCH_ORIGIN[1] + row * TOUCH_STEP[1]
        return x, y, *TOUCH_SIZE
    touch_match = re.search(r"(?:timer )?touch (\d+)", control)
    if touch_match:
        number = int(touch_match.group(1))
        column, row = (number - 1) % 4, (number - 1) // 4
        x = TOUCH_ORIGIN[0] + column * TOUCH_STEP[0]
        y = TOUCH_ORIGIN[1] + row * TOUCH_STEP[1]
        return x, y, *TOUCH_SIZE
    if control.startswith("swipe-right"):
        # The swiped Deliver page places Clear Queue / Export Folder / Thumbnail
        # on top-row columns 1 / 2 / 3 even though the catalog presents a task order.
        columns = {"clear render queue": 0, "export folder": 1, "thumbnail": 2}
        column = columns.get(function, 0)
        return TOUCH_ORIGIN[0] + column * TOUCH_STEP[0], TOUCH_ORIGIN[1], *TOUCH_SIZE
    if "center wheel" in control:
        return 1512, 567, 200, 200
    dial_match = re.search(r"(top-left|middle-left|bottom-left|top-right|middle-right|bottom-right) dial", control)
    if dial_match:
        cx, cy = DIALS[dial_match.group(1)]
        return cx - 43, cy - 43, 86, 86
    round_match = re.search(r"round button (\d+)", control)
    if round_match and not control.startswith("fn +"):
        cx, cy = ROUND_CENTERS[int(round_match.group(1))]
        return cx - 31, cy - 31, 62, 62
    if control in {"undo", "save"}:
        cx, cy = KEY_CENTERS[control]
        return cx - 31, cy - 31, 62, 62
    square_match = re.fullmatch(r"square ([abcde])", control)
    if square_match:
        cx, cy = KEY_CENTERS[square_match.group(1)]
        return cx - 31, cy - 31, 62, 62
    if control.startswith("fn + round"):
        number = int(re.search(r"round (\d+)", control).group(1))
        cx, _ = ROUND_CENTERS[number]
        # Display round-page selection with the Fn control below it.
        return cx - 42, 471, 84, 245
    if control.startswith("fn +"):
        key = control[-1]
        cx, cy = KEY_CENTERS.get(key, KEY_CENTERS["fn"])
        # Include the Fn key and modified key together wherever they sit.
        return min(cx, KEY_CENTERS["fn"][0]) - 37, min(cy, KEY_CENTERS["fn"][1]) - 37, abs(cx - KEY_CENTERS["fn"][0]) + 74, abs(cy - KEY_CENTERS["fn"][1]) + 74
    # Every catalog item should resolve to a concrete CT control crop.
    raise ValueError(f"No crop rule for {item['control']!r} / {item['function']!r}")


def timestamp_midpoint(timestamp_range: str) -> float:
    timestamp_range = timestamp_range.split(";", 1)[0].strip()
    first, second = [part.strip() for part in timestamp_range.split("–", 1)]
    def parse(value: str) -> float:
        hours, minutes, seconds = value.split(":")
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    return (parse(first) + parse(second)) / 2


def item_frame(item: dict[str, str]) -> Path | None:
    if item["control"].lower() == "alternate bottom row":
        frame = "edit3"
    elif item["control"].lower() == "free edition deliver":
        frame = "free-deliver"
    else:
        frame = item["frame"]
    path = SOURCE_FRAMES / f"{frame}.jpg"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def run_crop(ffmpeg: str, source: Path, crop: tuple[int, int, int, int], destination: Path, timestamp: float | None = None) -> None:
    x, y, width, height = crop
    filter_expr = f"crop={width}:{height}:{x}:{y},scale=256:256:force_original_aspect_ratio=decrease,pad=256:256:(ow-iw)/2:(oh-ih)/2:color=0x101826"
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
    if timestamp is not None:
        command.extend(["-ss", f"{timestamp:.3f}"])
    command.extend(["-i", str(source), "-vf", filter_expr, "-frames:v", "1", str(destination)])
    subprocess.run(command, check=True)


def main() -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required to extract reference icons.")
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str]] = []
    for index, item in enumerate(ITEMS, start=1):
        filename = f"{index:03d}.png"
        crop = crop_for(item)
        source_frame = item_frame(item)
        # Alternate Free-edition layouts are only shown as page overviews. Every
        # normal mapping uses its own action timestamp, so the icon crop shows
        # the action while it is demonstrated/highlighted in the walkthrough.
        source = source_frame if item["control"].lower() in {"alternate bottom row", "free edition deliver"} else VIDEO
        timestamp = None if source is source_frame else timestamp_midpoint(item["source_time"])
        run_crop(ffmpeg, source, crop, PNG_DIR / filename, timestamp)
        manifest.append({
            "id": f"rupokar.reference.{index:03d}",
            "filename": f"reference-png/{filename}",
            "function": item["function"],
            "control": item["control"],
            "section": item["section"],
            "availability": item["availability"],
            "source_time": item["source_time"],
            "source_frame": f"../Loupedeck-CT-Master-Reference/images/{item['frame']}.jpg" if source is source_frame else "walkthrough-video",
            "source_timestamp_seconds": timestamp,
            "crop": {"x": crop[0], "y": crop[1], "width": crop[2], "height": crop[3]},
        })
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tiles = "\n".join(
        f'''<article class="tile"><img src="{html.escape(record['filename'])}" alt="Exact CT crop: {html.escape(record['function'])}"><div><p class="number">#{index:03d} · {html.escape(record['section'])}</p><h2>{html.escape(record['function'])}</h2><p class="control">{html.escape(record['control'])}</p><small>{html.escape(record['availability'])} · {html.escape(record['source_time'])}</small></div></article>'''
        for index, record in enumerate(manifest, start=1)
    )
    BOARD.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rupokar Resolve CT — Exact Reference Icon Board</title><style>body{{margin:0;padding:38px;background:#09101c;color:#eef4ff;font:15px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}h1{{font-size:clamp(2rem,5vw,4rem);line-height:1;margin:0}}.lead{{max-width:860px;color:#b9c8df}}.notice{{max-width:1000px;padding:15px 18px;border-left:4px solid #4de2e1;background:#11263a}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin-top:28px}}.tile{{display:grid;grid-template-columns:128px 1fr;gap:12px;padding:12px;border:1px solid #2a3a52;border-radius:12px;background:#111b2a}}img{{width:128px;height:128px;border-radius:8px;background:#101826;image-rendering:auto}}h2{{font-size:1.03rem;margin:2px 0 4px}}p{{margin:0}}.number{{color:#54d7bf;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}.control{{color:#eef4ff;font-weight:700;margin-top:5px}}small{{display:block;margin-top:7px;color:#b9c8df;font-size:.75rem}}@media(max-width:560px){{body{{padding:20px}}.grid{{grid-template-columns:1fr}}}}</style></head><body><h1>Rupokar Resolve CT<br>Exact Reference Icon Board</h1><p class="lead">{len(manifest)} individual assets extracted from the supplied walkthrough. Each asset is the actual CT button, dial, wheel, or physical-key crop seen in the reference video—no generic substitute glyphs.</p><p class="notice"><strong>Verification rule:</strong> the name, control placement, edition, and timestamp are kept beside each exact source crop. This makes every action easy to compare against the catalog before it is packaged in the final CT profile.</p><main class="grid">{tiles}</main></body></html>''', encoding="utf-8")
    print(f"Generated {len(manifest)} exact reference icon crops in {PNG_DIR}")
    print(f"Updated board: {BOARD}")


if __name__ == "__main__":
    main()
