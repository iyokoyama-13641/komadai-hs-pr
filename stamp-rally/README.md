# 校内クイズ探検（学校説明会）

| ファイル | 内容 |
|---|---|
| `docs/index.html` | アプリ本体（1ファイル）。問題は中の `SPOTS` を編集 |
| `stamp-rally/make_posters.py` | 問題データから、ポスター `posters.html` / `posters.pdf` と先生用の答え `poster-answers.md` を作る |
| `stamp-rally/make_flyer.py` | QRコード入りの案内紙 `flyer.html` / `flyer.pdf` を作る（`pip install segno` が必要） |
| `stamp-rally/photos/` | 写真を使う場合の置き場所（`README.md` に一覧） |

## ネットで公開する（GitHub Pages）
1. GitHub のこのリポジトリで **Settings → Pages** を開く
2. Source を「Deploy from a branch」、Branch を `main`、フォルダを **`/docs`** にして Save
3. 数分後に公開URL `https://iyokoyama-13641.github.io/komadai-hs-pr/` で開ける
4. 案内紙のQRコードは、上のURLそのもの（絵や文字を4つの中から選ぶ、ふつうのクイズ）。
5. ポスターを貼って遊ぶ「ポスター版」は、URLの末尾に `?mode=poster` を付けたときだけ。参加者には切り替えボタンは表示されません。先生用に、`?staff` を付けると、ポスター版/通常版の切り替えボタンが出ます（今回の説明会では使いません）

## 注意
- このリポジトリは **公開(public)** です。訪問カードなど、個人情報を含むファイルは置かないでください。
- 先生用の答え `poster-answers.md` は、公開されないよう `.gitignore` で管理から外してあります。
- アプリの問題と答えは、ページのソースを見れば分かる作りです（景品なしの運用を前提にしています）。

## 利用人数の集計（GoatCounter）
当日に「何人が遊んだか」を数えるため、無料のアクセス解析 [GoatCounter](https://www.goatcounter.com/) に対応しています。個人は特定せず、端末ごとに数えます。

1. https://www.goatcounter.com/ でアカウントを作り、サイトの名前（コード、例 `komadai-hs`）を決める
2. `docs/index.html` の `const GC_CODE = "";` に、そのコードを入れる（空のままなら何も送りません）
3. 管理画面（`https://コード.goatcounter.com`）で、次が見られます
   - ページの表示数・端末数 …… QRコードから開いた人数
   - `event/first-correct` …… 1問以上正解した端末の数
   - `event/stage-clear` …… ステージクリア（8問）の端末の数
   - `event/complete` …… コンプリート（13問）の端末の数
4. 公開ページでだけ数えます。先生用の確認（`?staff`）と、手元のファイルは数えません。

※ 数えているのは人ではなく端末です。親子で1台のスマホを使えば1つ、同じ人が2台で開けば2つになります。
