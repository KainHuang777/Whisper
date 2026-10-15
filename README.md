# Whisper 語音辨識與 Edge TTS 語音合成專案

本專案提供端到端的高效語音處理工作流程：
1. **語音辨識 (STT)**：支援將影音自動抽取音訊，透過地端 GPU (Whisper `large-v3`) 或雲端 API (Gemini API) 進行繁體中文語音轉文字並輸出 `.srt` 字幕，支援使用 FFmpeg 將字幕高品質燒錄至影片。
2. **語音合成 (TTS)**：整合微軟 Edge Neural TTS 服務，提供高自然度、零本地 GPU 負擔、完全免費且支援語速/音調調節的繁體中文語音生成功能。

---

## 專案目錄結構

```
Whisper/
├── docs/                           # 專案文件庫
│   ├── meetings/                   # 歷次顧問交流會會議紀錄、週報與簡報
│   ├── manuals/                    # 操作手冊（Timeline 編輯、場景設置、文本申請教學）
│   └── glossaries/                 # 專有名詞對照庫、本地化指引與術語表
│
├── media/                          # 影音多媒體存放區
│   ├── videos/                     # 原始教學與會議影片 (.mp4)
│   └── audio/                      # 原始輸入音訊 (.mp3)
│
├── data/                           # 專案資料輸出入
│   ├── input/                      # 待處理字幕或原始文字
│   ├── output/                     # 最終校正後 .srt 字幕、TTS 合成音訊 (.mp3)
│   └── audio/                      # 轉檔抽取之中間 .wav 暫存
│
├── src/                            # 核心原始程式碼
│   ├── transcribe_local.py         # Whisper 地端 GPU 轉錄核心
│   ├── transcribe_api.py           # Gemini 雲端 API 轉錄核心
│   ├── tts_service.py              # Edge TTS 語音合成核心服務
│   ├── clean_srt.py                # 字幕清理工具
│   └── utils/
│       └── media_utils.py          # 影音抽取與轉換工具
│
├── tests/                          # 整合測試腳本集中管理
│   ├── test_edge_tts.py            # TTS 整合測試
│   ├── test_workflow.py            # 轉錄工作流測試
│   └── proofread/                  # 逐字稿校對驗證測試集
│
├── run_transcribe.bat / .ps1       # 語音辨識快捷啟動腳本
├── run_tts.bat / .ps1              # 語音合成快捷啟動腳本
├── activate.bat / setup.ps1        # 環境初始化與啟用腳本
├── requirements.txt                # Python 相依套件清單
├── README.md                       # 專案說明文件
└── Update.txt                      # 專案更新履歷
```

---

## 環境建置與跨機器遷移指南

當您需要將此專案部署到另一台配有獨立顯卡 (如 RTX 5060 Ti / 40 系列) 的 Windows 電腦時，請參閱以下指南：

### 1. 複製專案檔案 (勿複製 `.venv`)
- **[重要警告] 絕對不要直接複製 `.venv` 目錄**：
  虛擬環境寫死了當前電腦的絕對路徑、作業系統環境與底層 C/CUDA 編譯二進位檔。複製到其他機器將導致無法啟動或路徑噴錯。
- **僅需複製**：專案根目錄中的程式碼、腳本與設定（`src/`, `docs/`, `requirements.txt`, `setup.ps1`, `run_*.bat` 等），容量不到 1MB。

