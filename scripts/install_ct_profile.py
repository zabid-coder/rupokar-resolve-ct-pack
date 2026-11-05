#!/usr/bin/env python3
"""Installer script for Rupokar Loupedeck CT Profile directly into Loupedeck20 format.

Injects all 8 workspaces, 168 actions, icons, dials, wheel, round buttons, and physical keys
into the user's active Loupedeck CT profile 'D94DAE0ACAAC4F4DA61287C9CB088BC8'.
Includes round-button macro navigation to switch workspaces & DaVinci Resolve pages.
"""

import hashlib
import json
import os
import shutil
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "icons" / "final-icon-manifest.json"
PNG_DIR = REPO_ROOT / "icons" / "export-png"
SHORTCUTS_TXT = REPO_ROOT / "keyboard-preset" / "Rupokar_Resolve_Keys.txt"

TARGET_PROFILE_ID = "D94DAE0ACAAC4F4DA61287C9CB088BC8"
PROFILE_DIR = Path(
    f"/Users/audiovisual/Library/Application Support/Logi/LogiPluginService/Applications/Loupedeck20/com.blackmagic-design.davinciresolve/Profiles/{TARGET_PROFILE_ID}"
)
ACTION_IMAGES_DIR = PROFILE_DIR / "ActionImages"


def deterministic_guid(seed: str) -> str:
    """Generate a consistent uppercase UUID without dashes from a seed string."""
    hex_digest = hashlib.md5(seed.encode("utf-8")).hexdigest()
    return str(uuid.UUID(hex_digest)).upper().replace("-", "")


# Resolve keyboard shortcut mapping
SHORTCUT_MAP = {
    # Navigation / Pages
    "media page": "Shift+Key2___132105___Shift+2___",
    "edit page 1": "Shift+Key4___132105___Shift+4___",
    "edit page 2": "Shift+Key4___132105___Shift+4___",
    "edit page 3": "Shift+Key4___132105___Shift+4___",
    "color page": "Shift+Key6___132105___Shift+6___",
    "fairlight page": "Shift+Key7___132105___Shift+7___",
    "deliver page": "Shift+Key8___132105___Shift+8___",
    "quick export": "Shift+Key9___132105___Shift+9___",
    # Media Pool
    "import media": "ControlOrCommand+KeyI___132105___Cmd+I___",
    "new bin": "ControlOrCommand+Shift+KeyN___132105___Cmd+Shift+N___",
    "project notes": "Shift+Key9___132105___Shift+9___",
    "project manager": "Shift+Key1___132105___Shift+1___",
    "project settings": "Shift+Key9___132105___Shift+9___",
    "new project": "ControlOrCommand+KeyN___132105___Cmd+N___",
    "new timeline": "ControlOrCommand+KeyN___132105___Cmd+N___",
    "duplicate timeline": "ControlOrCommand+Shift+KeyD___132105___Cmd+Shift+D___",
    # Edit Page
    "split": "ControlOrCommand+KeyB___132105___Cmd+B___",
    "delete": "Back___132105___Back___",
    "ripple delete": "Shift+Back___132105___Shift+Back___",
    "trim start": "Shift+Oem4___132105___Shift+Oem4___",
    "trim end": "Shift+Oem6___132105___Shift+Oem6___",
    "ripple start": "ControlOrCommand+Shift+Oem4___132105___Cmd+Shift+Oem4___",
    "ripple end": "ControlOrCommand+Shift+Oem6___132105___Cmd+Shift+Oem6___",
    "select forward all": "KeyY___132105___Y___",
    "select backward all": "ControlOrCommand+KeyY___132105___Cmd+Y___",
    "snapping": "KeyN___132105___N___",
    "retime controls": "ControlOrCommand+KeyR___132105___Cmd+R___",
    "change clip speed": "ControlOrCommand+KeyR___132105___Cmd+R___",
    "play/pause": "Space___132105___Space___",
    "play": "Space___132105___Space___",
    "shuttle": "KeyL___132105___L___",
    "fast shuttle": "Shift+KeyL___132105___Shift+L___",
    "next clip": "ArrowDown___132105___Down___",
    "add marker": "KeyM___132105___M___",
    "delete all markers": "ControlOrCommand+Alt+KeyM___132105___Cmd+Opt+M___",
    "linked selection": "ControlOrCommand+Shift+KeyL___132105___Cmd+Shift+L___",
    "link clips": "ControlOrCommand+Alt+KeyL___132105___Cmd+Opt+L___",
    "compound clip": "Alt+KeyC___132105___Opt+C___",
    "mark in": "KeyI___132105___I___",
    "mark out": "KeyO___132105___O___",
    "loop": "ControlOrCommand+OemSlash___132105___Cmd+/___",
    "match frame": "KeyF___132105___F___",
    "cinema viewer": "ControlOrCommand+KeyF___132105___Cmd+F___",
    "enable clip": "KeyD___132105___D___",
    "freeze frame": "Shift+KeyR___132105___Shift+R___",
    "find clip": "Alt+KeyF___132105___Opt+F___",
    "crossfade": "ControlOrCommand+KeyT___132105___Cmd+T___",
    "swap left": "ControlOrCommand+Shift+OemComma___132105___Cmd+Shift+,___",
    "swap right": "ControlOrCommand+Shift+OemPeriod___132105___Cmd+Shift+.___",
    "undo": "ControlOrCommand+KeyZ___132105___Cmd+Z___",
    "save": "ControlOrCommand+KeyS___132105___Cmd+S___",
    "save project": "ControlOrCommand+KeyS___132105___Cmd+S___",
    "timeline zoom": "Shift+KeyZ___132105___Shift+Z___",
    "zoom to fit": "Shift+KeyZ___132105___Shift+Z___",
    # Panels & Fn
    "media pool panel": "ControlOrCommand+Key1___132105___Cmd+1___",
    "effects library panel": "ControlOrCommand+Key2___132105___Cmd+2___",
    "inspector panel": "ControlOrCommand+Key3___132105___Cmd+3___",
    "mixer panel": "ControlOrCommand+Key4___132105___Cmd+4___",
    "power bins panel": "ControlOrCommand+Key5___132105___Cmd+5___",
    "metadata panel": "ControlOrCommand+Key6___132105___Cmd+6___",
    "index panel": "ControlOrCommand+Key7___132105___Cmd+7___",
    "copy": "ControlOrCommand+KeyC___132105___Cmd+C___",
    "paste attributes": "Alt+KeyV___132105___Opt+V___",
    # Color Page
    "add node": "Alt+KeyS___132105___Opt+S___",
    "node before": "Shift+KeyS___132105___Shift+S___",
    "grab still": "ControlOrCommand+Alt+KeyG___132105___Cmd+Opt+G___",
    "bypass all grades": "Shift+KeyD___132105___Shift+D___",
    "scopes": "ControlOrCommand+Shift+KeyW___132105___Cmd+Shift+W___",
    "light box": "Shift+KeyF___132105___Shift+F___",
    # Deliver / Export
    "add to queue": "ControlOrCommand+Shift+KeyA___132105___Cmd+Shift+A___",
}


