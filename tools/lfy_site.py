"""Put 《拉法叶赋（并序）》 on the reading site.

Run in the site folder:  python3 tools/lfy_site.py
Reads 拉法叶赋/正文.md (序, 二十五段赋, 四行乱曰, one per line), 拉法叶赋/注.md
(27 notes, one per line, **key** marks the annotated words) and 拉法叶赋/致敬篇目.md,
writes txt/lfy-zh.html and the `lfy` entry in toc.json.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "拉法叶赋"

body = [l for l in (SRC / "正文.md").read_text().split("\n") if l.strip()]
notes = [l for l in (SRC / "注.md").read_text().split("\n") if l.strip()]
trib = [l for l in (SRC / "致敬篇目.md").read_text().split("\n") if l.strip()]
assert len(body) == 30, len(body)
assert len(notes) == 27, len(notes)

# note number -> body paragraphs it annotates (0 = 序, 1-25 = 赋, 26-29 = 乱曰)
ITEM = {1: [0], 2: [0], 3: [0], 4: [1], 5: [2], 6: [3], 7: [4], 8: [5], 9: [6], 10: [6],
        11: [7], 12: [8], 13: [9], 14: [10], 15: [11], 16: [12], 17: [13], 18: [14],
        19: [15], 20: [16], 21: [17], 22: [18], 23: [19, 20], 24: [21, 22], 25: [23],
        26: [24], 27: [29]}
after = {}
for n, ps in ITEM.items():
    after.setdefault(max(ps), []).append(n)


def inline(s):
    s = html.escape(s, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def aside(n):
    return f'<aside class="note"><p><span class="nl">注{n}</span> {inline(notes[n - 1])}</p></aside>'


out = ['<section class="note-preface"><h2>读前说明</h2>'
       '<p>注释二十七条，放在所注那一段后面的灰框里，按出现先后。只注生僻的典故和词，以及换了说法的现代事物。</p>'
       '<p>篇末另附致敬篇目：本赋取法、化用或反用的前人作品。</p></section>']
out.append("<h2>序</h2>")
for i, p in enumerate(body):
    if i == 1:
        out.append("<h2>赋</h2>")
    if i == 26:
        out.append("<blockquote>" + "".join(f"<p>{inline(x)}</p>" for x in body[26:30]) + "</blockquote>")
    if i < 26:
        out.append(f"<p>{inline(p)}</p>")
    for n in after.get(i, []):
        out.append(aside(n))

out.append("<h2>致敬篇目</h2>")
out.append(f"<p>{inline(trib[0])}</p>")
for l in trib[1:]:
    if l.startswith("# "):
        out.append(f"<h3>{inline(l[2:])}</h3>")
    else:
        w, rest = l.split("：", 1)
        out.append(f"<p><strong>{inline(w)}</strong>：{inline(rest)}</p>")

(ROOT / "txt" / "lfy-zh.html").write_text("\n".join(out) + "\n")

toc_path = ROOT / "toc.json"
toc = json.loads(toc_path.read_text())
entry = {"zh": "拉法叶赋", "title": "拉法叶赋（并序）",
         "desc": "骈赋一篇，写印第安纳州的拉法叶与西拉法叶：从三月写到来年二月，一月一宜，月与月之间写十一个在这里遇见的人。"}
new = {}
for k, v in toc.items():
    if k != "lfy":
        new[k] = v
    if k == "fh":
        new["lfy"] = entry
if "lfy" not in new:
    new["lfy"] = entry
toc_path.write_text(json.dumps(new, ensure_ascii=False, indent=1) + "\n")  # pretty-printed, like tools/huohou_site.py
print("wrote txt/lfy-zh.html and toc.json[lfy]")
