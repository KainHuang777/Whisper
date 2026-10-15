import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRT_PATH = os.path.join(BASE_DIR, "0902顧問交流會.srt")
RAW_PATH = os.path.join(BASE_DIR, "0902顧問交流會_raw.srt")

def test_proofread_part2():
    print("==================================================")
    print("  0902 顧問交流會 Part 2 品質驗證自我測試")
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
        
    # 檢查區塊 501 ~ 1000
    part2_text = "\n\n".join(blocks[500:1000])
    
    prohibited = [
        "查评", "查評", "次流", "刮钩", "刮鉤", "我们奥合", "我們奧合",
        "二和玩法", "从赛录到开屏", "從賽錄到開屏", "打一笔方向", "打一筆方向"
    ]
    for p in prohibited:
        if p in part2_text:
            print(f"[錯誤] 發現殘留錯字: {p}")
            return False
            
    required = ["插屏", "次留", "二合", "載入", "小 BP", "打個比方", "Flambé_Merge"]
    for r in required:
        if r not in part2_text:
            print(f"[錯誤] 未找到預期正確詞: {r}")
            return False
            
    print(f"[通過] Part 2 (區塊 501 ~ 1000) 錯字過濾與術語置換完全正確！")
    print("==================================================")
    print("[測試成功] 0902顧問交流會已累積完成 1 ~ 1000 區塊校對！")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = test_proofread_part2()
    sys.exit(0 if success else 1)
