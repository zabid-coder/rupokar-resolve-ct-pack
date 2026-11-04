from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PRESET_FILE = REPO_ROOT / "keyboard-preset" / "Rupokar_Resolve_Keys.txt"
DOC_FILE = REPO_ROOT / "docs" / "keyboard-preset-map.md"


def test_keyboard_preset_exists():
    assert PRESET_FILE.exists()
    content = PRESET_FILE.read_text(encoding="utf-8")
    assert "Ripple Delete" in content
    assert "Split" in content or "Blade" in content
    assert "Compound Clip" in content


def test_keyboard_preset_no_duplicate_shortcuts():
    assert PRESET_FILE.exists()
    content = PRESET_FILE.read_text(encoding="utf-8")
    shortcuts = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = [part.strip() for part in line.split("=", 1)]
            val = val.strip('"\'')
            if key in ("Version", "Profile"):
                continue
            assert val not in shortcuts, f"Duplicate shortcut '{val}' for '{key}' and '{shortcuts[val]}'"
            shortcuts[val] = key


def test_keyboard_preset_structure():
    assert PRESET_FILE.exists()
    content = PRESET_FILE.read_text(encoding="utf-8")
    assert "Version = 1" in content
    assert 'Profile = "Rupokar Loupedeck CT"' in content


def test_docs_keyboard_preset_map_exists():
    assert DOC_FILE.exists()
    doc_content = DOC_FILE.read_text(encoding="utf-8")
    assert "Keyboard Customization" in doc_content
    assert "Import Preset" in doc_content
    assert "Rupokar_Resolve_Keys.txt" in doc_content
    assert "Rupokar Loupedeck CT" in doc_content
