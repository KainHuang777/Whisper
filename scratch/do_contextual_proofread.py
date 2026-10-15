import os
import re

try:
    import opencc
    converter = opencc.OpenCC('s2t.json')
    def s2t(text):
        return converter.convert(text)
except ImportError:
    try:
        import zhconv
        def s2t(text):
            return zhconv.convert(text, 'zh-hant')
    except ImportError:
        # 內建常規簡轉繁基礎對照與替換
        def s2t(text):
            # 常見簡體字簡轉繁映射
            s2t_map = {
                '对': '對', '它': '它', '是': '是', '在': '在', '这': '這', '些': '些', '们': '們', '时': '時',
                '间': '間', '会': '會', '个': '個', '月': '月', '以': '以', '来': '來', '大': '大', '概': '概',
                '数': '數', '值': '值', '都': '都', '往': '往', '难': '難', '的': '的', '方': '方', '向': '向',
                '调': '調', '战': '戰', '加': '加', '点': '點', '而': '而', '已': '已', '其': '其', '实': '實',
                '就': '就', '针': '針', '老': '老', '用': '用', '户': '戶', '还': '還', '是': '是', '活': '活',
                '跃': '躍', '我': '我', '觉': '覺', '得': '得', '初': '初', '期': '期', '可': '可', '能': '能',
                '不': '不', '太': '太', '建': '建', '议': '議', '么': '麼', '低': '低', '到': '到', '版': '版',
                '本': '本', '从': '從', '宽': '寬', '松': '鬆', '开': '開', '始': '始', '进': '進', '去': '去',
                '要': '要', '挑': '挑', '后': '後', '面': '面', '应': '應', '该': '該', '慢': '慢', '拉': '拉',
                '起': '起', '两': '兩', '害': '害', '相': '相', '权': '權', '取': '取', '轻': '輕', '线': '線',
                '设': '設', '计': '計', '图': '圖', '纸': '紙', '盘': '盤', '棋': '棋', '子': '子', '体': '體',
                '力': '力', '钻': '鑽', '石': '石', '宝': '寶', '箱': '箱', '竞': '競', '品': '品', '游': '遊',
                '戏': '戲', '业': '業', '务': '務', '关': '關', '卡': '卡', '商': '商', '城': '城', '礼': '禮',
                '包': '包', '额': '額', '度': '度', '维': '維', '护': '護', '变': '變', '现': '現', '广': '廣',
                '告': '告', '组': '組', '合': '合', '动': '動', '作': '作', '场': '場', '景': '景', '节': '節',
                '点': '點', '练': '練', '习': '習', '书': '書', '页': '頁', '录': '錄', '像': '像', '单': '單',
                '词': '詞', '语': '語', '境': '境', '选': '選', '择': '擇', '标': '標', '准': '準', '测': '測',
                '试': '試', '检': '檢', '查': '查', '发': '發', '布': '布', '网': '網', '站': '站', '电': '電',
                '脑': '腦', '软': '軟', '件': '件', '硬': '硬', '件': '件', '码': '碼', '库': '庫', '类': '類',
                '型': '型', '表': '表', '格': '格', '数': '數', '据': '據', '显': '顯', '示': '示', '隐': '隱',
                '藏': '藏', '错': '錯', '误': '誤', '警': '警', '告': '告', '提': '提', '示': '示', '确': '確',
                '认': '認', '取消': '取消', '保存': '保存', '加載': '加載', '加載中': '載入中', '加載失敗': '載入失敗'
            }
            res = list(text)
            for i, c in enumerate(res):
                if c in s2t_map:
                    res[i] = s2t_map[c]
            return "".join(res)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_DIR = os.path.join(BASE_DIR, "scratch", "chunks")
PROOFREAD_DIR = os.path.join(BASE_DIR, "scratch", "proofread_chunks")

