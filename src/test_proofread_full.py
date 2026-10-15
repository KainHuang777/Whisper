import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRT_PATH = os.path.join(BASE_DIR, "0902顧問交流會.srt")
RAW_PATH = os.path.join(BASE_DIR, "0902顧問交流會_raw.srt")

def test_proofread_full():
    print("==================================================")
    print("  0902 顧問交流會【全檔 1 ~ 2878 區塊】完整品質檢驗")
    print("==================================================")
    
    if not os.path.exists(SRT_PATH):
        print(f"[錯誤] 找不到目標 SRT 檔: {SRT_PATH}")
        return False
    if not os.path.exists(RAW_PATH):
        print(f"[錯誤] 找不到原始備份檔: {RAW_PATH}")
        return False
        
    with open(SRT_PATH, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_content = f.read().replace("\r\n", "\n")
        
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    raw_blocks = [b.strip() for b in raw_content.split("\n\n") if b.strip()]
    total = len(blocks)
    
    print(f"[區塊總數校驗] 目前區塊數: {total} | 原始區塊數: {len(raw_blocks)}")
    if total != len(raw_blocks) or total != 2878:
        print(f"[錯誤] 區塊總數不符！預期 2878，實際 {total}")
        return False
    print("  -> 區塊總數嚴格一致 (2878 區塊) 通過！\n")
    
    full_text = content
    
    # -------------------------------------------------------------
    # 1. 各階段禁止殘留錯字全域掃描 (跨全檔檢查)
    # -------------------------------------------------------------
    print("[全檔禁止殘留錯字檢驗]")
    prohibited_dict = {
        "Part 1 (商業化/買量)": [
            "AO 还是 VO", "AO 還是 VO", "破标", "破標", "久未登你",
            "买体", "買體力買", "在線市場", "罰球流存", "笔值"
        ],
        "Part 2 (插屏/BP/二合)": [
            "查评", "查評", "次流", "刮钩", "刮鉤", "我们奥合", "我們奧合",
            "二和玩法", "从赛录到开屏", "從賽錄到開屏", "打一笔方向", "打一筆方向",
            "柠檬的flambor", "檸檬的flambor"
        ],
        "Part 3 (買量素材/自然量)": [
            "Klaus Haber", "Flambor", "合成奇葩", "买掉素材", "買掉素材",
            "又便宜又洗脸", "又便宜又洗臉", "自燃量", "把憋泪提的太高了", "把憋淚提的太高了",
            "卖蝉", "賣蟬", "民国的用户", "民國的用戶", "中卫是", "中衛是",
            "打一笔法", "打一筆法", "被超烂了", "被超爛了", "让公司火下去", "讓公司火下去"
        ],
        "Part 4 (三合/三消/競品)": [
            "triple time", "Triple time", "Mirror Dragons", "air merge",
            "三盒", "三核", "三宵", "三销", "三銷", "点宵", "點宵", "肉哥",
            "合成王法", "一件建造", "30流的流存", "30流的留存", "王冯", "王馮",
            "赚笔", "大家比方", "打成补顶了", "打成補頂了", "每一支NBC"
        ],
        "Part 5 (SLG/趣加/乙女)": [
            "去家", "曲家", "SRG", "仪女", "儀女", "Avata",
            "王蓝梅", "王藍梅", "下网的生活", "下網的生活", "甄嬛壮", "甄嬛壯",
            "手冲六块", "手沖六塊", "年轻会激高", "年輕會激高", "被剧情给拿出的玩家",
            "卷股风", "卷股風", "修箱玩法", "抠梦拐骗", "摳夢拐騙", "两分你们那边"
        ],
        "Part 6 (AppLovin/麥吉/收尾)": [
            "Apple Loving", "apple loving", "麦吉泰文", "麥吉泰文",
            "多个城市", "多個城市", "test travel", "Travel Town", "Survival Merge",
            "Mersweil", "立会家对话", "立會家對話", "紫娃娃", "很有带路感", "很有帶路感",
            "视网", "視網", "谢谢王冲", "謝謝王沖"
        ]
    }
    
    error_count = 0
    for part_name, term_list in prohibited_dict.items():
        failed_in_part = []
        for term in term_list:
            if term in full_text:
                failed_in_part.append(term)
        if failed_in_part:
            print(f"  [X] {part_name} 發現殘留錯字: {failed_in_part}")
            error_count += len(failed_in_part)
        else:
            print(f"  [V] {part_name} 錯字過濾通過")
            
    if error_count > 0:
        print(f"\n[檢驗失敗] 全檔累計發現 {error_count} 個未清除錯字！")
        return False
    print("  -> 全檔禁止錯字掃描 100% 通過！\n")
    
    # -------------------------------------------------------------
    # 2. 各階段核心正確術語存在性驗證
    # -------------------------------------------------------------
    print("[全檔核心正確專有名詞檢驗]")
    required_terms = [
        # Part 1
        "IAA", "AEO", "VO", "七日", "破冰", "在線時長", "付費留存",
        # Part 2
        "插屏", "次留", "二合", "小 BP", "Flambé_Merge", "載入",
        # Part 3
        "Gossip Harbor", "自然量", "買量素材", "又便宜又吸量", "做變體",
        "家裝素材", "家裝題材", "壁壘", "賣慘", "美國的用戶", "中位數",
        # Part 4
        "Triple Town", "Merge Dragons!", "EverMerge", "三合", "三消",
        "點消", "連消", "肉鴿", "一鍵建造", "30日留存", "王聰", "轉筆",
        # Part 5
        "趣加", "SLG", "乙女賽道", "Avatar", "王藍莓", "《嚮往的生活》",
        "《甄嬛傳》", "首充6元", "黏性會極高", "休閒玩法", "兩方你們那邊",
        # Part 6
        "AppLovin", "麥吉太文", "波克城市", "Tasty Travels: Merge Game",
        "Merge Survival", "立繪加對話", "紙娃娃", "很有代入感", "試玩", "謝謝王聰"
    ]
    
    missing_required = []
    for req in required_terms:
        if req not in full_text:
            missing_required.append(req)
            
    if missing_required:
        print(f"  [X] 未找到預期正確術語: {missing_required}")
        return False
    print(f"  [V] 全檔 {len(required_terms)} 項跨階段核心專有名詞全數驗證存在！\n")
    
    print("==================================================")
    print("★ 完美！0902顧問交流會.srt 全檔 2,878 區塊完整性與品質 100% 通過！★")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = test_proofread_full()
    sys.exit(0 if success else 1)
