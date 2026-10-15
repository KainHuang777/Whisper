# -*- coding: utf-8 -*-
"""
Edge TTS 整合測試腳本 (加強版)
驗證項目：
1. 繁體中文音色清單查詢功能
2. 台灣繁體女聲 (zh-TW-HsiaoChenNeural, 曉臻) 合成驗證
3. 台灣繁體女聲備選 (zh-TW-HsiaoYuNeural, 曉雨) 合成驗證
4. 熱門旁白男聲 (zh-CN-YunxiNeural, 雲希，繁體相容) 合成驗證
5. 台灣男聲 (zh-TW-YunJheNeural) 容錯與自動備援合成驗證
6. 語速與音調參數微調合成驗證
"""

import os
import sys
import asyncio

# 加入上層目錄至 sys.path 以便引用模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tts_service import (
    get_available_voices,
    generate_speech_async,
    VOICE_TW_FEMALE_HSIAOCHEN,
    VOICE_TW_FEMALE_HSIAOYU,
    VOICE_TW_MALE_YUNJHE,
    VOICE_CN_MALE_YUNXI
)


async def run_tests():
    print("=" * 65)
    print("  [Edge TTS] 語音合成完整整合測試 (含容錯機制驗證)")
    print("=" * 65)

    test_output_dir = os.path.join("data", "output")
    os.makedirs(test_output_dir, exist_ok=True)

    passed_count = 0
    total_count = 6

    # ----------------------------------------------------
    # 測試項目 1: 查詢台灣繁體中文 (zh-TW) 音色清單
    # ----------------------------------------------------
    print("\n[測試 1/6] 查詢台灣繁體中文 (zh-TW) 音色清單...")
    try:
        tw_voices = await get_available_voices(locale_filter="zh-TW")
        assert len(tw_voices) > 0, "未獲取到任何 zh-TW 音色！"
        voice_names = [v["ShortName"] for v in tw_voices]
        print(f"  -> 成功獲取 {len(tw_voices)} 組音色: {', '.join(voice_names)}")
        print("  -> [通過] 音色清單查詢成功。")
        passed_count += 1
    except Exception as e:
        print(f"  -> [失敗] 測試 1 發生錯誤: {e}")

    # ----------------------------------------------------
    # 測試項目 2: 台灣繁體女聲 (曉臻)
    # ----------------------------------------------------
    female_output = os.path.join(test_output_dir, "test_tts_hsiaochen.mp3")
    print(f"\n[測試 2/6] 台灣繁體女聲合成 (音色: {VOICE_TW_FEMALE_HSIAOCHEN} 曉臻)...")
    text_female = "您好，這是微軟 Edge TTS 台灣女聲曉臻的語音合成測試。"
    try:
        out_path = await generate_speech_async(
            text=text_female,
            output_path=female_output,
            voice=VOICE_TW_FEMALE_HSIAOCHEN
        )
        assert os.path.exists(out_path) and os.path.getsize(out_path) > 1024
        print(f"  -> 成功產出: {out_path} ({os.path.getsize(out_path):,} bytes)")
        print("  -> [通過] 曉臻女聲合成驗證成功。")
        passed_count += 1
    except Exception as e:
        print(f"  -> [失敗] 測試 2 發生錯誤: {e}")

    # ----------------------------------------------------
    # 測試項目 3: 台灣繁體女聲備選 (曉雨)
    # ----------------------------------------------------
    hsiaoyu_output = os.path.join(test_output_dir, "test_tts_hsiaoyu.mp3")
    print(f"\n[測試 3/6] 台灣繁體女聲備選 (音色: {VOICE_TW_FEMALE_HSIAOYU} 曉雨)...")
    text_hsiaoyu = "這是微軟 Edge TTS 台灣女聲曉雨的測試，聲音活潑自然。"
    try:
        out_path = await generate_speech_async(
            text=text_hsiaoyu,
            output_path=hsiaoyu_output,
            voice=VOICE_TW_FEMALE_HSIAOYU
        )
        assert os.path.exists(out_path) and os.path.getsize(out_path) > 1024
        print(f"  -> 成功產出: {out_path} ({os.path.getsize(out_path):,} bytes)")
        print("  -> [通過] 曉雨女聲合成驗證成功。")
        passed_count += 1
    except Exception as e:
        print(f"  -> [失敗] 測試 3 發生錯誤: {e}")

    # ----------------------------------------------------
    # 測試項目 4: 熱門旁白男聲 (雲希，繁體文字相容性佳)
    # ----------------------------------------------------
    yunxi_output = os.path.join(test_output_dir, "test_tts_yunxi.mp3")
    print(f"\n[測試 4/6] 熱門旁白男聲合成 (音色: {VOICE_CN_MALE_YUNXI} 雲希)...")
    text_yunxi = "大家好，這是熱門旁白男聲雲希，朗讀繁體中文內容一樣非常流暢沉穩。"
    try:
        out_path = await generate_speech_async(
            text=text_yunxi,
            output_path=yunxi_output,
            voice=VOICE_CN_MALE_YUNXI
        )
        assert os.path.exists(out_path) and os.path.getsize(out_path) > 1024
        print(f"  -> 成功產出: {out_path} ({os.path.getsize(out_path):,} bytes)")
        print("  -> [通過] 雲希男聲合成驗證成功。")
        passed_count += 1
    except Exception as e:
        print(f"  -> [失敗] 測試 4 發生錯誤: {e}")

    # ----------------------------------------------------
    # 測試項目 5: 台灣男聲 (雲哲) + 自動容錯降級機制
    # ----------------------------------------------------
    yunjhe_output = os.path.join(test_output_dir, "test_tts_yunjhe.mp3")
    print(f"\n[測試 5/6] 台灣男聲雲哲合成 (支援微軟端點異常之自動降級備援)...")
    text_yunjhe = "這是台灣男聲雲哲的合成測試，若端點異常將觸發平滑備援機制。"
    try:
        out_path = await generate_speech_async(
            text=text_yunjhe,
            output_path=yunjhe_output,
            voice=VOICE_TW_MALE_YUNJHE,
            auto_fallback=True
        )
        assert os.path.exists(out_path) and os.path.getsize(out_path) > 1024
        print(f"  -> 成功產出: {out_path} ({os.path.getsize(out_path):,} bytes)")
        print("  -> [通過] 雲哲男聲（含容錯）驗證成功。")
        passed_count += 1
    except Exception as e:
        print(f"  -> [失敗] 測試 5 發生錯誤: {e}")

    # ----------------------------------------------------
    # 測試項目 6: 參數調節（語速 +25%、音調 +5Hz）
    # ----------------------------------------------------
    custom_output = os.path.join(test_output_dir, "test_tts_fast.mp3")
    print(f"\n[測試 6/6] 語速與音調微調合成 (語速 +25%, 音調 +5Hz)...")
    text_custom = "這是一段經過語速提升百分之二十五，並且提高音調的快節奏測試語音。"
    try:
        out_path = await generate_speech_async(
            text=text_custom,
            output_path=custom_output,
            voice=VOICE_TW_FEMALE_HSIAOCHEN,
            rate="+25%",
            pitch="+5Hz"
        )
        assert os.path.exists(out_path) and os.path.getsize(out_path) > 1024
        print(f"  -> 成功產出: {out_path} ({os.path.getsize(out_path):,} bytes)")
        print("  -> [通過] 參數調節合成驗證成功。")
        passed_count += 1
    except Exception as e:
        print(f"  -> [失敗] 測試 6 發生錯誤: {e}")

    # ----------------------------------------------------
    # 結算報告
    # ----------------------------------------------------
    print("\n" + "=" * 65)
    print(f"  測試結果結算: {passed_count}/{total_count} 通過")
    print("=" * 65)

    if passed_count == total_count:
        print("[ALL PASSED] 所有 Edge TTS 整合與容錯測試皆順利通過！")
        return 0
    else:
        print("[WARNING] 部分測試未通過，請檢視上方錯誤訊息。")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_tests())
    sys.exit(exit_code)
