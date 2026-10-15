import os
import argparse
from datetime import datetime
from faster_whisper import WhisperModel
from utils.media_utils import extract_audio, preprocess_audio, write_srt

def transcribe_video(
    video_path: str,
    model_size: str = "large-v3",
    device: str = "cuda",
    compute_type: str = "int8_float16",
    language: str = "zh",
    vad_filter: bool = True,
    preprocess: bool = False
):
    """
    本機 GPU 語音辨識與字幕生成主流程
    """
    # 1. 確保目錄路徑正確
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    video_filename = os.path.basename(video_path)
    video_name, _ = os.path.splitext(video_filename)
    
    # 定義音訊與字幕輸出路徑
    audio_path = os.path.join(base_dir, "data", "audio", f"{video_name}.wav")
    srt_path = os.path.join(base_dir, "data", "output", f"{video_name}.srt")
    
    # 2. 抽離音訊
    try:
        extract_audio(video_path, audio_path)
    except Exception as e:
        print(f"[錯誤] 音訊抽取失敗，結束程序: {e}")
        return

    # 2.5. 語音增強前處理 (可選)
    if preprocess:
        enhanced_path = os.path.join(base_dir, "data", "audio", f"{video_name}_enhanced.wav")
        try:
            audio_path = preprocess_audio(audio_path, enhanced_path)
        except Exception as e:
            print(f"[警告] 音訊前處理失敗，改用原始音訊繼續: {e}")

    # 3. 決定降級嘗試的計算精度順序
    fallback_types = [compute_type]
    if device == "cuda":
        # 依效能與顯存友善度排序的 CUDA 精度降級順序
        priority_order = ["int8_float16", "int8", "float32"]
        for ct in priority_order:
            if ct not in fallback_types:
                fallback_types.append(ct)

    start_time = datetime.now()

    for attempt_idx, current_ct in enumerate(fallback_types):
        print(f"==================================================")
        print(f"[模型載入] 正在初始化 Whisper 模型...")
        print(f"  - 模型大小: {model_size}")
        print(f"  - 執行裝置: {device}")
        print(f"  - 計算精度: {current_ct}")
        print(f"==================================================")
        
        try:
            model = WhisperModel(model_size, device=device, compute_type=current_ct)
            print(f"[語音辨識] 開始進行語音辨識 (VAD 語音活動偵測狀態: {vad_filter})...")
            
            segments, info = model.transcribe(
                audio_path,
                beam_size=5,
                language=language,
                initial_prompt="大家好，今天我們要來介紹這個部分的教學內容。",
                condition_on_previous_text=False, 
                vad_filter=vad_filter, 
                vad_parameters=dict(
                    min_speech_duration_ms=250,
                    threshold=0.35,                 # 降至 0.35，對微弱聲音更敏感，不易漏字
                    min_silence_duration_ms=1000,   # 大於 1 秒的靜音才進行切分，確保句子完整
                    speech_pad_ms=400               # 語音邊界前後擴展 400ms，防字頭字尾被切
                ) if vad_filter else None
            )
            
            print(f"[語音辨識] 偵測到語言: {info.language} (信心度: {info.language_probability:.2f})")
            print(f"[語音辨識] 音訊時長: {info.duration:.2f} 秒")
            
            segment_list = []
            for segment in segments:
                segment_list.append(segment)
                print(f"[{format_time(segment.start)} -> {format_time(segment.end)}] {segment.text}")

            # 寫入 SRT 字幕檔
            write_srt(segment_list, srt_path)
            
            end_time = datetime.now()
            elapsed_time = end_time - start_time
            print(f"==================================================")
            print(f"[完成] 語音轉文字作業成功結束！")
            print(f"  - 輸出字幕: {srt_path}")
            print(f"  - 總花費時間: {elapsed_time}")
            print(f"==================================================")
            return

        except Exception as e:
            err_str = str(e)
            is_oom = "out of memory" in err_str.lower() or "cuda" in err_str.lower()
            if is_oom and attempt_idx < len(fallback_types) - 1:
                next_ct = fallback_types[attempt_idx + 1]
                print(f"\n[警告] 轉錄過程爆顯存 (OOM): {err_str}")
                print(f"[降級對策] 正在釋放顯存，準備降級至精度 {next_ct} 重新嘗試...\n")
                try:
                    del model
                    import gc
                    gc.collect()
                    try:
                        import torch
                        torch.cuda.empty_cache()
                    except ImportError:
                        pass
                except Exception:
                    pass
                continue
            else:
                print(f"[錯誤] 語音辨識失敗: {e}")
                raise e

