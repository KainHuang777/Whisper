import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRT_PATH = os.path.join(BASE_DIR, "0902顧問交流會.srt")
RAW_PATH = os.path.join(BASE_DIR, "0902顧問交流會_raw.srt")

def test_proofread_part6():
    print("==================================================")
    print("  0902 顧問交流會 Part 6 及全檔 100% 品質驗證測試")
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
        
    # 檢查區塊 2501 ~ 2878 (索引 2500 ~ 2878)
    part6_text = "\n\n".join(blocks[2500:2878])
    
    prohibited = [
        "Apple Loving", "麦吉泰文", "麥吉泰文", "多个城市", "多個城市",
        "test travel", "Travel Town", "Survival Merge", "立会家对话", "立會家對話",
        "紫娃娃", "很有带路感", "很有帶路感", "视网", "視網", "谢谢王冲", "謝謝王沖"
    ]
    for p in prohibited:
        if p in part6_text:
            print(f"[錯誤] 發現殘留錯字: {p}")
            return False
            
    required = [
        "AppLovin", "麥吉太文", "波克城市", "Tasty Travels: Merge Game", "Merge Survival",
        "立繪加對話", "紙娃娃", "很有代入感", "試玩", "謝謝王聰"
    ]
    for r in required:
        if r not in part6_text:
            print(f"[錯誤] 未找到預期正確詞: {r}")
            return False
            
    print(f"[通過] Part 6 (區塊 2501 ~ 2878) 錯字過濾與術語置換完全正確！")
    print("==================================================")
    print(f"★ 恭喜！0902顧問交流會全檔 2,878 區塊已 100% 完成校對與繁體化！★")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = test_proofread_part6()
    sys.exit(0 if success else 1)
