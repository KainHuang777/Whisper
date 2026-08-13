@echo off
chcp 65001 >nul
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

if "%~1"=="" (
    set "TARGET_VIDEO=D:\Temp\2026_08_12_19_03_14_462.mp4"
) else (
    set "TARGET_VIDEO=%~1"
)

echo ==================================================
echo   Whisper Transcription Tool
echo   Target: %TARGET_VIDEO%
echo ==================================================

".venv\Scripts\python.exe" src/transcribe_local.py --video "%TARGET_VIDEO%"

if %ERRORLEVEL% equ 0 goto :success
goto :error

:error
echo.
echo [ERROR] Transcription failed. Please check error messages above.
goto :end

:success
echo.
echo [SUCCESS] Transcription completed successfully!
goto :end

:end
pause
