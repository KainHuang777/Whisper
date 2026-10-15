from pathlib import Path
from html import escape
import re
import markdown

ROOT = Path(__file__).resolve().parents[1]
meeting_path = ROOT / '1012顧問交流會_會議紀錄.md'
appendix_path = ROOT / '1012顧問交流會_延伸參考附件.md'
output_path = ROOT / '1012顧問交流會_會議紀錄與參考附件.html'

# Normalize the newly authored appendix; source minutes and transcript stay intact.
appendix = appendix_path.read_text(encoding='utf-8')
for a, b in {'画':'畫','安装':'安裝','点击':'點擊','検':'檢','体验':'體驗','写':'寫',
             '指标':'指標','应':'應','人数':'人數','组':'組','归':'歸','行业':'行業',
             '优化':'優化', '浏览':'瀏覽', '项':'項'}.items():
    appendix = appendix.replace(a, b)
appendix = appendix.replace('abtest-config#metrics', 'abtest-config')
appendix_path.write_text(appendix, encoding='utf-8')
meeting = meeting_path.read_text(encoding='utf-8-sig')
meeting = meeting.replace('E:/WORK/Whisper/data/output/1012顧問交流會_校正版.srt',
                          '1012顧問交流會_校正版.srt')

def convert(text, prefix):
    text = re.sub(r'^# .+\n', '', text, count=1)
    body = markdown.markdown(text, extensions=['tables', 'sane_lists'])
    headings = []
    def heading(match):
        label = re.sub('<[^>]+>', '', match.group(1))
        anchor = f'{prefix}-{len(headings)+1}'
        headings.append((anchor, label))
        return f'<h2 id="{anchor}">{match.group(1)}</h2>'
    body = re.sub(r'<h2>(.*?)</h2>', heading, body)
    body = re.sub(r'<table>(.*?)</table>', r'<div class="table-wrap" tabindex="0"><table>\1</table></div>', body, flags=re.S)
    body = re.sub(r'<th>(.*?)</th>', r'<th scope="col">\1</th>', body, flags=re.S)
    return body, headings

meeting_body, meeting_heads = convert(meeting, 'meeting')
appendix_body, appendix_heads = convert(appendix, 'appendix')
stages = [('市場與口徑', '對齊受眾、目的與回收要求'), ('概念方向測試', '題材／畫風／劇情吸引力'),
          ('真實 Demo 包', '核心循環、承接與埋點'), ('導量與漏斗', 'CPI、轉化、首日與留存'),
          ('七日內容商測', '素材與內容並行，驗證回收'), ('逐步擴量', '新增成本、回收與內容供給')]
track = '<ol class="stage-track" aria-label="相對階段時間軸，依序由零至五">' + ''.join(
    f'<li><span class="stage-no">{n:02d}</span><strong>{title}</strong><small>{description}</small></li>'
    for n, (title, description) in enumerate(stages)) + '</ol>'
appendix_body = appendix_body.replace('<h3>0．', track + '<h3>0．', 1)
nav = '<a class="nav-part" href="#minutes">01　會議紀錄</a>'
nav += ''.join(f'<a href="#{i}">{escape(t)}</a>' for i, t in meeting_heads)
nav += '<a class="nav-part ref" href="#references">02　延伸參考附件</a>'
nav += ''.join(f'<a href="#{i}">{escape(t)}</a>' for i, t in appendix_heads)

