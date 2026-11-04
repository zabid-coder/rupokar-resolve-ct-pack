"""Strict allow-list command router for Rupokar Resolve Bridge."""

from __future__ import annotations
from typing import Any
from bridge.rupokar_resolve_bridge.resolve_client import ResolveClient

resolve_client = ResolveClient()


def handle_command(request: dict[str, Any], client: ResolveClient | None = None) -> dict[str, Any]:
    active_client = client or resolve_client
    cmd_id = request.get("id")
    request_id = request.get("requestId", "")
    payload = request.get("payload", {}) or {}

    if cmd_id == "resolve.ping":
        status = active_client.get_status()
        return {
            "requestId": request_id,
            "ok": True,
            "state": "CONNECTED" if status.get("connected") else "OFFLINE",
            "data": status,
        }

    if cmd_id == "render.start.all":
        result = active_client.start_rendering()
        return {"requestId": request_id, **result}

    if cmd_id == "render.stop":
        result = active_client.stop_rendering()
        return {"requestId": request_id, **result}

    if cmd_id == "render.queue.status":
        result = active_client.get_render_jobs()
        return {"requestId": request_id, **result}

    if cmd_id == "timeline.copy.aspect":
        ratio = payload.get("ratio", "9:16")
        result = active_client.duplicate_timeline(ratio)
        return {"requestId": request_id, **result}

    return {
        "requestId": request_id,
        "ok": False,
        "error": "UNKNOWN_COMMAND",
        "message": f"Command {cmd_id} is not supported",
    }
