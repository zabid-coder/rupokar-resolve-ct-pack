#!/usr/bin/env python3
"""Build a screenshot-backed reference from the supplied walkthrough and SRT."""

from __future__ import annotations

import html
import shutil
import subprocess
from collections import Counter
from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parent
VIDEO = SOURCE_DIR / "Loupedeck CT for Davinci Resolve Every Button Explained (Full Walkthrough)-1920x1080-avc1-mp4a.mp4"
OUTPUT_DIR = SOURCE_DIR / "Loupedeck-CT-Master-Reference"
IMAGE_DIR = OUTPUT_DIR / "images"
HTML_FILE = OUTPUT_DIR / "LoupeDeck-CT-Master-Reference.html"

# One untouched frame from the supplied walkthrough is reused only on cards whose
# labelled control is visibly shown in that frame. Individual action cards still
# retain their own source timestamp beside the image.
FRAMES = {
    "overview": "00:00:40",
    "media": "00:01:40",
    "timer": "00:03:46",
    "edit1": "00:04:58",
    "edit2": "00:08:52",
    "edit3": "00:11:40",
    "physical": "00:13:46",
    "color": "00:15:42",
    "fairlight": "00:18:08",
    "deliver": "00:19:13",
    "deliver-extras": "00:20:18",
    "free-deliver": "00:20:38",
    "quick-export": "00:20:55",
}

ITEMS: list[dict[str, str]] = []


def add(section: str, control: str, function: str, detail: str, availability: str, source_time: str, frame: str) -> None:
    ITEMS.append(
        {
            "section": section,
            "control": control,
            "function": function,
            "detail": detail,
            "availability": availability,
            "source_time": source_time,
            "frame": frame,
        }
    )


# CT page navigation
for control, function, detail in [
    ("Round button 1", "Media page", "Opens the Media / project-management page."),
    ("Round button 2", "Edit page 1", "Keeps Resolve on Edit and loads the first CT Edit tool page."),
    ("Round button 3", "Edit page 2", "Keeps Resolve on Edit and loads the second CT Edit tool page."),
    ("Round button 4", "Edit page 3", "Keeps Resolve on Edit and loads the third CT Edit tool page."),
    ("Round button 5", "Color page", "Switches Resolve and the CT to Color tools."),
    ("Round button 6", "Fairlight page", "Switches Resolve and the CT to Fairlight tools."),
    ("Round button 7", "Deliver page", "Switches Resolve and the CT to render/export tools."),
    ("Round button 8", "Quick Export", "Opens Resolve's Quick Export flow."),
]:
    add("Navigation", control, function, detail, "Both editions", "00:00:34–00:01:05", "overview")

# Media page
for control, function, detail, availability, time in [
    ("Touch 1 · top-left", "Import Media", "Open the file picker and import selected media into the active bin.", "Both editions", "00:02:04–00:02:21"),
    ("Touch 2 · top row", "New Bin", "Create a new Media Pool folder/bin.", "Both editions", "00:01:50–00:02:02"),
    ("Touch 3 · top row", "Project Notes", "Open, edit, save, and close the project's notes.", "Both editions", "00:02:33–00:02:44"),
    ("Touch 4 · top-right", "Project Manager", "Open the Project Manager to open or switch projects.", "Both editions", "00:02:44–00:02:51"),
    ("Touch 5 · middle-left", "Prefer Proxy", "Prefer generated proxy files for playback when they exist.", "Both editions", "00:03:01–00:03:10"),
    ("Touch 6 · middle row", "Camera Originals", "Switch playback back to original camera media.", "Both editions", "00:03:10–00:03:15"),
    ("Touch 7 · middle row", "Project Settings", "Open the project settings, including timeline size and frame rate.", "Both editions", "00:01:35–00:01:50"),
    ("Touch 8 · middle-right", "New Project", "Open the new-project flow.", "Both editions", "00:02:51–00:02:57"),
    ("Touch 9 · bottom-left", "Power Bins", "Toggle Power Bins, reusable media folders shared across projects.", "Both editions", "00:02:21–00:02:33"),
    ("Touch 10 · bottom row", "Timeline 9:16", "Create a vertical copy of the current timeline for TikTok, Reels, and Shorts; original is retained.", "Studio only", "00:03:15–00:03:29; 00:21:03–00:21:14"),
    ("Touch 11 · bottom row", "Timeline 4:5", "Create a 4:5 copy of the timeline for an Instagram feed.", "Studio only", "00:03:15–00:03:29; 00:21:14–00:21:19"),
    ("Touch 12 · bottom-right", "Timeline 4:3", "Create a 4:3 copy of the timeline.", "Studio only", "00:03:15–00:03:29; 00:21:19–00:21:24"),
    ("Alternate bottom row", "Duplicate Timeline", "Free-edition replacement option: make a safe working copy of a timeline.", "Free edition", "00:03:31–00:03:36"),
    ("Alternate bottom row", "New Timeline", "Free-edition replacement option: create a new timeline.", "Free edition", "00:03:31–00:03:36"),
]:
    add("Media / Project", control, function, detail, availability, time, "media")

