namespace Rupokar.Resolve.Actions.IPC;

using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class BridgeSocketClient
{
    private readonly string _socketPath;

    public BridgeSocketClient()
    {
        var home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        _socketPath = Path.Combine(home, ".rupokar", "bridge.sock");
    }

    public async Task<string?> SendCommandAsync(string commandId, object? payload = null)
    {
        if (!File.Exists(_socketPath)) return null;

        using var client = new Socket(AddressFamily.Unix, SocketType.Stream, ProtocolType.Unspecified);
        var endpoint = new UnixDomainSocketEndPoint(_socketPath);
        await client.ConnectAsync(endpoint);

        var req = new { id = commandId, requestId = Guid.NewGuid().ToString(), payload = payload ?? new { } };
        var json = JsonSerializer.Serialize(req) + "\n";
        var bytes = Encoding.UTF8.GetBytes(json);
        await client.SendAsync(bytes, SocketFlags.None);

        var buffer = new byte[4096];
        var received = await client.ReceiveAsync(buffer, SocketFlags.None);
        return Encoding.UTF8.GetString(buffer, 0, received).Trim();
    }
}
