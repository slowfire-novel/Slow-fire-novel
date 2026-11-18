#!/usr/bin/env python3
"""Put a 《火候》 clean edition (洁本) on the Slow Fire reading site.

usage: python3 tools/huohou_site.py <edition-folder> [juan|-] [repo-root]
  <edition-folder>  a folder laid out like the GitHub edition, e.g. 火候/: chapters/NN_标题.md and figs/
  [juan]            the part name shown in the crumb; '-' or omitted: 上部（洁本） for 1–22, 下部（洁本） for 23 on
  [repo-root]       the site repository (default: the current folder)

Writes txt/huohou-NN-zh.html and img/huohou_NN_K.webp for every chapter in the folder, and adds or
replaces those chapters in toc.json under "huohou" ("hh" is the reader's guide, a separate page). Chapters already listed under other numbers are kept, so
上部 (1–22) and 下部 (23–45) can be added in either order. Run it again after any change to a chapter.

Chapter Markdown it understands (what the editions use): '# ' title; a 回目 couplet line right after
it; '**…**' alone on a line for a time heading; '![alt](path)' for a figure, followed by an '*图…*'
caption line, or the caption as the alt text (上部's way); '---' for a rule (the chapter notes of 上部 follow one); '>' for a quoted block; inline
*italic* and **bold**; everything else a plain paragraph. For 上部, 例言.md becomes page hh-00.
"""
import html, json, os, re, sys

KEY = 'huohou'   # page ids #huohou-NN; 'hh' is the reader's guide (《火候》导读兼评)
DESC = ('《阴燃》系列的一部长篇，世情小说。二〇四八年春节前后，成都一间茶铺的后屋和美国小城西拉法叶，隔着十三个钟头，'
        '十几户人家的吃饭、算账、男女和生死。上部从小年写到除夕，下部从正月初一写到十七，另有外一章。'
        '这是洁本：写男女之事的段落，到了那一步就收住；完整的本子可以向作者索取。')
NOTE = ('<p class="notice" style="text-align:left">这是洁本。完整的本子可以发邮件索取。<br/>'
        'This is the clean edition. The full text is available on request.<br/>'
        '<a href="mailto:frogfromyangzhou@gmail.com">frogfromyangzhou@gmail.com</a></p>\n')   # shown above the 例言
from PIL import Image

def inline(p):
    p = re.sub(r'\[([^\]]*)\]\{[^}]*\}', r'\1', p)            # pandoc spans such as [x]{.underline}
    p = re.sub(r'\\([\\`*_{}\[\]()#+\-.!~$^<>|"\'])', r'\1', p)   # markdown escapes
    p = html.escape(p.replace('\n', ''), quote=False)
    p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p)
    p = re.sub(r'\*(.+?)\*', r'<em>\1</em>', p)
    return p

