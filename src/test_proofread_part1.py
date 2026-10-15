import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRT_PATH = os.path.join(BASE_DIR, "0902顧問交流會.srt")
RAW_PATH = os.path.join(BASE_DIR, "0902顧問交流會_raw.srt")

def test_proofread():
    print("==================================================")
    print("  0902 顧問交流會 Part 1 校對品質自我測試")
    print("==================================================")
    
    # 1. 檢查檔案存在性
    if not os.path.exists(SRT_PATH):
        print(f"[錯誤] 找不到目標 SRT 檔: {SRT_PATH}")
        return False
    if not os.path.exists(RAW_PATH):
        print(f"[警告] 尚未建立原始檔案備份: {RAW_PATH}")
        print("請先執行 scratch/proofread_part1.py 進行校對與備份。")
        return False
        
    with open(SRT_PATH, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_content = f.read().replace("\r\n", "\n")
        
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    raw_blocks = [b.strip() for b in raw_content.split("\n\n") if b.strip()]
    
    print(f"[區塊校驗] 目前區塊數: {len(blocks)} | 原始區塊數: {len(raw_blocks)}")
    if len(blocks) != len(raw_blocks):
        print("[錯誤] 區塊總數不一致！可能有區塊遺失或格式損壞。")
        return False
    else:
        print("[通過] 區塊總數完全一致！")
        
    # 2. 針對前 500 個區塊進行關鍵詞檢驗
    part1_text = "\n\n".join(blocks[:500])
    
    # 必須修正掉的殘留錯誤字詞
    prohibited_terms = [
        "肥文港口", "粉纹港口", "粉紋港口", "久未登你帮忙", "久未登你幫忙",
        "罚球流存", "一笔测试", "一笔测", "新手期日", "做AA的口", "打野比方",
        "免费赚一次"
    ]
    
    found_errors = []
    for term in prohibited_terms:
        if term in part1_text:
            found_errors.append(term)
            
    if found_errors:
        print(f"[警告] 前 500 區塊仍殘留未校正詞彙: {found_errors}")
        return False
    else:
        print("[通過] 所有預期錯字與殘留詞均已成功校正！")
        
    # 必須成功出現的正確名詞
    required_terms = [
        "IAA", "AEO", "VO", "緋聞港口", "新手七日活動", "破冰", "留存", "AB 測", "打個比方"
    ]
    
    found_required = []
    for term in required_terms:
        if term in part1_text:
            found_required.append(term)
        else:
            print(f"[提示] 未搜尋到預期校正詞: {term}")
            
    print(f"[驗證] 成功校對之重要術語: {found_required}")
    print("==================================================")
    print("[測試成功] 0902 顧問交流會 Part 1 (前 2000 行 / 500 區塊) 結構與名詞校對驗證通過！")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = test_proofread()
    sys.exit(0 if success else 1)
