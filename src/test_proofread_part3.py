import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRT_PATH = os.path.join(BASE_DIR, "0902顧問交流會.srt")
RAW_PATH = os.path.join(BASE_DIR, "0902顧問交流會_raw.srt")

def test_proofread_part3():
    print("==================================================")
    print("  0902 顧問交流會 Part 3 品質驗證自我測試")
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
        
    # 檢查區塊 1001 ~ 1500 (索引 1000 ~ 1499)
    part3_text = "\n\n".join(blocks[1000:1500])
    
    prohibited = [
        "Klaus Haber", "Flambor", "合成奇葩", "买掉素材", "買掉素材",
        "又便宜又洗脸", "又便宜又洗臉", "自燃量", "把憋泪提的太高了", "把憋淚提的太高了",
        "卖蝉", "賣蟬", "民国的用户", "民國的用戶", "中卫是", "中衛是",
        "打一笔法", "打一筆法", "被超烂了", "被超爛了", "让公司火下去", "讓公司火下去"
    ]
    for p in prohibited:
        if p in part3_text:
            print(f"[錯誤] 發現殘留錯字: {p}")
            return False
            
    required = [
        "Gossip Harbor", "Flambé_Merge", "Merge Hope", "合成棋盤", "買量素材",
        "又便宜又吸量", "做變體", "家裝素材", "家裝題材", "自然量", "壁壘",
        "賣慘", "美國的用戶", "中位數", "打個比方", "被抄爛了", "讓公司活下去"
    ]
    for r in required:
        if r not in part3_text:
            print(f"[錯誤] 未找到預期正確詞: {r}")
            return False
            
    print(f"[通過] Part 3 (區塊 1001 ~ 1500) 錯字過濾與術語置換完全正確！")
    print("==================================================")
    print(f"[測試成功] 0902顧問交流會已累積完成 1 ~ 1500 區塊校對 (52.1%)！")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = test_proofread_part3()
    sys.exit(0 if success else 1)
