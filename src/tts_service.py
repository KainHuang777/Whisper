# -*- coding: utf-8 -*-
"""
Edge TTS 語音合成核心服務模組
基於微軟 Edge Neural 語音端點，提供高自然度、零 GPU 負擔的語音合成功能。
"""

import os
import sys
import asyncio
import argparse
from typing import List, Dict, Optional
import edge_tts
from edge_tts.exceptions import NoAudioReceived

# 常用優質中文預設語音清單
VOICE_TW_FEMALE_HSIAOCHEN = "zh-TW-HsiaoChenNeural"  # 曉臻 (台灣女聲，最穩定自然)
VOICE_TW_FEMALE_HSIAOYU   = "zh-TW-HsiaoYuNeural"    # 曉雨 (台灣女聲，活潑清晰)
VOICE_TW_MALE_YUNJHE       = "zh-TW-YunJheNeural"      # 雲哲 (台灣男聲，偶受微軟雲端端點限制)
VOICE_CN_MALE_YUNXI        = "zh-CN-YunxiNeural"       # 雲希 (頂級熱門旁白男聲，繁中相容性極佳且極度穩定)

DEFAULT_VOICE_FEMALE = VOICE_TW_FEMALE_HSIAOCHEN
DEFAULT_VOICE_MALE   = VOICE_CN_MALE_YUNXI


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
    :param text: 要合成的文字內容
    :param output_path: 輸出的檔案路徑 (.mp3)
    :param voice: 角色語音名稱
    :param rate: 語速調整 (例: '+10%', '-20%', '+0%')
    :param pitch: 音調調整 (例: '+5Hz', '-5Hz', '+0Hz')
    :param volume: 音量調整 (例: '+0%', '-10%')
    :param auto_fallback: 當指定音色（如 YunJhe）遇到微軟端點異常無音訊時，是否自動切換備援音色
    :return: 輸出的音訊絕對路徑
    """
    if not text or not text.strip():
        raise ValueError("輸入文字不能為空。")

    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    try:
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume
        )
        await communicate.save(output_path)
    except NoAudioReceived as e:
        # 微軟端點有時會對特定音色 (如 zh-TW-YunJheNeural) 暫時中斷或限流
        if auto_fallback and voice == VOICE_TW_MALE_YUNJHE:
            print(f"[警告] 音色 {voice} 目前微軟伺服器無回應，自動無縫切換備援男聲 {VOICE_CN_MALE_YUNXI}...")
            communicate = edge_tts.Communicate(
                text=text,
                voice=VOICE_CN_MALE_YUNXI,
                rate=rate,
                pitch=pitch,
                volume=volume
            )
            await communicate.save(output_path)
        else:
            raise e

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
    """
    同步輔助函式，方便一般的 Python 腳本直接呼叫
    """
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


def main():
    parser = argparse.ArgumentParser(description="Edge TTS 語音合成服務工具")
    parser.add_argument("--text", "-t", type=str, help="欲合成的文字內容")
    parser.add_argument("--file", "-f", type=str, help="欲讀取並合成的文字檔路徑 (.txt)")
    parser.add_argument("--output", "-o", type=str, default="data/output/tts_output.mp3", help="輸出音訊路徑 (預設: data/output/tts_output.mp3)")
    parser.add_argument("--voice", "-v", type=str, default=DEFAULT_VOICE_FEMALE, help=f"選擇音色名稱 (預設: {DEFAULT_VOICE_FEMALE})")
    parser.add_argument("--rate", type=str, default="+0%", help="語速調整 (例: +20%, -10%)")
    parser.add_argument("--pitch", type=str, default="+0Hz", help="音調調整 (例: +5Hz, -5Hz)")
    parser.add_argument("--volume", type=str, default="+0%", help="音量調整 (例: +0%, -20%)")
    parser.add_argument("--list-voices", action="store_true", help="列出台灣繁體中文 (zh-TW) 可用音色")
    parser.add_argument("--all-voices", action="store_true", help="列出全部可用音色")

    args = parser.parse_args()

    if args.list_voices or args.all_voices:
        filter_str = None if args.all_voices else "zh-TW"
        print(f"正在查詢可用語音清單 (篩選: {filter_str or '全部'})...")
        voices = asyncio.run(get_available_voices(filter_str))
        print(f"{'語音代碼 (ShortName)':<30} | {'性別':<8} | {'語言代碼':<10} | {'名稱'}")
        print("-" * 75)
        for v in voices:
            print(f"{v['ShortName']:<30} | {v['Gender']:<8} | {v['Locale']:<10} | {v['FriendlyName']}")
        return

    content = ""
    if args.text:
        content = args.text
    elif args.file:
        if not os.path.exists(args.file):
            print(f"[錯誤] 找不到文字檔: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        print("[提示] 請提供 --text 或 --file 參數，或使用 --list-voices 檢視可用音色。", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

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
