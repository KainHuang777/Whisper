import re
import os

srt_path = r"d:\work\非目前專案調研\Whisper\data\output\文本申請與翻譯流程完整教學.srt"
output_path = r"d:\work\非目前專案調研\Whisper\clean_text.txt"

with open(srt_path, "r", encoding="utf-8") as f:
    content = f.read()

# 移除 SRT 時間戳和序號
pattern = re.compile(r'\d+\n\d{2}:\d{2}:\d{2}[,\.]\d{3} --> \d{2}:\d{2}:\d{2}[,\.]\d{3}\n')
clean_blocks = pattern.split(content)

text_lines = []
for block in clean_blocks:
    lines = [line.strip() for line in block.split('\n') if line.strip()]
    text_lines.extend(lines)

clean_text = "\n".join(text_lines)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(clean_text)

print(f"轉換完成，檔案大小：{os.path.getsize(output_path)} bytes")
