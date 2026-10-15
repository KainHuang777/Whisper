import os
import re

input_path = r"data/input/聲音_2026_09_14_19_00_42_113.srt"
scratch_dir = r"scratch"

def parse_srt(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read().strip()
    
    # 標準 SRT 區塊依雙換行分割
    raw_blocks = re.split(r'\n\s*\n', content)
    blocks = []
    for b in raw_blocks:
        b = b.strip()
        if not b:
            continue
        lines = b.split('\n')
        if len(lines) >= 2:
            try:
                idx = int(lines[0].strip())
                blocks.append((idx, b))
            except ValueError:
                # 若首行不是純數字，仍保留區塊
                blocks.append((len(blocks) + 1, b))
    return blocks

def main():
    os.makedirs(scratch_dir, exist_ok=True)
    blocks = parse_srt(input_path)
    total = len(blocks)
    print(f"總共解析到 {total} 條字幕區塊。")

    ranges = [
        (1, 1000, "scratch/batch_1_1000.srt"),
        (1001, 2000, "scratch/batch_1001_2000.srt"),
        (2001, 3000, "scratch/batch_2001_3000.srt"),
        (3001, total, "scratch/batch_3001_3732.srt")
    ]

    for start_idx, end_idx, out_name in ranges:
        batch_blocks = [b[1] for b in blocks if start_idx <= b[0] <= end_idx]
        with open(out_name, "w", encoding="utf-8") as f:
            f.write("\n\n".join(batch_blocks) + "\n")
        print(f"已輸出 {out_name}：包含第 {start_idx} 至 {min(end_idx, total)} 句，共 {len(batch_blocks)} 句。")

if __name__ == "__main__":
    main()