# Break Timer — screenshot confirms all twelve labelled choices.
for control, function, detail, time in [
    ("Timer touch 1", "25-minute interval", "Select a 25-minute editing interval.", "00:03:45–00:03:56"),
    ("Timer touch 2", "45-minute interval", "Select a 45-minute editing interval.", "00:03:36–00:04:06"),
    ("Timer touch 3", "1-hour interval", "Select a 1-hour editing interval.", "00:03:36–00:04:06"),
    ("Timer touch 4", "1.5-hour interval", "Select a 90-minute editing interval.", "00:03:36–00:04:06"),
    ("Timer touch 5", "2-hour interval", "Select a 2-hour editing interval.", "00:03:36–00:04:06"),
    ("Timer touch 6", "2.5-hour interval", "Select a 150-minute editing interval.", "00:03:36–00:04:06"),
    ("Timer touch 7", "3-hour interval", "Select a 3-hour editing interval.", "00:03:36–00:04:06"),
    ("Timer touch 8", "4-hour interval", "Select a 4-hour editing interval.", "00:03:36–00:04:06"),
    ("Timer touch 9", "Rushwise", "Open Rushwise, described in the walkthrough as a project manager for DaVinci editors.", "00:04:01–00:04:06"),
    ("Timer touch 10", "Break! status", "Shows that the selected work interval has ended; it is a non-blocking break reminder.", "00:15:08–00:15:29"),
    ("Timer touch 11", "Start timer", "Start the selected work interval and update the running status.", "00:03:45–00:03:56"),
    ("Timer touch 12", "Stop timer", "End a running timer early.", "00:03:59–00:04:01"),
]:
    add("Media / Break Timer", control, function, detail, "Studio only", time, "timer")

# Edit 1 touch screen
for control, function, detail, time in [
    ("Touch 1 · top-left", "Select Backward All", "Select all timeline items to the left of the playhead.", "00:07:06–00:07:20"),
    ("Touch 2 · top row", "Select Forward All", "Select all timeline items to the right of the playhead.", "00:07:06–00:07:16"),
    ("Touch 3 · top row", "Snapping", "Toggle magnetic snapping to clip edges; off permits free frame placement.", "00:07:20–00:07:42"),
    ("Touch 4 · top-right", "Delete", "Delete the selected clip, leaving a gap.", "00:06:41–00:06:51"),
    ("Touch 5 · middle-left", "Trim Start", "Trim a selected clip before the playhead while leaving other material in place.", "00:06:51–00:07:03"),
    ("Touch 6 · middle row", "Trim End", "Trim a selected clip after the playhead while leaving other material in place.", "00:06:51–00:07:03"),
    ("Touch 7 · middle row", "Retime Controls", "Show or hide the clip's retime/speed overlay.", "00:07:57–00:08:03"),
    ("Touch 8 · middle-right", "Change Clip Speed", "Open speed change; walkthrough example uses 200%, doubling speed and halving duration.", "00:07:42–00:07:57"),
    ("Touch 9 · bottom-left", "Ripple Start", "Remove the selected clip portion before the playhead and close the gap.", "00:06:07–00:06:21"),
    ("Touch 10 · bottom row", "Split", "Split the selected clip at the playhead.", "00:06:32–00:06:41"),
    ("Touch 11 · bottom row", "Ripple End", "Remove the selected clip portion after the playhead and close the gap.", "00:06:21–00:06:32"),
    ("Touch 12 · bottom-right", "Play/Pause", "Start/pause playback; this control is also on Edit pages 2 and 3.", "00:05:31–00:05:40"),
]:
    add("Edit 1", control, function, detail, "Both editions", time, "edit1")

