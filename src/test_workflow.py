import os
import sys
import subprocess

def test_ffmpeg():
    """檢查系統是否安裝了 FFmpeg"""
    print("[測試 1/3] 正在檢查 FFmpeg...")
    try:
        # 執行 ffmpeg -version
        result = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            version_line = result.stdout.decode('utf-8', errors='ignore').split('\n')[0]
            print(f"  [成功] 偵測到 FFmpeg: {version_line}")
            return True
    except FileNotFoundError:
        pass
    print("  [失敗] 系統中找不到 ffmpeg。請下載並將其加入 PATH 中。")
    return False

def test_pytorch_cuda():
    """檢查 PyTorch 與 CUDA 環境是否正常"""
    print("[測試 2/3] 正在檢查 PyTorch 與 CUDA...")
    try:
        import torch
        print(f"  - PyTorch 版本: {torch.__version__}")
        cuda_available = torch.cuda.is_available()
        print(f"  - CUDA 是否可用: {cuda_available}")
        if cuda_available:
            print(f"  - GPU 裝置名稱: {torch.cuda.get_device_name(0)}")
            print(f"  - 可用 GPU 數量: {torch.cuda.device_count()}")
        else:
            print("  [提示] 目前無法使用 GPU。若要使用地端 GPU 加速，請安裝支援 CUDA 的 PyTorch 並且確認顯卡驅動正常。")
        return True
    except ImportError:
        print("  [失敗] 找不到 PyTorch 套件，請先執行 setup.ps1 初始化環境。")
        return False

def test_whisper_model():
    """使用 tiny 模型測試 faster-whisper 是否能正常運作"""
    print("[測試 3/3] 正在測試 faster-whisper (使用 tiny 模型進行輕量測試)...")
    try:
        from faster_whisper import WhisperModel
        import torch
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 依序嘗試的計算精度列表 (依優先順序)
        compute_types = ["float16", "int8_float16", "int8", "float32"] if device == "cuda" else ["float32", "int8"]
        model = None
        used_compute_type = None
        
        for ct in compute_types:
            try:
                print(f"  - 嘗試載入 tiny 模型 (裝置: {device}, 精度: {ct})...")
                model = WhisperModel("tiny", device=device, compute_type=ct)
                used_compute_type = ct
                break
            except Exception as inner_e:
                print(f"    [提示] 精度 {ct} 載入失敗，原因: {str(inner_e).split('.')[0]}...")
                continue
                
        if model is None:
            raise RuntimeError("所有計算精度皆載入失敗")
            
        print(f"  [成功] faster-whisper 載入成功！(最終使用精度: {used_compute_type})")
        return True
    except Exception as e:
        print(f"  [失敗] 載入 faster-whisper 或模型時出錯: {e}")
        return False


if __name__ == "__main__":
    print("==================================================")
    print("  Whisper 專案環境與相依性自我測試")
    print("==================================================")
    
    ffmpeg_ok = test_ffmpeg()
    torch_ok = test_pytorch_cuda()
    whisper_ok = test_whisper_model() if torch_ok else False
    
    print("==================================================")
    print("測試結果摘要：")
    print(f"1. FFmpeg 環境: {'通過' if ffmpeg_ok else '未通過'}")
    print(f"2. PyTorch/CUDA 環境: {'通過' if torch_ok else '未通過'}")
    print(f"3. Whisper 模型測試: {'通過' if whisper_ok else '未通過'}")
    print("==================================================")
    
    if ffmpeg_ok and torch_ok and whisper_ok:
        print("恭喜！環境檢測完全通過，您可以正常開始執行轉錄工作流。")
        sys.exit(0)
    else:
        print("請根據上方的失敗訊息進行排查與調整。")
        sys.exit(1)
