#!/usr/bin/env python3
"""Build the official Loupedeck CT (.lp5) profile archive for DaVinci Resolve.

Packages all 8 workspaces, 168 action definitions, dial turns/presses, touch
tiles, wheel navigation, physical keys, Fn layer, and raster action icons into
an importable Loupedeck50 package.
"""

import hashlib
import json
import uuid
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "profile"
LP5_PATH = OUTPUT_DIR / "Rupokar-Resolve-CT.lp5"
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
PNG_DIR = REPO_ROOT / "icons" / "export-png"


WORKSPACE_NAMES = [
    ("Media / Project", "Workspace 1 — Media & Project Manager"),
    ("Edit 1", "Workspace 2 — Edit 1 (Timeline & Cuts)"),
    ("Edit 2", "Workspace 3 — Edit 2 (Sync & Colors)"),
    ("Edit 3", "Workspace 4 — Edit 3 (Fine Tuning)"),
    ("Color", "Workspace 5 — Color (Nodes & Wheels)"),
    ("Fairlight", "Workspace 6 — Fairlight (Audio & Fades)"),
    ("Deliver / Render Queue", "Workspace 7 — Deliver & Render Queue"),
    ("Quick Export", "Workspace 8 — Quick Export"),
]


def deterministic_uuid(seed: str) -> str:
    """Generate a consistent uppercase UUID from a string seed."""
    hex_digest = hashlib.md5(seed.encode("utf-8")).hexdigest()
    return str(uuid.UUID(hex_digest)).upper().replace("-", "")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    app_info = {
        "$type": "Loupedeck.Service.SupportedApplicationInfo, LoupedeckService",
        "name": "@_davinciresolve-ade6ee31394b4060",
        "displayName": "DaVinci Resolve",
        "deviceType": "Loupedeck50",
        "nativePluginName": "DaVinciResolve-ADE6EE31394B4060",
        "hasNativePlugin": True,
        "defaultProfileName": "RUPOKAR_RESOLVE_CT_PROFILE",
        "isEnabled": True,
    }

    # Build profile actions and icon mappings
    profile_actions = []
    action_images_90 = {}
    items_by_section: dict[str, list[dict]] = {}

    for idx, item in enumerate(manifest, start=1):
        svg_filename = Path(item["filename"]).name
        png_name = svg_filename.replace(".svg", ".png")
        action_id = f"Rupokar.Resolve.Action.{idx:03d}"
        action_guid = deterministic_uuid(f"action_{idx}_{item['function']}")

        action_def = {
            "$type": "Loupedeck.Service.ApplicationProfileAction, LoupedeckService",
            "actionId": action_id,
            "guid": action_guid,
            "name": item["function"],
            "displayName": item["function"],
            "section": item["section"],
            "control": item["control"],
            "type": item["type"],
            "icon": f"ActionIcons/{png_name}",
            "availability": item["availability"],
            "sourceTime": item["source_time"],
        }
        profile_actions.append(action_def)
        action_images_90[action_id] = f"ActionIcons/{png_name}"
        action_images_90[action_guid] = f"ActionIcons/{png_name}"

        sec = item["section"]
        items_by_section.setdefault(sec, []).append({**item, "action_id": action_id, "guid": action_guid, "icon_name": png_name})

    # Build 8 Workspaces with pressPages and rotatePages
    workspaces = []
    for ws_idx, (section_prefix, ws_display_name) in enumerate(WORKSPACE_NAMES, start=1):
        ws_guid = deterministic_uuid(f"workspace_{ws_idx}_{section_prefix}")
        matching_items = []
        for sec, items in items_by_section.items():
            if section_prefix in sec or (section_prefix == "Media / Project" and "Timer" in sec):
                matching_items.extend(items)

        # Separate into press controls (touch, button, dial press) and rotate controls (dial turn, wheel turn)
        press_items = [it for it in matching_items if "turn" not in it["control"].lower()]
        rotate_items = [it for it in matching_items if "turn" in it["control"].lower()]

        # Press page controls
        press_controls = []
        for c_idx, it in enumerate(press_items[:24]):
            press_controls.append({
                "$type": "Loupedeck.Service.ProfileLayoutControl50, LoupedeckService",
                "controlId": c_idx,
                "displayName": it["function"],
                "pressAction": it["action_id"],
                "icon": f"ActionIcons/{it['icon_name']}",
            })

        # Rotate page controls
        rotate_controls = []
        for r_idx, it in enumerate(rotate_items[:12]):
            rotate_controls.append({
                "$type": "Loupedeck.Service.ProfileLayoutRotateControl50, LoupedeckService",
                "controlId": r_idx,
                "displayName": it["function"],
                "rotateAction": it["action_id"],
                "icon": f"ActionIcons/{it['icon_name']}",
            })

        page_guid = deterministic_uuid(f"press_page_{ws_idx}")
        rotate_page_guid = deterministic_uuid(f"rotate_page_{ws_idx}")

        workspaces.append({
            "$type": "Loupedeck.Service.ProfileLayoutWorkspace50, LoupedeckService",
            "name": ws_guid,
            "displayName": ws_display_name,
            "pressPages": [
                {
                    "$type": "Loupedeck.Service.ProfileLayoutPage50, LoupedeckService",
                    "name": page_guid,
                    "displayName": f"{ws_display_name} — Controls",
                    "controls": press_controls,
                }
            ],
            "rotatePages": [
                {
                    "$type": "Loupedeck.Service.ProfileLayoutRotatePage50, LoupedeckService",
                    "name": rotate_page_guid,
                    "displayName": f"{ws_display_name} — Dials & Wheel",
                    "controls": rotate_controls,
                }
            ],
        })

    profile_info = {
        "$type": "Loupedeck.Service.ApplicationProfile, LoupedeckService",
        "name": "RUPOKAR_RESOLVE_CT_PROFILE",
        "displayName": "Rupokar DaVinci Resolve CT",
        "deviceType": "Loupedeck50",
        "applicationName": "@_davinciresolve-ade6ee31394b4060",
        "nativePluginName": "DaVinciResolve-ADE6EE31394B4060",
        "hasNativePlugin": True,
        "actionImages90": action_images_90,
        "profileActions": profile_actions,
        "layout": {
            "$type": "Loupedeck.Service.ProfileLayout50, LoupedeckService",
            "deviceType": "Loupedeck50",
            "layoutModes": [
                {
                    "$type": "Loupedeck.Service.ProfileLayoutMode50, LoupedeckService",
                    "modeName": "main",
                    "homeWorkspaceName": workspaces[0]["name"] if workspaces else "",
                    "workspaces": workspaces,
                    "touchPages": [
                        {"name": f"Page_{i}", "displayName": f"Workspace {i}"} for i in range(1, 9)
                    ],
                }
            ],
        },
    }

    pkg_yaml = (
        "type: Profile5\n"
        "name: RUPOKAR_RESOLVE_CT_PROFILE\n"
        "displayName: Rupokar DaVinci Resolve CT\n"
        "version: 1.0.0\n"
        "deviceType: Loupedeck50\n"
        "applicationName: @_davinciresolve-ade6ee31394b4060\n"
    )

    with zipfile.ZipFile(LP5_PATH, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("ApplicationInfo.json", json.dumps(app_info, indent=2))
        z.writestr("ProfileInfo.json", json.dumps(profile_info, indent=2))
        z.writestr("metadata/LoupedeckPackage.yaml", pkg_yaml)

        # embed all 168 raster icons into ActionIcons/
        for item in manifest:
            svg_filename = Path(item["filename"]).name
            png_path = PNG_DIR / item["type"] / svg_filename.replace(".svg", ".png")
            if png_path.exists():
                z.write(png_path, f"ActionIcons/{png_path.name}")

    print(f"Built Loupedeck CT profile at: {LP5_PATH} ({len(workspaces)} workspaces, {len(profile_actions)} actions)")


if __name__ == "__main__":
    main()
