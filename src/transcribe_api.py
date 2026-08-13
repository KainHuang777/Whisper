import os
import argparse
import subprocess
import hashlib
import tempfile
from google import genai
from google.genai import types


def extract_compressed_audio(video_path: str, audio_path: str) -> str:
    """
    從影片中抽取音訊並轉成 MP3 格式 (64kbps, 單聲道)
    這能讓 2 小時的音訊檔案體積大幅縮小至 30~50MB 以內，加快上傳至 API 的速度。
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"找不到影片檔案: {video_path}")
        
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    if os.path.exists(audio_path):
        print(f"[提示] 壓縮音訊已存在，跳過抽取: {audio_path}")
        return audio_path

    print(f"[音訊抽取] 正在抽取並壓縮音訊為 MP3: {os.path.basename(video_path)} ...")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "64k",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"[音訊抽取] 成功儲存壓縮音訊至: {audio_path}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8', errors='ignore')
        print(f"[錯誤] ffmpeg 執行失敗。請確認系統已安裝 ffmpeg 並加入環境變數。")
        print(f"詳細錯誤資訊: {error_msg}")
        raise e
        
    return audio_path

def transcribe_with_gemini(video_path: str, model_name: str = "gemini-2.5-flash"):
    """
    使用 Google Gemini API 進行多模態音訊轉錄並直接生成 SRT 字幕
    """
    # 確保 API Key 存在
    if not os.environ.get("GEMINI_API_KEY"):
        print("[錯誤] 未設定 GEMINI_API_KEY 環境變數。")
        print("請在執行前設定環境變數，例如:")
        print("Windows (PowerShell): $env:GEMINI_API_KEY=\"your_key_here\"")
        print("Windows (CMD): set GEMINI_API_KEY=your_key_here")
        print("Linux/macOS: export GEMINI_API_KEY=\"your_key_here\"")
        return

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    video_filename = os.path.basename(video_path)
    video_name, _ = os.path.splitext(video_filename)
    
    # 使用影片絕對路徑的 MD5 雜湊作為臨時檔名，確保路徑與檔名完全是英文 ASCII
    # 同時對於同一個影片，其臨時檔名是固定的，能保留 ffmpeg 音訊抽取的快取功能
    video_abs_path = os.path.abspath(video_path)
    video_hash = hashlib.md5(video_abs_path.encode("utf-8")).hexdigest()
    audio_path = os.path.join(tempfile.gettempdir(), f"whisper_temp_{video_hash}.mp3")
    
    srt_path = os.path.join(base_dir, "data", "output", f"{video_name}.srt")
    
    # 1. 抽取壓縮音訊
    try:
        extract_compressed_audio(video_path, audio_path)
    except Exception as e:
        print(f"[錯誤] 音訊抽取失敗，結束程序: {e}")
        return

    # 2. 初始化 Gemini SDK 客戶端
    print(f"[Gemini API] 正在連接 Gemini API...")
    client = genai.Client()

    # 3. 上傳音訊檔案到 Google 伺服器 (File API)
    # 這是處理大檔案 (>20MB) 的標準推薦做法，上傳後會自動產生一組 URI 供模型調用
    print(f"[Gemini API] 正在上傳音訊檔至 Google File API (這可能需要幾分鐘，取決於您的網路速度)...")
    try:
        uploaded_file = client.files.upload(file=audio_path)
        print(f"[Gemini API] 檔案上傳成功，遠端名稱: {uploaded_file.name}")
        print(f"[Gemini API] 正在等待檔案由 Google 伺服器處理完成...")
        
        # 等待檔案狀態變更為 ACTIVE
        import time
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(5)
            uploaded_file = client.files.get(name=uploaded_file.name)
            
        if uploaded_file.state.name != "ACTIVE":
            raise Exception(f"檔案上傳後狀態異常: {uploaded_file.state.name}")
            
        print(f"[Gemini API] 檔案處理完成。")
        
    except Exception as e:
        print(f"[錯誤] 檔案上傳至 Gemini API 失敗: {e}")
        return

    try:
        # 4. 呼叫多模態模型進行轉錄
        print(f"[Gemini API] 正在使用 {model_name} 進行音訊分析與 SRT 字幕生成...")
        prompt = (
            "你是一個專業的影音語音轉錄專家。請仔細聆聽這段音訊，將其轉錄為精確的繁體中文逐字稿，"
            "並輸出為標準的 `.srt` 字幕格式。\n\n"
            "規範限制：\n"
            "1. 必須嚴格使用 SRT 時間戳記格式: [順序編號]\\n[HH:MM:SS,mmm] --> [HH:MM:SS,mmm]\\n[字幕內容]\\n\\n\n"
            "2. 請將繁體中文口語轉化為合適的書面字幕，並保留正確的中英夾雜專有名詞（如 API, CUDA, GPU 等）。\n"
            "3. 確保字幕時間戳記與語音內容儘量對齊。\n"
            "4. **請只輸出 SRT 檔案內容，不要包含額外的 Markdown 標籤 (例如 ```srt) 或任何說明文字。**"
        )
        
        response = client.models.generate_content(
            model=model_name,
            contents=[uploaded_file, prompt]
        )
        
        srt_content = response.text
        
        # 清理可能被模型多加的 ```srt 或 ``` 標記
        if srt_content.startswith("```"):
            lines = srt_content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].strip() == "```":
                lines = lines[:-1]
            srt_content = "\n".join(lines)

        # 5. 寫入 SRT 字幕檔
        os.makedirs(os.path.dirname(srt_path), exist_ok=True)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content.strip() + "\n")
            
        print(f"==================================================")
        print(f"[完成] Gemini API 語音轉字幕成功！")
        print(f"  - 輸出字幕: {srt_path}")
        print(f"==================================================")

    except Exception as e:
        print(f"[錯誤] 呼叫 Gemini API 轉錄失敗: {e}")
    finally:
        # 6. 清理遠端暫存檔案
        print(f"[Gemini API] 正在清理雲端暫存音訊檔...")
        try:
            client.files.delete(name=uploaded_file.name)
            print(f"[Gemini API] 雲端清理完成。")
        except Exception as e:
            print(f"[警告] 清理雲端暫存檔失敗: {e}")
            
        # 清理地端暫存檔
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gemini API 影片語音轉文字工具")
    parser.add_argument("--video", type=str, help="輸入影片的絕對路徑或相對路徑")
    parser.add_argument(
        "--model", 
        type=str, 
        default="gemini-2.5-flash", 
        help="Gemini 模型版本 (預設使用 gemini-2.5-flash)"
    )
    
    args = parser.parse_args()
    
    if not args.video:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_dir = os.path.join(base_dir, "data", "input")
        output_dir = os.path.join(base_dir, "data", "output")
        os.makedirs(input_dir, exist_ok=True)
        
        video_exts = (".mp4", ".mkv", ".avi", ".mov")
        
        def pick_unprocessed_video(source_dir, source_name):
            """從指定目錄中挑選尚未產出 .srt 字幕的影片"""
            candidates = []
            skipped = 0
            for f in os.listdir(source_dir):
                if f.lower().endswith(video_exts):
                    name = os.path.splitext(f)[0]
                    srt = os.path.join(output_dir, f"{name}.srt")
                    if os.path.exists(srt):
                        skipped += 1
                    else:
                        candidates.append(os.path.join(source_dir, f))
            if skipped > 0:
                print(f"[提示] 跳過 {skipped} 個已處理影片（{source_name} 中 .srt 已存在）")
            return candidates
        
        videos = pick_unprocessed_video(input_dir, "data/input")
        source = "輸入資料夾"
        
        if not videos:
            videos = pick_unprocessed_video(base_dir, "根目錄")
            source = "根目錄"
        
        if videos:
            selected_video = videos[0]
            print(f"[提示] 未指定影片，自動選擇{source}中的影片: {selected_video}")
            args.video = selected_video
        else:
            print(f"[錯誤] 沒有尚未處理的影片。請使用 --video 參數指定影片，或將影片放入 data/input/ 中。")
            parser.print_help()
            exit(1)
                
    transcribe_with_gemini(video_path=args.video, model_name=args.model)
