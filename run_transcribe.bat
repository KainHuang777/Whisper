@echo off
chcp 65001 >nul
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

if "%~1"=="" (
    set "TARGET_VIDEO=media\audio\0902顧問交流會.mp3"
) else (
    set "TARGET_VIDEO=%~1"
)

rem 若原路徑不存在，檢查 media/audio 與 media/videos
if not exist "%TARGET_VIDEO%" (
    if exist "media\audio\%TARGET_VIDEO%" set "TARGET_VIDEO=media\audio\%TARGET_VIDEO%"
    if exist "media\videos\%TARGET_VIDEO%" set "TARGET_VIDEO=media\videos\%TARGET_VIDEO%"
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
