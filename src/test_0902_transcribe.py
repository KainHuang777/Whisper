import os
import sys

def test_environment_and_file():
    print("==================================================")
    print("  0902 顧問交流會轉錄流程 - 前置驗證測試")
    print("==================================================")
    
    # 1. 檢查 Python 執行環境
    print(f"[環境資訊] Python 執行路徑: {sys.executable}")
    is_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if is_venv:
        print("[環境檢查] 成功載入虛擬環境 (.venv)")
    else:
        print("[環境警告] 目前非虛擬環境，若套件缺失請透過 activate.bat 載入環境。")

    # 2. 檢查 faster-whisper 套件
    try:
        import faster_whisper
        print(f"[套件檢查] faster-whisper 載入成功 (版本: {getattr(faster_whisper, '__version__', '未知')})")
    except ImportError as e:
        print(f"[套件錯誤] 無法載入 faster-whisper: {e}")
        print("請確認是否使用 .venv 虛擬環境執行。")
        return False

    # 3. 檢查 PyTorch 與 CUDA
    try:
        import torch
        cuda_avail = torch.cuda.is_available()
        print(f"[硬體檢查] PyTorch 載入成功，CUDA 可用性: {cuda_avail}")
        if cuda_avail:
            print(f"  - 顯示卡: {torch.cuda.get_device_name(0)}")
    except ImportError:
        print("[套件警告] 尚未安裝 PyTorch，將依賴 ctranslate2 底層推論")

    # 4. 檢查目標音訊檔案
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_mp3 = os.path.join(base_dir, "0902顧問交流會.mp3")
    if os.path.exists(target_mp3):
        file_size_mb = os.path.getsize(target_mp3) / (1024 * 1024)
        print(f"[檔案檢查] 找到目標音訊: {target_mp3} ({file_size_mb:.2f} MB)")
    else:
        print(f"[檔案錯誤] 找不到目標音訊檔案: {target_mp3}")
        return False

    print("==================================================")
    print("[測試通過] 前置環境與目標檔案確認無誤！")
    print("您可以直接執行以下指令開始轉錄：")
    print("  python src/transcribe_local.py --video \"0902顧問交流會.mp3\"")
    print("  或者在專案根目錄執行 .\\run_transcribe.ps1")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = test_environment_and_file()
    sys.exit(0 if success else 1)
