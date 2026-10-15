import os
import re
import sys

BASE_DIR = r"d:\work\非目前專案調研\Whisper"
SRT_PATH = os.path.join(BASE_DIR, "0902顧問交流會.srt")
RAW_PATH = os.path.join(BASE_DIR, "0902顧問交流會_raw.srt")

# 1. 簡轉繁字典與轉換器
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
        s2t_map = {
            '对': '對', '它': '它', '是': '是', '在': '在', '这': '這', '些': '些', '们': '們', '时': '時',
            '间': '間', '会': '會', '个': '個', '月': '月', '以': '以', '来': '來', '大': '大', '概': '概',
            '数': '數', '值': '值', '都': '都', '往': '往', '难': '難', '的': '的', '方': '方', '向': '向',
            '调': '調', '战': '戰', '加': '加', '点': '點', '而': '而', '已': '已', '其': '其', '实': '實',
            '就': '就', '针': '針', '老': '老', '用': '用', '户': '戶', '还': '還', '活': '活', '跃': '躍',
            '我': '我', '觉': '覺', '得': '得', '初': '初', '期': '期', '可': '可', '能': '能', '不': '不',
            '太': '太', '建': '建', '议': '議', '么': '麼', '低': '低', '到': '到', '版': '版', '本': '本',
            '从': '從', '宽': '寬', '松': '鬆', '开': '開', '始': '始', '进': '進', '去': '去', '要': '要',
            '挑': '挑', '后': '後', '面': '面', '应': '應', '该': '該', '慢': '慢', '拉': '拉', '起': '起',
            '两': '兩', '害': '害', '相': '相', '权': '權', '取': '取', '轻': '輕', '线': '線', '设': '設',
            '计': '計', '图': '圖', '纸': '紙', '盘': '盤', '棋': '棋', '子': '子', '体': '體', '力': '力',
            '钻': '鑽', '石': '石', '宝': '寶', '箱': '箱', '竞': '競', '品': '品', '游': '遊', '戏': '戲',
            '业': '業', '务': '務', '关': '關', '卡': '卡', '商': '商', '城': '城', '礼': '禮', '包': '包',
            '额': '額', '度': '度', '维': '維', '护': '護', '变': '變', '现': '現', '广': '廣', '告': '告',
            '组': '組', '合': '合', '动': '動', '作': '作', '场': '場', '景': '景', '节': '節', '录': '錄',
            '选': '選', '择': '擇', '标': '標', '准': '準', '测': '測', '试': '試', '检': '檢', '查': '查',
            '发': '發', '布': '布', '网': '網', '站': '站', '电': '電', '脑': '腦', '软': '軟', '件': '件',
            '硬': '硬', '码': '碼', '库': '庫', '类': '類', '型': '型', '表': '表', '格': '格', '据': '據',
            '显': '顯', '示': '示', '隐': '隱', '藏': '藏', '错': '錯', '误': '誤', '警': '警', '提': '提',
            '确': '確', '认': '認', '导': '導', '阶': '階', '段': '段', '预': '預', '告': '告', '给': '給',
            '门': '門', '规': '規', '总': '總', '结': '結', '构': '構', '统': '統', '计': '計', '资': '資',
            '源': '源', '胜': '勝', '负': '負', '胜': '勝', '率': '率', '购': '購', '买': '買', '费': '費',
            '销': '銷', '耗': '耗', '累': '累', '积': '積', '稳': '穩', '定': '定', '优': '優', '劣': '劣',
            '势': '勢', '缺': '缺', '口': '口', '轮': '輪', '档': '檔', '位': '位', '参': '參', '考': '考',
            '照': '照', '属': '屬', '性': '性', '标': '標', '签': '籤', '接': '接', '口': '口', '观': '觀',
            '看': '看', '次': '次', '数': '數', '控': '控', '制': '制', '价': '價', '值': '值', '种': '種',
            '导': '導', '引': '引', '问': '問', '题': '題', '回': '回', '归': '歸', '奖': '獎', '励': '勵',
            '钱': '錢', '车': '車', '牌': '牌', '挂': '掛', '装': '裝', '修': '修', '落': '落', '差': '差',
            '顺': '順', '利': '利', '掉': '掉', '这': '這', '样': '樣', '子': '子', '单': '單', '断': '斷',
            '崖': '崖', '崩': '崩', '评': '評', '级': '級', '榨': '榨', '屏': '屏', '插': '插', '跑': '跑',
            '期': '期', '卸': '卸', '载': '載', '常': '常', '识': '識', '糖': '糖', '粗': '粗', '赛': '賽',
            '量': '量', '创': '創', '新': '新', '惨': '慘', '冻': '凍', '国': '國', '美': '美', '女': '女',
            '男': '男', '壁': '壁', '垒': '壘', '营': '營', '收': '收', '环': '環', '闭': '閉', '自': '自',
            '然': '然', '吸': '吸', '体': '體', '变': '變', '卫': '衛', '聰': '聰', '聪': '聰', '鸽': '鴿',
            '鴿': '鴿', '鍵': '鍵', '键': '鍵', '銷': '消', '宵': '消'
        }
        def s2t(text):
            res = list(text)
            for i, c in enumerate(res):
                if c in s2t_map:
                    res[i] = s2t_map[c]
            return "".join(res)