# Edit 1 dials and center wheel
for control, function, detail, time in [
    ("Top-left dial · turn", "Shuttle", "Move the playhead frame by frame.", "00:05:09–00:05:13"),
    ("Top-left dial · press", "Orange clip color", "Apply Orange to the selected clip.", "00:08:03–00:08:13"),
    ("Middle-left dial · turn", "Audio level", "Adjust selected audio by 1 dB per dial step.", "00:08:19–00:08:28"),
    ("Middle-left dial · press", "Yellow clip color", "Apply Yellow to the selected clip.", "00:08:13–00:08:16"),
    ("Bottom-left dial · turn", "Dynamic Trim", "Move a selected edit point frame by frame while showing both sides of the cut.", "00:08:28–00:08:43"),
    ("Bottom-left dial · press", "Dynamic Trim on/off", "Enable or disable Dynamic Trim mode.", "00:08:28–00:08:43"),
    ("Top-right dial · turn", "Fast Shuttle", "Move the playhead by one second per dial step.", "00:05:13–00:05:18"),
    ("Top-right dial · press", "Green clip color", "Apply Green to the selected clip.", "00:08:16–00:08:19"),
    ("Middle-right dial · turn", "Timeline Zoom", "Zoom the timeline in or out.", "00:05:22–00:05:25"),
    ("Middle-right dial · press", "Zoom to Fit", "Fit the complete timeline on screen.", "00:04:44–00:04:52"),
    ("Bottom-right dial · turn", "Next Clip", "Jump from cut to cut.", "00:05:18–00:05:22"),
    ("Bottom-right dial · press", "Add Marker", "Add a marker to the selected clip, or to the timeline when nothing is selected.", "00:05:44–00:06:07"),
    ("Center wheel · turn", "Frame-by-frame navigation", "Turn right to move forward and left to move backward one frame at a time.", "00:04:59–00:05:07"),
    ("Center wheel · press", "Play/Pause", "Start or pause playback.", "00:05:40–00:05:44"),
]:
    add("Edit 1", control, function, detail, "Both editions", time, "edit1")

# Edit 2 touch screen
for control, function, detail, time in [
    ("Touch 1 · top-left", "Delete All Markers", "Remove the project's clip/timeline markers.", "00:08:49–00:09:00"),
    ("Touch 2 · top row", "Linked Selection", "Toggle whether linked video and audio select together.", "00:09:00–00:09:15"),
    ("Touch 3 · top row", "Link Clips", "Link separate selections, or unlink items already joined.", "00:09:15–00:09:50"),
    ("Touch 4 · top-right", "Compound Clip", "Create one compound clip from selected clips.", "00:09:51–00:10:06"),
    ("Touch 5 · middle-left", "Normalize", "Choose a target level and normalize selected audio.", "00:10:06–00:10:16"),
    ("Touch 6 · middle row", "Auto Align", "Align clips through matching audio, useful for multi-camera recordings.", "00:10:16–00:10:28"),
    ("Touch 7 · middle row", "Mark In", "Set the in point of a playback/export range.", "00:10:28–00:10:34"),
    ("Touch 8 · middle-right", "Mark Out", "Set the out point of a playback/export range.", "00:10:28–00:10:34"),
    ("Touch 9 · bottom-left", "Match Frame", "Open the original source at the exact displayed frame.", "00:10:42–00:10:52"),
    ("Touch 10 · bottom row", "Cinema Viewer", "Show the timeline in full screen; Escape returns.", "00:10:52–00:10:59"),
    ("Touch 11 · bottom row", "Loop", "Toggle repeated playback of the marked range.", "00:10:34–00:10:42"),
    ("Touch 12 · bottom-right", "Play/Pause", "Start/pause playback.", "00:05:31–00:05:40"),
]:
    add("Edit 2", control, function, detail, "Both editions", time, "edit2")

for control, function in [
    ("Top-left dial · press", "Apricot clip color"),
    ("Middle-left dial · press", "Blue clip color"),
    ("Bottom-left dial · press", "Lime clip color"),
    ("Top-right dial · press", "Brown clip color"),
    ("Middle-right dial · press", "Pink clip color"),
    ("Bottom-right dial · press", "Purple clip color"),
]:
    add("Edit 2", control, function, "Swipe the dial labels down to the second color bank, then press the labelled dial to apply this clip color.", "Both editions", "00:10:59–00:11:12", "edit2")

