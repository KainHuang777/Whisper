from pathlib import Path
import html
import re

import markdown


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '1012-1014顧問交流會_專案週報_PPT三頁內容.md'
OUTPUT = ROOT / '1012-1014顧問交流會_專案週報.html'
text = SOURCE.read_text(encoding='utf-8')
parts = re.findall(
    r'## 第 (\d) 頁｜[^\n]+\n(.*?)(?=\n## 第 |\n## 來源註記)',
    text,
    re.S,
)
assert len(parts) == 3


def render_md(content):
    # Relative links let the HTML travel together with the source documents.
    content = content.replace('D:/work/非目前專案調研/Whisper/', '')
    result = markdown.markdown(content, extensions=['tables', 'sane_lists'])
    return result.replace('<table>', '<div class="table-scroll" tabindex="0"><table>').replace(
        '</table>', '</table></div>'
    )


sections = []
themes = ['signal', 'verify', 'action']
for (number, content), theme in zip(parts, themes):
    concise = re.search(r'```text\n(.*?)\n```', content, re.S).group(1).splitlines()
    title = concise[0]
    points = [line[2:] for line in concise[1:] if line.startswith('- ')]
    assert len(points) <= 4
    assert all(len(line) <= 10 for line in concise)
    explanation = content.split('### MD 詳細說明', 1)[1].strip()
    explanation = re.sub(r'\n---\s*$', '', explanation)
    cards = ''.join(
        f'<li><span class="point-number" aria-hidden="true">0{i}</span>'
        f'<span class="point-text">{html.escape(point)}</span></li>'
        for i, point in enumerate(points, 1)
    )
    sections.append(f'''
<section class="report-section {theme}" id="page-{number}" aria-labelledby="title-{number}">
  <article class="slide">
    <div class="slide-heading"><h2 id="title-{number}">{html.escape(title)}</h2><span class="page-number">0{number} / 03</span></div>
    <ul class="points">{cards}</ul>
    <div class="slide-rule" aria-hidden="true"></div>
  </article>
  <details class="notes"><summary>展開完整說明<span aria-hidden="true">＋</span></summary>
    <div class="notes-body">{render_md(explanation)}</div>
  </details>
</section>''')

