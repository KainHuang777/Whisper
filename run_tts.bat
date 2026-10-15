@echo off
chcp 65001 >nul
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

set "PYTHON_EXE=%BASE_DIR%.venv\Scripts\python.exe"
set "TTS_SCRIPT=%BASE_DIR%src\tts_service.py"

if not exist "%PYTHON_EXE%" goto :no_venv

if "%~1"=="" goto :interactive
goto :args_mode

:interactive
"%PYTHON_EXE%" "%TTS_SCRIPT%" --interactive
if %ERRORLEVEL% equ 0 goto :success
goto :error

:args_mode
echo ==================================================
echo   Edge TTS Tool
echo ==================================================
"%PYTHON_EXE%" "%TTS_SCRIPT%" %*
if %ERRORLEVEL% equ 0 goto :success
goto :error

:no_venv
echo.
echo [ERROR] Virtual environment Python not found: %PYTHON_EXE%
goto :end

:error
echo.
echo [ERROR] TTS task failed with error.
goto :end

:success
echo.
echo [SUCCESS] TTS task completed successfully.
goto :end

:end
echo.
pause