# Edit 3 touch screen
for control, function, detail, time in [
    ("Touch 1 · top-left", "Enable Clip", "Disable a clip without deleting it; press again to restore it.", "00:11:52–00:11:59"),
    ("Touch 2 · top row", "Freeze Frame", "Freeze the image at the playhead; press again to restore normal playback.", "00:11:59–00:12:15"),
    ("Touch 3 · top row", "Title Safe", "Toggle the safe-area guide for text visibility.", "00:12:27–00:12:36"),
    ("Touch 4 · top-right", "Delete Gaps", "Close all gaps that are empty on every enabled track.", "00:11:20–00:11:43"),
    ("Touch 5 · middle-left", "Find Clip", "Reveal the selected clip in the Media Pool.", "00:12:36–00:12:42"),
    ("Touch 6 · middle row", "Crossfade", "Apply a crossfade between adjacent audio clips.", "00:12:15–00:12:27"),
    ("Touch 7 · middle row", "Swap Left", "Swap the selected clip with its left neighbor.", "00:11:43–00:11:52"),
    ("Touch 8 · middle-right", "Swap Right", "Swap the selected clip with its right neighbor.", "00:11:43–00:11:52"),
    ("Touch 9 · bottom-left", "Find Timeline", "Reveal the current timeline.", "00:12:41–00:12:46"),
    ("Touch 10 · bottom row", "New Timeline", "Create a new timeline.", "00:04:18–00:04:37; 00:12:46–00:12:50"),
    ("Touch 11 · bottom row", "Duplicate Timeline", "Make a copy of the timeline for safe experiments.", "00:13:04–00:13:17"),
    ("Touch 12 · bottom-right", "Play/Pause", "Start/pause playback.", "00:05:31–00:05:40"),
]:
    add("Edit 3", control, function, detail, "Both editions", time, "edit3")

for control, function in [
    ("Top-left dial · press", "Olive clip color"),
    ("Middle-left dial · press", "Teal clip color"),
    ("Bottom-left dial · press", "Navy clip color"),
    ("Top-right dial · press", "Violet clip color"),
    ("Middle-right dial · press", "Tan clip color"),
    ("Bottom-right dial · press", "Beige clip color"),
]:
    add("Edit 3", control, function, "Swipe the dial labels down twice to the third color bank, then press the labelled dial to apply this clip color.", "Both editions", "00:12:50–00:13:04", "edit3")

# Physical keys and Fn layer
for control, function, detail, time in [
    ("Undo", "Undo", "Restore the last action.", "00:13:50–00:13:54"),
    ("Save", "Save project", "Save the Resolve project.", "00:13:54–00:14:00"),
    ("Square A", "Move clip up", "Move the selected clip up one track.", "00:14:00–00:14:06"),
    ("Square B", "Move clip down", "Move the selected clip down one track.", "00:14:00–00:14:06"),
    ("Square C", "Timeline start", "Jump to the start of the timeline.", "00:05:25–00:05:31"),
    ("Square D", "Timeline end", "Jump to the end of the timeline.", "00:05:25–00:05:31"),
    ("Square E", "Right-click", "Issue a right-click at the current mouse location.", "00:14:06–00:14:10"),
    ("Fn + B", "Ripple Delete", "Delete the selected clip and close the gap.", "00:13:41–00:13:50"),
    ("Fn + round 1", "Media Pool panel", "Toggle the Media Pool panel.", "00:14:15–00:14:23"),
    ("Fn + round 2", "Effects Library panel", "Toggle Effects Library, including transitions and titles.", "00:14:23–00:14:28"),
    ("Fn + round 3", "Inspector panel", "Toggle Inspector for clip settings.", "00:14:28–00:14:32"),
    ("Fn + round 4", "Mixer panel", "Toggle Mixer.", "00:14:32–00:14:34"),
    ("Fn + round 5", "Power Bins panel", "Toggle Power Bins.", "00:14:34–00:14:38"),
    ("Fn + round 6", "Metadata panel", "Toggle clip Metadata.", "00:14:38–00:14:42"),
    ("Fn + round 7", "Index panel", "Toggle Index, the timeline cut list.", "00:14:42–00:14:47"),
    ("Fn + C", "Copy", "Copy the selected clip.", "00:14:48–00:14:56"),
    ("Fn + A", "Paste Attributes", "Paste chosen attributes to another clip; example shown is clip color.", "00:14:51–00:15:08"),
    ("Fn + D", "Bypass All Grades", "Toggle a before/after view by bypassing all grades.", "00:17:47–00:17:55"),
]:
    add("Physical keys & Fn layer", control, function, detail, "Both editions", time, "physical")

