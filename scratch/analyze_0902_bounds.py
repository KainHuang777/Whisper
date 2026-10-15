import os

BASE_DIR = r"d:\work\非目前專案調研\Whisper"
SRT_PATH = os.path.join(BASE_DIR, "0902顧問交流會.srt")

with open(SRT_PATH, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# 尋找第 2000 行附近的區塊邊界 (\n)
target_line = 2000
split_line = target_line
for i in range(target_line, min(target_line + 50, len(lines))):
    if lines[i].strip() == "" and (i + 1 < len(lines)) and lines[i+1].strip().isdigit():
        split_line = i + 1
        break

print(f"Nearest clean block boundary around line 2000: line {split_line}")
print("Line around boundary:")
for j in range(max(0, split_line - 5), min(len(lines), split_line + 6)):
    print(f"{j+1}: {lines[j].strip()}")