def make_profile_action(item: dict) -> tuple[dict, str]:
    """Create an ApplicationProfileCommand dict and return (action_dict, action_name)."""
    fn = item["function"]
    guid = deterministic_guid(f"rupokar_action_{item['id']}_{fn}")
    action_name = f"$@Generic___@ProfileAction___{guid}"

    kb_key = SHORTCUT_MAP.get(fn.lower())
    if not kb_key:
        kb_key = "Space___132105___Space___" if "play" in fn.lower() else ""

    action_params = {
        "$type": "Loupedeck.ActionEditorActionParameters, PluginApi",
        "parameters": {
            "$type": "Loupedeck.StringDictionaryNoCase, PluginApi",
        },
        "count": 1 if kb_key else 0,
    }
    if kb_key:
        action_params["parameters"]["keyboardKey"] = kb_key

    action_def = {
        "$type": "Loupedeck.Service.ApplicationProfileCommand, LoupedeckService",
        "isCommand": True,
        "name": action_name,
        "templateActionName": "$@Generic___@KeyboardKey" if kb_key else None,
        "actionParameters": action_params if kb_key else None,
        "displayName": fn,
        "description": item.get("detail", ""),
        "groupName": item["section"],
        "superGroupName": "@desktop",
        "isProfileAction": True,
        "isMultiState": False,
        "isResetCommand": False,
        "adjustmentName": None,
        "states": None,
    }
    return action_def, action_name


