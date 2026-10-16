#!/usr/bin/env python3
"""校内の各場所に貼る「場所の表示板」signs.html を作る（A4縦・1か所1枚）。
場所の名前・番号・地区/階は docs/index.html の SPOTS から取る。PDFにするときは、ブラウザの印刷で「PDFとして保存」
（背景のグラフィックをオン）。使い方： python3 make_signs.py
"""
import re, pathlib

here = pathlib.Path(__file__).parent
src = (here.parent / "docs" / "index.html").read_text(encoding="utf8")
spots = re.search(r"const SPOTS = \[.*?\n\];", src, re.S).group(0)

PAGE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>校内クイズ探検 場所の表示板</title>
<style>
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; }
  body { margin: 0; color: #111; background: #fff; font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "Noto Sans JP", "Noto Sans CJK JP", "IPAexGothic", "IPAGothic", sans-serif; }
  .page { width: 210mm; height: 297mm; padding: 12mm 14mm; display: flex; flex-direction: column; gap: 10mm; page-break-after: always; break-after: page; overflow: hidden; }
  .photo { flex: none; height: 78mm; border-radius: 6mm; color: #fff; display: flex; flex-direction: column; justify-content: flex-end; padding: 6mm 8mm; text-shadow: 0 0 4mm rgba(0, 0, 0, .6);
    background: linear-gradient(180deg, rgba(0, 0, 0, 0) 35%, rgba(0, 0, 0, .7)), url("../docs/hero.jpg") center 45% / cover #1f5a45; }
  .photo .school { font-size: 14pt; font-weight: 700; letter-spacing: .1em; }
  .photo .title { font-size: 34pt; font-weight: 800; line-height: 1.25; }
  .main { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12mm; text-align: center; }
  .no { width: 70mm; height: 70mm; border-radius: 50%; background: #1f5a45; color: #fff; display: grid; place-items: center; font-size: 110pt; font-weight: 800; line-height: 1; }
  .name { font-size: 58pt; font-weight: 800; line-height: 1.25; word-break: keep-all; padding: 0 4mm; }
  .where { font-size: 30pt; font-weight: 700; color: #1f5a45; border: 3pt solid #1f5a45; border-radius: 99mm; padding: 3mm 12mm; }
  .foot { flex: none; font-size: 13pt; color: #444; text-align: center; border-top: 1pt solid #bbb; padding-top: 4mm; }
</style></head><body>
<div id="root"></div>
<script>
__SPOTS__
const CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫";
document.getElementById("root").innerHTML = SPOTS.map(s => {
  const m = s.name.match(/^([①-⑫])\\s*(.*)$/);
  const no = CIRCLED.indexOf(m[1]) + 1, name = m[2], where = s.hint.split("｜")[0];
  const size = name.length <= 8 ? 58 : name.length <= 10 ? 46 : 40;   // 長い名前は小さくして、1行に収める
  return `<section class="page">
  <div class="photo"><div class="school">駒澤大学高等学校　令和8年度 学校説明会</div><div class="title">校内クイズ探検</div></div>
  <div class="main"><div class="no">${no}</div><div class="name" style="font-size:${size}pt">${name}</div><div class="where">${where}</div></div>
  <div class="foot">この場所のクイズは、スマホの「校内クイズ探検」で挑戦できます。</div>
</section>`;
}).join("");
</script></body></html>
"""
(here / "signs.html").write_text(PAGE.replace("__SPOTS__", spots), encoding="utf8")
print("signs.html を作りました")
