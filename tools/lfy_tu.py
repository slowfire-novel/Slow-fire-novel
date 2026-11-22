"""Gallery page for 《拉法叶赋》: twelve months and eleven people, in the order of the 赋.

Run in the site folder:  python3 tools/lfy_tu.py
Images: img/lfy_mNN.webp (months, NN = 01..12) and img/lfy_pNN.webp (people, 00..10).
Every caption is a phrase from 拉法叶赋/正文.md; the script checks that it is still there.
Writes txt/lfytu-zh.html and the `lfytu` entry in toc.json (right after `lfy`).
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
body = re.sub(r"\*\*", "", (ROOT / "拉法叶赋" / "正文.md").read_text())

# (month heading, month image, alt, caption from the 赋, person or None)
# person = (image, name, alt, caption from the 赋)
ROWS = [
    ("三月宜草", "m03", "返青的冬小麦田，河边枯白的芦苇梢上站着一只红翅黑鹂，浅水里薄冰正化",
     "宿麦先青，一夜遍野；枯苇犹白，赤羽已鸣。", None),
    ("四月宜花", "m04", "河岸上紫荆开满老枝，河滩铺满蓝色的弗吉尼亚蓝钟花",
     "紫荆夹岸，花不待叶，簇于老干，若绛霜之凝铁；蓝钟铺滩，色欲夺波",
     ("p00", "越栏之女", "清晨的跑道上，一个卷发的年轻女子正腾身跨过栏架",
      "及其腾身越栏，翩若惊鸿，落地而几无声。")),
    ("五月宜树", "m05", "河边林荫古道，大树新叶浓密，远处有散步和骑车的人",
     "群木交柯，清润无暑；白昼既永，林间至晚，犹留微光。",
     ("p01", "操棹之女", "薄雾的河上，赛艇靠在木码头边，金红头发的女子肩扛一支桨走上码头",
      "及其登岸，行不视足，亦不顾人之视己")),
    ("六月宜雨", "m06", "平野上雷雨刚过，远处云底一道闪电，夕阳下土路冒着水汽",
     "雷自西原殷殷而至，电先掣于天际，雨继注于田畴",
     ("p02", "讲问之人", "朴素的小礼堂里，一个戴眼镜的中年男子站在木讲台后，抬手向台下发问",
      "七日一登堂，只讲一字曰“问”，微言义长。")),
    ("七月宜水", "m07", "清浅的溪水两岸树木浓绿，水上漂着独木舟和轮胎浮圈，远处一座低桥",
     "蒂川之上，浮圈相属；狸溪之中，独木相衔。",
     ("p03", "华女", "溪边，一个眼镜推在头顶的年轻女子笑着拧湿头发",
      "覆舟于狸溪，攀岸而上，拧发复跃入清漪")),
    ("八月宜菌", "m08", "林下倒木上叠生橙黄的硫磺菌，落叶间有靛蓝乳菇、白色鹅膏和金黄的鸡油菌",
     "透雨既过三日，地气蒸郁，蕈花戢戢而竞滋。",
     ("p04", "攀壁之女", "体育馆攀岩墙下，一个黑色卷发的年轻女子仰头看墙顶的人，笑了",
      "及有人初登其顶，乃莞尔一笑：深色之中，皓齿一闪")),
    ("九月宜毬", "m09", "清晨的高尔夫球场，草坪平整挂露，球道边野花丛，远处一个独自打球的人",
     "天高至此而极，草芟平如铺毡。",
     ("p05", "天竺少年", "晴天的网球场上，一个卷发青年正在发球",
      "发毬之际，通体如绳之急绞，忽焉而释，势若弧张。")),
    ("十月宜览", "m10", "河岸满林红黄，草地上帆布帐篷连成一片，穿旧式衣服的人生火做饭",
     "河畔古堡有市，人效三百年前之法，生火而炊，竟日盘桓",
     ("p06", "歌女", "老砖楼改成的小剧场里，一个头巾松松搭着的年轻女子对着麦克风唱歌，台下人听得出神",
      "头巾或裹或否，曰视天色，亦视心情。")),
    ("十一月宜写", "m11", "收割后的田边土路上停着一辆熄了灯的车，一个人倚车仰望满天星斗",
     "人多驱车而南，熄其灯，倚车而仰星辰，星汉若乘槎可近。",
     ("p07", "营造少年", "深夜的建筑系工作室，戴细边眼镜的青年在台灯下把笔一支支插回笔筒",
      "及至寅初，一一插笔还筒，而后灯灭，静敛其光。")),
    ("十二月宜聚", "m12", "冬夜的红砖老火车站，窗里透出暖光，散场的人站在门外路灯下说笑",
     "既散，犹恋恋不去，灯下呵气成团。",
     ("p08", "当垆之女", "冬夜小餐馆的热菜柜台后，一个年轻女子拿着大勺笑着问客人，柜台外排着队",
      "凡至其前者，无论男女，必视其目而问：“更益一勺否？”")),
    ("一月宜睡", "m01", "冬日清晨，薄霜下的黑麦田仍泛着绿，雾气漫过沼泽，远处农舍",
     "暖岁则重阴多雾，湿气漫野，苔草滋蔓",
     ("p09", "袒跑少年", "天未亮的雪坡上，一个肩背宽厚的青年赤着上身奔跑，身上冒着白气",
      "雪落其肩，不能栖止，化为白气，曳于身后而霏微。")),
    ("二月宜雪", "m02", "大雪后的校园小坡上，人们坐着雪橇滑下，坡下一辆亮着黄灯的铲雪车",
     "童子之橇，磨西坡光可鉴人；不待昧晨，辟雪之车，灯烛县道而驰轮。",
     ("p10", "红发之女", "雪中的街道上，一个红发碧眼的小个子女子回头一望，背包上挂着一串铜色小零件",
      "回首顾盼，恍若荷兰旧画明珠之女")),
]

for row in ROWS:
    caps = [row[3]] + ([row[4][3]] if row[4] else [])
    for c in caps:
        assert c in body, f"caption not in the 赋: {c}"


def fig(img, alt, cap):
    return (f'<figure><img alt="{html.escape(alt)}" loading="lazy" src="img/lfy_{img}.webp"/>'
            f'<figcaption>{html.escape(cap, quote=False)}</figcaption></figure>')


def end(c):
    return c if c[-1] in "。”？" else c + "……"


out = ['<p>二十三张图，照赋的次序排：三月到二月，每月一景；四月起，每月再配一人。'
       '图下所引，都是赋中写这一景、这一人的句子。'
       '图是 AI 照赋中的文字生成的写实图像：景用 Gemini；人物 Gemini、Qwen 各出一版，由作者选定。'
       '人物的面貌都是虚构的，不对应任何真人。</p>']
for month, mimg, malt, mcap, person in ROWS:
    out.append(f"<h2>{month}</h2>")
    out.append(fig(mimg, f"{month[:-2]}：{malt}", end(mcap)))
    if person:
        pimg, name, palt, pcap = person
        out.append(fig(pimg, f"{name}：{palt}", f"{name}　{end(pcap)}"))

(ROOT / "txt" / "lfytu-zh.html").write_text("\n".join(out) + "\n")

toc_path = ROOT / "toc.json"
toc = json.loads(toc_path.read_text())
entry = {"zh": "拉法叶赋·图", "title": "拉法叶赋·图",
         "desc": "《拉法叶赋》的配图二十三张：十二个月的景，十一个人，照赋的次序排，图下引赋中原句。"}
new = {}
for k, v in toc.items():
    if k != "lfytu":
        new[k] = v
    if k == "lfy":
        new["lfytu"] = entry
toc_path.write_text(json.dumps(new, ensure_ascii=False, indent=1) + "\n")
print("wrote txt/lfytu-zh.html and toc.json[lfytu]")
