# -*- coding: utf-8 -*-
"""
Edge TTS 語音合成核心服務模組
基於微軟 Edge Neural 語音端點，提供高自然度、零 GPU 負擔的語音合成功能。
支援互動式終端介面、長文字自動切分拼接、以及多種熱門中文音色自訂選擇。
"""

import os
import sys
import re
import asyncio
import argparse
from datetime import datetime
from typing import List, Dict, Optional
import edge_tts
from edge_tts.exceptions import NoAudioReceived

# 常用優質中文預設語音清單
VOICE_TW_FEMALE_HSIAOCHEN = "zh-TW-HsiaoChenNeural"  # 曉臻 (台灣女聲，最穩定自然)
VOICE_TW_FEMALE_HSIAOYU   = "zh-TW-HsiaoYuNeural"    # 曉雨 (台灣女聲，活潑清晰)
VOICE_TW_MALE_YUNJHE       = "zh-TW-YunJheNeural"      # 雲哲 (台灣男聲，偶受微軟雲端端點限制)
VOICE_CN_MALE_YUNXI        = "zh-CN-YunxiNeural"       # 雲希 (頂級熱門旁白男聲，繁中相容性極佳且極度穩定)
VOICE_CN_MALE_YUNJIAN      = "zh-CN-YunjianNeural"     # 雲健 (說書、小說長篇男聲)

DEFAULT_VOICE_FEMALE = VOICE_TW_FEMALE_HSIAOCHEN
DEFAULT_VOICE_MALE   = VOICE_CN_MALE_YUNXI

# 推薦音色清單（供互動介面快速選取）
RECOMMENDED_VOICES = [
    {
        "id": "1",
        "name": "曉臻 (台灣知性女聲 - 預設推薦)",
        "voice": VOICE_TW_FEMALE_HSIAOCHEN,
        "desc": "標準台灣口音，發音清晰自然，適合教學、會議與旁白"
    },
    {
        "id": "2",
        "name": "曉雨 (台灣活潑女聲)",
        "voice": VOICE_TW_FEMALE_HSIAOYU,
        "desc": "音調明亮活潑，適合解說、助理與輕鬆對話"
    },
    {
        "id": "3",
        "name": "雲希 (頂級熱門男聲 - 極度推薦)",
        "voice": VOICE_CN_MALE_YUNXI,
        "desc": "影視解說、知識類熱門男聲，繁體中文相容極佳，極度穩定"
    },
    {
        "id": "4",
        "name": "雲哲 (台灣沉穩男聲)",
        "voice": VOICE_TW_MALE_YUNJHE,
        "desc": "台灣青年男聲（若遇伺服器忙碌會自動轉備援）"
    },
    {
        "id": "5",
        "name": "雲健 (影視說書男聲)",
        "voice": VOICE_CN_MALE_YUNJIAN,
        "desc": "語調沉穩，適合長篇故事、小說閱讀"
    }
]


