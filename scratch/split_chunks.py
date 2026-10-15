import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_SRT = os.path.join(BASE_DIR, "data", "input", "2026_08_12_19_03_14_462.srt")
CHUNKS_DIR = os.path.join(BASE_DIR, "scratch", "chunks")

def split_srt():
    os.makedirs(CHUNKS_DIR, exist_ok=True)
    
    with open(INPUT_SRT, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 標準化換行並以雙換行拆分成字幕區塊
    content = content.replace("\r\n", "\n")
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    
    total_blocks = len(blocks)
    num_chunks = 7
    blocks_per_chunk = (total_blocks + num_chunks - 1) // num_chunks
    
    print(f"[切分] 總字幕區塊數: {total_blocks}，切分為 {num_chunks} 個 Chunk（每 Chunk 約 {blocks_per_chunk} 區塊）")
    
    for i in range(num_chunks):
        start_idx = i * blocks_per_chunk
        end_idx = min((i + 1) * blocks_per_chunk, total_blocks)
        chunk_blocks = blocks[start_idx:end_idx]
        
        chunk_path = os.path.join(CHUNKS_DIR, f"chunk_{i+1}.srt")
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(chunk_blocks) + "\n")
            
        print(f"  - Chunk {i+1}: 區塊 {start_idx+1} ~ {end_idx} (共 {len(chunk_blocks)} 個區塊) -> {chunk_path}")

if __name__ == "__main__":
    split_srt()