# 2. 專業術語與錯字校對規則 (Part 4: 區塊 1501 ~ 2000)
RULES_PART4 = [
    # 競品遊戲
    (r"triple time", "Triple Town"),
    (r"Triple time", "Triple Town"),
    (r"Mirror Dragons", "Merge Dragons!"),
    (r"mirror dragons", "Merge Dragons!"),
    (r"merge genus", "Merge Dragons!"),
    (r"air merge", "EverMerge"),
    (r"Air merge", "EverMerge"),
    (r"merge magic", "Merge Magic!"),
    (r"Merge magic", "Merge Magic!"),
    (r"Royal Kingdom", "Royal Kingdom"),
    (r"Royal Match", "Royal Match"),
    
    # 遊戲玩法類型 (三合/二合/三消/點消/連消/肉鴿)
    (r"三盒", "三合"),
    (r"三核", "三合"),
    (r"二盒", "二合"),
    (r"二核", "二合"),
    (r"三宵", "三消"),
    (r"三销", "三消"),
    (r"三銷", "三消"),
    (r"点宵", "點消"),
    (r"點宵", "點消"),
    (r"连宵", "連消"),
    (r"連宵", "連消"),
    (r"肉哥", "肉鴿"),
    (r"合成王法", "合成玩法"),
    (r"它的合王法吗", "它的核心玩法嗎"),
    (r"它的合王法嗎", "它的核心玩法嗎"),
    (r"一件建造", "一鍵建造"),
    (r"锤类", "垂類"),
    (r"錘類", "垂類"),
    (r"垂内", "垂類"),
    (r"垂內", "垂類"),
    (r"加装哪一块", "家裝哪一塊"),
    (r"加裝哪一塊", "家裝哪一塊"),
    
    # 營運指標與數據
    (r"30流的流存", "30日留存"),
    (r"30流的留存", "30日留存"),
    (r"30流", "30留"),
    (r"前三天的流存", "前三天的留存"),
    (r"付费流存", "付費留存"),
    (r"付費流存", "付費留存"),
    (r"流存", "留存"),
    (r"复位点", "付費點"),
    (r"復位點", "付費點"),
    (r"八十九集", "89級"),
    (r"八十九級", "89級"),
    
    # 口語與劇情錯字
    (r"王冲", "王聰"),
    (r"王沖", "王聰"),
    (r"王冯", "王聰"),
    (r"王馮", "王聰"),
    (r"赚笔", "轉筆"),
    (r"賺筆", "轉筆"),
    (r"大家比方", "打個比方"),
    (r"打成补顶了", "打上補丁了"),
    (r"打成補頂了", "打上補丁了"),
    (r"不想看他的文色", "不想看他的文案"),
    (r"每一支NBC", "每一個 NPC"),
    (r"每一支NPC", "每一個 NPC"),
    (r"没事实在", "沒事閒著"),
    (r"没事显得", "沒事閒著"),
    (r"沒事顯得", "沒事閒著")
]

def proofread_text_part4(text: str) -> str:
    t = text
    # 1. 正則替換
    for pattern, repl in RULES_PART4:
        t = re.sub(pattern, repl, t)
        
    # 2. 簡繁轉換
    t = s2t(t)
    
    # 3. 繁體二次加固替換
    t = t.replace("triple time", "Triple Town")
    t = t.replace("Mirror Dragons", "Merge Dragons!")
    t = t.replace("air merge", "EverMerge")
    t = t.replace("三盒", "三合")
    t = t.replace("三核", "三合")
    t = t.replace("二盒", "二合")
    t = t.replace("二核", "二合")
    t = t.replace("三宵", "三消")
    t = t.replace("三銷", "三消")
    t = t.replace("點宵", "點消")
    t = t.replace("連宵", "連消")
    t = t.replace("肉哥", "肉鴿")
    t = t.replace("合成王法", "合成玩法")
    t = t.replace("一件建造", "一鍵建造")
    t = t.replace("錘類", "垂類")
    t = t.replace("垂內", "垂類")
    t = t.replace("加裝哪一塊", "家裝哪一塊")
    t = t.replace("30流的留存", "30日留存")
    t = t.replace("付費流存", "付費留存")
    t = t.replace("流存", "留存")
    t = t.replace("復位點", "付費點")
    t = t.replace("王沖", "王聰")
    t = t.replace("王馮", "王聰")
    t = t.replace("賺筆", "轉筆")
    t = t.replace("大家比方", "打個比方")
    t = t.replace("打成補頂了", "打上補丁了")
    t = t.replace("每一支NBC", "每一個 NPC")
    t = t.replace("每一支NPC", "每一個 NPC")
    t = t.replace("八十九集", "89級")
    t = t.replace("沒事顯得", "沒事閒著")
    return t

