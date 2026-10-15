#!/usr/bin/env python3
"""QRコードだけの qr.html を作る（PDFにするときは、ブラウザの印刷で「PDFとして保存」）。
使い方： python3 make_qr.py [URL]      segno が必要です（pip install segno）
"""
import sys, pathlib, io, re
import segno

URL = sys.argv[1] if len(sys.argv) > 1 else "https://iyokoyama-13641.github.io/komadai-hs-pr/"
here = pathlib.Path(__file__).parent
buf = io.BytesIO()
segno.make(URL, error="m").save(buf, kind="svg", scale=1, border=4, dark="#000000", light="#ffffff", xmldecl=False, svgns=True, nl=False)
svg = buf.getvalue().decode()
m = re.search(r'<svg[^>]*?width="(\d+)"[^>]*?height="(\d+)"', svg)
svg = re.sub(r'(<svg[^>]*?) width="\d+"', r'\1', svg, count=1)
svg = re.sub(r'(<svg[^>]*?) height="\d+"', r'\1 viewBox="0 0 %s %s"' % (m.group(1), m.group(2)), svg, count=1)
html = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>QRコード</title>
<style>
  @page { size: A4; margin: 0; }
  html, body { margin: 0; background: #fff; }
  .page { width: 210mm; height: 297mm; display: grid; place-items: center; }
  .page svg { width: 150mm; height: 150mm; display: block; }
</style></head><body><div class="page">__SVG__</div></body></html>
"""
(here / "qr.html").write_text(html.replace("__SVG__", svg), encoding="utf8")
print("qr.html を作りました:", URL)
