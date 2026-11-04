import json
import socket
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock
import pytest

from bridge.rupokar_resolve_bridge.command_router import handle_command
from bridge.rupokar_resolve_bridge.resolve_client import ResolveClient
from bridge.rupokar_resolve_bridge.socket_server import SocketServer


def test_command_router_offline():
    # When resolve is offline or mocked
    response = handle_command({"id": "resolve.ping", "requestId": "123"})
    assert response["requestId"] == "123"
    assert "ok" in response
    assert "state" in response


def test_command_router_unknown():
    response = handle_command({"id": "non_existent_command", "requestId": "999"})
    assert response["ok"] is False
    assert response["error"] == "UNKNOWN_COMMAND"


def test_command_router_with_mocked_client():
    mock_client = MagicMock(spec=ResolveClient)
    mock_client.get_status.return_value = {"connected": True, "version": "21.1.2", "activeProject": "TestProject"}
    mock_client.start_rendering.return_value = {"ok": True, "message": "Rendering started"}
    mock_client.stop_rendering.return_value = {"ok": True, "message": "Rendering stopped"}
    mock_client.get_render_jobs.return_value = {"ok": True, "jobs": [{"JobId": "1"}], "isRendering": True}
    mock_client.duplicate_timeline.return_value = {"ok": True, "message": "Created timeline: Timeline 1 (9:16)"}

    # ping
    res = handle_command({"id": "resolve.ping", "requestId": "p1"}, client=mock_client)
    assert res["ok"] is True
    assert res["state"] == "CONNECTED"
    assert res["data"]["activeProject"] == "TestProject"

    # render.start.all
    res = handle_command({"id": "render.start.all", "requestId": "r1"}, client=mock_client)
    assert res["ok"] is True
    assert res["message"] == "Rendering started"

    # render.stop
    res = handle_command({"id": "render.stop", "requestId": "r2"}, client=mock_client)
    assert res["ok"] is True
    assert res["message"] == "Rendering stopped"

    # render.queue.status
    res = handle_command({"id": "render.queue.status", "requestId": "r3"}, client=mock_client)
    assert res["ok"] is True
    assert len(res["jobs"]) == 1
    assert res["isRendering"] is True

    # timeline.copy.aspect
    res = handle_command(
        {"id": "timeline.copy.aspect", "requestId": "r4", "payload": {"ratio": "9:16"}},
        client=mock_client,
    )
    assert res["ok"] is True
    mock_client.duplicate_timeline.assert_called_with("9:16")


def test_resolve_client_disconnected_fallbacks():
    client = ResolveClient()
    # Force resolve instance to None to simulate Resolve not being running
    client.resolve = None
    client._init_resolve = lambda: None  # prevent re-connecting

    assert client.is_connected() is False

    status = client.get_status()
    assert status == {"connected": False, "version": None, "activeProject": None}

    start = client.start_rendering()
    assert start["ok"] is False

    stop = client.stop_rendering()
    assert stop["ok"] is False

    jobs = client.get_render_jobs()
    assert jobs["ok"] is False
    assert jobs["jobs"] == []

    dup = client.duplicate_timeline("9:16")
    assert dup["ok"] is False


def test_socket_server_roundtrip():
    test_socket = Path.home() / ".rupokar" / "test_bridge.sock"

    server = SocketServer(socket_path=test_socket)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.3)

    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(str(test_socket))
        payload = json.dumps({"id": "resolve.ping", "requestId": "req-1"}).encode("utf-8") + b"\n"
        client.sendall(payload)
        data = client.recv(4096).decode("utf-8").strip()
        client.close()

        res = json.loads(data)
        assert res["requestId"] == "req-1"
        assert res["ok"] is True
    finally:
        server.stop()
        assert not test_socket.exists()


def test_socket_server_invalid_json():
    test_socket = Path.home() / ".rupokar" / "test_bridge_invalid.sock"

    server = SocketServer(socket_path=test_socket)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.3)

    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(str(test_socket))
        client.sendall(b"NOT_VALID_JSON\n")
        data = client.recv(4096).decode("utf-8").strip()
        client.close()

        res = json.loads(data)
        assert res["ok"] is False
        assert res["error"] == "INVALID_JSON"
    finally:
        server.stop()
        assert not test_socket.exists()