# Color page touchscreen
for control, function, detail, time in [
    ("Touch 1 · top-left", "Scopes", "Toggle video scopes for checking exposure and color.", "00:15:40–00:15:48"),
    ("Touch 2 · top row", "Light Box", "Toggle a view of all clips side by side.", "00:17:38–00:17:43"),
    ("Touch 3 · top row", "Cinema Viewer", "Judge the grade in full screen.", "00:17:43–00:17:47"),
    ("Touch 4 · top-right", "Printer Lights", "Change the right dials to Red, Green, and Blue printer-light controls; press again to exit.", "00:16:45–00:17:01"),
    ("Touch 5 · middle-left", "Add Node", "Add an empty serial node.", "00:15:52–00:15:57"),
    ("Touch 6 · middle row", "Node Before", "Insert a node before the current node.", "00:16:35–00:16:40"),
    ("Touch 7 · middle row", "Label Node", "Name a node so its role is clear.", "00:16:40–00:16:45"),
    ("Touch 8 · middle-right", "Grab Still", "Save the current graded frame to the Gallery.", "00:17:01–00:17:07"),
    ("Touch 9 · bottom-left", "Split Selected", "Compare two selected clips side by side.", "00:17:22–00:17:28"),
    ("Touch 10 · bottom row", "Split Prev/Next", "Compare the previous and next clips around the current clip.", "00:17:28–00:17:33"),
    ("Touch 11 · bottom row", "Split Original", "Compare the current grade beside the original.", "00:17:12–00:17:18"),
    ("Touch 12 · bottom-right", "Split Stills", "Compare a Gallery still beside the current clip.", "00:17:18–00:17:22"),
]:
    add("Color", control, function, detail, "Both editions", time, "color")

for control, function, detail, availability, time in [
    ("Top-left dial · turn", "Saturation", "Adjust saturation on the active node.", "Studio only", "00:16:02–00:16:26"),
    ("Top-left dial · press", "Reset Saturation", "Return Saturation to normal.", "Studio only", "00:16:30–00:16:35"),
    ("Middle-left dial · turn", "Gamma", "Adjust the midtones on the active node.", "Studio only", "00:16:30–00:16:35"),
    ("Middle-left dial · press", "Reset Gamma", "Return Gamma to normal.", "Studio only", "00:16:30–00:16:35"),
    ("Bottom-left dial · turn", "Gain", "Adjust highlights on the active node.", "Studio only", "00:16:26–00:16:30"),
    ("Bottom-left dial · press", "Reset Gain", "Return Gain to normal.", "Studio only", "00:16:30–00:16:35"),
    ("Top-right dial · turn", "Printer Light Red", "Adjust red while Printer Lights mode is active.", "Both editions", "00:16:45–00:17:01"),
    ("Middle-right dial · turn", "Printer Light Green", "Adjust green while Printer Lights mode is active.", "Both editions", "00:16:45–00:17:01"),
    ("Bottom-right dial · turn", "Printer Light Blue", "Adjust blue while Printer Lights mode is active.", "Both editions", "00:16:45–00:17:01"),
    ("Top-right dial · press", "Exit split comparison", "Return to normal viewing when any Split comparison mode is active.", "Both editions", "00:17:33–00:17:38"),
]:
    add("Color", control, function, detail, availability, time, "color")

