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
