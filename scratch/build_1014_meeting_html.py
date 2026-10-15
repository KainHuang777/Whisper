from pathlib import Path
from html import escape
import hashlib
import re
import markdown

ROOT = Path(__file__).resolve().parents[1]
minutes_path = ROOT / '1014顧問交流會_會議紀錄.md'
appendix_path = ROOT / '1014顧問交流會_延伸研究附錄.md'
output_path = ROOT / '1014顧問交流會_會議紀錄與延伸研究.html'
original_hash = hashlib.sha256(minutes_path.read_bytes()).hexdigest()
minutes = minutes_path.read_text(encoding='utf-8-sig')
minutes = minutes.replace('D:/work/非目前專案調研/Whisper/data/output/1014顧問交流會_校正版.srt',
                          'data/output/1014顧問交流會_校正版.srt')
appendix = appendix_path.read_text(encoding='utf-8-sig')
appendix = appendix.replace('D:/work/非目前專案調研/Whisper/data/output/1014顧問交流會_校正版.srt',
                            'data/output/1014顧問交流會_校正版.srt')
appendix = appendix.replace('D:/work/非目前專案調研/Whisper/1012顧問交流會_校正版.srt',
                            '1012顧問交流會_校正版.srt')

def convert(source, prefix):
    source = re.sub(r'^# .+\n', '', source, count=1)
    body = markdown.markdown(source, extensions=['tables', 'sane_lists'])
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

meeting_body, meeting_headings = convert(minutes, 'meeting')
appendix_body, appendix_headings = convert(appendix, 'appendix')
nav = '<a class="nav-part" href="#minutes">01　會議紀錄</a>'
nav += ''.join(f'<a href="#{anchor}">{escape(title)}</a>' for anchor, title in meeting_headings)
nav += '<a class="nav-part ref" href="#research">02　延伸研究附錄</a>'
nav += ''.join(f'<a href="#{anchor}">{escape(title)}</a>' for anchor, title in appendix_headings)

existing = (ROOT / '1012顧問交流會_會議紀錄與參考附件.html').read_text(encoding='utf-8')
css = re.search(r'<style>(.*?)</style>', existing, flags=re.S).group(1)
css += '''
.conclusion{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin:24px 0 34px}.conclusion>div{border-top:2px solid #bd955d;padding-top:14px}.conclusion .value{display:block;font-size:27px;line-height:1.3;font-weight:700;color:#795727}.conclusion strong{display:block;font-size:15px;margin:8px 0 5px}.conclusion small{display:block;color:var(--muted);font-size:13px;line-height:1.7}.source-note a{color:inherit}.toc summary{font-size:14px;font-weight:700;color:var(--ink);padding:8px 0;cursor:pointer}.toc[open] summary{margin-bottom:8px}blockquote{margin:24px 0;padding:16px 22px;border-left:4px solid #a37a43;background:#faf6ef;color:#55422e}blockquote p{margin:4px 0}.mix-lab{background:#f5f0e7;padding:22px;margin:24px 0;border-radius:4px}.mix-lab h4{font-size:17px;margin:0 0 8px}.mix-lab .demo-note{font-size:13px;color:#705127;margin:0 0 16px}.mix-labels{display:flex;justify-content:space-between;gap:18px;font-size:14px}.mix-lab input{width:100%;margin:18px 0;accent-color:#946b35}.mix-value{display:flex;gap:18px;align-items:baseline;flex-wrap:wrap;margin-top:8px}.mix-value output{font-size:36px;line-height:1.5;font-weight:700;color:#795727}.mix-track{display:flex;height:14px;margin:10px 0 16px;background:#ddd4c5;overflow:hidden}.mix-track span:first-child{background:#a37a43}.mix-track span:last-child{background:#74899c}.mix-lab .formula{font-size:13px;color:#465568;line-height:1.8}.mix-lab .presets{display:flex;gap:10px;flex-wrap:wrap}.mix-lab .presets button{background:transparent;border-color:#b4a58f;color:#654d2c}.mix-print{display:none}.comparison-intro{margin:0 0 28px}.comparison-intro p{font-size:15px}.hero-meta a{color:inherit}.evidence-label{color:#8b612c;font-size:13px;font-weight:bold;letter-spacing:.08em}@media(max-width:600px){.conclusion{grid-template-columns:1fr;gap:18px}.conclusion .value{font-size:24px}.mix-lab{padding:18px}.mix-labels{flex-direction:column;gap:6px}}@media print{.conclusion{grid-template-columns:repeat(3,minmax(0,1fr));break-inside:avoid}.conclusion .value{font-size:16pt}.mix-lab{break-inside:avoid;border:1px solid #ddd}.mix-interactive{display:none}.mix-print{display:block}.mix-value output{font-size:20pt}blockquote{background:none}}
'''

summary = '''<div class="comparison-intro"><div class="evidence-label">綜合判讀 · 接受跳過現象，改善內容與承接</div>
<div class="conclusion"><div><span class="value">高 CG 跳過</span><strong>1012 的專案經驗</strong><small>顧問未提供具體百分比；以內容品質、產品需要與改動結果判斷取捨。</small></div>
<div><span class="value">約七成</span><strong>1014 的劇情案例</strong><small>顧問認為泛用戶跳過並不罕見，仍指出我方開場鋪墊與目標可改善。</small></div>
<div><span class="value">優化承接</span><strong>兩場方向相容</strong><small>我方約六成作情境判讀；加強 CG、開頭鉤子與目標，以後續體驗驗證。</small></div></div></div>'''

html = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="1014 顧問交流會會議紀錄，附獨立標示的劇情跳過率、獲客客群與專案指標取捨延伸研究。">
<title>1014 顧問交流會｜會議紀錄與延伸研究</title><style>{css}</style></head><body>
<a class="skip" href="#minutes">跳至會議紀錄</a><div class="shell" id="top"><header class="hero">
<div class="eyebrow">CONSULTANT EXCHANGE · OCTOBER 14</div><h1>1014 顧問交流會</h1>
<p>會議紀錄與延伸研究<br>從劇情跳過率，回看獲客客群、產品承接與回收指標的取捨。</p>
<div class="hero-meta"><span>錄音：1 小時 27 分 39 秒</span><span>會議紀錄：16 個章節</span><span>附錄研究：2026-10-15</span></div>
<div class="quick"><a href="#minutes">原會議紀錄</a><a href="#research">附錄與共同觀點</a><a href="#appendix-2">CG／鉤子與承接改善</a><a href="#appendix-3">如何驗證</a><a href="#appendix-4">階段與指標取捨</a></div></header>
<div class="layout"><aside class="sidebar" aria-label="文件目錄"><details class="toc" id="contents" open><summary>章節目錄 / CONTENTS</summary><nav>{nav}</nav></details>
<div class="tools"><button id="print-button" type="button">列印／另存 PDF</button></div></aside><main class="main">
<section class="paper" id="minutes" aria-labelledby="minutes-title"><header class="part-head"><div class="part-label">PART 01 · 會議直接紀錄</div>
<h2 id="minutes-title">1014 會議紀錄</h2><p>保留原 Markdown 的 16 章、來源時間碼與意見性質。</p></header>
<div class="source-note">本部分由既有 <a href="1014顧問交流會_會議紀錄.md">1014 會議紀錄 Markdown</a> 轉為 HTML。跨場次比較、研究假設與外部方法均置於後方附錄，不補入會議正文。</div>
<div class="meeting-content">{meeting_body}</div><a class="scroll-top" href="#top">回到頁首 ↑</a></section>
<section class="paper reference-paper" id="research" aria-labelledby="research-title"><header class="part-head"><div class="part-label">PART 02 · 延伸研究，非會議直接紀錄</div>
<h2 id="research-title">劇情跳過率、內容改善與指標取捨</h2><p>兩場共同方向、CG 與鉤子改善、目標承接及驗證方案。</p></header>
<div class="source-note"><strong>以下屬於會議內容的延伸研究，非會議中直接紀錄的內容。</strong> 顧問原文、綜合判讀與改善提案分開標示；約六成的情境分析不是顧問共同訂定的數值標準，也不代表團隊決議。</div>
{summary}{appendix_body}<a class="scroll-top" href="#top">回到頁首 ↑</a></section>
<footer class="footer"><p>本檔可離線閱讀；外部官方參考連結需要網路。列印時附錄另起新頁。</p>
<p>檔案：<a href="1014顧問交流會_會議紀錄.md">會議紀錄 Markdown</a> · <a href="1014顧問交流會_延伸研究附錄.md">延伸研究 Markdown</a> · <a href="data/output/1014顧問交流會_校正版.srt">1014 逐字稿</a> · <a href="1012顧問交流會_校正版.srt">1012 逐字稿</a> · <a href="1012顧問交流會_會議紀錄與參考附件.html">1012 HTML</a></p></footer>
</main></div></div><script>
document.getElementById('print-button').addEventListener('click',()=>window.print());
if(window.matchMedia('(max-width:820px)').matches) document.getElementById('contents').open=false;
const navLinks=[...document.querySelectorAll('.sidebar nav a')];
const observer=new IntersectionObserver(entries=>{{for(const entry of entries)if(entry.isIntersecting)for(const link of navLinks)link.classList.toggle('active',link.hash==='#'+entry.target.id);}},{{rootMargin:'-5% 0px -72% 0px'}});
for(const heading of document.querySelectorAll('.main h2[id]')) observer.observe(heading);
</script></body></html>'''

ids = re.findall(r'id="([^"]+)"', html)
assert len(ids) == len(set(ids)), 'Duplicate IDs'
assert all(target in ids for target in re.findall(r'href="#([^"]+)"', html)), 'Broken anchors'
for target in re.findall(r'href="([^"]+)"', html):
    if not target.startswith(('#', 'https:')):
        assert (ROOT / target).is_file(), f'Broken local link: {target}'
assert '\ufffd' not in html, 'Invalid encoding replacement'
assert hashlib.sha256(minutes_path.read_bytes()).hexdigest() == original_hash, 'Minutes were changed'
assert len(meeting_headings) == 16 and len(appendix_headings) == 6
assert not re.search(r'40[%％]|四十|四成', appendix_body + summary), 'Obsolete comparison remains in appendix'
output_path.write_text(html, encoding='utf-8')
print(f'HTML bytes: {output_path.stat().st_size}; meeting chapters: 16; research sections: 6')
print('Verified: source minutes unchanged, local links, anchors, IDs, UTF-8.')
