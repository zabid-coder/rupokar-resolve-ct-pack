"""Client interfacing with DaVinci Resolve 21.1.2 Scripting API."""

from __future__ import annotations
import sys
from pathlib import Path


class ResolveClient:
    def __init__(self) -> None:
        self.resolve = None
        self._init_resolve()

    def _init_resolve(self) -> None:
        # Standard DaVinci Resolve Scripting module paths on macOS
        paths = [
            "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules",
            "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Resources/ResolvePython",
        ]
        for p in paths:
            if p not in sys.path and Path(p).exists():
                sys.path.append(p)
        try:
            import DaVinciResolveScript as dvr_script
            self.resolve = dvr_script.scriptapp("Resolve")
        except Exception:
            self.resolve = None

    def is_connected(self) -> bool:
        if self.resolve is None:
            self._init_resolve()
        return self.resolve is not None

    def get_status(self) -> dict:
        if not self.is_connected():
            return {"connected": False, "version": None, "activeProject": None}
        try:
            pm = self.resolve.GetProjectManager()
            project = pm.GetCurrentProject() if pm else None
            return {
                "connected": True,
                "version": self.resolve.GetVersionString(),
                "activeProject": project.GetName() if project else None,
            }
        except Exception:
            self.resolve = None
            return {"connected": False, "version": None, "activeProject": None}

    def start_rendering(self) -> dict:
        if not self.is_connected():
            return {"ok": False, "message": "Resolve not connected"}
        try:
            pm = self.resolve.GetProjectManager()
            project = pm.GetCurrentProject() if pm else None
            if not project:
                return {"ok": False, "message": "No active project"}
            started = bool(project.StartRendering())
            return {"ok": started, "message": "Rendering started" if started else "Failed to start render"}
        except Exception as err:
            return {"ok": False, "message": str(err)}

    def stop_rendering(self) -> dict:
        if not self.is_connected():
            return {"ok": False, "message": "Resolve not connected"}
        try:
            pm = self.resolve.GetProjectManager()
            project = pm.GetCurrentProject() if pm else None
            if not project:
                return {"ok": False, "message": "No active project"}
            project.StopRendering()
            return {"ok": True, "message": "Rendering stopped"}
        except Exception as err:
            return {"ok": False, "message": str(err)}

    def get_render_jobs(self) -> dict:
        if not self.is_connected():
            return {"ok": False, "jobs": []}
        try:
            pm = self.resolve.GetProjectManager()
            project = pm.GetCurrentProject() if pm else None
            if not project:
                return {"ok": False, "jobs": []}
            jobs = project.GetRenderJobList() or []
            is_rendering = bool(project.IsRenderingInProgress())
            return {"ok": True, "jobs": jobs, "isRendering": is_rendering}
        except Exception as err:
            return {"ok": False, "jobs": [], "error": str(err)}

    def duplicate_timeline(self, aspect_ratio: str) -> dict:
        if not self.is_connected():
            return {"ok": False, "message": "Resolve not connected"}
        try:
            pm = self.resolve.GetProjectManager()
            project = pm.GetCurrentProject() if pm else None
            if not project:
                return {"ok": False, "message": "No active project"}
            timeline = project.GetCurrentTimeline()
            if not timeline:
                return {"ok": False, "message": "No active timeline"}
            orig_name = timeline.GetName()
            new_name = f"{orig_name} ({aspect_ratio})"
            timeline.DuplicateTimeline(new_name)
            return {"ok": True, "message": f"Created timeline: {new_name}"}
        except Exception as err:
            return {"ok": False, "message": str(err)}
