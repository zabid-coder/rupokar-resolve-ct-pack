import json
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILE_LP5 = REPO_ROOT / "profile" / "Rupokar-Resolve-CT.lp5"


def test_profile_lp5_is_valid_zip():
    assert PROFILE_LP5.exists()
    with zipfile.ZipFile(PROFILE_LP5, "r") as z:
        names = z.namelist()
        assert "ProfileInfo.json" in names
        assert "ApplicationInfo.json" in names
        assert "metadata/LoupedeckPackage.yaml" in names

        profile_json = json.loads(z.read("ProfileInfo.json").decode("utf-8"))
        assert profile_json["deviceType"] == "Loupedeck50"
        assert profile_json["displayName"] == "Rupokar DaVinci Resolve CT"


def test_profile_lp5_action_icons():
    assert PROFILE_LP5.exists()
    with zipfile.ZipFile(PROFILE_LP5, "r") as z:
        names = z.namelist()
        action_icons = [n for n in names if n.startswith("ActionIcons/") and n != "ActionIcons/"]
        assert len(action_icons) == 168


def test_profile_lp5_workspaces_and_actions():
    assert PROFILE_LP5.exists()
    with zipfile.ZipFile(PROFILE_LP5, "r") as z:
        profile_json = json.loads(z.read("ProfileInfo.json").decode("utf-8"))
        assert "profileActions" in profile_json
        assert len(profile_json["profileActions"]) == 168
        assert "actionImages90" in profile_json
        assert len(profile_json["actionImages90"]) > 0

        workspaces = profile_json["layout"]["layoutModes"][0]["workspaces"]
        assert len(workspaces) == 8
        for ws in workspaces:
            assert "pressPages" in ws
            assert "rotatePages" in ws

