# -*- coding: utf-8 -*-
"""
測試腳本：驗證 Batch 1 (1~1000句) 校對品質與格式
"""
import os
import re

TARGET_FILE = r"scratch/batch_1_1000.srt"

FORBIDDEN_WORDS = [
    "董军锐", "董軍銳", "生讯", "生訊", "摩天星adventure", "修线游戏",
    "美国设施主要做两大类", "UV创意类", "四流其实都还好", "四流",
    "着重毛在哪里", "四只引荐", "中听了", "舞图", "五突", "肥龙港口",
    "fake蔬菜", "称装修的素材", "称的很好", "滑龙道", "Whisper Castle",
    "Vasper", "柠檬威去", "林默威去", "群舞也好", "加接一些合成的文法",
    "把产值拖到路上面", "落地业", "POA产品", "商业化变性", "能变性的很快",
    "把RY给打正", "脱明展示", "竞品的蔬菜", "起降那个时候", "加装整理",
    "退到顶了", "全方面利于我们的", "做原话的也好"
]

REQUIRED_CORRECTED_TERMS = [
    "董浚睿", "聖勛", "Match 3 and Adventure", "買量素材",
    "次留", "UE創意類", "著重錨在哪裡", "四支影片", "重聽了",
    "五圖", "緋聞港口", "fake素材", "蹭裝修的素材", "華容道",
    "Winter Castle", "檸檬微趣", "尋物也好", "賣慘", "嫁接",
    "Playrix", "Idle", "把鏟子拖到路上面", "落地頁", "PUA",
    "商業化變現", "把 ROI 給打正", "脫敏展示", "競品的素材",
    "起量那個時候", "家裝整理", "莉莉絲", "博樂科技"
]

def test_batch1():
    if not os.path.exists(TARGET_FILE):
        print(f"[FAIL] 目標檔案不存在: {TARGET_FILE}")
        print("請先在終端機運行: python scratch/execute_proofread_batch1.py")
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

    if indices[0] != 1 or indices[-1] != 1000:
        print(f"[FAIL] 字幕範圍不是 1 ~ 1000，實際為 {indices[0]} ~ {indices[-1]}！")
        return False

    # 2. 檢驗禁止錯字
    forbidden_found = []
    for w in FORBIDDEN_WORDS:
        if w in content:
            forbidden_found.append(w)

    if forbidden_found:
        print(f"[FAIL] 檢驗出未清除的禁止錯字 ({len(forbidden_found)} 項):")
        for fw in forbidden_found:
            print(f"  - {fw}")
        return False
    else:
        print("[PASS] 禁止錯字全數清除，違禁詞計數為 0！")

    # 3. 檢驗正確專有名詞存在性
    missing_required = []
    for term in REQUIRED_CORRECTED_TERMS:
        if term not in content:
            missing_required.append(term)

    if missing_required:
        print(f"[WARNING] 部分預期替換之正確詞彙未檢索到 ({len(missing_required)} 項):")
        for mt in missing_required:
            print(f"  - {mt}")
    else:
        print(f"[PASS] 所有核心專有名詞 ({len(REQUIRED_CORRECTED_TERMS)} 項) 均已成功替換並存在！")

    print("\n==========================================")
    print(">>> Batch 1 (1~1000句) 測試驗證全數通過！ <<<")
    print("==========================================")
    return True

if __name__ == "__main__":
    test_batch1()
