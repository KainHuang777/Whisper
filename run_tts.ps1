# Edge TTS 語音合成 PowerShell 腳本
param(
    [string]$Text = "歡迎使用 Edge TTS 語音合成服務，這是一段繁體中文示範音訊。",
    [string]$OutputFile = "data/output/tts_demo.mp3",
    [string]$Voice = "zh-TW-HsiaoChenNeural",
    [string]$Rate = "+0%",
    [string]$Pitch = "+0Hz",
    [switch]$ListVoices
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = Get-Location }
Set-Location $ScriptDir

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Whisper 專案 - Edge TTS 語音合成作業" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$PythonExe = "$ScriptDir\.venv\Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
    Write-Host "[錯誤] 找不到虛擬環境 Python: $PythonExe" -ForegroundColor Red
    exit 1
}

if ($ListVoices) {
    & $PythonExe "$ScriptDir\src\tts_service.py" --list-voices
} else {
    Write-Host "目標文字: $Text" -ForegroundColor Yellow
    Write-Host "目標音色: $Voice" -ForegroundColor Yellow
    Write-Host "輸出檔案: $OutputFile" -ForegroundColor Yellow
    Write-Host "--------------------------------------------------" -ForegroundColor Cyan

    & $PythonExe "$ScriptDir\src\tts_service.py" --text "$Text" --output "$OutputFile" --voice "$Voice" --rate "$Rate" --pitch "$Pitch"
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[成功] TTS 作業順利完成！" -ForegroundColor Green
} else {
    Write-Host "`n[錯誤] TTS 過程發生異常，請檢查上方的錯誤訊息。" -ForegroundColor Red
}
