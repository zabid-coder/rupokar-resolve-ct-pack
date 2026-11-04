namespace Rupokar.Resolve.Actions;

using Loupedeck;

public class RupokarResolvePlugin : Plugin
{
    public override bool HasNoApplication => false;
    public override bool UsesApplicationApiOnly => false;

    public override void Load()
    {
        PluginLog.Info("Rupokar Resolve Actions Plugin Loaded");
    }

    public override void Unload()
    {
        PluginLog.Info("Rupokar Resolve Actions Plugin Unloaded");
    }
}
