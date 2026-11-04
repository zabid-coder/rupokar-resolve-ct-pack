namespace Rupokar.Resolve.Actions.Actions;

using Loupedeck;
using System.Timers;
using Rupokar.Resolve.Actions.DynamicDisplay;

public class BreakTimerAction : PluginDynamicCommand
{
    private static Timer? _timer;
    private static int _remainingSeconds;
    private static bool _isRunning;

    public BreakTimerAction() : base("Break Timer", "Timer controls and countdown display", "Break Timer")
    {
        this.AddParameter("25m", "25 Minutes", "Intervals");
        this.AddParameter("45m", "45 Minutes", "Intervals");
        this.AddParameter("1h", "1 Hour", "Intervals");
        this.AddParameter("1.5h", "1.5 Hours", "Intervals");
        this.AddParameter("2h", "2 Hours", "Intervals");
        this.AddParameter("2.5h", "2.5 Hours", "Intervals");
        this.AddParameter("3h", "3 Hours", "Intervals");
        this.AddParameter("4h", "4 Hours", "Intervals");
        this.AddParameter("start", "Start Timer", "Controls");
        this.AddParameter("stop", "Stop Timer", "Controls");
        this.AddParameter("status", "Timer Status", "Display");

        if (_timer == null)
        {
            _timer = new Timer(1000);
            _timer.Elapsed += OnTimerElapsed;
            _timer.AutoReset = true;
        }
    }

    private void OnTimerElapsed(object? sender, ElapsedEventArgs e)
    {
        if (!_isRunning) return;

        if (_remainingSeconds > 0)
        {
            _remainingSeconds--;
        }
        this.ActionImageChanged();
    }

    protected override void RunCommand(string actionParameter)
    {
        if (actionParameter == "start")
        {
            _isRunning = true;
            _timer?.Start();
        }
        else if (actionParameter == "stop")
        {
            _isRunning = false;
            _timer?.Stop();
            _remainingSeconds = 0;
            this.ActionImageChanged();
        }
        else if (actionParameter.EndsWith("m") || actionParameter.EndsWith("h"))
        {
            _remainingSeconds = actionParameter switch
            {
                "25m" => 25 * 60,
                "45m" => 45 * 60,
                "1h" => 60 * 60,
                "1.5h" => 90 * 60,
                "2h" => 120 * 60,
                "2.5h" => 150 * 60,
                "3h" => 180 * 60,
                "4h" => 240 * 60,
                _ => 25 * 60
            };
            this.ActionImageChanged();
        }
    }

    protected override BitmapImage GetCommandImage(string actionParameter, PluginImageSize imageSize)
    {
        if (actionParameter == "status")
        {
            var minutes = _remainingSeconds / 60;
            var seconds = _remainingSeconds % 60;
            var text = _isRunning ? $"{minutes:00}:{seconds:00}" : "IDLE";
            return TileImageRenderer.DrawTimerCountdown(text, _isRunning && _remainingSeconds == 0);
        }
        return base.GetCommandImage(actionParameter, imageSize);
    }
}
