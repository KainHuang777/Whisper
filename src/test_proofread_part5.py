import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRT_PATH = os.path.join(BASE_DIR, "0902顧問交流會.srt")
RAW_PATH = os.path.join(BASE_DIR, "0902顧問交流會_raw.srt")

def test_proofread_part5():
    print("==================================================")
    print("  0902 顧問交流會 Part 5 品質驗證自我測試")
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
        
    # 檢查區塊 2001 ~ 2500 (索引 2000 ~ 2499)
    part5_text = "\n\n".join(blocks[2000:2500])
    
    prohibited = [
        "去家", "曲家", "SRG", "仪女", "儀女", "Avata",
        "王蓝梅", "王藍梅", "下网的生活", "下網的生活", "甄嬛壮", "甄嬛壯",
        "手冲六块", "手沖六塊", "年轻会激高", "年輕會激高", "被剧情给拿出的玩家",
        "卷股风", "卷股風", "修箱玩法", "抠梦拐骗", "摳夢拐騙", "两分你们那边"
    ]
    for p in prohibited:
        if p in part5_text:
            print(f"[錯誤] 發現殘留錯字: {p}")
            return False
            
    required = [
        "趣加", "SLG", "乙女賽道", "Avatar", "王藍莓", "《嚮往的生活》",
        "《甄嬛傳》", "首充6元", "黏性會極高", "被劇情給拿住的玩家", "休閒玩法", "兩方你們那邊"
    ]
    for r in required:
        if r not in part5_text:
            print(f"[錯誤] 未找到預期正確詞: {r}")
            return False
            
    print(f"[通過] Part 5 (區塊 2001 ~ 2500) 錯字過濾與術語置換完全正確！")
    print("==================================================")
    print(f"[測試成功] 0902顧問交流會已累積完成 1 ~ 2500 區塊校對 (86.9%)！")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = test_proofread_part5()
    sys.exit(0 if success else 1)
