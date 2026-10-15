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
4. ポスター版で開くURLは、末尾に `#poster` を付けたもの（案内紙のQRコードはこちら）

## 注意
- このリポジトリは **公開(public)** です。訪問カードなど、個人情報を含むファイルは置かないでください。
- 先生用の答え `poster-answers.md` は、公開されないよう `.gitignore` で管理から外してあります。
- アプリの問題と答えは、ページのソースを見れば分かる作りです（景品なしの運用を前提にしています）。
