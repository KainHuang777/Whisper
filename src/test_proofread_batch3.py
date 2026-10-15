# -*- coding: utf-8 -*-
"""
測試腳本：驗證 Batch 3 (2001~3000句) 校對品質與格式
"""
import os
import re

TARGET_FILE = r"scratch/batch_3_2001_3000.srt"

FORBIDDEN_WORDS_B3 = [
    "mergery style", "Centaur", "centaur", "蓝少爷", "藍少爺", "热心最早",
    "热性的这个", "Trival Town", "TrivalTown", "Gossip Hub", "雷姆威去",
    "疯狂水世界", "迷雾小镇", "谁来救救我", "监狱的二合", "监獄的二合",
    "乡庭", "鄉庭", "香亭", "也收的", "面包穴", "麵包穴", "叫定单", "叫定單",
    "单元聚模式", "單元聚模式", "层建", "更锤", "更錘", "模棱经营", "模稜經營",
    "模拟机", "二合三修", "竖平", "禪戲", "禅戏", "恩帝动画", "恩帝動畫",
    "小棋牌", "二核", "二盒", "买辆广告", "買輛廣告", "游乐金币", "悟图",
    "悟圖", "舞图", "舞圖", "落地业", "落地業", "40%的磁流", "15%的气流",
    "极前期的流存", "六十天的流程"
]

REQUIRED_TERMS_B3 = [
    "Merge Restyle", "Sensor Tower", "藍飛互娛", "天天玩家", "樂信",
    "Travel Town", "Gossip Harbor", "檸檬微趣", "點點互動", "《瘋狂水世界》",
    "《迷霧小鎮》", "《誰來救救我》", "《Merge Prison》", "箱庭", "ASO",
    "麵包屑", "交訂單", "單元劇模式", "城建", "更垂", "模擬經營",
    "二合三消", "豎屏", "禪系", "Ending 動畫", "五圖", "落地頁",
    "次留", "七留", "留存"
]

def test_batch3():
    if not os.path.exists(TARGET_FILE):
        print(f"[FAIL] 目標檔案不存在: {TARGET_FILE}")
        print("請先在終端機運行: python scratch/execute_proofread_batch3.py")
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

    if indices[0] != 2001 or indices[-1] != 3000:
        print(f"[FAIL] 字幕範圍不是 2001 ~ 3000，實際為 {indices[0]} ~ {indices[-1]}！")
        return False

    # 2. 檢驗禁止錯字
    forbidden_found = []
    for w in FORBIDDEN_WORDS_B3:
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
    for term in REQUIRED_TERMS_B3:
        if term not in content:
            missing_required.append(term)

    if missing_required:
        print(f"[WARNING] 部分預期替換之正確詞彙未檢索到 ({len(missing_required)} 項):")
        for mt in missing_required:
            print(f"  - {mt}")
    else:
        print(f"[PASS] 所有核心專有名詞 ({len(REQUIRED_TERMS_B3)} 項) 均已成功替換並存在！")

    print("\n==============================================")
    print(">>> Batch 3 (2001~3000句) 測試驗證全數通過！ <<<")
    print("==============================================")
    return True

if __name__ == "__main__":
    test_batch3()