def convert(md, n, figdir, imgdir):
    # split and trim on ASCII whitespace only: a paragraph of full-width spaces (　) is a deliberate blank, kept as <p>　</p>
    paras = [p.strip(' \t\r\n') for p in re.split(r'\n[ \t\r]*\n', md) if p.strip(' \t\r\n')]
    out, title, k, fig = [], None, 0, 0
    seen_head = False
    while k < len(paras):
        p = paras[k]
        if title is None and p.startswith('# '):
            title = p[2:].strip(); k += 1; continue
        if p.startswith('#'):
            raise SystemExit(f'{n}: unexpected heading {p[:40]}')
        m = re.match(r'^!\[(.*?)\]\((.*?)\)(\{.*?\})?$', p, re.S)
        if m:
            fig += 1
            src = os.path.normpath(os.path.join(figdir, '..', m.group(2))) if not os.path.isabs(m.group(2)) else m.group(2)
            if not os.path.exists(src):
                src = os.path.join(figdir, os.path.basename(m.group(2)))
            name = f'{KEY}_{n:02d}_{fig}.webp'
            im = Image.open(src).convert('RGB')
            if im.width > 1600:
                im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            im.save(os.path.join(imgdir, name), 'WEBP', quality=82, method=6)
            cap = ''
            if k + 1 < len(paras) and re.match(r'^\*图.*\*$', paras[k + 1]):
                cap = paras[k + 1].strip('*'); k += 1
            elif m.group(1).startswith('图'):
                cap = m.group(1)
            out.append(f'<figure><img alt="{html.escape(m.group(1))}" loading="lazy" src="img/{name}"/>'
                       + (f'<figcaption>{html.escape(cap)}</figcaption>' if cap else '') + '</figure>')
            k += 1; continue
        m = re.match(r'^\*\*([^*]+)\*\*$', p)
        if m:
            seen_head = True
            out.append(f'<h3>{html.escape(m.group(1))}</h3>'); k += 1; continue
        if not seen_head and not out and re.match(r'^[^\s　，。？！：“”*]{3,14}　[^\s　，。？！：“”*]{3,14}$', p):
            out.append(f'<p class="huimu">{html.escape(p)}</p>'); k += 1; continue
        if re.match(r'^-{3,}$', p):
            out.append('<hr/>'); k += 1; continue
        if p.startswith('>'):
            lines = [re.sub(r'^>\s?', '', l) for l in p.split('\n')]
            out.append('<blockquote>' + ''.join(f'<p>{inline(l)}</p>' for l in lines if l.strip()) + '</blockquote>'); k += 1; continue
        out.append(f'<p>{inline(p)}</p>'); k += 1
    return title, '\n'.join(out) + '\n'

def main():
    folder = sys.argv[1]
    juan = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '-' else None
    root = sys.argv[3] if len(sys.argv) > 3 else '.'
    chdir, figdir = os.path.join(folder, 'chapters'), os.path.join(folder, 'figs')
    os.makedirs(os.path.join(root, 'txt'), exist_ok=True)
    os.makedirs(os.path.join(root, 'img'), exist_ok=True)
    tocp = os.path.join(root, 'toc.json')
    toc = json.load(open(tocp, encoding='utf-8'))
    hh = toc.get(KEY) or {'zh': '火候', 'desc': DESC, 'parts': []}
    hh['desc'] = hh.get('desc') or DESC
    parts = {c['n']: c for c in hh['parts']}
    for f in sorted(os.listdir(chdir)):
        m = re.match(r'^(\d+)_.*\.md$', f)
        if not m: continue
        n = int(m.group(1))
        title, body = convert(open(os.path.join(chdir, f), encoding='utf-8').read(), n, figdir, os.path.join(root, 'img'))
        open(os.path.join(root, 'txt', f'{KEY}-{n:02d}-zh.html'), 'w', encoding='utf-8').write(body)
        part = {'n': n, 'zh': title, 'juan': juan or ('上部（洁本）' if n <= 22 else '下部（洁本）')}
        if title.startswith('外'):
            part['k'] = '外'
        parts[n] = part
        print(f'{KEY}-{n:02d}', title)
    liyan = os.path.join(folder, '例言.md')
    if any(c <= 22 for c in parts) and os.path.exists(liyan):
        title, body = convert(open(liyan, encoding='utf-8').read(), 0, figdir, os.path.join(root, 'img'))
        open(os.path.join(root, 'txt', f'{KEY}-00-zh.html'), 'w', encoding='utf-8').write(NOTE + body)
        parts[0] = {'n': 0, 'zh': title or '例言', 'juan': '上部（洁本）', 'k': '例'}
        print(f'{KEY}-00', title)
    hh['parts'] = [parts[n] for n in sorted(parts)]
    toc[KEY] = hh
    open(tocp, 'w', encoding='utf-8').write(json.dumps(toc, ensure_ascii=False, indent=1) + '\n')  # the repo keeps it pretty-printed
    print(f'toc.json: {KEY} has', len(hh['parts']), 'parts')

if __name__ == '__main__':
    main()
