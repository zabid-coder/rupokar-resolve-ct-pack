from pathlib import Path
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = REPO_ROOT / "plugin" / "Rupokar.Resolve.Actions"


def test_plugin_files_exist():
    expected_files = [
        "Rupokar.Resolve.Actions.csproj",
        "RupokarResolvePlugin.cs",
        "Actions/BreakTimerAction.cs",
        "Actions/RenderQueueAction.cs",
        "DynamicDisplay/TileImageRenderer.cs",
        "IPC/BridgeSocketClient.cs",
    ]
    for rel_path in expected_files:
        p = PLUGIN_ROOT / rel_path
        assert p.exists(), f"Expected {p} to exist"
        assert p.stat().st_size > 100, f"File {p} is empty"


def test_break_timer_intervals():
    timer_cs = (PLUGIN_ROOT / "Actions" / "BreakTimerAction.cs").read_text(encoding="utf-8")
    assert "25" in timer_cs
    assert "45" in timer_cs
    assert "1.5" in timer_cs or "90" in timer_cs


def test_csproj_configuration():
    csproj_path = PLUGIN_ROOT / "Rupokar.Resolve.Actions.csproj"
    tree = ET.parse(csproj_path)
    root = tree.getroot()

    tf = root.find(".//TargetFramework")
    assert tf is not None and tf.text == "net8.0"

    pkg = root.find(".//PackageReference[@Include='Loupedeck.PluginApi']")
    assert pkg is not None
    assert pkg.get("Version") == "6.4.1"


def test_bridge_socket_client_contract():
    client_cs = (PLUGIN_ROOT / "IPC" / "BridgeSocketClient.cs").read_text(encoding="utf-8")
    assert ".rupokar" in client_cs
    assert "bridge.sock" in client_cs
    assert "UnixDomainSocketEndPoint" in client_cs
    assert "AddressFamily.Unix" in client_cs


def test_tile_renderer_contract():
    renderer_cs = (PLUGIN_ROOT / "DynamicDisplay" / "TileImageRenderer.cs").read_text(encoding="utf-8")
    assert "256, 256" in renderer_cs
    assert "BREAK NOW!" in renderer_cs
    assert "BitmapBuilder" in renderer_cs
