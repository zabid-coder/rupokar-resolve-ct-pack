#!/usr/bin/env python3
"""Build the official Loupedeck CT (.lp5) profile archive for DaVinci Resolve."""

import json
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "profile"
LP5_PATH = OUTPUT_DIR / "Rupokar-Resolve-CT.lp5"
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
PNG_DIR = REPO_ROOT / "icons" / "export-png"


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
        "isEnabled": True
    }

    profile_info = {
        "$type": "Loupedeck.Service.ApplicationProfile, LoupedeckService",
        "name": "RUPOKAR_RESOLVE_CT_PROFILE",
        "displayName": "Rupokar DaVinci Resolve CT",
        "deviceType": "Loupedeck50",
        "applicationName": "@_davinciresolve-ade6ee31394b4060",
        "nativePluginName": "DaVinciResolve-ADE6EE31394B4060",
        "hasNativePlugin": True,
        "layout": {
            "$type": "Loupedeck.Service.ProfileLayout20, LoupedeckService",
            "deviceType": "Loupedeck50",
            "layoutModes": [
                {
                    "modeName": "main",
                    "touchPages": [
                        {"name": f"Page_{i}", "displayName": f"Workspace {i}"} for i in range(1, 9)
                    ]
                }
            ]
        }
    }

    pkg_yaml = "type: Profile5\nname: RUPOKAR_RESOLVE_CT_PROFILE\ndisplayName: Rupokar DaVinci Resolve CT\nversion: 1.0.0\n"

    with zipfile.ZipFile(LP5_PATH, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("ApplicationInfo.json", json.dumps(app_info, indent=2))
        z.writestr("ProfileInfo.json", json.dumps(profile_info, indent=2))
        z.writestr("metadata/LoupedeckPackage.yaml", pkg_yaml)

        # embed raster icons into ActionIcons/
        for item in manifest:
            svg_filename = Path(item["filename"]).name
            png_path = PNG_DIR / item["type"] / svg_filename.replace(".svg", ".png")
            if png_path.exists():
                z.write(png_path, f"ActionIcons/{png_path.name}")

    print(f"Built Loupedeck CT profile at: {LP5_PATH}")


if __name__ == "__main__":
    main()
