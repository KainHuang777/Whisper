# Edge TTS 語音合成 PowerShell 腳本
param(
    [string]$Text,
    [string]$File,
    [string]$OutputFile,
    [string]$Voice,
    [string]$Rate = "+0%",
    [string]$Pitch = "+0Hz",
    [switch]$Interactive,
    [switch]$ListVoices
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = Get-Location }
Set-Location $ScriptDir

$PythonExe = "$ScriptDir\.venv\Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
    Write-Host "[錯誤] 找不到虛擬環境 Python: $PythonExe" -ForegroundColor Red
    exit 1
}

if ($ListVoices) {
    & $PythonExe "$ScriptDir\src\tts_service.py" --list-voices
} elseif ($Interactive -or (-not $Text -and -not $File)) {
    # 預設無參數時啟動互動模式
    & $PythonExe "$ScriptDir\src\tts_service.py" --interactive
} else {
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "  Whisper 專案 - Edge TTS 語音合成作業" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan

    $argsList = @()
    if ($Text) { $argsList += @("--text", $Text) }
    if ($File) { $argsList += @("--file", $File) }
    if ($OutputFile) { $argsList += @("--output", $OutputFile) }
    if ($Voice) { $argsList += @("--voice", $Voice) }
    if ($Rate) { $argsList += @("--rate", $Rate) }
    if ($Pitch) { $argsList += @("--pitch", $Pitch) }

    & $PythonExe "$ScriptDir\src\tts_service.py" @argsList

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[成功] TTS 作業順利完成！" -ForegroundColor Green
    } else {
        Write-Host "`n[錯誤] TTS 過程發生異常，請檢查上方的錯誤訊息。" -ForegroundColor Red
    }
}
