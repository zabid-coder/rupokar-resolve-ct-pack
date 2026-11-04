# Rupokar Studios LoupeDeck CT Pack — Installation Guide

## Step 1: Import Loupedeck Profile
1. Double-click `profile/Rupokar-Resolve-CT.lp5` to open it in **Loupedeck 6.4.1+**.
2. When prompted, select **DaVinci Resolve** as the target application.

## Step 2: Load DaVinci Resolve Keyboard Preset
1. Launch **DaVinci Resolve 21.1.2**.
2. Navigate to **DaVinci Resolve** menu -> **Keyboard Customization...**.
3. Select `...` in top right -> **Import Preset**.
4. Choose `keyboard-preset/Rupokar_Resolve_Keys.txt` and activate it.

## Step 3: Enable External Scripting
1. In DaVinci Resolve, go to **Preferences** -> **System** -> **General**.
2. Set **External scripting using** to **Local**.
3. Save preferences.

## Step 4: Run the Automation Bridge (Studio Features)
Run:
```bash
./scripts/run_bridge.sh
```
This enables YouTube/TikTok render queue automation, timeline aspect ratio duplication, and real-time timer sync.
