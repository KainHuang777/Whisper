# Windows PowerShell Environment Initialization Script

Write-Host "==================================================" -ForegroundColor Green
Write-Host "  Whisper ASR Project - Windows Initialization" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# 1. Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found. Please install Python 3.10+ and add it to PATH."
    exit 1
}

# 2. Create Virtual Environment
if (!(Test-Path ".venv")) {
    Write-Host "[1/4] Creating virtual environment (.venv)..." -ForegroundColor Cyan
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment!"
        exit 1
    }
} else {
    Write-Host "[1/4] Virtual environment (.venv) already exists." -ForegroundColor Yellow
}

# 3. Upgrade pip
Write-Host "[2/4] Upgrading pip..." -ForegroundColor Cyan
& .venv\Scripts\python.exe -m pip install --upgrade pip

# 4. Install PyTorch with CUDA 12.1
Write-Host "[3/4] Installing PyTorch with CUDA 12.1..." -ForegroundColor Cyan
& .venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 5. Install other requirements
Write-Host "[4/4] Installing other requirements (requirements.txt)..." -ForegroundColor Cyan
& .venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "==================================================" -ForegroundColor Green
Write-Host "  Initialization Completed!" -ForegroundColor Green
Write-Host "  To activate virtual environment:" -ForegroundColor Green
Write-Host "  Run: .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Green