### 2. 新機器前置系統工具準備
在新機器執行初始化前，請確認具備：
1. **Python 3.10 或 3.11**：
   - 請至 [Python 官網](https://www.python.org/downloads/) 下載安裝，務必勾選 **"Add Python to PATH"**。
2. **FFmpeg**：
   - 確保已安裝 FFmpeg 且 `ffmpeg` 已加入系統環境變數 `PATH`（PowerShell 執行 `ffmpeg -version` 可驗證）。
3. **NVIDIA 顯示卡驅動**：
   - 確保安裝最新 NVIDIA 官方驅動以支援 CUDA 硬體加速。

### 3. 一鍵安裝與自動配置
在專案根目錄下，開啟 PowerShell 執行：

```powershell
# 若遇到 PowerShell 執行策略限制，請先執行此行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 一鍵自動建置虛擬環境並安裝所有依賴 (包含 PyTorch CUDA 與 edge-tts)
.\setup.ps1
```

*(手動安裝方式：`python -m venv .venv` 後執行 `.\.venv\Scripts\pip.exe install -r requirements.txt`)*

---

## 核心功能使用說明

啟用虛擬環境（`.venv\Scripts\Activate.ps1` 或直接使用根目錄的快捷腳本）後即可操作：

### 1. Edge TTS 語音合成 (`src/tts_service.py`)

基於微軟 Edge Neural 在線語音技術，提供高自然度、零本地顯存開銷的語音合成功能。

#### 快捷方式：
* **雙擊批次檔**：執行根目錄的 `run_tts.bat` 即可快速測試繁中示範音訊。
* **PowerShell 腳本**：
  ```powershell
  # 自訂文字與指定台灣女聲
  .\run_tts.ps1 -Text "歡迎收聽今天的會議摘要" -Voice "zh-TW-HsiaoChenNeural" -OutputFile "data/output/meeting_intro.mp3"

  # 查詢可用語音清單
  .\run_tts.ps1 -ListVoices
  ```

#### Python CLI 命令列進階調用：
```bash
# 基礎文字合成
python src/tts_service.py --text "這是語音合成測試" --output "data/output/speech.mp3"

# 讀取純文字檔合成
python src/tts_service.py --file "docs/manuals/sample.txt" --output "data/output/manual.mp3"

# 調整語速 (+20%) 與音調 (+5Hz)
python src/tts_service.py --text "快節奏語音" --rate "+20%" --pitch "+5Hz"

# 查詢所有可用台灣繁體中文音色
python src/tts_service.py --list-voices
```

#### 推薦常用音色清單：
| 音色代碼 (ShortName) | 類型 | 適用場合與特色 |
|----------------------|------|----------------|
| `zh-TW-HsiaoChenNeural` | 台灣女聲 (曉臻) | **【首選推薦】** 自然親切、連線極度穩定，適合導讀與教學 |
| `zh-TW-HsiaoYuNeural` | 台灣女聲 (曉雨) | 活潑清脆、發音清晰，適合短影片與旁白 |
| `zh-CN-YunxiNeural` | 中文男聲 (雲希) | **【男聲首選】** 熱門旁白男聲，對繁體中文相容極佳、沉穩流暢 |
| `zh-TW-YunJheNeural` | 台灣男聲 (雲哲) | 台灣腔男聲（已內建微軟端點異常時的自動降級備援機制） |

---

### 2. 地端 GPU 轉錄 (`src/transcribe_local.py`)

使用 `faster-whisper` 在本地 GPU 進行語音轉文字，產出精準帶時間戳的 `.srt` 字幕。

```bash
# 快捷執行（自動抓取 media/ 目錄中的影片/音訊）
.\run_transcribe.bat "0902顧問交流會.mp3"

# 或直接透過 Python 執行
python src/transcribe_local.py --video "media/videos/教學影片.mp4" --model_size large-v3
```

| 常用參數 | 預設值 | 說明 |
|----------|--------|------|
| `--video` | 自動掃描 | 輸入影片或音訊路徑 (支援相對路徑與 media/ 自動探測) |
| `--model_size` | `large-v3` | 模型規格：`tiny`, `base`, `small`, `medium`, `large-v3` |
| `--device` | `cuda` | 執行運算裝置：`cuda` 或 `cpu` |
| `--compute_type` | `float16` | 計算精度：`float16` (支援舊卡自動回退降級) |

---

### 3. 雲端 API 轉錄 (`src/transcribe_api.py`)

使用 Google Gemini API 進行多模態音訊轉錄，適合無獨立顯卡或長音訊處理：

```powershell
$env:GEMINI_API_KEY = "您的_API_KEY"
python src/transcribe_api.py --video "media/videos/教學影片.mp4"
```

---

### 4. 字幕壓制燒錄 (FFmpeg)

將生成的 `.srt` 字幕以微軟正黑體高品質硬編碼燒錄至影片底部：

```cmd
.\burn_subtitles.bat "media/videos/教學影片.mp4"
```

---

## 測試與驗證

專案提供完整的自我檢測腳本（位於 `tests/` 目錄），請於終端機執行：

* **TTS 語音合成測試**：
  ```powershell
  .\.venv\Scripts\python.exe tests/test_edge_tts.py
  ```
  *(驗證繁中女聲、男聲、微調參數及雲端容錯機制)*

* **轉錄工作流程測試**：
  ```powershell
  .\.venv\Scripts\python.exe tests/test_workflow.py
  ```
