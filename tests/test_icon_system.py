import json
from pathlib import Path
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
TOUCH_DIR = REPO_ROOT / "icons" / "final-svg" / "touch"
DIAL_DIR = REPO_ROOT / "icons" / "final-svg" / "dial"
PHYSICAL_DIR = REPO_ROOT / "icons" / "final-svg" / "physical"

EXPECTED_DIMS = {
    "touch": ("256", "256"),
    "dial": ("120", "180"),
    "physical": ("320", "160"),
}


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


def test_svg_dimensions_and_xml_validity():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        file_path = REPO_ROOT / "icons" / item["filename"]
        assert file_path.exists(), f"File {file_path} must exist"
        content = file_path.read_text(encoding="utf-8")

        # ElementTree will raise ParseError if XML is malformed or has duplicate attributes
        root = ET.fromstring(content)
        expected_w, expected_h = EXPECTED_DIMS[item["type"]]
        assert root.attrib["width"] == expected_w, f"File {file_path} width mismatch: expected {expected_w}, got {root.attrib.get('width')}"
        assert root.attrib["height"] == expected_h, f"File {file_path} height mismatch: expected {expected_h}, got {root.attrib.get('height')}"