def split_text_into_chunks(text: str, max_chars: int = 800) -> List[str]:
    """
    將長文本依照句號、換行等標點符號切分成適當大小的片段，
    避免單次請求超出微軟 Edge 端點連線限制。
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    # 依照段落或常用標點符號切割
    sentences = re.split(r'(?<=[。！？\n!?；;])', text)
    current_chunk = ""

    for s in sentences:
        if not s:
            continue
        if len(current_chunk) + len(s) <= max_chars:
            current_chunk += s
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            # 如果單個句子就超過 max_chars，強制以逗號或長度切分
            if len(s) > max_chars:
                sub_parts = re.split(r'(?<=[，,])', s)
                sub_chunk = ""
                for p in sub_parts:
                    if len(sub_chunk) + len(p) <= max_chars:
                        sub_chunk += p
                    else:
                        if sub_chunk.strip():
                            chunks.append(sub_chunk.strip())
                        sub_chunk = p
                if sub_chunk.strip():
                    current_chunk = sub_chunk
                else:
                    current_chunk = ""
            else:
                current_chunk = s

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks if chunks else [text]


async def get_available_voices(locale_filter: Optional[str] = "zh-TW") -> List[Dict[str, str]]:
    """
    獲取微軟 Edge TTS 支援的語音清單
    :param locale_filter: 語言代碼過濾（例如 'zh-TW', 'zh-CN', 'en-US'），設為 None 則回傳所有
    :return: 包含 ShortName, Gender, Locale, FriendlyName 的清單
    """
    voices = await edge_tts.list_voices()
    results = []
    for v in voices:
        locale = v.get("Locale", "")
        if locale_filter is None or locale_filter.lower() in locale.lower():
            results.append({
                "ShortName": v.get("ShortName", ""),
                "Gender": v.get("Gender", ""),
                "Locale": locale,
                "FriendlyName": v.get("FriendlyName", "")
            })
    return results


async def synthesize_chunk_async(
    chunk: str,
    voice: str,
    rate: str,
    pitch: str,
    volume: str,
    auto_fallback: bool = True
) -> bytes:
    """合成單一片段並回傳音訊二進位 bytes"""
    try:
        communicate = edge_tts.Communicate(
            text=chunk,
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume
        )
        audio_data = b""
        async for chunk_data in communicate.stream():
            if chunk_data["type"] == "audio":
                audio_data += chunk_data["data"]
        return audio_data
    except NoAudioReceived as e:
        if auto_fallback and voice == VOICE_TW_MALE_YUNJHE:
            print(f"[警告] 音色 {voice} 暫無回應，自動無縫切換備援男聲 {VOICE_CN_MALE_YUNXI}...")
            communicate = edge_tts.Communicate(
                text=chunk,
                voice=VOICE_CN_MALE_YUNXI,
                rate=rate,
                pitch=pitch,
                volume=volume
            )
            audio_data = b""
            async for chunk_data in communicate.stream():
                if chunk_data["type"] == "audio":
                    audio_data += chunk_data["data"]
            return audio_data
        else:
            raise e


async def generate_speech_async(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE_FEMALE,
    rate: str = "+0%",
    pitch: str = "+0Hz",
    volume: str = "+0%",
    auto_fallback: bool = True
) -> str:
    """
    非同步將文字轉換為音訊檔案 (MP3)
    支援長文本自動切分分段合成與無縫拼接
    """
    if not text or not text.strip():
        raise ValueError("輸入文字不能為空。")

    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    chunks = split_text_into_chunks(text.strip(), max_chars=800)
    total_chunks = len(chunks)

    if total_chunks > 1:
        print(f"[長文本處理] 偵測到總字數 {len(text)} 字，自動分段為 {total_chunks} 個音訊區塊合成...")

    combined_audio = b""
    for idx, chunk in enumerate(chunks, start=1):
        if total_chunks > 1:
            print(f"  - 正在合成區塊 ({idx}/{total_chunks}) [長度: {len(chunk)} 字]...")
        audio_bytes = await synthesize_chunk_async(
            chunk=chunk,
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume,
            auto_fallback=auto_fallback
        )
        combined_audio += audio_bytes

    with open(output_path, "wb") as f:
        f.write(combined_audio)

    return os.path.abspath(output_path)


def generate_speech(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE_FEMALE,
    rate: str = "+0%",
    pitch: str = "+0Hz",
    volume: str = "+0%",
    auto_fallback: bool = True
) -> str:
    """同步輔助函式"""
    return asyncio.run(
        generate_speech_async(
            text=text,
            output_path=output_path,
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume,
            auto_fallback=auto_fallback
        )
    )


def interactive_mode():
    """
    互動式終端控制台介面
    引導使用者完成文字輸入/載入、音色選取、檔名自訂及語音生成
    """
    print("=" * 60)
    print("        Edge TTS 互動式語音合成工具")
    print("=" * 60)

    # 1. 選擇輸入來源
    print("\n【步驟 1/3】請選擇文字來源：")
    print("  [1] 直接手動輸入文字（可貼上多行）")
    print("  [2] 從文字檔案 (.txt) 載入")
    
    choice_src = input("請選擇 [1 或 2，預設 1]: ").strip()
    if choice_src == "2":
        while True:
            file_path = input("請輸入或拖曳文字檔路徑 (.txt): ").strip()
            # 移除常見的拖曳外包引號
            file_path = file_path.strip('"').strip("'")
            if not file_path:
                print("[錯誤] 路徑不可為空，請重新輸入。")
                continue
            if not os.path.exists(file_path):
                print(f"[錯誤] 找不到檔案: {file_path}，請重新輸入。")
                continue
            
            # 嘗試讀取檔案內容（支援 utf-8 與相容 ansi/gbk/cp950）
            content = None
            for enc in ["utf-8", "utf-8-sig", "cp950", "gbk"]:
                try:
                    with open(file_path, "r", encoding=enc) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None or not content.strip():
                print("[錯誤] 無法解析該檔案編碼或檔案內容為空，請檢查檔案。")
                continue
            
            text_content = content.strip()
            print(f"[成功載入] 已成功讀取檔案，共 {len(text_content)} 字。")
            break
    else:
        print("\n請輸入欲合成的文字內容（若有多行，請輸入完成後直接在空行按 Enter 或輸入 END 送出）：")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip().upper() == "END":
                break
            if not line and lines:  # 空行且已有輸入內容，完成輸入
                break
            lines.append(line)
        text_content = "\n".join(lines).strip()
        if not text_content:
            print("[提示] 未輸入有效文字，使用示範文字。")
            text_content = "歡迎使用 Edge TTS 語音合成服務，這是一段繁體中文示範音訊。"

    # 2. 選擇音色
    print("\n【步驟 2/3】請選擇語音音色：")
    for item in RECOMMENDED_VOICES:
        print(f"  [{item['id']}] {item['name']}")
        print(f"      說明: {item['desc']}")
    print("  [6] 手動輸入其他音色名稱 (進階)")

    choice_voice = input("請選擇音色編號 [1-6，預設 1]: ").strip()
    selected_voice = DEFAULT_VOICE_FEMALE
    if choice_voice in ["1", "2", "3", "4", "5"]:
        for item in RECOMMENDED_VOICES:
            if item["id"] == choice_voice:
                selected_voice = item["voice"]
                print(f"-> 已選擇音色: {item['name']}")
                break
    elif choice_voice == "6":
        custom = input("請輸入完整音色名稱 (例如 en-US-AriaNeural): ").strip()
        if custom:
            selected_voice = custom
            print(f"-> 已設定自訂音色: {selected_voice}")
    else:
        print(f"-> 採用預設音色: 曉臻 ({DEFAULT_VOICE_FEMALE})")

    # 3. 設定輸出檔案名稱
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"tts_{timestamp}.mp3"
    default_output = os.path.join("data", "output", default_filename)

    print("\n【步驟 3/3】設定輸出檔案名稱：")
    print(f"  預設儲存位置: {default_output}")
    custom_name = input("請輸入檔案名稱 (例如: my_voice.mp3，按 Enter 使用預設): ").strip()

    if custom_name:
        if not custom_name.lower().endswith(".mp3"):
            custom_name += ".mp3"
        # 若使用者只輸入檔名，預設放入 data/output/
        if os.path.dirname(custom_name):
            target_output = custom_name
        else:
            target_output = os.path.join("data", "output", custom_name)
    else:
        target_output = default_output

    print("\n" + "=" * 60)
    print("【開始進行語音合成】")
    print(f"  - 輸出目標: {target_output}")
    print(f"  - 選擇音色: {selected_voice}")
    print(f"  - 文本總字數: {len(text_content)} 字")
    print("=" * 60)

    start_time = datetime.now()
    try:
        final_path = generate_speech(
            text=text_content,
            output_path=target_output,
            voice=selected_voice
        )
        elapsed = datetime.now() - start_time
        print("\n" + "*" * 60)
        print("[成功] 語音合成順利完成！")
        print(f"  - 音訊路徑: {final_path}")
        print(f"  - 耗費時間: {elapsed}")
        print("*" * 60 + "\n")
    except Exception as e:
        print(f"\n[錯誤] 語音合成過程中發生異常: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Edge TTS 語音合成服務工具")
    parser.add_argument("--interactive", "-i", action="store_true", help="啟動互動式操作介面")
    parser.add_argument("--text", "-t", type=str, help="欲合成的文字內容")
    parser.add_argument("--file", "-f", type=str, help="欲讀取並合成的文字檔路徑 (.txt)")
    parser.add_argument("--output", "-o", type=str, default=None, help="輸出音訊路徑 (預設: data/output/tts_<時間>.mp3)")
    parser.add_argument("--voice", "-v", type=str, default=DEFAULT_VOICE_FEMALE, help=f"選擇音色名稱 (預設: {DEFAULT_VOICE_FEMALE})")
    parser.add_argument("--rate", type=str, default="+0%", help="語速調整 (例: +20%%, -10%%)")
    parser.add_argument("--pitch", type=str, default="+0Hz", help="音調調整 (例: +5Hz, -5Hz)")
    parser.add_argument("--volume", type=str, default="+0%", help="音量調整 (例: +0%%, -20%%)")
    parser.add_argument("--list-voices", action="store_true", help="列出台灣繁體中文 (zh-TW) 可用音色")
    parser.add_argument("--all-voices", action="store_true", help="列出全部可用音色")

    args = parser.parse_args()

    # 若指定列出音色
    if args.list_voices or args.all_voices:
        filter_str = None if args.all_voices else "zh-TW"
        print(f"正在查詢可用語音清單 (篩選: {filter_str or '全部'})...")
        voices = asyncio.run(get_available_voices(filter_str))
        print(f"{'語音代碼 (ShortName)':<30} | {'性別':<8} | {'語言代碼':<10} | {'名稱'}")
        print("-" * 75)
        for v in voices:
            print(f"{v['ShortName']:<30} | {v['Gender']:<8} | {v['Locale']:<10} | {v['FriendlyName']}")
        return

    # 若指定互動模式，或未提供文字與檔案參數時，自動啟動互動介面
    if args.interactive or (not args.text and not args.file):
        interactive_mode()
        return

    # 命令列模式處理
    content = ""
    if args.text:
        content = args.text
    elif args.file:
        if not os.path.exists(args.file):
            print(f"[錯誤] 找不到文字檔: {args.file}", file=sys.stderr)
            sys.exit(1)
        # 多編碼相容讀取
        for enc in ["utf-8", "utf-8-sig", "cp950", "gbk"]:
            try:
                with open(args.file, "r", encoding=enc) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        if not content:
            print(f"[錯誤] 無法讀取文字檔內容或檔案為空: {args.file}", file=sys.stderr)
            sys.exit(1)

    # 決定輸出路徑
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = os.path.join("data", "output", f"tts_{timestamp}.mp3")

    print(f"開始合成語音...")
    print(f"  - 音色: {args.voice}")
    print(f"  - 語速: {args.rate} / 音調: {args.pitch} / 音量: {args.volume}")
    print(f"  - 內容長度: {len(content)} 字")
    print(f"  - 輸出目標: {args.output}")

    try:
        out_path = generate_speech(
            text=content,
            output_path=args.output,
            voice=args.voice,
            rate=args.rate,
            pitch=args.pitch,
            volume=args.volume
        )
        print(f"[成功] 語音合成完成！檔案已儲存至：{out_path}")
    except Exception as e:
        print(f"[錯誤] 語音合成失敗：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
