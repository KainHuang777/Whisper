# Whisper 語音轉文字 PowerShell 腳本
param(
    [string]$VideoPath = "D:\Temp\2026_08_12_19_03_14_462.mp4"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = Get-Location }
Set-Location $ScriptDir

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Whisper 專案 - 語音轉文字作業" -ForegroundColor Cyan
Write-Host "  目標影片: $VideoPath" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

& "$ScriptDir\.venv\Scripts\python.exe" "$ScriptDir\src\transcribe_local.py" --video "$VideoPath"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[成功] 轉錄作業順利完成！" -ForegroundColor Green
} else {
    Write-Host "`n[錯誤] 轉錄過程發生異常，請檢查上方的錯誤訊息。" -ForegroundColor Red
}
