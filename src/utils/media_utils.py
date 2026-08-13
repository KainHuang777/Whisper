import os
import subprocess

def format_timestamp(seconds: float) -> str:
    """將秒數轉換為 SRT 格式的時間字串 (HH:MM:SS,mmm)"""
    milliseconds = int(round((seconds - int(seconds)) * 1000))
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def extract_audio(video_path: str, audio_path: str) -> str:
    """
    從影片中抽取音訊，儲存為 WAV 格式 (16kHz, 單聲道，適合 ASR)
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"找不到影片檔案: {video_path}")
        
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    
    # 如果已經存在對應的音訊檔，直接返回 (避免重複抽取)
    if os.path.exists(audio_path):
        print(f"[提示] 音訊檔已存在，跳過抽取: {audio_path}")
        return audio_path

    print(f"[音訊抽取] 正在從 {os.path.basename(video_path)} 抽離音訊...")
    
    # 呼叫 ffmpeg 指令
    # -y: 強制覆寫
    # -i: 輸入檔案
    # -vn: 停用影片
    # -acodec pcm_s16le: 設定音訊編碼為 16-bit PCM WAV
    # -ar 16000: 取樣率 16kHz
    # -ac 1: 單聲道
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]
    
    try:
        # 使用 subprocess 執行，不顯示詳細 log，只在錯誤時報錯
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"[音訊抽取] 成功儲存至: {audio_path}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8', errors='ignore')
        print(f"[錯誤] ffmpeg 執行失敗。請確認系統是否已安裝 ffmpeg 並加入環境變數中。")
        print(f"詳細錯誤資訊: {error_msg}")
        raise e
        
    return audio_path

def preprocess_audio(input_path: str, output_path: str) -> str:
    """
    對音訊進行語音增強前處理：高通濾波 (80Hz)、降噪 (afftdn)、動態響度標準化 (dynaudnorm)
    能有效提升微弱語音訊號，避免被 VAD 過濾掉。
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"找不到音訊檔案: {input_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.exists(output_path):
        print(f"[提示] 前處理音訊已存在，跳過: {output_path}")
        return output_path

    print(f"[音訊前處理] 正在加強語音訊號 (除噪 + 動態響度標準化)...")

    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-af", "highpass=f=80,afftdn=nr=10:nf=-30,dynaudnorm",
        "-ar", "16000",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"[音訊前處理] 完成，儲存至: {output_path}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8', errors='ignore')
        print(f"[錯誤] 音訊前處理失敗。請確認 ffmpeg 支援 afftdn 與 dynaudnorm 濾鏡。")
        print(f"詳細錯誤資訊: {error_msg}")
        raise e

    return output_path


def write_srt(segments, srt_path: str):
    """
    將 Whisper 的 segments 寫入成 SRT 字幕檔
    """
    os.makedirs(os.path.dirname(srt_path), exist_ok=True)
    print(f"[字幕生成] 正在寫入 SRT 字幕檔: {srt_path} ...")
    
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(segments, start=1):
            start_str = format_timestamp(segment.start)
            end_str = format_timestamp(segment.end)
            text = segment.text.strip()
            
            # 寫入 SRT 段落
            f.write(f"{idx}\n")
            f.write(f"{start_str} --> {end_str}\n")
            f.write(f"{text}\n\n")
            
    print(f"[字幕生成] 字幕寫入完成！共 {idx} 段字幕。")
