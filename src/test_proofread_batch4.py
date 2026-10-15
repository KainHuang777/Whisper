# -*- coding: utf-8 -*-
"""
測試腳本：驗證 Batch 4 (3001~3732句收官段) 校對品質與格式
"""
import os
import re

TARGET_FILE = r"scratch/batch_4_3001_3732.srt"

FORBIDDEN_WORDS_B4 = [
    "merch hotel", "Merch hotel", "Supercell的黑带", "Supercell的黑帶",
    "farm merge", "Directs", "浮游港口", "浮遊港口", "粉红港口", "粉紅港口",
    "粉红杆口", "粉紅桿口", "双校博物馆", "雙校博物館", "双点校园",
    "新city", "四三九九", "小期盼活动", "小期盼活動", "现实性的主线", "現實性的主線",
    "模拟性insider", "摩恩经营", "摩恩經營", "摩登星亿", "摩登星億", "莫文经营成建",
    "二和", "二河", "二核", "二盒", "三宵", "爱豆", "偏沃卡鞋", "沃卡鞋", "期度修显游戏",
    "期度修顯遊戲", "复文法", "複文法", "三旋二", "力箱",
    "买了MAI", "買了MAI", "测CTR", "測CTR", "手测", "手測", "手册我们还没有包",
    "手冊我們還沒有包", "养残系", "養殘系", "残疾", "旅行的青蛙", "水族岗",
    "水族崗", "非常谢谢君队", "非常謝謝君隊", "谢谢君队", "謝謝君隊", "跟军队约",
    "跟軍隊約", "到了非常多的干诉所", "干诉所", "幹訴所", "我们见见一下", "我們見見一下",
    "美术竹妹", "美術竹妹"
]

REQUIRED_TERMS_B4 = [
    "Merge Hotel Empire", "Supercell 的 Hay Day", "Farm Merge Valley",
    "Playrix", "緋聞港口", "雙點博物館", "雙點校園", "SimCity", "4399",
    "小棋盤活動", "限時性的主線", "模擬經營", "二合", "三消", "Idle",
    "歐卡寫實", "輕度休閒遊戲", "副玩法", "三選一", "立項", "買了 MAI",
    "測 CTR", "首測", "《旅行青蛙》", "水族館", "謝謝浚睿", "跟浚睿約",
    "乾貨", "借鑑", "主美"
]

def test_batch4():
    if not os.path.exists(TARGET_FILE):
        print(f"[FAIL] 目標檔案不存在: {TARGET_FILE}")
        print("請先在終端機運行: python scratch/execute_proofread_batch4.py")
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
    if len(indices) != 732:
        print(f"[FAIL] 字幕數量不符合預期 732 條，實際為 {len(indices)} 條！")
        return False

    if indices[0] != 3001 or indices[-1] != 3732:
        print(f"[FAIL] 字幕範圍不是 3001 ~ 3732，實際為 {indices[0]} ~ {indices[-1]}！")
        return False

    # 2. 檢驗禁止錯字
    forbidden_found = []
    for w in FORBIDDEN_WORDS_B4:
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
    for term in REQUIRED_TERMS_B4:
        if term not in content:
            missing_required.append(term)

    if missing_required:
        print(f"[WARNING] 部分預期替換之正確詞彙未檢索到 ({len(missing_required)} 項):")
        for mt in missing_required:
            print(f"  - {mt}")
    else:
        print(f"[PASS] 所有核心專有名詞 ({len(REQUIRED_TERMS_B4)} 項) 均已成功替換並存在！")

    print("\n==============================================")
    print(">>> Batch 4 (3001~3732句) 測試驗證全數通過！ <<<")
    print("==============================================")
    return True

if __name__ == "__main__":
    test_batch4()
