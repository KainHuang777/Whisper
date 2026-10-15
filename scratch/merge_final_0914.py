# -*- coding: utf-8 -*-
"""
將 Batch 1 ~ 4（共 3732 條字幕）無縫合併為最終交付成果：
data/output/聲音_2026_09_14_19_00_42_113.srt
"""
import os
import re

BATCH_FILES = [
    (1, 1000, r"scratch/batch_1_1000.srt"),
    (1001, 2000, r"scratch/batch_2_1001_2000.srt"),
    (2001, 3000, r"scratch/batch_3_2001_3000.srt"),
    (3001, 3732, r"scratch/batch_4_3001_3732.srt"),
]

FINAL_OUTPUT = r"data/output/聲音_2026_09_14_19_00_42_113.srt"

def main():
    all_blocks = []
    total_count = 0

    for start_idx, end_idx, fpath in BATCH_FILES:
        if not os.path.exists(fpath):
            print(f"[FAIL] 缺少批次檔案: {fpath}")
            return False

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read().strip()

        raw_blocks = re.split(r'\n\s*\n', content)
        batch_blocks = [b.strip() for b in raw_blocks if b.strip()]
        expected_len = end_idx - start_idx + 1

        print(f"[INFO] 讀取 {fpath}: 預期 {expected_len} 條，實際 {len(batch_blocks)} 條。")
        if len(batch_blocks) != expected_len:
            print(f"[FAIL] {fpath} 數量不符合預期！")
            return False

        all_blocks.extend(batch_blocks)
        total_count += len(batch_blocks)

    print(f"\n[INFO] 4 個批次全數讀取完成，累計字幕條數: {total_count} 條。")
    os.makedirs(os.path.dirname(FINAL_OUTPUT), exist_ok=True)

    result_content = "\n\n".join(all_blocks) + "\n"
    with open(FINAL_OUTPUT, "w", encoding="utf-8") as f:
        f.write(result_content)

    print(f"[SUCCESS] 最終成果成功輸出至: {FINAL_OUTPUT}")
    print(f"檔案大小: {os.path.getsize(FINAL_OUTPUT):,} bytes")
    return True

if __name__ == "__main__":
    main()
