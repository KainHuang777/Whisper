import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRT_PATH = os.path.join(BASE_DIR, "0902顧問交流會.srt")
RAW_PATH = os.path.join(BASE_DIR, "0902顧問交流會_raw.srt")

def test_proofread_part4():
    print("==================================================")
    print("  0902 顧問交流會 Part 4 品質驗證自我測試")
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
    
    print(f"[區塊校驗] 目前全檔區塊數: {len(blocks)} | 原始區塊數: {len(raw_blocks)}")
    if len(blocks) != len(raw_blocks) or len(blocks) != 2878:
        print("[錯誤] 區塊總數異常！")
        return False
        
    # 檢查區塊 1501 ~ 2000 (索引 1500 ~ 1999)
    part4_text = "\n\n".join(blocks[1500:2000])
    
    prohibited = [
        "triple time", "Mirror Dragons", "air merge", "三盒", "三核",
        "三宵", "三销", "三銷", "点宵", "點宵", "肉哥", "合成王法",
        "一件建造", "30流的流存", "30流的留存", "王冲", "王沖", "王冯", "王馮",
        "赚笔", "賺筆", "大家比方", "打成补顶了", "打成補頂了", "每一支NBC"
    ]
    for p in prohibited:
        if p in part4_text:
            print(f"[錯誤] 發現殘留錯字: {p}")
            return False
            
    required = [
        "Triple Town", "Merge Dragons!", "EverMerge", "三合", "二合",
        "三消", "點消", "連消", "肉鴿", "合成玩法", "一鍵建造", "垂類",
        "30日留存", "付費留存", "王聰", "轉筆", "打個比方", "每一個 NPC"
    ]
    for r in required:
        if r not in part4_text:
            print(f"[錯誤] 未找到預期正確詞: {r}")
            return False
            
    print(f"[通過] Part 4 (區塊 1501 ~ 2000) 錯字過濾與術語置換完全正確！")
    print("==================================================")
    print(f"[測試成功] 0902顧問交流會已累積完成 1 ~ 2000 區塊校對 (69.5%)！")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = test_proofread_part4()
    sys.exit(0 if success else 1)
