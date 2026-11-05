@echo off
setlocal enabledelayedexpansion
title Rupokar Studios - Loupedeck CT Pack Installer for DaVinci Resolve

echo ========================================================================
echo    ____             _              ____  _             _ _            
echo   ^|  _ \ _   _ _ __ ^| ^| _____  _ __/ ___^|^| ^|_ _   _  __^| (_) ___  ___ 
echo   ^| ^|_) ^| ^| ^| ^| '_ \^| ^|/ / _ \^| '__\___ \^| __^| ^| ^| ^|/ _` ^| ^|/ _ \/ __^|
echo   ^|  _ ^<^| ^|_^| ^| ^|_) ^|   ^< (_) ^| ^|   ___) ^| ^|_^| ^|_^| ^| (_^| ^| ^| (_) \__ \
echo   ^|_^| \_\\__,_^| .__/^|_^|\_\___/^|_^|  ^|____/ \__^|\__,_^|\__,_^|_^|\___/^|___/
echo               ^|_^|                                                     
echo       Loupedeck CT 168-Action Master Pack for DaVinci Resolve Studio    
echo ========================================================================
echo.

:: 1. Close Loupedeck processes to unlock files
echo [*] Closing Loupedeck to prevent file conflicts...
taskkill /F /IM Loupedeck.exe 2>nul
taskkill /F /IM LogiPluginService.exe 2>nul
timeout /t 2 /nobreak >nul

:: 2. Auto-copy keyboard shortcuts preset into DaVinci Resolve
set "RESOLVE_KEY_DIR=%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Keyboard Shortcuts"
if not exist "%RESOLVE_KEY_DIR%" (
    mkdir "%RESOLVE_KEY_DIR%" 2>nul
)
if exist "keyboard-preset\Rupokar_Resolve_Keys.txt" (
    copy /Y "keyboard-preset\Rupokar_Resolve_Keys.txt" "%RESOLVE_KEY_DIR%\" >nul
    echo [OK] Auto-installed DaVinci Resolve keyboard shortcut preset:
    echo      ^-%RESOLVE_KEY_DIR%\Rupokar_Resolve_Keys.txt
)

:: 3. Check for Python 3
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Detected Python. Running full profile injector...
    python scripts\build_icons.py
    python scripts\export_raster_icons.py
    python scripts\build_profile.py
    python scripts\install_ct_profile.py
) else (
    echo [i] Python not detected. Installing pre-built Loupedeck profile package...
    if exist "profile\Rupokar-Resolve-CT.lp5" (
        start "" "profile\Rupokar-Resolve-CT.lp5"
    )
)

:: 4. Relaunch Loupedeck
echo [*] Restarting Loupedeck...
if exist "%LOCALAPPDATA%\Programs\Loupedeck\Loupedeck.exe" (
    start "" "%LOCALAPPDATA%\Programs\Loupedeck\Loupedeck.exe"
) else (
    start "" "loupedeck:" 2>nul
)

echo.
echo ========================================================================
echo  INSTALLATION SUCCESSFUL! All 8 Workspaces ^& 168 Actions Ready!
echo ========================================================================
echo [1] Media ^& Project (Media Pool + Auto Break Timers)
echo [2] Edit 1 - Timeline ^& Cuts (Razor, Trims, Ripple, Gaps)
echo [3] Edit 2 - Sync ^& Colors (Audio Sync ^& Clip Colors)
echo [4] Edit 3 - Fine Tuning (Precision Nudge ^& Timing)
echo [5] Color - Nodes ^& Wheels (Node Tree, Scopes, Still, Compare)
echo [6] Fairlight - Audio ^& Fades (Audio Level, Zoom, Normalize)
echo [7] Deliver ^& Render Queue (YouTube, ProRes, Queue, Render)
echo [8] Quick Export ^& Panels (Quick Export, 7 UI Panels, Bypass)
echo ========================================================================
echo.
pause
