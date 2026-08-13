#!/bin/bash

# Linux/macOS 環境初始化腳本
echo "=================================================="
echo "  Whisper 語音轉文字專案 - Linux/macOS 環境初始化開始"
echo "=================================================="

# 1. 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "錯誤: 找不到 python3，請先安裝 Python 3。"
    exit 1
fi

# 2. 建立虛擬環境
if [ ! -d ".venv" ]; then
    echo "[1/4] 正在建立 Python 虛擬環境 (.venv)..."
    python3 -m venv .venv
else
    echo "[1/4] 虛擬環境 (.venv) 已存在，跳過建立。"
fi

# 3. 啟動並升級 pip
echo "[2/4] 正在升級 pip..."
source .venv/bin/activate
pip install --upgrade pip

# 4. 安裝支援 CUDA 12.1 的 PyTorch (在 Mac 上會自動安裝 CPU/MPS 版本)
echo "[3/4] 正在安裝支援 CUDA 的 PyTorch..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
else
    # macOS 或其他
    pip install torch torchvision torchaudio
fi

# 5. 安裝其餘依賴套件
echo "[4/4] 正在安裝其餘相依套件 (requirements.txt)..."
pip install -r requirements.txt

echo "=================================================="
echo "  初始化完成！"
echo "  如何使用虛擬環境："
echo "  執行: source .venv/bin/activate"
echo "=================================================="
