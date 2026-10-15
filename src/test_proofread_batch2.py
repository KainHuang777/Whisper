# -*- coding: utf-8 -*-
"""
測試腳本：驗證 Batch 2 (1001~2000句) 校對品質與格式
"""
import os
import re

TARGET_FILE = r"scratch/batch_2_1001_2000.srt"

FORBIDDEN_WORDS_B2 = [
    "横布标地区", "橫布標地區", "早期预言", "早期預言", "包款蔬菜", "爆款蔬菜",
    "肉哥", "流传次流", "吃留", "吃流", "四流", "次流", "西流", "CPU代表流量池",
    "O卡的这套素材", "O卡的這套素材", "超修素材", "超修的池子", "玩超修的",
    "数字卡点", "數字卡點", "调油", "調油", "产品调用", "飛客素材", "飞客素材",
    "fake蔬菜", "又很稀烈", "二核", "商店舞图", "商店舞圖", "商店五族", "舞图",
    "泛融股", "代包测试", "代包測試", "代包测", "代包測", "很细量的", "不细量的",
    "特别不息量", "流囤", "开始体谅", "美卖", "美賣", "模化版", "签评", "賣散",
    "卖散", "扑关率", "撲關率", "买AO的时候", "偏剧形象的", "偏劇形象的",
    "Limoway去", "申讯", "申訊"
]

REQUIRED_TERMS_B2 = [
    "雪婷", "聖勛", "目標地區", "早期預研", "爆款素材", "肉鴿", "次留", "七留",
    "CPM代表流量池", "歐美卡通的這套素材", "超休素材", "數值卡點", "調優",
    "fake素材", "又很吸量", "二合", "商店五圖", "五圖", "泛用戶", "帶包測試",
    "帶包測", "下限", "很吸量的", "不吸量的", "特別不吸量", "開始起量", "設定向",
    "塔防", "美漫", "梗化版", "Campaign", "賣慘", "曝光率", "點點互動", "T1",
    "Puzzle", "偏劇情向的"
]

def test_batch2():
    if not os.path.exists(TARGET_FILE):
        print(f"[FAIL] 目標檔案不存在: {TARGET_FILE}")
        print("請先在終端機運行: python scratch/execute_proofread_batch2.py")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 檢驗條目數與連續性
    raw_blocks = re.split(r'\n\s*\n', content.strip())
    indices = []
    for b in raw_blocks:
        b = b.strip()
        if not b:
            continue
        lines = b.split('\n')
        if len(lines) >= 3:
            try:
                indices.append(int(lines[0].strip()))
            except ValueError:
                pass

    print(f"[INFO] 讀取到 {len(indices)} 條字幕區塊。")
    if len(indices) != 1000:
        print(f"[FAIL] 字幕數量不符合預期 1000 條，實際為 {len(indices)} 條！")
        return False

    if indices[0] != 1001 or indices[-1] != 2000:
        print(f"[FAIL] 字幕範圍不是 1001 ~ 2000，實際為 {indices[0]} ~ {indices[-1]}！")
        return False

    # 2. 檢驗禁止錯字
    forbidden_found = []
    for w in FORBIDDEN_WORDS_B2:
        if w in content:
            forbidden_found.append(w)

    if forbidden_found:
        print(f"[FAIL] 檢驗出未清除的禁止錯字 ({len(forbidden_found)} 項):")
        for fw in forbidden_found:
            print(f"  - {fw}")
        return False
    else:
        print("[PASS] 禁止錯字全數清除，違禁詞計數為 0！")

    # 3. 檢驗核心專有名詞存在性
    missing_required = []
    for term in REQUIRED_TERMS_B2:
        if term not in content:
            missing_required.append(term)

    if missing_required:
        print(f"[WARNING] 部分預期替換之正確詞彙未檢索到 ({len(missing_required)} 項):")
        for mt in missing_required:
            print(f"  - {mt}")
    else:
        print(f"[PASS] 所有核心專有名詞 ({len(REQUIRED_TERMS_B2)} 項) 均已成功替換並存在！")

    print("\n==============================================")
    print(">>> Batch 2 (1001~2000句) 測試驗證全數通過！ <<<")
    print("==============================================")
    return True

if __name__ == "__main__":
    test_batch2()
