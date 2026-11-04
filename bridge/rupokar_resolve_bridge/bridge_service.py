#!/usr/bin/env python3
"""Main service entry point for Rupokar Resolve Bridge."""

import signal
import sys
from bridge.rupokar_resolve_bridge.socket_server import SocketServer


def main():
    server = SocketServer()

    def handle_sig(sig, frame):
        print("\nStopping Rupokar Resolve Bridge...")
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sig)
    signal.signal(signal.SIGTERM, handle_sig)
    print("Starting Rupokar Resolve Bridge on ~/.rupokar/bridge.sock")
    server.start()


if __name__ == "__main__":
    main()