# Fairlight
for control, function, detail, time in [
    ("Touch 1 · middle-left", "Batch Fade Settings", "Set fade-in and fade-out durations before applying them; example shown is 1.5 s in and 2 s out.", "00:18:08–00:18:19"),
    ("Touch 2 · middle row", "Apply Batch Fades", "Apply the saved batch-fade settings without reopening the settings dialog.", "00:18:19–00:18:29"),
    ("Touch 3 · bottom-left", "Loop", "Toggle looping of the marked range.", "00:18:39–00:18:48"),
    ("Touch 4 · bottom row", "Mark In", "Set the in point.", "00:18:39–00:18:48"),
    ("Touch 5 · bottom row", "Mark Out", "Set the out point.", "00:18:39–00:18:48"),
    ("Touch 6 · bottom-right", "Play/Pause", "Start/pause playback.", "00:18:39–00:18:48"),
    ("Top-left dial · turn", "Shuttle", "Move through the timeline frame by frame.", "00:18:48–00:18:57"),
    ("Middle-left dial · turn", "Track Height", "Resize tracks while the pointer is over the tracks.", "00:18:29–00:18:34"),
    ("Bottom-left dial · turn", "Waveform Zoom", "Make audio waveforms larger or smaller.", "00:18:34–00:18:39"),
    ("Bottom-left dial · press", "Reset Waveform Zoom", "Restore waveform size to normal.", "00:18:34–00:18:39"),
    ("Top-right dial · turn", "Fast Shuttle", "Move through the timeline in faster increments.", "00:18:48–00:18:57"),
    ("Middle-right dial · turn", "Timeline Zoom", "Zoom the Fairlight timeline.", "00:18:48–00:18:57"),
    ("Bottom-right dial · turn", "Next Clip", "Jump from cut to cut.", "00:18:48–00:18:57"),
]:
    add("Fairlight", control, function, detail, "Both editions", time, "fairlight")

# Deliver and export controls
for control, function, detail, availability, time, frame in [
    ("Touch 1 · top-left", "YouTube preset", "Add the timeline to the render queue with the YouTube preset.", "Studio only", "00:19:06–00:19:13", "deliver"),
    ("Touch 2 · top row", "Vimeo preset", "Add the timeline to the render queue with the Vimeo preset.", "Studio only", "00:19:10–00:19:16", "deliver"),
    ("Touch 3 · top row", "TikTok preset", "Add the timeline to the render queue with the TikTok preset.", "Studio only", "00:19:10–00:19:16", "deliver"),
    ("Touch 4 · top-right", "Instagram 4:5 preset", "Add the timeline to the render queue with the Instagram 4:5 preset.", "Studio only", "00:19:10–00:19:16", "deliver"),
    ("Touch 5 · middle-left", "ProRes 422 HQ preset", "Add a high-quality master to the render queue.", "Studio only", "00:19:16–00:19:23", "deliver"),
    ("Touch 6 · middle row", "Custom preset 1", "Apply the custom preset whose Resolve preset name ends in #1.", "Studio only", "00:19:23–00:19:54", "deliver"),
    ("Touch 7 · middle row", "Custom preset 2", "Apply the custom preset whose Resolve preset name ends in #2.", "Studio only", "00:19:23–00:19:54", "deliver"),
    ("Touch 8 · middle-right", "Custom preset 3", "Apply the custom preset whose Resolve preset name ends in #3.", "Studio only", "00:19:23–00:19:54", "deliver"),
    ("Touch 9 · bottom-left", "Add to Queue", "Add the timeline using whichever render settings are active.", "Studio only", "00:19:54–00:19:59", "deliver"),
    ("Touch 10 · bottom row", "Render All", "Render every job in the queue.", "Studio only", "00:19:59–00:20:03", "deliver"),
    ("Touch 11 · bottom row", "Render New", "Render only the new queue job, skipping older queued jobs.", "Studio only", "00:20:03–00:20:09", "deliver"),
    ("Touch 12 · bottom-right", "Stop Render", "Stop an in-progress render.", "Studio only", "00:20:09–00:20:13", "deliver"),
    ("Swipe-right touch 1", "Thumbnail", "Save the current frame as an image, intended for a video thumbnail.", "Studio only", "00:20:13–00:20:21", "deliver-extras"),
    ("Swipe-right touch 2", "Export Folder", "Open the folder containing exports.", "Studio only", "00:20:21–00:20:25", "deliver-extras"),
    ("Swipe-right touch 3", "Clear Render Queue", "Empty the render queue.", "Studio only", "00:20:25–00:20:27", "deliver-extras"),
    ("Top-left dial · press", "Mark In for export", "Set export in point to render only a portion of the timeline.", "Both editions", "00:20:27–00:20:35", "deliver"),
    ("Top-right dial · press", "Mark Out for export", "Set export out point to render only a portion of the timeline.", "Both editions", "00:20:27–00:20:35", "deliver"),
    ("Free edition Deliver", "Free Deliver controls", "Walkthrough lists Quick Export, Add to Queue, Render All, Mark In, Mark Out, and Play.", "Free edition", "00:20:35–00:20:43", "deliver"),
]:
    add("Deliver / Render Queue", control, function, detail, availability, time, frame)

