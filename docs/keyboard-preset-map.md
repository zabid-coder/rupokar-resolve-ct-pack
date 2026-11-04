# DaVinci Resolve Keyboard Preset Setup

This document describes how to import and configure the custom conflict-free DaVinci Resolve keyboard shortcut preset for the **Rupokar Loupedeck CT Pack**.

---

## 1. Import Instructions

1. Open **DaVinci Resolve**.
2. Click **DaVinci Resolve** menu -> **Keyboard Customization...** (`Option+Command+K` on macOS, `Ctrl+Alt+K` on Windows).
3. Click the three dots `...` in the top right -> **Import Preset**.
4. Select `keyboard-preset/Rupokar_Resolve_Keys.txt`.
5. Name it **Rupokar Loupedeck CT** and click **Save**.
6. Ensure that **Rupokar Loupedeck CT** is the actively selected preset in the dropdown.

> [!TIP]
> **Studio Edition Scripting Setup:**  
> If using DaVinci Resolve Studio, open **Preferences** (`Command+,`) -> **System** -> **General** -> set **External scripting using** to **Local**. This enables the Python bridge daemon to communicate with the DaVinci Resolve Scripting API.

---

## 2. Shortcut Map Reference

### Edit Actions
| Action | Shortcut | Description |
| :--- | :--- | :--- |
| **Split** | `Ctrl+B` | Split / Blade at playhead position |
| **Ripple Delete** | `Shift+Backspace` | Ripple delete selected clip / gap |
| **Ripple Start** | `Ctrl+Shift+[` | Ripple delete from clip start to playhead |
| **Ripple End** | `Ctrl+Shift+]` | Ripple delete from playhead to clip end |
| **Trim Start** | `Shift+[` | Trim clip in point to playhead |
| **Trim End** | `Shift+]` | Trim clip out point to playhead |
| **Select Forward All** | `Y` | Select all clips forward on all tracks |
| **Select Backward All**| `Ctrl+Y` | Select all clips backward on all tracks |
| **Snapping** | `N` | Toggle snapping on/off |
| **Change Clip Speed** | `Ctrl+R` | Open change clip speed dialog |
| **Retime Controls** | `Ctrl+Alt+R` | Toggle retime controls bar |
| **Add Marker** | `M` | Add marker at playhead |
| **Delete All Markers** | `Ctrl+Alt+M` | Clear all markers on clip / timeline |
| **Compound Clip** | `Alt+C` | Create compound clip from selection |

### Navigation & Transport
| Action | Shortcut | Description |
| :--- | :--- | :--- |
| **Zoom to Fit** | `Shift+Z` | Zoom timeline to fit window |
| **Next Clip** | `Down` | Jump playhead to next edit point |
| **Previous Clip** | `Up` | Jump playhead to previous edit point |
| **Shuttle Reverse** | `J` | Play backward (press repeatedly to accelerate) |
| **Shuttle Stop** | `K` | Pause / Stop playback |
| **Shuttle Forward** | `L` | Play forward (press repeatedly to accelerate) |
| **Play Pause** | `Space` | Toggle playback |

### Panels & Fn Layer
| Action | Shortcut | Target Panel |
| :--- | :--- | :--- |
| **Media Pool Panel** | `Ctrl+1` | Toggle Media Pool |
| **Effects Library Panel** | `Ctrl+2` | Toggle Effects Library |
| **Inspector Panel** | `Ctrl+3` | Toggle Inspector |
| **Mixer Panel** | `Ctrl+4` | Toggle Fairlight Mixer |
| **Power Bins Panel** | `Ctrl+5` | Toggle Power Bins |
| **Metadata Panel** | `Ctrl+6` | Toggle Metadata View |
| **Index Panel** | `Ctrl+7` | Toggle Edit Index |

### Color Page
| Action | Shortcut | Description |
| :--- | :--- | :--- |
| **Add Node** | `Alt+S` | Add serial node |
| **Node Before** | `Shift+S` | Add serial node before current node |
| **Grab Still** | `Ctrl+Alt+G` | Grab still into gallery |
| **Bypass All Grades** | `Shift+D` | Toggle grade bypass |

---

## 3. Troubleshooting

- **Hardware button does not trigger action:** Ensure that **Rupokar Loupedeck CT** is selected under **Keyboard Customization** in DaVinci Resolve.
- **Mac OS Shortcut Conflicts:** Ensure macOS System Settings -> Keyboard -> Keyboard Shortcuts does not intercept `Ctrl+1` to `Ctrl+7` (Mission Control Spaces). If so, disable Mission Control Space shortcuts or use the alternate Fn assignments.
