#!/usr/bin/env python3
"""校内の各場所に貼る「場所の説明板」signs.html を作る（A4縦・1か所1枚・全13枚）。
名前・番号・地区/階・説明文は docs/index.html の SPOTS（name / hint / msg）から取る。
絵は、その場所の絵文字（SPOTS の emoji）。写真があるときは stamp-rally/photos/place-<id>.jpg を置くと、写真に差し替わる
（<id> は s1, s2, s3, s4, s5, s6, s7, s8a, s8b, s9, s10, s11, s12）。
PDFにするときは、ブラウザの印刷で「PDFとして保存」（背景のグラフィックをオン）。使い方： python3 make_signs.py
"""
import re, json, pathlib

here = pathlib.Path(__file__).parent
src = (here.parent / "docs" / "index.html").read_text(encoding="utf8")
spots = re.search(r"const SPOTS = \[.*?\n\];", src, re.S).group(0)
ids = re.findall(r'\{ "?id"?: "(s\w+)"', spots)
photos = {}
for i in ids:
    for ext in ("jpg", "jpeg", "png", "webp"):
        f = here / "photos" / f"place-{i}.{ext}"
        if f.exists():
            photos[i] = f"photos/{f.name}"
            break

PAGE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>場所の説明板</title>
<style>
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; }
  body { margin: 0; color: #111; background: #fff; font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "Noto Sans JP", "Noto Sans CJK JP", "IPAexGothic", "IPAGothic", sans-serif; }
  .page { width: 210mm; height: 297mm; padding: 14mm 15mm 11mm; display: flex; flex-direction: column; gap: 8mm; page-break-after: always; break-after: page; overflow: hidden; }
  .head { flex: none; display: flex; align-items: center; gap: 9mm; }
  .no { flex: none; width: 36mm; height: 36mm; border-radius: 50%; background: #1f5a45; color: #fff; display: grid; place-items: center; font-size: 62pt; font-weight: 800; line-height: 1; }
  .ttl { min-width: 0; display: flex; flex-direction: column; gap: 4mm; }
  .name { font-weight: 800; line-height: 1.2; word-break: keep-all; }
  .where { align-self: flex-start; font-size: 22pt; font-weight: 700; color: #1f5a45; border: 2.5pt solid #1f5a45; border-radius: 99mm; padding: 1.5mm 8mm; }
  .pic { flex: 1; min-height: 0; border-radius: 6mm; background: #eef5f0; display: grid; place-items: center; overflow: hidden; }
  .pic .em { font-size: 150pt; line-height: 1; }
  .pic img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .desc { flex: none; font-size: 24pt; line-height: 1.75; word-break: auto-phrase; text-wrap: pretty; padding: 6mm 8mm; border: 2.5pt solid #1f5a45; border-radius: 5mm; background: #f6faf7; }
  .foot { flex: none; font-size: 12pt; color: #555; text-align: center; letter-spacing: .1em; }
</style></head><body>
<div id="root"></div>
<script>
__SPOTS__
const PHOTOS = __PHOTOS__;
const CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫";
document.getElementById("root").innerHTML = SPOTS.map(s => {
  const m = s.name.match(/^([①-⑫])\\s*(.*)$/);
  const no = CIRCLED.indexOf(m[1]) + 1, name = m[2], where = s.hint.split("｜")[0];
  const size = name.length <= 6 ? 50 : name.length <= 8 ? 42 : name.length <= 10 ? 34 : 30;   // 長い名前は小さくして、1行に収める
  const pic = PHOTOS[s.id] ? `<img src="${PHOTOS[s.id]}" alt="">` : `<span class="em">${s.emoji}</span>`;
  return `<section class="page">
  <div class="head"><div class="no">${no}</div><div class="ttl"><div class="name" style="font-size:${size}pt">${name}</div><div class="where">${where}</div></div></div>
  <div class="pic">${pic}</div>
  <div class="desc">${s.msg}</div>
  <div class="foot">駒澤大学高等学校</div>
</section>`;
}).join("");
</script></body></html>
"""
(here / "signs.html").write_text(PAGE.replace("__SPOTS__", spots).replace("__PHOTOS__", json.dumps(photos, ensure_ascii=False)), encoding="utf8")
print("signs.html を作りました（写真あり: %d か所）" % len(photos))