def format_time(seconds: float) -> str:
    """輔助函數：格式化輸出即時進度時間"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

if __name__ == "__main__":
    # 解析命令列參數
    parser = argparse.ArgumentParser(description="Whisper 影片語音轉文字工具 (地端 GPU 優先)")
    parser.add_argument("--video", type=str, help="輸入影片的絕對路徑或相對路徑")
    
    # 預設值改為 int8_float16 以兼顧大型模型品質與顯存友善
    parser.add_argument(
        "--model_size", 
        type=str, 
        default="large-v3", 
        choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
        help="Whisper 模型大小 (推薦 large-v3，若顯存小於 4GB 可改為 medium)"
    )
    parser.add_argument(
        "--device", 
        type=str, 
        default="cuda", 
        choices=["cuda", "cpu"],
        help="執行硬體 (cuda 或 cpu)"
    )
    parser.add_argument(
        "--compute_type", 
        type=str, 
        default="int8_float16", 
        choices=["float16", "int8", "int8_float16", "float32"],
        help="計算精度 (預設 int8_float16 兼具低顯存需求與高精度)"
    )
    parser.add_argument(
        "--language", 
        type=str, 
        default="zh",
        help="指定辨識語言，zh 為中文"
    )
    parser.add_argument(
        "--no_vad",
        action="store_true",
        help="停用 VAD (語音活動偵測)。預設會開啟寬鬆的 VAD 以過濾無聲區段防止解碼卡死與幻覺。"
    )
    parser.add_argument(
        "--preprocess",
        action="store_true",
        help="啟用音訊前處理 (高通濾波 + 降噪 + 響度標準化)。建議語音偏弱或背景雜訊較大時使用。"
    )
    
    args = parser.parse_args()
    
    # 如果使用者沒有傳入影片路徑，則自動掃描 data/input/ 中尚未處理的影片
    if not args.video:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_dir = os.path.join(base_dir, "data", "input")
        output_dir = os.path.join(base_dir, "data", "output")
        os.makedirs(input_dir, exist_ok=True)
        
        media_exts = (".mp4", ".mkv", ".avi", ".mov", ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")
        
        def pick_unprocessed_media(source_dir, source_name):
            """從指定目錄中挑選尚未產出 .srt 字幕的媒體檔案 (音訊/影片)"""
            candidates = []
            skipped = 0
            for f in os.listdir(source_dir):
                if f.lower().endswith(media_exts):
                    name = os.path.splitext(f)[0]
                    srt = os.path.join(output_dir, f"{name}.srt")
                    if os.path.exists(srt):
                        skipped += 1
                    else:
                        candidates.append(os.path.join(source_dir, f))
            if skipped > 0:
                print(f"[提示] 跳過 {skipped} 個已處理檔案（{source_name} 中 .srt 已存在）")
            return candidates
        
        media_files = pick_unprocessed_media(input_dir, "data/input")
        source = "輸入資料夾"
        
        if not media_files:
            media_files = pick_unprocessed_media(base_dir, "根目錄")
            source = "根目錄"
        
        if media_files:
            selected_media = media_files[0]
            print(f"[提示] 未指定媒體檔案，自動選擇{source}中的檔案: {selected_media}")
            args.video = selected_media
        else:
            print(f"[錯誤] 沒有尚未處理的音訊或影片檔案。請使用 --video 參數指定檔案，或將檔案放入 data/input/ 中。")
            parser.print_help()
            exit(1)
                
    transcribe_video(
        video_path=args.video,
        model_size=args.model_size,
        device=args.device,
        compute_type=args.compute_type,
        language=args.language,
        vad_filter=not args.no_vad,
        preprocess=args.preprocess
    )
