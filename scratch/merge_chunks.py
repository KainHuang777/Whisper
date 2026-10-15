import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROOFREAD_DIR = os.path.join(BASE_DIR, "scratch", "proofread_chunks")
OUTPUT_SRT = os.path.join(BASE_DIR, "data", "output", "2026_08_12_19_03_14_462.srt")

def merge_srt():
    os.makedirs(os.path.dirname(OUTPUT_SRT), exist_ok=True)
    
    chunk_files = sorted([f for f in os.listdir(PROOFREAD_DIR) if f.startswith("chunk_") and f.endswith(".srt")])
    all_blocks = []
    
    for f_name in chunk_files:
        chunk_path = os.path.join(PROOFREAD_DIR, f_name)
        with open(chunk_path, "r", encoding="utf-8") as f:
            content = f.read().replace("\r\n", "\n")
        blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
        all_blocks.extend(blocks)
        print(f"  - 合併 {f_name}: 包含 {len(blocks)} 個區塊")
        
    final_content = "\n\n".join(all_blocks) + "\n"
    
    with open(OUTPUT_SRT, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"==================================================")
    print(f"[完成] 校稿字幕合併成功！")
    print(f"  - 輸出檔案: {OUTPUT_SRT}")
    print(f"  - 總區塊數: {len(all_blocks)}")
    print(f"==================================================")

if __name__ == "__main__":
    merge_srt()
