# Whisper 語音轉文字 PowerShell 腳本
param(
    [string]$VideoPath = "0902顧問交流會.mp3"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = Get-Location }
Set-Location $ScriptDir

# 自動解析路徑 (相容根目錄、media/audio、media/videos)
$ResolvedPath = $VideoPath
if (-not (Test-Path $ResolvedPath)) {
    if (Test-Path "$ScriptDir\media\audio\$VideoPath") {
        $ResolvedPath = "$ScriptDir\media\audio\$VideoPath"
    } elseif (Test-Path "$ScriptDir\media\videos\$VideoPath") {
        $ResolvedPath = "$ScriptDir\media\videos\$VideoPath"
    }
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Whisper 專案 - 語音轉文字作業" -ForegroundColor Cyan
Write-Host "  目標影片/音訊: $ResolvedPath" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

& "$ScriptDir\.venv\Scripts\python.exe" "$ScriptDir\src\transcribe_local.py" --video "$ResolvedPath"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[成功] 轉錄作業順利完成！" -ForegroundColor Green
} else {
    Write-Host "`n[錯誤] 轉錄過程發生異常，請檢查上方的錯誤訊息。" -ForegroundColor Red
}