add(
    "Quick Export",
    "Round button 8",
    "Quick Export",
    "Choose a format in Resolve's Quick Export flow, then select Export.",
    "Both editions",
    "00:20:47–00:20:59",
    "quick-export",
)


def extract_frames() -> None:
    if not VIDEO.exists():
        raise FileNotFoundError(f"Walkthrough video not found: {VIDEO}")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required to build the screenshot evidence.")
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    for key, timestamp in FRAMES.items():
        output = IMAGE_DIR / f"{key}.jpg"
        subprocess.run(
            [ffmpeg, "-hide_banner", "-loglevel", "error", "-ss", timestamp, "-i", str(VIDEO), "-frames:v", "1", "-q:v", "2", "-y", str(output)],
            check=True,
        )


def render_html() -> str:
    section_counts = Counter(item["section"] for item in ITEMS)
    section_ids = {section: f"section-{index}" for index, section in enumerate(section_counts)}
    nav_count = sum(1 for item in ITEMS if item["section"] == "Navigation")
    option_count = sum(1 for item in ITEMS if "interval" in item["function"].lower() or "preset" in item["function"].lower() or "color" in item["function"].lower())
    cards: list[str] = []
    active_section = ""
    for index, item in enumerate(ITEMS, start=1):
        if item["section"] != active_section:
            active_section = item["section"]
            cards.append(f'<h2 id="{section_ids[active_section]}">{html.escape(active_section)} <span>{section_counts[active_section]} mappings</span></h2>')
        image_name = f'{item["frame"]}.jpg'
        cards.append(
            f'''<article class="card" data-section="{html.escape(item["section"])}">
  <a class="evidence" href="images/{image_name}" target="_blank" title="Open untouched walkthrough frame">
    <img src="images/{image_name}" alt="Walkthrough evidence for {html.escape(item["function"])}">
    <small>Exact walkthrough frame · click to enlarge</small>
  </a>
  <div class="copy">
    <p class="eyebrow">#{index:03d} · {html.escape(item["section"])}</p>
    <h3>{html.escape(item["function"])}</h3>
    <dl>
      <dt>Control</dt><dd>{html.escape(item["control"])}</dd>
      <dt>What it does</dt><dd>{html.escape(item["detail"])}</dd>
      <dt>Edition</dt><dd>{html.escape(item["availability"])}</dd>
      <dt>Video evidence</dt><dd>{html.escape(item["source_time"])}</dd>
    </dl>
  </div>
</article>'''
        )
    nav_links = "".join(f'<a href="#{section_ids[section]}">{html.escape(section)}</a>' for section in section_counts)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LoupeDeck CT Master Reference — DaVinci Resolve</title>