source_note = render_md(text.split('## 來源註記（MD／講者備註）', 1)[1].strip())
style = '''
:root{--paper:#fffefa;--bg:#eeeae2;--ink:#182d33;--muted:#59676a;--line:#d8ded9;--accent:#226b59}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:84px}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Microsoft JhengHei","PingFang TC",sans-serif;line-height:1.8}a{color:var(--accent);text-underline-offset:4px}button,summary,a{touch-action:manipulation}button:focus-visible,summary:focus-visible,a:focus-visible,.table-scroll:focus-visible{outline:3px solid #ac6e19;outline-offset:4px}
.site-header{max-width:1160px;margin:auto;padding:48px 20px 24px;display:flex;align-items:end;justify-content:space-between;gap:24px}.kicker{font-size:12px;letter-spacing:.16em;color:var(--muted)}h1{margin:7px 0 8px;font-size:32px;letter-spacing:.04em;line-height:1.35}.meta{display:flex;gap:8px 20px;flex-wrap:wrap;font-size:13px;color:var(--muted)}.toolbar{display:flex;flex-wrap:wrap;gap:8px}button{font:inherit;font-size:13px;background:transparent;border:1px solid #aab6ae;border-radius:5px;padding:8px 14px;color:var(--ink);cursor:pointer}button:hover{background:#e0e5dd}.print-button{background:var(--ink);border-color:var(--ink);color:white}.print-button:hover{background:#2b4850}
.navigation{position:sticky;top:0;z-index:10;background:#eeeae2f5;border-bottom:1px solid #d4d8cf;backdrop-filter:blur(8px)}.nav-inner{max-width:1120px;margin:auto;display:flex;gap:28px;padding:13px 20px}.nav-inner a{text-decoration:none;color:var(--muted);font-size:14px}.nav-inner a:hover{color:var(--accent)}main{max-width:1160px;margin:auto;padding:28px 20px 56px}.report-section{margin-bottom:32px;--accent:#226b59}.verify{--accent:#916225}.action{--accent:#355b89}
.slide{width:100%;min-width:0;background:var(--paper);padding:44px 56px 38px;aspect-ratio:16/9;min-height:490px;display:flex;flex-direction:column;border:1px solid #dfe1d7;border-radius:8px 8px 0 0;box-shadow:0 8px 24px #28352a06}.slide-heading{display:flex;justify-content:space-between;align-items:center;padding-bottom:22px;border-bottom:1px solid var(--line)}h2{font-size:clamp(30px,3.2vw,44px);letter-spacing:.12em;line-height:1.4;margin:0;color:var(--ink)}.page-number{color:var(--accent);font-size:14px;letter-spacing:.1em}.points{padding:0;margin:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:0 48px;flex:1;align-content:center}.points li{display:flex;gap:15px;align-items:center;padding:32px 0;border-bottom:1px solid var(--line);min-width:0}.point-number{font-size:14px;letter-spacing:.04em;color:var(--accent);flex-shrink:0}.point-text{font-size:clamp(21px,2.35vw,30px);font-weight:700;letter-spacing:.015em;white-space:nowrap;line-height:1.5}.slide-rule{height:4px;width:48px;background:var(--accent);margin-top:26px}
.notes{background:#f9f8f3;border:1px solid #dfe1d7;border-top:0;border-radius:0 0 8px 8px}.notes summary{padding:15px 24px;font-size:14px;cursor:pointer;list-style:none;color:var(--muted);display:flex;justify-content:space-between;align-items:center}.notes summary::-webkit-details-marker{display:none}.notes summary span{font-size:20px;color:var(--accent);transition:transform .15s}.notes[open] summary{border-bottom:1px solid var(--line);color:var(--accent)}.notes[open] summary span{transform:rotate(45deg)}.notes-body{padding:18px 32px 28px;font-size:15px;overflow-wrap:anywhere}.notes-body>p:first-child{margin-top:0}.notes-body h4{font-size:17px;margin:26px 0 10px}.notes-body li{margin:9px 0}.table-scroll{overflow-x:auto;margin:22px 0;border:1px solid var(--line);border-radius:4px}table{border-collapse:collapse;width:100%;min-width:620px;font-size:14px;line-height:1.8;text-align:left}th,td{padding:13px 16px;vertical-align:top;border-bottom:1px solid var(--line)}th{background:#edf1e9;font-weight:700}tr:last-child td{border-bottom:0}.sources{border-top:1px solid #cfd6cc;margin-top:40px;padding-top:20px;color:var(--muted);font-size:13px}.sources h3{font-size:14px;margin:0 0 12px}.sources p{margin:10px 0}.status{font-size:12px;color:var(--muted);margin:10px 0 0}.skip{position:absolute;left:-9999px}.skip:focus{left:20px;top:12px;background:white;padding:8px;z-index:20}
@media(max-width:950px){.slide{padding:30px 34px;min-height:430px}.points{column-gap:28px}.points li{gap:10px}.point-text{font-size:24px}}
@media(max-width:700px){.site-header{padding:28px 18px 20px;display:block}h1{font-size:28px}.toolbar{margin-top:18px}.nav-inner{justify-content:space-between;gap:8px;padding:12px 18px}main{padding:20px 12px 36px}.slide{aspect-ratio:auto;min-height:0;padding:26px 24px}.slide-heading{padding-bottom:20px}h2{font-size:30px}.points{grid-template-columns:1fr}.points li{padding:23px 0;gap:17px}.point-text{font-size:clamp(18px,5.3vw,27px)}.notes-body{padding:18px}.notes summary{padding:13px 20px}.report-section{margin-bottom:24px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.notes summary span{transition:none}}
@media print{@page{size:A4 landscape;margin:10mm}html{scroll-padding-top:0}body{background:white;print-color-adjust:exact;-webkit-print-color-adjust:exact}.site-header,.navigation,.notes,.sources,.skip{display:none!important}main{max-width:none;padding:0;margin:0}.report-section{margin:0;break-after:page;page-break-after:always}.report-section:last-of-type{break-after:auto;page-break-after:auto}.slide{width:100%;height:188mm;min-height:0;aspect-ratio:auto;padding:15mm 17mm;border:0;border-radius:0;box-shadow:none;break-inside:avoid}.slide-heading{padding-bottom:10mm}h2{font-size:30pt}.page-number{font-size:11pt}.points{grid-template-columns:1fr 1fr;column-gap:16mm}.points li{padding:12mm 0;gap:5mm}.point-text{font-size:21pt;white-space:nowrap}.point-number{font-size:11pt}.slide-rule{margin-top:8mm}}
'''
page = '''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="10/12 與 10/14 顧問交流週報：核心結論、風險驗證與下期建議，附完整說明。">
<title>1012／1014 顧問交流週報</title><style>''' + style + '''</style></head><body>
<a href="#report" class="skip">跳至週報</a>
<header class="site-header"><div><div class="kicker">WEEKLY REPORT · 2026</div><h1>顧問交流週報</h1>
<div class="meta"><span>會議 10/12、10/14</span><span>整理 2026/10/15</span><span>二合遊戲專案</span></div></div>
<div class="toolbar"><button type="button" id="toggle-notes" aria-controls="report" aria-expanded="false">展開所有說明</button><button type="button" class="print-button" id="print-report">列印精簡版</button></div></header>
<nav class="navigation" aria-label="週報導覽"><div class="nav-inner"><a href="#page-1">01 核心結論</a><a href="#page-2">02 風險驗證</a><a href="#page-3">03 下期建議</a></div></nav>
<main id="report">''' + ''.join(sections) + '''
<footer class="sources"><h3>資料與說明</h3><p>各頁重點維持每行不超過 10 字、每頁最多四項；完整說明可展開閱讀。列印精簡版僅輸出三頁重點。</p>
<p>團隊回報、後續計畫與顧問建議依原紀錄區分；行動優先級為週報整理建議，尚未核定排期。</p>''' + source_note + '''
<p><a href="1012-1014顧問交流會_專案週報_PPT三頁內容.md">週報 Markdown 原稿</a></p></footer></main>
<script>
const notes = [...document.querySelectorAll('.notes')];
const toggle = document.getElementById('toggle-notes');
function syncToggle(){const allOpen=notes.every(note=>note.open);toggle.textContent=allOpen?'收合所有說明':'展開所有說明';toggle.setAttribute('aria-expanded',String(allOpen));}
toggle.addEventListener('click',()=>{const open=!notes.every(note=>note.open);notes.forEach(note=>note.open=open);syncToggle();});
notes.forEach(note=>note.addEventListener('toggle',syncToggle));
document.getElementById('print-report').addEventListener('click',()=>window.print());
</script></body></html>'''
OUTPUT.write_text(page, encoding='utf-8')
print(f'Created {OUTPUT.name}; {len(parts)} pages; 4 points per page; full notes preserved.')