# 專有名詞與錯字對照替換規則（優先匹配較長詞組）
REPLACEMENT_RULES = [
    # H01 ~ H50 (0812 會議)
    ("宣章挑戰", "勳章挑戰"),
    ("宣章", "勳章"),
    ("畢克", "逼課"),
    ("逼客", "逼課"),
    ("一氪", "課金"),
    ("Ghost Harbor", "Gossip Harbor"),
    ("高斯哈佛", "Gossip Harbor"),
    ("高斯哈博", "Gossip Harbor"),
    ("高斯哈爾", "Gossip Harbor"),
    ("高斯哈勃", "Gossip Harbor"),
    ("Flambor", "Gossip Harbor"),
    ("Crimester", "Coin Master"),
    ("普蘭幣", "Plan B"),
    ("最始A", "測試 A"),
    ("最始B", "測試 B"),
    ("最始", "測試"),
    ("組線表", "主線配置表"),
    ("組線", "主線"),
    ("付配玩家", "付費玩家"),
    ("付配", "付費"),
    ("高活藥", "高活躍"),
    ("兩箱其害", "兩害相權"),
    ("五腦衝", "無腦衝"),
    ("五腦", "無腦"),
    ("簽列", "策略"),
    ("六四吧", "648"),
    ("三二八", "328"),
    ("pull冰", "破冰"),
    ("CM版", "CN版"),
    ("進桶", "靜彤"),
    ("流存", "留存"),
    ("流損", "流失"),
    ("流算", "留存"),
    ("UP值", "ARPU值"),
    ("新手導演", "新手引導"),
    ("選手引導", "新手引導"),
    ("富士團", "副棋盤"),
    ("復起盤", "副棋盤"),
    ("復棋盤", "副棋盤"),
    ("複習盤", "副棋盤"),
    ("副旗盤", "副棋盤"),
    ("夫妻斑斑", "副棋盤"),
    ("保障票流", "寶箱波流"),
    ("小妹子", "小機制"),
    ("小小木子", "小機制"),
    ("雙倍產中", "雙倍產出"),
    ("母旗鐵帶", "母棋迭代"),
    ("母旗", "母棋"),
    ("母期", "母棋"),
    ("一筆測試", "AB測試"),
    ("EP測試", "AB測試"),
    ("EP測", "AB測試"),
    ("跌跌樂", "疊疊樂"),
    ("苗欄曼", "浪漫餐廳"),
    ("浪浪餐廳", "浪漫餐廳"),
    ("二六次幫", "64次"),
    ("侏儒這種", "諸如此種"),
    ("二的八字方", "2的8次方"),
    ("又撒勾結", "下鉤子"),
    ("護士線", "故事線"),
    ("草位", "槽位"),
    ("sloss", "slots"),
    ("換修", "浣熊"),
    ("萬雄", "浣熊"),
    ("萬兄", "浣熊"),
    
    # G01 ~ G12 (0723 顧問交流會)
    ("期子", "棋子"),
    ("妻子", "棋子"),
    ("母旗", "母棋"),
    ("副旗盤", "副棋盤"),
    ("附棋盤", "副棋盤"),
    ("生產期", "生成器"),
    ("生產基", "生成器"),
    ("生產器", "生成器"),
    ("Ted Trouble", "Travel Town"),
    ("TelTurbo", "Travel Town"),
    ("Techable", "Travel Town"),
    ("Telchabot", "Travel Town"),
    ("太久不", "Travel Town"),
    ("K-SHABLE", "Travel Town"),
    ("Ted Chappell", "Travel Town"),
    ("Tay Chabot", "Travel Town"),
    ("Tastic Travel", "Travel Town"),
    ("C-Trival", "Travel Town"),
    ("開期休一", "開七休一"),
    ("流春數據", "留存數據"),
    ("流春", "留存"),
]

def proofread_chunk(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    proofread_lines = []
    for line in lines:
        # 如果是字幕序號或時間戳行，保持原樣
        if line.strip().isdigit() or "-->" in line:
            proofread_lines.append(line)
        else:
            text = line
            # 1. 執行簡轉繁
            text = s2t(text)
            # 2. 執行對照表替換
            for src, tgt in REPLACEMENT_RULES:
                text = text.replace(src, tgt)
            proofread_lines.append(text)
            
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(proofread_lines)

def run_proofread():
    os.makedirs(PROOFREAD_DIR, exist_ok=True)
    
    chunk_files = sorted([f for f in os.listdir(CHUNKS_DIR) if f.startswith("chunk_") and f.endswith(".srt")])
    print(f"[校稿] 開始處理 {len(chunk_files)} 個 Chunk 檔案...")
    
    for f_name in chunk_files:
        in_path = os.path.join(CHUNKS_DIR, f_name)
        out_path = os.path.join(PROOFREAD_DIR, f_name)
        proofread_chunk(in_path, out_path)
        print(f"  - 完成 Chunk 校稿: {f_name} -> {out_path}")

if __name__ == "__main__":
    run_proofread()
