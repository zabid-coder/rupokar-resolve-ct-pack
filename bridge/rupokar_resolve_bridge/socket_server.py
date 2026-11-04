"""Unix Domain Socket server for local IPC."""

from __future__ import annotations
import json
import os
import socket
from pathlib import Path
from bridge.rupokar_resolve_bridge.command_router import handle_command


class SocketServer:
    def __init__(self, socket_path: Path | None = None) -> None:
        self.socket_path = Path(socket_path) if socket_path else (Path.home() / ".rupokar" / "bridge.sock")
        self.running = False
        self.server_sock: socket.socket | None = None

    def start(self) -> None:
        self.socket_path.parent.mkdir(parents=True, exist_ok=True)
        if self.socket_path.exists():
            try:
                self.socket_path.unlink()
            except OSError:
                pass

        self.server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_sock.bind(str(self.socket_path))
        os.chmod(str(self.socket_path), 0o600)
        self.server_sock.listen(5)
        self.running = True

        while self.running:
            try:
                conn, _ = self.server_sock.accept()
                with conn:
                    reader = conn.makefile("r", encoding="utf-8")
                    line = reader.readline()
                    if not line:
                        continue
                    data = line.strip()
                    try:
                        req = json.loads(data)
                        res = handle_command(req)
                    except Exception as err:
                        res = {"ok": False, "error": "INVALID_JSON", "message": str(err)}
                    conn.sendall(json.dumps(res).encode("utf-8") + b"\n")
            except OSError:
                break

    def stop(self) -> None:
        self.running = False
        if self.server_sock:
            try:
                self.server_sock.close()
            except OSError:
                pass
        if self.socket_path.exists():
            try:
                self.socket_path.unlink()
            except OSError:
                pass
