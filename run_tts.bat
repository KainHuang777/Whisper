@echo off
chcp 65001 >nul
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

echo ==================================================
echo   Edge TTS 語音合成工具
echo ==================================================

if "%~1"=="" (
    echo [提示] 未傳入參數，將以預設文字進行示範合成...
    ".venv\Scripts\python.exe" src/tts_service.py --text "歡迎使用 Edge TTS 語音合成服務，這是一段繁體中文示範音訊。" --output "data/output/tts_demo.mp3"
) else (
    ".venv\Scripts\python.exe" src/tts_service.py %*
)

if %ERRORLEVEL% equ 0 (
    echo.
    echo [成功] 語音作業順利完成！
) else (
    echo.
    echo [錯誤] 語音作業發生異常，請檢查上方訊息。
)

echo.
pause
