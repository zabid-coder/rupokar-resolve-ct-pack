namespace Rupokar.Resolve.Actions.DynamicDisplay;

using Loupedeck;
using System.Drawing;

public static class TileImageRenderer
{
    public static BitmapImage DrawTimerCountdown(string timeText, bool isElapsed)
    {
        using var builder = new BitmapBuilder(256, 256);
        builder.FillRectangle(0, 0, 256, 256, BitmapColor.Black);

        var accentColor = isElapsed ? new BitmapColor(255, 60, 60) : new BitmapColor(78, 224, 226);
        builder.DrawRectangle(4, 4, 248, 248, accentColor);

        builder.DrawText(isElapsed ? "BREAK NOW!" : timeText, 0, 80, 256, 60, BitmapColor.White, 36);
        builder.DrawText("Break Status", 0, 180, 256, 40, accentColor, 20);

        return builder.ToImage();
    }
}