<style>
  :root {{ --ink:#edf3ff; --muted:#a7b2c8; --panel:#111827; --panel-2:#172235; --line:#2b3951; --accent:#48e1bb; --purple:#bca7ff; --free:#8ec5ff; --studio:#ffd47c; }}
  * {{ box-sizing:border-box; }}
  html {{ scroll-behavior:smooth; }}
  body {{ margin:0; background:#09101c; color:var(--ink); font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
  header {{ padding:58px max(24px,calc((100vw - 1220px)/2)); background:radial-gradient(circle at 85% 0,#35275f 0,transparent 35%),linear-gradient(145deg,#101d32,#09101c); border-bottom:1px solid var(--line); }}
  .kicker {{ margin:0 0 10px; color:var(--accent); font-size:.78rem; font-weight:800; letter-spacing:.13em; text-transform:uppercase; }}
  h1 {{ max-width:900px; margin:0; font-size:clamp(2rem,5vw,4.4rem); line-height:1.04; letter-spacing:-.045em; }}
  .lead {{ max-width:880px; color:#ced8eb; font-size:1.1rem; }}
  .stats {{ display:flex; flex-wrap:wrap; gap:12px; margin:28px 0 0; }}
  .stat {{ min-width:170px; padding:13px 16px; border:1px solid var(--line); border-radius:12px; background:rgba(12,21,37,.7); }}
  .stat strong {{ display:block; color:var(--accent); font-size:1.45rem; }}
  nav {{ position:sticky; top:0; z-index:10; display:flex; gap:8px; overflow:auto; padding:13px max(20px,calc((100vw - 1220px)/2)); background:rgba(9,16,28,.94); backdrop-filter:blur(12px); border-bottom:1px solid var(--line); }}
  nav a {{ flex:0 0 auto; padding:6px 9px; color:#c5d0e7; border:1px solid var(--line); border-radius:999px; text-decoration:none; font-size:.8rem; }}
  nav a:hover {{ border-color:var(--accent); color:var(--accent); }}
  main {{ width:min(1220px,calc(100% - 40px)); margin:0 auto; padding:30px 0 80px; }}
  .notice {{ margin:0 0 32px; padding:17px 20px; border-left:4px solid var(--accent); border-radius:0 10px 10px 0; background:#11263a; color:#dbe8fa; }}
  h2 {{ display:flex; justify-content:space-between; gap:14px; margin:52px 0 16px; padding-bottom:9px; border-bottom:1px solid var(--line); font-size:1.4rem; }}
  h2 span {{ align-self:center; color:var(--muted); font-size:.83rem; font-weight:500; }}
  .card {{ display:grid; grid-template-columns:minmax(270px,39%) 1fr; margin:14px 0; overflow:hidden; border:1px solid var(--line); border-radius:14px; background:linear-gradient(125deg,var(--panel),var(--panel-2)); break-inside:avoid; }}
  .evidence {{ display:flex; flex-direction:column; justify-content:center; gap:5px; padding:10px; background:#07101d; color:var(--muted); font-size:.73rem; text-align:center; text-decoration:none; }}
  .evidence img {{ width:100%; height:auto; border-radius:8px; border:1px solid #26354c; }}
  .copy {{ padding:19px 20px 17px; }}
  .eyebrow {{ margin:0 0 5px; color:var(--accent); font-size:.72rem; font-weight:800; letter-spacing:.11em; text-transform:uppercase; }}
  h3 {{ margin:0 0 12px; font-size:1.32rem; letter-spacing:-.015em; }}
  dl {{ display:grid; grid-template-columns:120px 1fr; gap:7px 12px; margin:0; }}
  dt {{ color:var(--muted); font-weight:700; }}
  dd {{ margin:0; color:#e6edf9; }}
  @media (max-width:700px) {{ .card {{ grid-template-columns:1fr; }} .evidence {{ padding:8px; }} dl {{ grid-template-columns:1fr; gap:2px; }} dd {{ margin:0 0 8px; }} header {{ padding-top:38px; }} }}
  @media print {{ body {{ background:white; color:#111; }} header,nav {{ background:white; color:#111; }} .lead,.notice,dd {{ color:#222; }} .stat,.card {{ background:white; border-color:#aaa; }} .evidence {{ background:#f5f5f5; }} .eyebrow,.kicker,.stat strong {{ color:#076c57; }} h2 {{ color:#111; }} .card {{ page-break-inside:avoid; }} }}
</style>
</head>
<body>
<header>
  <p class="kicker">Source-audited visual catalog</p>
  <h1>LoupeDeck CT<br>DaVinci Resolve Master Reference</h1>
  <p class="lead">Every row pairs one documented mapping or selectable option with an untouched frame from the supplied walkthrough, so you can confirm the control label and CT location visually.</p>
  <div class="stats">
    <div class="stat"><strong>{len(ITEMS)}</strong>mapped actions & options</div>
    <div class="stat"><strong>{len(section_counts)}</strong>work areas</div>
    <div class="stat"><strong>{nav_count}</strong>round-button destinations</div>
    <div class="stat"><strong>{option_count}</strong>named presets, colors & intervals</div>
  </div>
</header>
<nav aria-label="Catalog sections">{nav_links}</nav>
<main>
  <p class="notice"><strong>How to read this file:</strong> “Mapped actions & options” counts separate physical assignments, timer choices, color choices, and render presets. It is deliberately higher than a count of unique Resolve commands because the same behaviour can be reachable from more than one CT control. Every image is a direct, unedited still extracted from the supplied video. Studio-only and Free-edition differences are marked row by row.</p>
  {''.join(cards)}
</main>
</body>
</html>'''


def main() -> None:
    extract_frames()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    HTML_FILE.write_text(render_html(), encoding="utf-8")
    print(f"Built {HTML_FILE}")
    print(f"Documented {len(ITEMS)} mappings/options across {len(set(item['section'] for item in ITEMS))} sections.")


if __name__ == "__main__":
    main()