css = '''
:root{--ink:#233148;--muted:#5e6d81;--bg:#f2f5f8;--paper:#fff;--line:#dce4ec;--accent:#164e74;--ref:#93632d;--soft:#edf5fa;--refsoft:#faf4e9}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:38px}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC",sans-serif;font-size:16px;line-height:1.85}a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:4px}a:hover{color:#087491}a:focus-visible,button:focus-visible,.table-wrap:focus-visible{outline:3px solid #b27623;outline-offset:4px}h1,h2,h3{line-height:1.4;font-weight:700}h1{font-size:clamp(30px,4vw,48px);margin:15px 0 12px;letter-spacing:.02em}h2{font-size:25px;margin:52px 0 22px;padding-top:8px;border-top:1px solid var(--line)}h3{font-size:19px;margin:28px 0 12px}p{margin:14px 0}li{margin:7px 0}strong{font-weight:700}ul,ol{padding-left:1.5em}.shell{max-width:1430px;margin:auto;padding:36px 36px 80px}.hero{background:#162e46;color:#f7fbff;padding:40px 44px;border-radius:8px;position:relative;overflow:hidden}.eyebrow{font-size:13px;letter-spacing:.14em;color:#bed1e1;font-weight:700}.hero p{max-width:760px;color:#d1dfeb;line-height:1.8}.hero-meta{display:flex;gap:12px 28px;flex-wrap:wrap;margin-top:24px;color:#c6d7e7;font-size:14px}.quick{display:flex;gap:10px;flex-wrap:wrap;margin-top:25px}.quick a{color:#f7fbff;border:1px solid #61758b;padding:7px 15px;text-decoration:none;border-radius:4px;font-size:14px}.layout{display:grid;grid-template-columns:238px minmax(0,1fr);gap:28px;margin-top:28px;align-items:start}.sidebar{position:sticky;top:24px;max-height:calc(100vh - 48px);overflow-y:auto;padding:8px 10px 16px 0}.sidebar-label{font-size:12px;color:var(--muted);letter-spacing:.12em;margin-bottom:10px}.sidebar a{display:block;color:var(--muted);font-size:13px;line-height:1.7;padding:8px 10px;margin:2px 0;text-decoration:none;border-left:2px solid transparent}.sidebar a:hover,.sidebar a.active{color:var(--accent);background:#e6edf4;border-left-color:var(--accent)}.sidebar .nav-part{font-size:14px;font-weight:bold;color:var(--ink);margin-top:14px}.sidebar .ref{color:var(--ref)}.main{min-width:0}.paper{background:var(--paper);padding:36px 40px;margin-bottom:30px;border-radius:6px;box-shadow:0 3px 12px #1b2e4010}.part-head{margin:0 0 28px;padding-bottom:22px;border-bottom:2px solid var(--accent)}.part-head h2{font-size:30px;margin:8px 0 10px;padding:0;border:0}.part-label{font-size:12px;font-weight:bold;letter-spacing:.13em;color:var(--accent)}.part-head p{color:var(--muted);margin:0}.reference-paper .part-head{border-color:var(--ref)}.reference-paper .part-label{color:var(--ref)}.source-note{background:var(--soft);padding:16px 20px;font-size:14px;color:#35516a;border-left:4px solid var(--accent);margin-bottom:24px}.reference-paper>.source-note{background:var(--refsoft);border-color:var(--ref);color:#725224}.table-wrap{max-width:100%;overflow-x:auto;margin:22px 0;border:1px solid var(--line);border-radius:4px}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.8;text-align:left}th{background:#eef3f7;color:#314a60;font-weight:bold;vertical-align:top}th,td{padding:13px 16px;border-bottom:1px solid var(--line);vertical-align:top}tr:last-child td{border-bottom:0}tbody tr:nth-child(even){background:#fafbfd}.reference-paper th{background:#f8f2e7;color:#745731}.reference-paper h2{color:#775526}.reference-paper h3{border-left:3px solid #c79e64;padding-left:12px}.meeting-content>p:has(strong:first-child){color:#455a70}.tools{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:18px 0 0}button{font:inherit;background:#fff;color:var(--ink);border:1px solid var(--line);border-radius:4px;padding:7px 14px;cursor:pointer;font-size:13px}.footer{font-size:13px;color:var(--muted);padding:8px 4px}.footer p{margin:7px 0}.skip{position:absolute;left:-1000px;top:0}.skip:focus{left:20px;top:15px;z-index:10;background:white;padding:10px}.scroll-top{display:block;text-align:right;margin-top:20px;font-size:13px}code{font-family:Consolas,monospace;background:#f0f3f6;padding:2px 4px;overflow-wrap:anywhere}h2[id],section[id]{scroll-margin-top:28px}
@media(max-width:1100px){.shell{padding:24px 22px 50px}.layout{grid-template-columns:200px minmax(0,1fr);gap:18px}.paper{padding:28px}.hero{padding:32px}th,td{padding:11px}}
@media(max-width:820px){.layout{display:block}.sidebar{position:static;max-height:none;padding:12px 16px;background:#eaf0f5;margin-bottom:20px;border-radius:4px}.sidebar nav{display:grid;grid-template-columns:1fr 1fr;gap:0 12px}.sidebar a{font-size:12px}.sidebar .nav-part{grid-column:1/-1}.paper{padding:24px}.hero{padding:28px}.table-wrap table{min-width:620px}h2{font-size:22px}.part-head h2{font-size:26px}}
@media(max-width:480px){.shell{padding:12px 10px 36px}.paper{padding:22px 18px}.hero{padding:26px 22px}body{font-size:15px}.hero-meta{gap:6px 16px}.quick a{font-size:12px}.sidebar nav{grid-template-columns:1fr}.sidebar a{padding:5px 8px}}
@media print{@page{size:A4;margin:16mm 13mm}html{scroll-behavior:auto}body{background:white;font-size:10.5pt;color:#111}.shell{max-width:none;padding:0}.hero{background:white;color:#111;padding:0 0 18px;border-radius:0}.hero p,.eyebrow,.hero-meta{color:#333}h1{font-size:26pt}.quick,.sidebar,.tools,.scroll-top,.skip{display:none}.layout{display:block;margin:0}.paper{padding:0;box-shadow:none;margin:18px 0;border-radius:0}.reference-paper{break-before:page}.part-head h2{font-size:20pt}.part-head{margin-top:22px}h2{font-size:16pt;margin-top:28px;break-after:avoid}h3{font-size:13pt;break-after:avoid}p,li{orphans:3;widows:3}.table-wrap{overflow:visible;border:0}table{font-size:9pt;min-width:0!important;table-layout:fixed}th,td{padding:7px 6px;overflow-wrap:anywhere}thead{display:table-header-group}tr{break-inside:avoid}a{color:#111}a[href^="https:"]{overflow-wrap:anywhere}.source-note{background:#f5f5f5!important;color:#222!important}.footer{font-size:9pt}}
'''
css += '''
.stage-track{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));list-style:none;padding:0;margin:28px 0 34px;gap:20px 24px}.stage-track li{margin:0;border-top:2px solid #bb935b;padding:12px 0 0}.stage-no{display:block;font-size:23px;color:var(--ref);font-weight:700;line-height:1.4}.stage-track strong{display:block;font-size:15px}.stage-track small{display:block;font-size:12px;color:var(--muted);line-height:1.6;margin-top:4px}@media(max-width:600px){.stage-track{grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}@media print{.stage-track{break-inside:avoid;grid-template-columns:repeat(3,minmax(0,1fr))}}
'''

