#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
export PYTHONPATH="$DIR"
exec python3 "$DIR/bridge/rupokar_resolve_bridge/bridge_service.py"
