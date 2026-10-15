#!/usr/bin/env python3
"""参加者向けの案内紙（QRコード入り）flyer.html を作る。
使い方： python3 make_flyer.py [URL]
  URL を省略すると、GitHub Pages の公開URL（絵や文字を4つの中から選ぶ、ふつうのクイズ）を使います。
  ポスター版で開きたいときは URL の末尾に ?mode=poster を付けてください。
  QRコードの作成に segno が必要です（pip install segno）。
"""
import sys, pathlib, io, re
import segno

URL = sys.argv[1] if len(sys.argv) > 1 else "https://iyokoyama-13641.github.io/komadai-hs-pr/"
here = pathlib.Path(__file__).parent
buf = io.BytesIO()
segno.make(URL, error="m").save(buf, kind="svg", scale=1, border=2, dark="#111111", light="#ffffff", xmldecl=False, svgns=True, nl=False)
svg = buf.getvalue().decode()
# 拡大しても崩れないよう、width/height を viewBox に置き換える
m = re.search(r'<svg[^>]*?width="(\d+)"[^>]*?height="(\d+)"', svg)
svg = re.sub(r'(<svg[^>]*?) width="\d+"', r'\1', svg, count=1)
svg = re.sub(r'(<svg[^>]*?) height="\d+"', r'\1 viewBox="0 0 %s %s"' % (m.group(1), m.group(2)), svg, count=1)

HTML = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>校内クイズ探検 案内</title>
<style>
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; }
  body { margin: 0; color: #111; font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "Noto Sans JP", "Noto Sans CJK JP", "IPAexGothic", "IPAGothic", sans-serif; }
  .page { width: 210mm; height: 297mm; padding: 12mm 16mm 10mm; display: flex; flex-direction: column; align-items: center; gap: 5mm; text-align: center; }
  .banner { flex: none; width: 100%; height: 66mm; border-radius: 6mm; color: #fff; display: flex; flex-direction: column; justify-content: flex-end; align-items: flex-start; padding: 6mm 8mm; text-align: left; text-shadow: 0 0 4mm rgba(0, 0, 0, .6);
    background: linear-gradient(180deg, rgba(0, 0, 0, 0) 30%, rgba(0, 0, 0, .7)), url("../docs/hero.jpg") center 58% / cover #1f5a45; }
  .school { font-size: 13pt; font-weight: 700; letter-spacing: .1em; }
  h1 { margin: 0; font-size: 40pt; line-height: 1.2; }
  .lead { font-size: 18pt; line-height: 1.6; }
  .qr { width: 74mm; height: 74mm; padding: 4mm; border: 3pt solid #1f5a45; border-radius: 6mm; }
  .qr svg { width: 100%; height: 100%; display: block; }
  .url { font-size: 10pt; color: #555; word-break: break-all; }
  ol { margin: 0; padding: 0; list-style: none; display: grid; gap: 3mm; width: 100%; text-align: left; font-size: 16pt; line-height: 1.5; }
  li { display: flex; gap: 5mm; align-items: center; background: #f1f7f3; border-radius: 4mm; padding: 3mm 6mm; }
  li b { flex: none; width: 12mm; height: 12mm; border-radius: 50%; background: #1f5a45; color: #fff; display: grid; place-items: center; font-size: 18pt; }
  .note { font-size: 12pt; color: #333; line-height: 1.7; }
</style></head><body><section class="page">
  <div class="banner"><div class="school">駒澤大学高等学校　令和8年度 学校説明会</div><h1>校内クイズ探検</h1></div>
  <div class="lead">保護者の方といっしょに、校内の場所をめぐって<br>クイズに挑戦しよう！</div>
  <div class="qr">__SVG__</div>
  <div class="url">__URL__</div>
  <ol>
    <li><b>1</b><span>スマホでQRコードを読み取る</span></li>
    <li><b>2</b><span>校内に貼ってある①〜⑫の場所へ行く</span></li>
    <li><b>3</b><span>歩きながら、絵を4つの中から選んで答える</span></li>
    <li><b>4</b><span>8問でステージクリア、13問でコンプリート！</span></li>
  </ol>
  <div class="note">校舎の見学では、玄関ホールで受け取る靴カバーを着けてください。<br>通信ができないときは、スタッフにお声がけください。</div>
</section></body></html>
"""
(here / "flyer.html").write_text(HTML.replace("__SVG__", svg).replace("__URL__", URL), encoding="utf8")
print("flyer.html を作りました:", URL)
