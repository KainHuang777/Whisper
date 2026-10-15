import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scratch"))

from split_chunks import split_srt
from do_contextual_proofread import run_proofread
from merge_chunks import merge_srt

def main():
    print("==================================================")
    print(" 2026_08_12_19_03_14_462.srt 校稿與無縫合併工作鏈")
    print("==================================================")
    
    # 步驟 1: 依據字幕區塊邊界切分 7 個 Chunk
    split_srt()
    
    # 步驟 2: 依據對照庫與簡轉繁邏輯進行 Chunk 校稿
    run_proofread()
    
    # 步驟 3: 無縫合併校稿後 Chunk 並產出至 data/output/
    merge_srt()

if __name__ == "__main__":
    main()
