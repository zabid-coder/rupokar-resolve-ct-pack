namespace Rupokar.Resolve.Actions.Actions;

using System;
using Loupedeck;
using Rupokar.Resolve.Actions.IPC;

public class RenderQueueAction : PluginDynamicCommand
{
    private readonly BridgeSocketClient _bridge = new();

    public RenderQueueAction() : base("Render Queue", "Render control and queue management", "Deliver")
    {
        this.AddParameter("start_all", "Render All", "Render");
        this.AddParameter("start_new", "Render New", "Render");
        this.AddParameter("stop", "Stop Render", "Render");
        this.AddParameter("status", "Queue Status", "Status");
    }

    protected override async void RunCommand(string actionParameter)
    {
        try
        {
            if (actionParameter == "start_all")
            {
                await _bridge.SendCommandAsync("render.start.all");
            }
            else if (actionParameter == "start_new")
            {
                await _bridge.SendCommandAsync("render.start.new");
            }
            else if (actionParameter == "stop")
            {
                await _bridge.SendCommandAsync("render.stop");
            }
        }
        catch (Exception ex)
        {
            PluginLog.Warning($"RenderQueueAction error: {ex.Message}");
        }
    }
}