html = f'''<!doctype html>
<html lang="zh-Hant">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="1012 顧問交流會：會議紀錄，以及獨立標示的 CPI、真實版本漏斗、題材判斷與廣宣研發協作參考附件。">
<title>1012 顧問交流會｜會議紀錄與延伸參考附件</title><style>{css}</style></head>
<body><a class="skip" href="#minutes">跳至會議紀錄</a><div class="shell" id="top">
<header class="hero"><div class="eyebrow">CONSULTANT EXCHANGE · MEETING NOTES</div>
<h1>1012 顧問交流會</h1><p>二合遊戲的立項、買量、玩家體驗與商業化。<br>保留會議脈絡，另附可回查的工作流與操作參考。</p>
<div class="hero-meta"><span>會議日期：10 月 12 日（年份未確認）</span><span>錄音：約 1 小時 29 分</span><span>整理：2026-10-13</span></div>
<div class="quick"><a href="#minutes">閱讀會議紀錄</a><a href="#appendix-1">查看階段工作流</a><a href="#appendix-2">CPI／題材判斷</a><a href="#appendix-3">廣宣 × 研發協作</a></div></header>
<div class="layout"><aside class="sidebar" aria-label="文件目錄"><div class="sidebar-label">目錄 / CONTENTS</div><nav>{nav}</nav>
<div class="tools"><button type="button" id="print-button">列印／另存 PDF</button></div></aside>
<main class="main"><section class="paper" id="minutes" aria-labelledby="minutes-title">
<header class="part-head"><div class="part-label">PART 01 · 會議內容</div><h2 id="minutes-title">會議紀錄</h2><p>團隊回報、顧問意見、案例與未確認事項。</p></header>
<div class="source-note">本部分依原會議紀錄轉為 HTML，保留原有九個章節及錄音時間碼。數據為會中口述，假設與建議維持其原有性質；未加入外部建議或補定決議。來源檔案連結已改為同資料夾的有效路徑。</div>
<div class="meeting-content">{meeting_body}</div><a class="scroll-top" href="#top">回到目錄 ↑</a></section>
<section class="paper reference-paper" id="references" aria-labelledby="references-title">
<header class="part-head"><div class="part-label">PART 02 · 會後補充</div><h2 id="references-title">延伸參考附件</h2><p>相對階段工作流、判斷條件、協作分工、測試工具與參考來源。</p></header>
<div class="source-note"><strong>以下不是會中決議。</strong>「會議依據」回查逐字稿；「整理建議」為會後操作補充。比例為排程示意，算例為教學用途，外部資料另附官方連結。</div>
{appendix_body}<a class="scroll-top" href="#top">回到目錄 ↑</a></section>
<footer class="footer"><p>本檔案可離線閱讀；外部參考連結需要網路。列印時會移除目錄與操作列，參考附件另起新頁。</p>
<p>本地來源：<a href="1012顧問交流會_會議紀錄.md">原會議紀錄 Markdown</a> · <a href="1012顧問交流會_校正版.srt">校正版逐字稿 SRT</a> · <a href="1012顧問交流會_延伸參考附件.md">延伸參考附件 Markdown</a></p></footer>
</main></div></div><script>
document.getElementById('print-button').addEventListener('click',()=>window.print());
const links=[...document.querySelectorAll('.sidebar nav a')];
const observer=new IntersectionObserver(entries=>{{for(const entry of entries){{if(entry.isIntersecting){{for(const link of links){{link.classList.toggle('active',link.hash==='#'+entry.target.id);}}}}}}}},{{rootMargin:'-5% 0px -72% 0px',threshold:0}});
for(const heading of document.querySelectorAll('.main h2[id]')) observer.observe(heading);
</script></body></html>'''
output_path.write_text(html, encoding='utf-8')
ids = re.findall(r'id="([^"]+)"', html)
targets = re.findall(r'href="#([^"]+)"', html)
assert len(ids) == len(set(ids)), 'Duplicate HTML IDs'
assert all(target in ids for target in targets), 'Broken document anchors'
assert '\ufffd' not in html, 'Invalid character replacement'
for link in re.findall(r'href="([^"]+)"', html):
    if not link.startswith(('#', 'https:')):
        assert (ROOT / link).is_file(), f'Broken local link: {link}'
print(f'Created: {output_path}')
print(f'Minutes chapters: {len(meeting_heads)}; appendix sections: {len(appendix_heads)}; bytes: {output_path.stat().st_size}')
print('Verified anchors, unique IDs, encoding and local source links.')
