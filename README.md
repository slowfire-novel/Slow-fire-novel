# 阴燃 · The Slow Fire — reading site

A static site with no build step: `index.html` loads `toc.json` and the chapter fragments in `txt/` with `fetch`, and the figures from `img/`.

## Publish on GitHub Pages

1. Create a public repository (for example `slowfire`) and put the contents of this folder at its root, including the hidden `.nojekyll` file.
2. Commit and push to `main`.
3. In the repository: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
4. The site appears at `https://<username>.github.io/<repository>/` within a minute or two.

Notes for whoever publishes this:
- Do not rename or move `txt/`, `img/` or `toc.json`; the page fetches them by relative path.
- Opening `index.html` straight from disk (file://) will not load chapters, because browsers block `fetch` there. Test with a local server instead: `python3 -m http.server` in this folder, then open http://localhost:8000.
- Pages are addressed by hash, for example `#v1-01`, `#v2-44`, `#jx`, `#guide`, `#preface`, `#mag-2`, `#afterword`, `#rights`.
- The notes switch (注释) and language choice are remembered in the reader's browser via localStorage.
- Fonts come from Google Fonts; everything else is in this folder.

Contents: preface (zh/en); Volume One 《阴燃》 chapters 1–22 and Volume Two 《余烬》 23–44 (zh/en, with switchable notes on the Chinese); the sequel 《焦线》 (zh, with notes); the prequel 《封火》, annotated edition with 36 switchable notes (zh, `#fh`); 《拉法叶赋（并序）》, a 骈赋 on Lafayette and West Lafayette with 27 switchable notes and a list of the older works it borrows from (zh, `#lfy`); the side story 《燎原》, 15 chapters plus prologue and epilogue (zh, page ids `#ly-00` to `#ly-16`); the popular volume 《明火》, 17 chapters (zh, `#mh-01` to `#mh-17`); 《火德》 (《阴燃》外一种), title page and cast, 13 chapters, epilogue and the extra chapter 外一章 乡愿 (zh, `#hd-00` to `#hd-15`); 《火候》导读兼评, a reader's guide and critique to the novel 《火候》 (zh, `#hh`); 《阴燃》导读 (zh); *Second Look*, a fictional magazine companion (en); 火德 · 乐, the music written for 《火德》, a player page with its 34 recordings (`music/huode/`); and The Ground Keeps Us Warm, sketches toward a score for the main books: five drawn plates and sixteen further pieces, 21 recordings (`music/ground/`).

Also here: `essays/`, three standalone pages by the same author and AI: the benchmark report 人比AI更像AI with its attribution spectrum (Chinese and English, `essays/benchmark.html`) and its stand-up edition with attribution spectrum (`essays/standup-zh.html`, `essays/standup-en.html`). The home page links to them.

Also here: `火候/`, 《火候》 in its public 洁本 edition: 上部 (chapters 1–22) and 下部 (chapters 23–44 and the extra chapter 外一章 野地), each as an A5 PDF and as Markdown with its 44 figures, and the 例言. `火候/上部人物关系图.html` and `火候/下部人物关系图.html` are the character graphs of 上部 (56 people, 99 ties) and 下部 (73 people, 114 ties), self-contained pages. Both volumes are also on the reading site (`#huohou-00` to `#huohou-45`), beside the 火候 reader’s guide (`#hh`). The full text is available from the author on request.

Also here: `拉法叶赋/`, 《拉法叶赋（并序）》: the text (`正文.md`, one paragraph per line: 序, 25 paragraphs of 赋, 4 lines of 乱曰), the 27 notes (`注.md`), the list of works it borrows from (`致敬篇目.md`) and the A5 print edition (`拉法叶赋.pdf`, 23 pages). `tools/lfy_site.py` turns them into `txt/lfy-zh.html` and the `lfy` entry in `toc.json`: run `python3 tools/lfy_site.py` in this folder after any change there.

`tools/huohou_site.py` puts the 《火候》 clean edition on the reading site from `火候/`: run `python3 tools/huohou_site.py 火候` in this folder after any change to a chapter there. It writes `txt/huohou-NN-zh.html` and `img/huohou_NN_K.webp` and updates the `huohou` entry in `toc.json`.

## Rights

© 2026 李星光 (Li Xingguang). All rights reserved. 保留所有权利。This repository is public so that the books can be read; it is not open source. See [LICENSE.md](LICENSE.md). Requests go to [Issues](https://github.com/slowfire-novel/Slow-fire-novel/issues).

Where the rights statement lives, for whoever maintains this:
- The terms readers see are the `#rights` page: `txt/rights-zh.html` and `txt/rights-en.html`. `index.html` prints the © line under every page (`OWNER`, `YEAR` and `foot()` in its script) and links to that page from the contents rail.
- The standalone pages carry the © line by hand: the three in `essays/`, the two in `music/`, and the two character graphs in `火候/`. If one of them is rebuilt or re-exported, put the line and the three `<meta>` tags back.
- Every page has `<meta name="robots" content="noai, noimageai">` and `<meta name="tdm-reservation" content="1">`: an opt-out from AI training and from text and data mining that leaves search engines alone. These are requests; a crawler may ignore them.
- `robots.txt` names the AI-training crawlers. Crawlers read it only at the root of a host, so on a project site (`https://<name>.github.io/<repository>/`) it does nothing. It takes effect with a custom domain, or when a copy is placed in the account's root site repository (the one named `<name>.github.io`).
- The print-edition PDFs do not carry a copyright page yet; add one at their next rebuild.
