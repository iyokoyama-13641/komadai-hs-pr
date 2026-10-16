#!/usr/bin/env python3
"""校内の各場所に貼る「場所の説明板」signs.html を作る（A4縦・1か所1枚・全13枚）。
名前・番号・地区/階は docs/index.html の SPOTS（name / hint）から取る。説明文（紹介・豆知識）は、下の SIGN_TEXT を編集する。
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

# 説明板の文章：（その場所の紹介, 豆知識）。案内図とクイズの正解の説明がもと。
SIGN_TEXT = {
 "s1": [
  "ジムのようにウエイトトレーニングマシーンがそろっています。部活動や授業で使います。",
  "ベンチプレスは胸、スクワットとレッグプレスは脚、アームカールは腕の筋肉を鍛えます。"
 ],
 "s2": [
  "カレーライスからケーキまで、楽しく実習を行います。男子も女子も一緒に作ります。部屋の前に、大学の資料・昨年度の入試問題・部活動案内があります。ご自由にお取りください。",
  "めん棒は、パンやうどん、クッキーなどの生地を、同じ厚さにのばす道具です。"
 ],
 "s3": [
  "書道の授業で使う特別教室です。説明会の日は、個別相談会場になっています。",
  "「弘法も筆の誤り」の弘法は、書の名人として知られる弘法大師（空海）のこと。名人でも失敗することがある、という意味です。"
 ],
 "s4": [
  "パソコンを使う実習室です。2か所あり、難しいことも、やさしく、深く、楽しく学べます。",
  "CPU（シーピーユー）は、計算や命令の処理をする、パソコンの頭脳です。"
 ],
 "s5": [
  "音楽の授業で使う特別教室です。",
  "「運命」「第九」を作曲したベートーヴェンは、耳が聞こえにくくなっても作曲を続けたことで知られています。"
 ],
 "s6": [
  "美術の授業で使う特別教室です。",
  "絵の具は、黄色と青を混ぜると緑、赤と青でむらさき、赤と黄でオレンジになります。"
 ],
 "s7": [
  "地下にある、柔道・剣道の道場です。伝統と趣があり、男子は体育の授業で柔道・剣道を行います。",
  "武道は「礼に始まり、礼に終わる」といわれます。相手や道場、道具への感謝と敬意を、おじぎ（礼）で表します。"
 ],
 "s8a": [
  "物理・地学の実験をする実験室です。3階にあります。",
  "太陽系でいちばん大きい惑星は木星です。地球が約1300個も入る大きさといわれています。"
 ],
 "s8b": [
  "生物・化学の実験をする実験室です。4階にあります。",
  "血液の中で酸素を運んでいるのは赤血球です。赤い色は、酸素と結びつく「ヘモグロビン」のはたらきです。"
 ],
 "s9": [
  "本格的な坐禅ができる施設です。校舎の屋上にあります。",
  "坐禅堂には、文殊菩薩（もんじゅぼさつ）様をお祀りしています。「三人寄れば文殊の知恵」の文殊です。"
 ],
 "s10": [
  "パンやおにぎりなどを販売する購買部がある、地下のホールです。",
  "パンがふくらむのは、酵母（イースト）が出す二酸化炭素のおかげです。"
 ],
 "s11": [
  "ビデオなどを大画面で見られる教室です。",
  "映画は、1秒間に24枚（24コマ）の絵を次々に映して、動いているように見せています。パラパラ漫画と同じしくみです。"
 ],
 "s12": [
  "蔵書は約4万冊。3階にある図書室です。",
  "「吾輩は猫である」は、夏目漱石のデビュー作です。気になる本を探してみよう。"
 ]
}

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
  .desc { flex: none; padding: 6mm 8mm; border: 2.5pt solid #1f5a45; border-radius: 5mm; background: #f6faf7; word-break: auto-phrase; text-wrap: pretty; display: flex; flex-direction: column; gap: 5mm; }
  .intro { font-size: 24pt; line-height: 1.7; font-weight: 700; }
  .trivia { font-size: 19pt; line-height: 1.7; color: #222; }
  .trivia b { display: inline-block; font-size: 15pt; background: #1f5a45; color: #fff; border-radius: 99mm; padding: 0 5mm; margin-right: 3mm; vertical-align: 1pt; }
  .foot { flex: none; font-size: 12pt; color: #555; text-align: center; letter-spacing: .1em; }
</style></head><body>
<div id="root"></div>
<script>
__SPOTS__
const PHOTOS = __PHOTOS__;
const SIGN_TEXT = __SIGN__;
const CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫";
document.getElementById("root").innerHTML = SPOTS.map(s => {
  const m = s.name.match(/^([①-⑫])\\s*(.*)$/);
  const no = CIRCLED.indexOf(m[1]) + 1, name = m[2], where = s.hint.split("｜")[0];
  const size = name.length <= 6 ? 50 : name.length <= 8 ? 42 : name.length <= 10 ? 34 : 30;   // 長い名前は小さくして、1行に収める
  const pic = PHOTOS[s.id] ? `<img src="${PHOTOS[s.id]}" alt="">` : `<span class="em">${s.emoji}</span>`;
  return `<section class="page">
  <div class="head"><div class="no">${no}</div><div class="ttl"><div class="name" style="font-size:${size}pt">${name}</div><div class="where">${where}</div></div></div>
  <div class="pic">${pic}</div>
  <div class="desc"><div class="intro">${SIGN_TEXT[s.id][0]}</div><div class="trivia"><b>豆知識</b>${SIGN_TEXT[s.id][1]}</div></div>
  <div class="foot">駒澤大学高等学校</div>
</section>`;
}).join("");
</script></body></html>
"""
(here / "signs.html").write_text(PAGE.replace("__SPOTS__", spots).replace("__PHOTOS__", json.dumps(photos, ensure_ascii=False)).replace("__SIGN__", json.dumps(SIGN_TEXT, ensure_ascii=False)), encoding="utf8")
print("signs.html を作りました（写真あり: %d か所）" % len(photos))
