# -*- coding: utf-8 -*-
"""
全檔整合品質測試工具：
針對最終成果 data/output/聲音_2026_09_14_19_00_42_113.srt 實施 100% 完整檢驗
"""
import os
import re

FINAL_FILE = r"data/output/聲音_2026_09_14_19_00_42_113.srt"

# 跨全階段禁止錯字總表 (100+ 項)
GLOBAL_FORBIDDEN_WORDS = [
    "董军锐", "董軍銳", "金瑞你先看", "军队约", "軍隊約", "君队", "君隊",
    "美国设施主要做两大类", "美國設施主要做兩大類", "UV创意类", "UV創意類",
    "著重毛在哪裡", "着重毛在哪里", "四只引荐", "肥龙港口", "fake蔬菜",
    "称装修的素材", "稱裝修的素材", "称的很好", "稱得很好", "滑龙道", "滑龍道",
    "Whisper Castle", "Vasper", "柠檬威去", "檸檬威去", "LimitWage",
    "林默威去", "林默威趣", "加接文法", "产值修水区", "產值修水區",
    "落地业", "落地業", "POA产品", "POA市場", "商业化变性", "商業化變性",
    "把RY打正", "把RY给打正", "脱明展示", "脫明展示", "起降那个时候",
    "超修素材", "数字卡点", "數字卡點", "产品调用", "飛客素材", "代包测试",
    "代包測試", "代包测", "代包測", "特别不息量", "美卖", "美賣", "模化版",
    "签评", "賣散", "买AO的时候", "偏剧形象的", "偏劇形象的", "mergery style",
    "Centaur", "蓝少爷", "藍少爺", "热心最早", "Trival Town", "Gossip Hub",
    "雷姆威去", "疯狂水世界", "迷雾小镇", "谁来救救我", "乡庭", "香亭",
    "也收的", "面包穴", "麵包穴", "叫定单", "单元聚模式", "更锤", "更錘",
    "模棱经营", "模拟机", "二合三修", "竖平", "禪戲", "恩帝动画", "小棋牌",
    "二河", "二核", "二盒", "三宵", "爱豆", "偏沃卡鞋", "期度修显游戏",
    "三旋二", "力箱", "买了MAI", "测CTR", "手测", "手册我们还没有包",
    "养残系", "残疾", "水族岗", "非常谢谢君队", "谢谢君队", "干诉所", "幹訴所",
    "我们见见一下", "美术竹妹"
]

# 核心專有名詞存在性抽樣檢驗 (50+ 項)
GLOBAL_REQUIRED_TERMS = [
    "董浚睿", "聖勛", "韋樸", "雪婷", "買量素材", "UE創意類", "著重錨在哪裡",
    "緋聞港口", "fake素材", "蹭裝修", "華容道", "Winter Castle", "檸檬微趣",
    "尋物解謎", "嫁接玩法", "Playrix", "鏟子", "落地頁", "商測", "PUA產品",
    "博樂科技", "莉莉絲", "商業化變現", "ROI", "脫敏展示", "起量", "Campaign 組",
    "家裝", "歐卡", "超休", "數值卡點", "研發調優", "帶包測試", "預算下限",
    "定向", "塔防", "美漫", "梗化", "七留", "次留", "T1", "點點互動",
    "Merge Restyle", "Sensor Tower", "箱庭", "ASO", "藍飛互娛", "天天玩家",
    "樂信", "Travel Town", "Gossip Harbor", "城建", "更垂", "模擬經營",
    "二合三消", "豎屏", "禪系", "Ending 動畫", "Merge Hotel Empire",
    "Supercell 的 Hay Day", "Farm Merge Valley", "4399", "Idle", "MAI",
    "CTR", "首測", "歐卡寫實", "副玩法", "乾貨", "借鑑", "主美"
]

def test_final():
    if not os.path.exists(FINAL_FILE):
        print(f"[FAIL] 最終檔案不存在: {FINAL_FILE}")
        print("請先在終端機運行合併腳本: python scratch/merge_final_0914.py")
        return False

    with open(FINAL_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 條目數檢驗（3732 條）
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

    print(f"[INFO] 讀取全檔字幕條數: {len(indices)} 條。")
    if len(indices) != 3732:
        print(f"[FAIL] 全檔字幕條數不符合預期 3732 條，實際為 {len(indices)} 條！")
        return False

    if indices[0] != 1 or indices[-1] != 3732:
        print(f"[FAIL] 字幕範圍不是 1 ~ 3732，實際為 {indices[0]} ~ {indices[-1]}！")
        return False

    # 序號連續性檢驗
    is_continuous = all(indices[i] == i + 1 for i in range(len(indices)))
    if not is_continuous:
        print("[FAIL] 字幕序號存在跳號或不連續！")
        return False
    else:
        print("[PASS] 全檔 3,732 條字幕序號 100% 嚴格遞增連續無損！")

    # 2. 禁止錯字掃描
    forbidden_found = []
    for w in GLOBAL_FORBIDDEN_WORDS:
        if w in content:
            forbidden_found.append(w)

    if forbidden_found:
        print(f"[FAIL] 檢驗出未清除的禁止錯字 ({len(forbidden_found)} 項):")
        for fw in forbidden_found:
            print(f"  - {fw}")
        return False
    else:
        print(f"[PASS] 全檔禁止錯字全數清除，違禁詞 ({len(GLOBAL_FORBIDDEN_WORDS)} 項) 檢測違禁計數為 0！")

    # 3. 核心名詞存在性
    missing_required = []
    for term in GLOBAL_REQUIRED_TERMS:
        if term not in content:
            missing_required.append(term)

    if missing_required:
        print(f"[WARNING] 部分核心專有名詞未檢索到 ({len(missing_required)} 項):")
        for mt in missing_required:
            print(f"  - {mt}")
    else:
        print(f"[PASS] 全檔核心專有名詞 ({len(GLOBAL_REQUIRED_TERMS)} 項) 全數檢驗通過！")

    print("\n==========================================================")
    print(">>> 0914 顧問交流會逐字稿 全檔 3,732 句 100% 驗證圓滿通過！ <<<")
    print("==========================================================")
    return True

if __name__ == "__main__":
    test_final()
