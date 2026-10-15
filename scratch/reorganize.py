# -*- coding: utf-8 -*-
"""
專案目錄結構整理與重構腳本
將散落於根目錄與 src 的檔案，依據職責清晰分類搬移至 docs/, media/, tests/, data/
"""

import os
import shutil
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 1. 欲建立的目錄結構
TARGET_DIRS = [
    os.path.join(BASE_DIR, "docs", "meetings"),
    os.path.join(BASE_DIR, "docs", "manuals"),
    os.path.join(BASE_DIR, "docs", "glossaries"),
    os.path.join(BASE_DIR, "media", "videos"),
    os.path.join(BASE_DIR, "media", "audio"),
    os.path.join(BASE_DIR, "tests", "proofread"),
    os.path.join(BASE_DIR, "data", "output"),
    os.path.join(BASE_DIR, "src"),
]

# 2. 搬移規則定義 (來源檔名/樣式 -> 目標目錄)
MOVE_MAPPINGS = [
    # --- 影音檔案 (media) ---
    (
        [
            "0723顧問交流會.mp4",
            "TimeLine劇情範本使用與教學0714.mp4",
            "Timeline編輯教學.mp4",
            "VIDEO_102647_1_24532_043c424ef7caf0bb4b00aae802eaf0b3.mp4",
            "場景設置教學1.mp4",
            "場景設置教學2.mp4",
            "文本申請與翻譯流程完整教學.mp4",
        ],
        os.path.join("media", "videos"),
    ),
    (
        [
            "0902顧問交流會.mp3",
        ],
        os.path.join("media", "audio"),
    ),

    # --- 會議紀錄與週報 (docs/meetings) ---
    (
        [
            "1012-1014顧問交流會_專案週報.html",
            "1012-1014顧問交流會_專案週報_PPT三頁內容.md",
            "1012顧問交流會_延伸參考附件.md",
            "1012顧問交流會_會議紀錄.md",
            "1012顧問交流會_會議紀錄與參考附件.html",
            "1014顧問交流會_延伸研究附錄.md",
            "1014顧問交流會_會議紀錄.md",
            "1014顧問交流會_會議紀錄與延伸研究.html",
            "FGUI多語言本地化_防錯風險分析報告.md",
            "技術架構分析報告.md",
        ],
        os.path.join("docs", "meetings"),
    ),

    # --- 操作手冊與技術指引 (docs/manuals) ---
    (
        [
            "Timeline編輯操作手冊.html",
            "Timeline編輯操作手冊.md",
            "場景設置與Timeline編輯_技術文件與操作手冊.html",
            "場景設置與Timeline編輯_技術文件與操作手冊.md",
            "文本申請與翻譯流程完整教學.html",
            "文本申請與翻譯流程完整教學.md",
            "文本申請表.xlsm",
            "IM_截圖_2026-08-20-09-19-40.png",
        ],
        os.path.join("docs", "manuals"),
    ),

    # --- 專有名詞與詞庫 (docs/glossaries) ---
    (
        [
            "專有名詞對照庫.md",
            "專有名詞對照庫_備份_20260914.md",
            "localization_guide_and_glossary.md",
            "translation_workflow_guide.md",
        ],
        os.path.join("docs", "glossaries"),
    ),

    # --- 字幕檔案歸檔 (data/output) ---
    (
        [
            "0902顧問交流會.srt",
            "0902顧問交流會_raw.srt",
            "1012顧問交流會_校正版.srt",
            "TimeLine劇情範本使用與教學0714.srt",
            "Timeline編輯教學.srt",
            "場景設置教學1.srt",
            "場景設置教學2.srt",
            "字串與填表申請.srt",
            "文本申請與翻譯流程完整教學.str",
        ],
        os.path.join("data", "output"),
    ),

    # --- 根目錄輔助腳本移至 src ---
    (
        [
            "clean_srt.py",
        ],
        "src",
    ),
]


def execute_reorganization():
    print("=" * 65)
    print("  Whisper 專案目錄重構與整理作業開始")
    print("=" * 65)

    # 步驟 1: 建立目標目錄
    print("\n[1/4] 檢查並建立目標資料夾...")
    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            print(f"  + 建立目錄: {os.path.relpath(target_dir, BASE_DIR)}")
        else:
            print(f"  v 目錄已存在: {os.path.relpath(target_dir, BASE_DIR)}")

    # 步驟 2: 搬移根目錄檔案
    print("\n[2/4] 搬移根目錄之影音、文件、字幕與工具檔...")
    moved_count = 0
    for file_list, target_rel_dir in MOVE_MAPPINGS:
        target_dir = os.path.join(BASE_DIR, target_rel_dir)
        for fname in file_list:
            src_path = os.path.join(BASE_DIR, fname)
            dst_path = os.path.join(target_dir, fname)

            if os.path.exists(src_path):
                # 若目標檔案已存在且是同一檔案，則覆蓋或更新
                shutil.move(src_path, dst_path)
                print(f"  -> [移動] {fname} => {target_rel_dir}/")
                moved_count += 1
            else:
                # 檢查是否已在目標位置
                if os.path.exists(dst_path):
                    print(f"  - [已存在目標位置] {fname} -> {target_rel_dir}/")
                else:
                    print(f"  ? [略過/未找到] {fname}")

    # 步驟 3: 整理 src/ 內的測試腳本移至 tests/
    print("\n[3/4] 整理 src/ 目錄中的測試腳本至 tests/ ...")
    src_dir = os.path.join(BASE_DIR, "src")
    tests_dir = os.path.join(BASE_DIR, "tests")
    proofread_dir = os.path.join(tests_dir, "proofread")

    test_moves = [
        ("test_edge_tts.py", tests_dir),
        ("test_workflow.py", tests_dir),
        ("test_0902_transcribe.py", tests_dir),
    ]

    for fname, dst_folder in test_moves:
        src_path = os.path.join(src_dir, fname)
        dst_path = os.path.join(dst_folder, fname)
        if os.path.exists(src_path):
            shutil.move(src_path, dst_path)
            print(f"  -> [移動] src/{fname} => tests/{fname}")
            moved_count += 1

    # 逐字稿校對批次測試腳本
    proofread_pattern = os.path.join(src_dir, "test_proofread_*.py")
    for src_path in glob.glob(proofread_pattern):
        fname = os.path.basename(src_path)
        dst_path = os.path.join(proofread_dir, fname)
        shutil.move(src_path, dst_path)
        print(f"  -> [移動] src/{fname} => tests/proofread/{fname}")
        moved_count += 1

    # 步驟 4: 修復 tests/proofread 下的測試腳本 sys.path
    print("\n[4/4] 更新 tests/ 內部測試腳本的模組引用路徑 (sys.path)...")
    for test_file in glob.glob(os.path.join(proofread_dir, "*.py")):
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 原本是 os.path.dirname(os.path.abspath(__file__)) 或上一層
        # 現在位於 tests/proofread/，需要往上兩層達到根目錄
        old_pattern = "sys.path.append(os.path.dirname(os.path.abspath(__file__)))"
        new_pattern = "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))"
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  * [路徑修訂] {os.path.basename(test_file)}")

    print("\n" + "=" * 65)
    print(f"  專案目錄整理順利完成！累計移動 {moved_count} 個項目。")
    print("=" * 65)


if __name__ == "__main__":
    execute_reorganization()
