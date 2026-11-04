#!/usr/bin/env python3
"""Export all 168 SVGs into high-DPI PNGs for Loupedeck packaging.

Uses PyQt6 QtSvg (fast, headless, pixel-perfect anti-aliased rendering) with
automatic fallback to cairosvg or macOS QuickLook (qlmanage).
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
SVG_ROOT = REPO_ROOT / "icons" / "final-svg"
PNG_ROOT = REPO_ROOT / "icons" / "export-png"

# Setup PyQt6 offscreen rendering if available
_PYQT_AVAILABLE = False
try:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QGuiApplication, QImage, QPainter
    from PyQt6.QtSvg import QSvgRenderer

    _QAPP = QGuiApplication.instance() or QGuiApplication([])
    _PYQT_AVAILABLE = True
except ImportError:
    _PYQT_AVAILABLE = False

_CAIROSVG_AVAILABLE = False
try:
    import cairosvg

    _CAIROSVG_AVAILABLE = True
except ImportError:
    _CAIROSVG_AVAILABLE = False


def export_svg_to_png(svg_path: Path, png_path: Path, width: int) -> None:
    """Export an SVG file to high-DPI PNG at specified base width (scaled 2x)."""
    png_path.parent.mkdir(parents=True, exist_ok=True)

    # Method 1: PyQt6 QSvgRenderer (preferred: fast, crisp, exact aspect ratio)
    if _PYQT_AVAILABLE:
        renderer = QSvgRenderer(str(svg_path))
        if renderer.isValid():
            sz = renderer.defaultSize()
            target_w = width * 2
            if sz.width() > 0 and sz.height() > 0:
                target_h = int(round(target_w * sz.height() / sz.width()))
            else:
                target_h = target_w

            img = QImage(target_w, target_h, QImage.Format.Format_ARGB32)
            img.fill(Qt.GlobalColor.transparent)
            painter = QPainter(img)
            renderer.render(painter)
            painter.end()

            if img.save(str(png_path)):
                return

    # Method 2: cairosvg if available
    if _CAIROSVG_AVAILABLE:
        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_path),
            output_width=width * 2,
        )
        if png_path.exists() and png_path.stat().st_size > 0:
            return

    # Method 3: macOS qlmanage fallback
    tmp_dir = png_path.parent / f"_tmp_{png_path.stem}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    try:
        cmd = ["qlmanage", "-t", "-s", str(width * 2), "-o", str(tmp_dir), str(svg_path)]
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
            check=True,
        )
        generated = tmp_dir / f"{svg_path.name}.png"
        if generated.exists():
            shutil.move(str(generated), str(png_path))
            return
    except Exception as exc:
        raise RuntimeError(f"Failed to export {svg_path} to PNG: {exc}") from exc
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    if not png_path.exists():
        raise RuntimeError(f"Export failed: target PNG {png_path} was not created.")


def main():
    if not MANIFEST_PATH.exists():
        print(f"Error: manifest not found at {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    print(f"Exporting {len(items)} SVGs to PNG...")
    widths = {"touch": 256, "dial": 120, "physical": 320}

    exported_count = 0
    for item in items:
        svg_file = REPO_ROOT / "icons" / item["filename"]
        target_png = PNG_ROOT / item["type"] / svg_file.name.replace(".svg", ".png")
        export_svg_to_png(svg_file, target_png, widths[item["type"]])
        exported_count += 1

    print(f"Raster export complete: {exported_count} PNGs exported to {PNG_ROOT}")


if __name__ == "__main__":
    main()
