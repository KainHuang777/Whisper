@echo off
chcp 65001 >nul
:: 設定 UTF-8 編碼以防止中文字在終端機亂碼

echo ==================================================
echo   Whisper 影片字幕燒錄工具 (FFmpeg)
echo ==================================================

:: 檢查 ffmpeg 是否可用
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo [錯誤] 系統中找不到 ffmpeg 指令。
    echo 請確保已安裝 ffmpeg 並將其路徑加入到環境變數 PATH 中。
    goto :end
)

:: 定義專案根目錄
set "BASE_DIR=%~dp0"
set "INPUT_DIR=%BASE_DIR%data\input"
set "OUTPUT_DIR=%BASE_DIR%data\output"

:: 初始化參數
set "VIDEO_PATH="
set "SRT_PATH="

:: 1. 檢查參數或自動偵測
if "%~1"=="" (
    echo [提示] 未提供參數，開始自動偵測 data\input 中的影片與 data\output 中的字幕...
    
    :: 尋找第一個影片
    for /f "delims=" %%f in ('dir /b /a-d "%INPUT_DIR%\*.mp4" 2^>nul') do (
        set "VIDEO_PATH=%INPUT_DIR%\%%f"
        set "VIDEO_NAME=%%~nf"
        goto :find_srt
    )
    
    :: 如果 input 沒有，去根目錄找
    for /f "delims=" %%f in ('dir /b /a-d "%BASE_DIR%\*.mp4" 2^>nul') do (
        set "VIDEO_PATH=%BASE_DIR%%%f"
        set "VIDEO_NAME=%%~nf"
        goto :find_srt
    )

    :find_srt
    if not defined VIDEO_PATH (
        echo [錯誤] 找不到任何 .mp4 影片檔案。
        echo 請將影片放入 data\input\ 中，或直接拖曳影片到此批次檔上。
        goto :end
    )

    :: 尋找同名的 SRT 字幕
    if exist "%OUTPUT_DIR%\%VIDEO_NAME%.srt" (
        set "SRT_PATH=%OUTPUT_DIR%\%VIDEO_NAME%.srt"
    ) else if exist "%BASE_DIR%\%VIDEO_NAME%.srt" (
        set "SRT_PATH=%BASE_DIR%\%VIDEO_NAME%.srt"
    ) else (
        echo [錯誤] 找到影片 %VIDEO_NAME%.mp4，但找不到對應的字幕檔 %VIDEO_NAME%.srt。
        echo 請確認字幕是否已生成，並放在 data\output\ 中。
        goto :end
    )
) else (
    :: 若有傳入參數
    set "VIDEO_PATH=%~1"
    set "SRT_PATH=%~2"
    
    if "%~2" == "" (
        :: 如果只傳入影片，自動推導同名 srt
        for %%f in ("%~1") do set "VIDEO_NAME=%%~nf"
        set "SRT_PATH=%OUTPUT_DIR%\%VIDEO_NAME%.srt"
    )
)

if not exist "%VIDEO_PATH%" (
    echo [錯誤] 影片檔案不存在: %VIDEO_PATH%
    goto :end
)

if not exist "%SRT_PATH%" (
    echo [錯誤] 字幕檔案不存在: %SRT_PATH%
    goto :end
)

:: 取得影片名稱與副檔名
for %%i in ("%VIDEO_PATH%") do (
    set "V_DIR=%%~dpi"
    set "V_NAME=%%~ni"
    set "V_EXT=%%~xi"
)

:: 產生輸出路徑 (加 _subtitle 字樣)
set "OUT_VIDEO_PATH=%OUTPUT_DIR%\%V_NAME%_subtitled%V_EXT%"
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo ==================================================
echo 準備燒錄字幕：
echo 影片：%VIDEO_PATH%
echo 字幕：%SRT_PATH%
echo 輸出：%OUT_VIDEO_PATH%
echo ==================================================
echo 正在使用 FFmpeg 進行燒錄，這可能需要幾分鐘...

:: 在 Windows 下，FFmpeg 的 subtitles filter 中，路徑的分隔符號必須特別處理：
:: 1. 冒號 ':' 要寫成 '\:'
:: 2. 斜線 '\' 要寫成 '/' 或 '\\'
:: 這裡透過變數替換將 SRT 路徑格式化
set "FFMPEG_SRT_PATH=%SRT_PATH:\=/%"
set "FFMPEG_SRT_PATH=%FFMPEG_SRT_PATH::=\:%"

ffmpeg -y -i "%VIDEO_PATH%" -vf "subtitles='%FFMPEG_SRT_PATH%':force_style='Fontname=Microsoft JhengHei,Fontsize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1,Shadow=0,Alignment=2,MarginV=20'" -c:a copy "%OUT_VIDEO_PATH%"

if %errorlevel% equ 0 (
    echo --------------------------------------------------
    echo [成功] 字幕已成功燒錄至影片中！
    echo 輸出影片路徑: %OUT_VIDEO_PATH%
    echo --------------------------------------------------
) else (
    echo --------------------------------------------------
    echo [錯誤] FFmpeg 燒錄字幕失敗！請檢查上方錯誤訊息。
    echo --------------------------------------------------
)

:end
pause
