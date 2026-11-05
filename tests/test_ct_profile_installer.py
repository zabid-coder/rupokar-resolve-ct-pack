"""Tests for Loupedeck CT Profile Installer and Layout integrity.

Verifies that all 8 workspaces are fully populated with 12 controls each,
all dials have active turn and press assignments, Round 1-8 navigation macros
are wired with ChangeWorkspace and Resolve shortcuts, and 168 actions are defined.
"""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
PROFILE_DIR = (
    Path.home()
    / "Library"
    / "Application Support"
    / "Logi"
    / "LogiPluginService"
    / "Applications"
    / "Loupedeck20"
    / "com.blackmagic-design.davinciresolve"
    / "Profiles"
    / "D94DAE0ACAAC4F4DA61287C9CB088BC8"
)
PROFILE_INFO_PATH = PROFILE_DIR / "ProfileInfo.json"


@pytest.fixture(scope="module")
def profile_data():
    assert PROFILE_INFO_PATH.exists(), f"ProfileInfo.json not found at {PROFILE_INFO_PATH}"
    with open(PROFILE_INFO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_profile_basic_metadata(profile_data):
    assert profile_data["name"] == "D94DAE0ACAAC4F4DA61287C9CB088BC8"
    assert profile_data["displayName"] == "DaVinci Resolve Rupokar"
    assert profile_data["deviceType"] == "Loupedeck20"
    assert len(profile_data["profileActions"]) == 168


def test_eight_workspaces_exist(profile_data):
    mode = profile_data["layout"]["layoutModes"][0]
    workspaces = mode["workspaces"]
    assert len(workspaces) == 8
    expected_titles = [
        "Workspace 1 — Media & Project",
        "Workspace 2 — Edit 1 (Timeline & Cuts)",
        "Workspace 3 — Edit 2 (Sync & Colors)",
        "Workspace 4 — Edit 3 (Fine Tuning)",
        "Workspace 5 — Color (Nodes & Wheels)",
        "Workspace 6 — Fairlight (Audio & Fades)",
        "Workspace 7 — Deliver & Render Queue",
        "Workspace 8 — Quick Export",
    ]
    for ws, expected in zip(workspaces, expected_titles):
        assert ws["displayName"] == expected


def test_zero_empty_touch_buttons(profile_data):
    mode = profile_data["layout"]["layoutModes"][0]
    tp_dict = {page["name"]: page for page in mode.get("touchPages", [])}
    for ws in mode["workspaces"]:
        for tp_name in ws["touchPageNames"]:
            page = tp_dict[tp_name]
            controls = page["controls"]
            assert len(controls) == 12, f"{page['displayName']} must have 12 controls"
            active_count = sum(1 for c in controls if c.get("pressAction") is not None)
            assert active_count == 12, f"{page['displayName']} has empty holes! ({active_count}/12)"


def test_all_dials_active(profile_data):
    mode = profile_data["layout"]["layoutModes"][0]
    ep_dict = {page["name"]: page for page in mode.get("encoderPages", [])}
    for ws in mode["workspaces"]:
        for ep_name in ws["encoderPageNames"]:
            page = ep_dict[ep_name]
            controls = page["controls"]
            assert len(controls) == 6, f"{page['displayName']} must have 6 dials"
            for d_idx, c in enumerate(controls, 1):
                assert c.get("rotateAction") is not None, f"Dial {d_idx} missing rotate action in {page['displayName']}"
                assert c.get("pressAction") is not None, f"Dial {d_idx} missing press action in {page['displayName']}"


def test_round_navigation_macros(profile_data):
    round_page = profile_data["layout"]["roundPage"]
    macros = {m["name"]: m for m in profile_data.get("macroCommands", [])}
    assert len(round_page["controls"]) == 8

    for r_idx, c in enumerate(round_page["controls"], 1):
        act = c.get("pressAction")
        assert act is not None, f"Round button {r_idx} has no action"
        macro_id = act.split("___")[-1]
        macro = macros.get(macro_id)
        assert macro is not None, f"Macro {macro_id} not defined"
        subcmds = macro.get("actions", [])
        assert len(subcmds) == 2, f"Round button {r_idx} macro must have 2 actions (ChangeWS + Shortcut)"
        # Check ChangeWorkspace action
        assert any("$@Generic___@ChangeWorkspace___Main|" in str(s) for s in subcmds)


def test_wheel_page_configured(profile_data):
    mode = profile_data["layout"]["layoutModes"][0]
    wheel_pages = mode["wheelPages"]
    assert len(wheel_pages) >= 1
    wp = wheel_pages[0]
    assert wp["templateName"] == "WheelToolGeneric3x1Horizontal"
    assert wp["parameters"]["adjustment"].startswith("$@Generic___@MacroAdjustment___")
