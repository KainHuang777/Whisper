@echo off
chcp 65001 >nul
:: 設定 UTF-8 編碼以防止中文字在終端機亂碼

echo ==================================================
echo   Whisper 專案 - 啟動 Python 虛擬環境 (.venv)
echo ==================================================

:: 定義專案根目錄
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

:: 檢查虛擬環境是否存在
if not exist ".venv\Scripts\Activate.ps1" (
    echo [錯誤] 找不到虛擬環境 .venv。
    echo 請先執行 setup.ps1 進行初始化安裝。
    pause
    exit /b 1
)

echo 正在使用 Bypass 權限啟動 PowerShell 並載入虛擬環境...
echo 提示：您可以直接在該視窗中執行轉錄指令（例如 python src/transcribe_local.py）
echo --------------------------------------------------

powershell -NoExit -ExecutionPolicy Bypass -Command "& '%BASE_DIR%.venv\Scripts\Activate.ps1'"