def main():
    print(f"Target profile directory: {PROFILE_DIR}")
    if not PROFILE_DIR.exists():
        raise FileNotFoundError(f"Profile directory {PROFILE_DIR} does not exist!")

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    print(f"Loaded {len(manifest)} manifest items.")

    ACTION_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Build profileActions and copy PNGs with exact action naming
    profile_actions = []
    action_by_id = {}

    for item in manifest:
        action_def, action_name = make_profile_action(item)
        profile_actions.append(action_def)
        action_by_id[item["id"]] = action_name

        svg_name = Path(item["filename"]).name
        png_name = svg_name.replace(".svg", ".png")
        src_png = PNG_DIR / item["type"] / png_name
        if src_png.exists():
            dst_png = ACTION_IMAGES_DIR / f"{action_name}.png"
            shutil.copy(src_png, dst_png)

    # 2. Build 8 Workspaces
    WORKSPACE_DEFS = [
        ("Workspace 1 — Media & Project", ["Navigation", "Media / Project", "Media / Break Timer"], "Shift+Key2___132105___Shift+2___"),
        ("Workspace 2 — Edit 1 (Timeline & Cuts)", ["Edit 1"], "Shift+Key4___132105___Shift+4___"),
        ("Workspace 3 — Edit 2 (Sync & Colors)", ["Edit 2"], "Shift+Key4___132105___Shift+4___"),
        ("Workspace 4 — Edit 3 (Fine Tuning)", ["Edit 3"], "Shift+Key4___132105___Shift+4___"),
        ("Workspace 5 — Color (Nodes & Wheels)", ["Color"], "Shift+Key6___132105___Shift+6___"),
        ("Workspace 6 — Fairlight (Audio & Fades)", ["Fairlight"], "Shift+Key7___132105___Shift+7___"),
        ("Workspace 7 — Deliver & Render Queue", ["Deliver / Render Queue"], "Shift+Key8___132105___Shift+8___"),
        ("Workspace 8 — Quick Export", ["Quick Export", "Physical keys & Fn layer"], "Shift+Key9___132105___Shift+9___"),
    ]

    workspaces = []
    touch_pages = []
    encoder_pages = []
    macro_commands = []

    # Common Jog/Shuttle dial adjustments
    shuttle_guid = deterministic_guid("rupokar_shuttle_adjustment")
    macro_adjustments = [
        {
            "$type": "Loupedeck.Service.ApplicationProfileMacroAdjustment, LoupedeckService",
            "isCommand": False,
            "name": shuttle_guid,
            "displayName": "Timeline Shuttle / Jog",
            "description": "Jog frame by frame or shuttle through timeline",
            "groupName": "Navigation",
            "superGroupName": None,
            "supportedOs": "All",
            "supportedModes": ["Main"],
            "showAsSingleAction": False,
            "actionEditorCommands": [],
            "actionsBefore": [],
            "actionsLeft": ["$@Generic___@ProfileAction___" + deterministic_guid("jog_left")],
            "actionsRight": ["$@Generic___@ProfileAction___" + deterministic_guid("jog_right")],
            "actionsReset": [],
            "clickRateLimit": 9,
        }
    ]

    # Wheel page (Common to all workspaces)
    wheel_page_guid = deterministic_guid("rupokar_wheel_page")
    wheel_pages = [
        {
            "$type": "Loupedeck.Service.ProfileLayoutWheelPage, LoupedeckService",
            "name": wheel_page_guid,
            "displayName": "Jog Shuttle Wheel",
            "description": "Jog shuttle wheel with play/pause tap",
            "templateName": "WheelToolGeneric3x1Horizontal",
            "parameters": {
                "$type": "Loupedeck.StringDictionaryNoCase, PluginApi",
                "adjustment": f"$@Generic___@MacroAdjustment___{shuttle_guid}",
                "actions": "$@Generic___@None,$@Generic___@ProfileAction___"
                + deterministic_guid("rupokar_action_rupokar.final.046_Play/Pause")
                + ",$@Generic___@None",
            },
        }
    ]

    for ws_idx, (ws_title, sections, page_shortcut) in enumerate(WORKSPACE_DEFS, start=1):
        ws_guid = deterministic_guid(f"rupokar_ws_{ws_idx}_{ws_title}")

        touch_items = [
            m for m in manifest if m["section"] in sections and m["type"] == "touch"
        ]
        dial_items = [
            m for m in manifest if m["section"] in sections and m["type"] == "dial"
        ]

        # Touch pages (12 controls each)
        ws_touch_page_guids = []
        for page_idx in range(max(1, (len(touch_items) + 11) // 12)):
            tp_guid = deterministic_guid(f"rupokar_touch_page_{ws_idx}_{page_idx}")
            ws_touch_page_guids.append(tp_guid)
            page_slice = touch_items[page_idx * 12 : (page_idx + 1) * 12]

            controls = []
            for c_idx in range(12):
                if c_idx < len(page_slice):
                    it = page_slice[c_idx]
                    act = action_by_id[it["id"]]
                    controls.append({
                        "$type": "Loupedeck.Service.ProfileLayoutButton, LoupedeckService",
                        "pressAction": act,
                        "fnPressAction": None,
                    })
                else:
                    controls.append({
                        "$type": "Loupedeck.Service.ProfileLayoutButton, LoupedeckService",
                        "pressAction": None,
                        "fnPressAction": None,
                    })

            touch_pages.append({
                "$type": "Loupedeck.Service.ProfileLayoutButtonPage, LoupedeckService",
                "name": tp_guid,
                "displayName": f"{ws_title} (Page {page_idx+1})",
                "description": None,
                "controls": controls,
                "dynamicPageName": None,
                "dynamicPagePluginName": None,
                "dynamicPageNumber": 0,
            })

        # Encoder page (6 dials: 3 on left, 3 on right)
        ep_guid = deterministic_guid(f"rupokar_encoder_page_{ws_idx}")
        dial_controls = []
        dials_turn = [d for d in dial_items if "turn" in d["control"].lower()]
        dials_press = [d for d in dial_items if "press" in d["control"].lower()]

        for d_idx in range(6):
            turn_act = action_by_id[dials_turn[d_idx]["id"]] if d_idx < len(dials_turn) else None
            press_act = action_by_id[dials_press[d_idx]["id"]] if d_idx < len(dials_press) else None

            dial_controls.append({
                "$type": "Loupedeck.Service.ProfileLayoutEncoder, LoupedeckService",
                "pressAction": press_act,
                "fnPressAction": None,
                "rotateAction": turn_act,
                "fnRotateAction": None,
            })

        encoder_pages.append({
            "$type": "Loupedeck.Service.ProfileLayoutEncoderPage, LoupedeckService",
            "name": ep_guid,
            "displayName": f"{ws_title} — Dials",
            "description": None,
            "controls": dial_controls,
            "dynamicPageName": None,
            "dynamicPagePluginName": None,
            "dynamicPageNumber": 0,
        })

        workspaces.append({
            "$type": "Loupedeck.Service.ProfileLayoutWorkspace20, LoupedeckService",
            "name": ws_guid,
            "displayName": ws_title,
            "description": None,
            "touchPageNames": ws_touch_page_guids,
            "encoderPageNames": [ep_guid],
            "wheelPageNames": [wheel_page_guid],
            "activationActions": [],
        })

    # 3. Round Buttons 1 to 8: Workspace switching macros!
    round_controls = []
    nav_manifest_items = [m for m in manifest if m["section"] == "Navigation"]

    for r_idx in range(8):
        ws = workspaces[r_idx]
        ws_guid = ws["name"]
        ws_title, _, page_shortcut = WORKSPACE_DEFS[r_idx]

        macro_guid = deterministic_guid(f"rupokar_round_btn_macro_{r_idx+1}")
        sub_cmd_guid = deterministic_guid(f"rupokar_round_btn_subcmd_{r_idx+1}")

        # Macro that changes workspace on CT AND switches Resolve page!
        macro_def = {
            "$type": "Loupedeck.Service.ApplicationProfileMacroCommand, LoupedeckService",
            "isCommand": True,
            "name": macro_guid,
            "displayName": ws_title,
            "description": f"Switch Loupedeck CT to {ws_title} and switch DaVinci Resolve page",
            "groupName": "Navigation",
            "superGroupName": "@macro",
            "supportedOs": "All",
            "supportedModes": ["Main"],
            "showAsSingleAction": False,
            "actionEditorCommands": [
                {
                    "$type": "Loupedeck.Service.MacroActionEditorCommand, LoupedeckService",
                    "name": sub_cmd_guid,
                    "templateName": "$@Generic___@KeyboardKey",
                    "actionParameters": {
                        "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.String, System.Private.CoreLib]], System.Private.CoreLib",
                        "keyboardKey": page_shortcut,
                    },
                }
            ],
            "isMultiState": False,
            "actions": [
                sub_cmd_guid,
                f"$@Generic___@ChangeWorkspace___Main|{ws_guid}",
            ],
        }
        macro_commands.append(macro_def)

        # Set round button action
        round_act = f"$@Generic___@Macro___{macro_guid}"
        round_controls.append({
            "$type": "Loupedeck.Service.ProfileLayoutButton, LoupedeckService",
            "pressAction": round_act,
            "fnPressAction": None,
        })

        # Copy nav icon for this round button macro
        if r_idx < len(nav_manifest_items):
            nav_item = nav_manifest_items[r_idx]
            svg_name = Path(nav_item["filename"]).name
            png_name = svg_name.replace(".svg", ".png")
            src_png = PNG_DIR / nav_item["type"] / png_name
            if src_png.exists():
                shutil.copy(src_png, ACTION_IMAGES_DIR / f"{round_act}.png")
                shutil.copy(src_png, ACTION_IMAGES_DIR / f"$@generic___@Macro___{macro_guid}.png")

    round_page = {
        "$type": "Loupedeck.Service.ProfileLayoutButtonPage, LoupedeckService",
        "name": deterministic_guid("rupokar_round_page"),
        "displayName": "Workspace Navigation (1-8)",
        "description": None,
        "controls": round_controls,
        "dynamicPageName": None,
        "dynamicPagePluginName": None,
        "dynamicPageNumber": 0,
    }

    # 4. Square Buttons 1 to 12: Physical keys
    physical_items = [m for m in manifest if m["section"] == "Physical keys & Fn layer"]
    square_controls = []
    for s_idx in range(12):
        if s_idx < len(physical_items):
            it = physical_items[s_idx]
            act = action_by_id[it["id"]]
            square_controls.append({
                "$type": "Loupedeck.Service.ProfileLayoutButton, LoupedeckService",
                "pressAction": act,
                "fnPressAction": None,
            })
        else:
            square_controls.append({
                "$type": "Loupedeck.Service.ProfileLayoutButton, LoupedeckService",
                "pressAction": None,
                "fnPressAction": None,
            })

    square_page = {
        "$type": "Loupedeck.Service.ProfileLayoutButtonPage, LoupedeckService",
        "name": deterministic_guid("rupokar_square_page"),
        "displayName": "Physical & Fn Controls",
        "description": None,
        "controls": square_controls,
        "dynamicPageName": None,
        "dynamicPagePluginName": None,
        "dynamicPageNumber": 0,
    }

    # 5. Full ProfileInfo.json structure
    profile_info = {
        "$type": "Loupedeck.Service.ApplicationProfile, LoupedeckService",
        "name": TARGET_PROFILE_ID,
        "profileFlags": "None",
        "displayName": "DaVinci Resolve Rupokar",
        "description": "Rupokar Studios 168-Action Professional DaVinci Resolve CT Pack",
        "deviceType": "Loupedeck20",
        "applicationName": "com.blackmagic-design.davinciresolve",
        "nativePluginName": None,
        "hasNativePlugin": False,
        "additionalNativePluginNames": ["Twitch", "DefaultMac"],
        "lastModifiedTimeUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "profileSettings": {
            "$type": "Loupedeck.DictionaryNoCase`1[[System.String, System.Private.CoreLib]], PluginApi"
        },
        "actionImages90": None,
        "actionImages60": None,
        "wheelImages": None,
        "actionColors": None,
        "layout": {
            "$type": "Loupedeck.Service.ProfileLayout20, LoupedeckService",
            "deviceType": "Loupedeck20",
            "profileFlags": "None",
            "layoutModes": [
                {
                    "$type": "Loupedeck.Service.ProfileLayoutMode20, LoupedeckService",
                    "deviceType": "Loupedeck20",
                    "modeName": "main",
                    "parentModeName": None,
                    "actions": None,
                    "dynamicButtonPages": None,
                    "dynamicEncoderPages": None,
                    "touchPages": touch_pages,
                    "encoderPages": encoder_pages,
                    "wheelPages": wheel_pages,
                    "workspaces": workspaces,
                    "homeWorkspaceName": workspaces[0]["name"],
                }
            ],
            "roundPage": round_page,
            "squarePage": square_page,
        },
        "macroCommands": macro_commands,
        "macroAdjustments": macro_adjustments,
        "profileCommands": [],
        "profileAdjustments": [],
        "conversionHistory": f"{datetime.now(timezone.utc).isoformat()} Rupokar Pack Installed\r\n",
        "packageName": None,
        "packageVersion": None,
        "profileActions": profile_actions,
    }

    out_file = PROFILE_DIR / "ProfileInfo.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profile_info, f, indent=4, ensure_ascii=False)

    print(f"✅ Successfully wrote ProfileInfo.json ({out_file.stat().st_size} bytes)")
    print(f"✅ Workspaces: {len(workspaces)}")
    print(f"✅ Macro commands (Round 1-8): {len(macro_commands)}")
    print(f"✅ Touch pages: {len(touch_pages)}")
    print(f"✅ Encoder pages: {len(encoder_pages)}")
    print(f"✅ Profile actions: {len(profile_actions)}")
    print(f"✅ ActionImages count: {len(list(ACTION_IMAGES_DIR.glob('*.png')))}")


if __name__ == "__main__":
    main()
