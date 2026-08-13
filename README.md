# Whisper 語音轉文字與自動字幕生成專案

本專案支援將影片自動抽取音訊、透過地端 GPU (Whisper `large-v3`) 或雲端 API (Gemini API) 進行繁體中文語音轉文字並輸出 `.srt` 字幕，最後使用 FFmpeg 將字幕高品質燒錄至影片下方。

---

## 搬移專案至新機器 (如 5060 Ti PC) 步驟

當您需要將此專案部署到另一台配有高階顯卡 (如 RTX 5060 Ti) 的 Windows 電腦時，請按照以下指南進行遷移與建置：

### 1. 複製專案檔案 (打包與搬移)
- 請將本專案目錄（`Whisper/`）打包或透過 Git 複製到新機器。
- **[重要] 勿複製虛擬環境資料夾**：請**不要**複製 `.venv` 資料夾。新機器必須重新建立專案專屬的 `.venv` 以避免路徑與套件相依性出錯。

### 2. 新機器環境準備 (系統級依賴)
在新機器執行初始化腳本前，請確保新機器已安裝以下工具：
1. **Python 3.10 或 3.11**：
   - 請至 [Python 官網](https://www.python.org/downloads/) 下載安裝。
   - 安裝時務必勾選 **"Add Python to PATH"** (將 Python 加入系統環境變數)。
2. **FFmpeg**：
   - 請確保新機器已安裝 FFmpeg，且 `ffmpeg` 指令已加入系統環境變數 `PATH` 中。
   - 您可開啟 PowerShell 輸入 `ffmpeg -version` 進行驗證。
3. **NVIDIA 顯示卡驅動**：
   - 請確保已安裝最新的 NVIDIA 官方顯卡驅動，以支援 CUDA 12 運算加速。

### 3. 一鍵建立虛擬環境與安裝依賴
在新機器的專案根目錄下，開啟 PowerShell 並執行：

```powershell
# 若遇到 PowerShell 執行策略限制，請先執行此行：
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

.\setup.ps1
```
*此腳本會在新機器上自動建立全新的 `.venv` 虛擬環境，並下載支援 CUDA 12.1 加速的 PyTorch (2.5.1+cu121) 以及 faster-whisper 等核心套件。*

### 4. 啟用環境與自我測試
環境建置完成後，請在新機器啟用虛擬環境並執行測試腳本：

```powershell
# 1. 啟用虛擬環境
.venv\Scripts\Activate.ps1

# 2. 執行自我測試
python src/test_workflow.py
```
*在 5060 Ti 的 PC 上，您應該會看到 `[成功] 載入 tiny 模型` 且最終使用的計算精度為 **`float16`** (不需像 1050 一樣降級到 float32)，這代表 GPU 硬體加速已完美啟動。*

---

## 核心功能執行說明

在新機器啟用虛擬環境 (`.venv\Scripts\Activate.ps1`) 後，即可使用以下功能：

### 1. 地端 GPU 轉錄 (`transcribe_local.py`)

使用 `faster-whisper` 在本機 GPU 上進行語音轉文字，預設針對 5060 Ti 最佳化。

```bash
# 基礎用法 ─ 自動掃描 data/input/ 或根目錄內的第一個影片
python src/transcribe_local.py

# 指定影片
python src/transcribe_local.py --video "您的影片.mp4"

# 完整參數範例 (1050 Ti 建議值)
python src/transcribe_local.py --video "影片.mp4" --model_size medium --compute_type int8_float16

# 使用 CPU 進行轉錄 (無 GPU 時)
python src/transcribe_local.py --video "影片.mp4" --device cpu --compute_type float32

# 停用 VAD 語音活動偵測
python src/transcribe_local.py --video "影片.mp4" --no_vad
```

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `--video` | `str` | 自動掃描 | 輸入影片路徑 |
| `--model_size` | `str` | `large-v3` | 模型大小：`tiny`, `base`, `small`, `medium`, `large-v2`, `large-v3` |
| `--device` | `str` | `cuda` | 執行硬體：`cuda` 或 `cpu` |
| `--compute_type` | `str` | `float16` | 計算精度：`float16`, `int8_float16`, `int8`, `float32` |
| `--language` | `str` | `zh` | 辨識語言代碼 |
| `--no_vad` | flag | 關閉 | 停用 VAD 語音活動偵測 |

*轉錄產出的 `.srt` 字幕檔會自動儲存於 `data/output/` 目錄中。*

---

### 2. 雲端 API 轉錄 (`transcribe_api.py`)

使用 Google Gemini API 進行多模態音訊轉錄，適合無 GPU 或需處理超長影片的情境。

**前置準備：** 需先設定 `GEMINI_API_KEY` 環境變數：

```powershell
# PowerShell
$env:GEMINI_API_KEY = "您的_API_金鑰"
```

```bash
# 基礎用法 ─ 自動掃描影片
python src/transcribe_api.py

# 指定影片
python src/transcribe_api.py --video "您的影片.mp4"

# 指定 Gemini 模型版本
python src/transcribe_api.py --video "影片.mp4" --model "gemini-2.5-pro"
```

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `--video` | `str` | 自動掃描 | 輸入影片路徑 |
| `--model` | `str` | `gemini-2.5-flash` | Gemini 模型版本 |

---

### 3. 字幕壓制燒錄 (FFmpeg)
字幕生成後，在新機器直接執行根目錄下的批次檔，即可將字幕壓入影片中：

```cmd
.\burn_subtitles.bat "您的影片.mp4"
```
- 字幕檔預設會自動在 `data/output/` 中尋找與影片同名的 `.srt`。
- 壓制後的影片會儲存在 `data/output/` 下，檔名為 `[原檔名]_subtitled.mp4`。
- 燒錄樣式預設為：**微軟正黑體 (Microsoft JhengHei)、18px、底部置中、帶有黑色邊框防雜訊**。

---

## 常見問題排查

1. **顯卡不支援 float16 / 載入模型失敗：**
   - 我們的 `transcribe_local.py` 內建**自動降級機制**。如果在其他不支援 float16 的舊機器上執行，它會自動回退使用 `int8_float16` 或 `float32`，不需手動調整程式碼。
2. **找不到 ffmpeg：**
   - 請確認新機器已將 `ffmpeg/bin` 資料夾路徑新增至 Windows 的「系統環境變數」中，並重啟終端機使設定生效。
