#!/usr/bin/env python3
"""docs/index.html の問題データ（SPOTS / ICONS）から、印刷用ポスター posters.html と答え一覧 poster-answers.md を作る。
問題を直したら、このスクリプトを実行し直してください： python3 make_posters.py
"""
import re, json, subprocess, pathlib

here = pathlib.Path(__file__).parent
src = (here.parent / "docs" / "index.html").read_text(encoding="utf8")
icons = re.search(r"const ICONS = \{.*?\n\};", src, re.S).group(0)
spots = re.search(r"const SPOTS = \[.*?\n\];", src, re.S).group(0)

PAGE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>校内クイズ探検 ポスター</title>
<style>
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; }
  body { margin: 0; color: #111; background: #fff; font-family: "Hiragino Sans", "Noto Sans JP", "Noto Sans CJK JP", system-ui, sans-serif; }
  .page { width: 210mm; height: 297mm; padding: 13mm 14mm; display: flex; flex-direction: column; gap: 6mm; page-break-after: always; break-after: page; overflow: hidden; }
  .top { display: flex; justify-content: space-between; font-size: 11pt; color: #1f5a45; font-weight: 700; letter-spacing: .08em; }
  h1 { margin: 0; font-size: 34pt; line-height: 1.2; }
  .where { font-size: 12pt; color: #555; margin-top: 1mm; }
  .q { font-size: 21pt; font-weight: 700; line-height: 1.45; padding: 5mm 6mm; border: 2.5pt solid #1f5a45; border-radius: 4mm; background: #f1f7f3; }
  .grid { flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 6mm; min-height: 0; }
  .cell { position: relative; border: 2.5pt solid #333; border-radius: 5mm; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3mm; padding: 8mm 5mm 5mm; }
  .no { position: absolute; left: 4mm; top: 4mm; width: 17mm; height: 17mm; border-radius: 50%; background: #1f5a45; color: #fff; font-size: 26pt; font-weight: 800; display: grid; place-items: center; }
  .pic svg { width: 52mm; height: 52mm; stroke: #111; fill: none; stroke-width: 2.6; stroke-linecap: round; stroke-linejoin: round; }
  .pic svg .plate { stroke-width: 4.5; }
  .pic .sw { display: block; width: 46mm; height: 46mm; border-radius: 50%; border: 1.5pt solid #999; }
  .pic .em { font-size: 60pt; line-height: 1; }
  .lab { font-size: 19pt; font-weight: 700; text-align: center; line-height: 1.3; }
  .lab.big { font-size: 27pt; text-wrap: balance; }
  .foot { font-size: 12pt; color: #333; text-align: center; border-top: 1pt solid #bbb; padding-top: 3mm; }
</style></head><body>
<div id="root"></div>
<script>
__ICONS__
__SPOTS__
// 正解の位置（pos）に正解を置き、残りは元の順に並べる
function posterOrder(s) {
  const [right, ...wrong] = s.choices;
  const list = wrong.slice(); list.splice(s.pos - 1, 0, right);
  return list;
}
const pic = c => c.c ? `<span class="sw" style="background:${c.c}"></span>` : c.i ? ICONS[c.i] : c.e ? `<span class="em">${c.e}</span>` : "";
document.getElementById("root").innerHTML = SPOTS.map(s => `
<section class="page">
  <div class="top"><span>校内クイズ探検</span><span>令和8年度 学校説明会｜駒澤大学高等学校</span></div>
  <div><h1>${s.name}</h1><div class="where">${s.hint}</div></div>
  <div class="q">${s.q}</div>
  <div class="grid">${posterOrder(s).map((c, i) => `
    <div class="cell"><div class="no">${i + 1}</div>
      ${pic(c) ? `<div class="pic">${pic(c)}</div><div class="lab">${c.t}</div>` : `<div class="lab big">${c.t}</div>`}
    </div>`).join("")}
  </div>
  <div class="foot">スマホの「校内クイズ探検」で、正しいと思う番号（1〜4）を選んでね。</div>
</section>`).join("");
</script></body></html>
"""
(here / "posters.html").write_text(PAGE.replace("__ICONS__", icons).replace("__SPOTS__", spots), encoding="utf8")

# 答え一覧（先生用）。ポスターの並びと同じ規則で、正解の番号を出す。
node = r"""
%s
%s
console.log(JSON.stringify(SPOTS.map(s => ({ name: s.name, q: s.q, pos: s.pos, ans: s.choices[0].t, others: s.choices.slice(1).map(c => c.t) }))));
""" % (icons, spots)
rows = json.loads(subprocess.run(["node", "-e", node], capture_output=True, text=True, check=True).stdout)
md = ["# ポスター版 答え一覧（先生用・掲示しないこと）", "", "| 場所 | 問題 | 正解の番号 | 正解 |", "|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['name']} | {r['q']} | **{r['pos']}** | {r['ans']} |")
md += ["", "ポスターの1〜4の並びは、正解の番号の位置に正解を置き、ほかの選択肢を元の順に並べています。", "問題や正解の番号を変えたら、`python3 make_posters.py` を実行し直してください。", ""]
(here / "poster-answers.md").write_text("\n".join(md), encoding="utf8")
print("posters.html / poster-answers.md を作りました（%d か所）" % len(rows))