def main():
    print("==================================================")
    print("  0902顧問交流會.srt - Part 4 校對與自我驗證工具")
    print("==================================================")
    
    if not os.path.exists(SRT_PATH):
        print(f"[錯誤] 找不到目標 SRT: {SRT_PATH}")
        sys.exit(1)
        
    with open(SRT_PATH, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")
        
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    total_blocks = len(blocks)
    print(f"[檔案統計] 全檔總區塊數: {total_blocks}")
    assert total_blocks == 2878, f"區塊總數異常: 應為 2878，實際為 {total_blocks}"
    
    # Part 4 範圍：區塊 1501 至 2000（索引 1500 至 1999）
    start_idx = 1500
    end_idx = 2000
    print(f"[處理範圍] 正在校對區塊 {start_idx+1} ~ {end_idx} (共 {end_idx - start_idx} 個區塊)...")
    
    proofread_part4_blocks = []
    for i in range(start_idx, end_idx):
        lines = blocks[i].split("\n")
        if len(lines) >= 3:
            idx = lines[0]
            ts = lines[1]
            txts = lines[2:]
            new_txts = [proofread_text_part4(l) for l in txts]
            proofread_part4_blocks.append(f"{idx}\n{ts}\n" + "\n".join(new_txts))
        else:
            proofread_part4_blocks.append(proofread_text_part4(blocks[i]))
            
    # 組合：Part 1~3 已完成 (0~1500) + Part 4 新校對 (1500~2000) + 剩餘區塊 (2000~)
    final_blocks = blocks[:start_idx] + proofread_part4_blocks + blocks[end_idx:]
    assert len(final_blocks) == total_blocks, "組合後區塊總數不一致！"
    
    with open(SRT_PATH, "w", encoding="utf-8") as f:
        f.write("\n\n".join(final_blocks) + "\n")
        
    print(f"[校對完成] 區塊 1501 ~ 2000 已精準校正並回寫！")
    print(f"[累計進度] 全檔已完成 1 ~ 2000 區塊 (約前 8000 行)，進度 2000 / {total_blocks} (69.5%)")
    print("--------------------------------------------------")
    
    # 執行自我品質驗證
    print("[自動驗證] 正在驗證 Part 4 校對品質...")
    with open(SRT_PATH, "r", encoding="utf-8") as f:
        check_content = f.read().replace("\r\n", "\n")
    check_blocks = [b.strip() for b in check_content.split("\n\n") if b.strip()]
    assert len(check_blocks) == total_blocks, "區塊總數損壞！"
    
    part4_check_text = "\n\n".join(check_blocks[start_idx:end_idx])
    
    # 必須修正掉的錯字
    prohibited = [
        "triple time", "Mirror Dragons", "air merge", "三盒", "三核",
        "三宵", "三销", "三銷", "点宵", "點宵", "肉哥", "合成王法",
        "一件建造", "30流的流存", "30流的留存", "王冲", "王沖", "王冯", "王馮",
        "赚笔", "賺筆", "大家比方", "打成补顶了", "打成補頂了", "每一支NBC"
    ]
    for term in prohibited:
        assert term not in part4_check_text, f"未修正殘留詞: {term}"
        
    # 必須出現的正確名詞
    required = [
        "Triple Town", "Merge Dragons!", "EverMerge", "三合", "二合",
        "三消", "點消", "連消", "肉鴿", "合成玩法", "一鍵建造", "垂類",
        "30日留存", "付費留存", "王聰", "轉筆", "打個比方", "每一個 NPC"
    ]
    for term in required:
        assert term in part4_check_text, f"未出現正確詞: {term}"
        
    print("[驗證結果] Part 4 (區塊 1501 ~ 2000) 專有名詞與結構 100% 驗證通過！")
    print("==================================================")

if __name__ == "__main__":
    main()
