# 技術士第一次試験 全過去問体系化プロジェクト

日本技術士会の[過去問題（第一次試験）](https://www.engineer.or.jp/c_categories/index02021.html)に掲載された平成23年度〜令和7年度の問題PDFを保存しています。

- 保存先: `sources/H23/`〜`sources/H30/`、`sources/R01/`〜`sources/R07/`、`sources/R01_retest/`
- 各回22件: `basic.pdf`（基礎科目）、`aptitude.pdf`（適性科目）、部門番号付きPDF（専門20部門）
- 応用理学部門: `17_applied_science.pdf`
- 合計: 16回 × 22科目 = 352件
- 取得元・ファイルサイズ・SHA-256: `data/source_files.csv`
- 取得元一覧の保存: `sources/index02021.html`
- 取得日: 2026-10-08（日本時間）

## 現在の状態

S0〜S3を実施し、Astra Checkpoint 1で停止しています。
教材対象は基礎・適性・応用理学の3科目、16回分48PDFです。対象外部門の原本も保持しています。
公式正答PDF9件を追加し、原典台帳には361件を登録しています。

問題DB初版は1,270問（基礎470、適性240、応用理学560）。令和元年度再試験は80問です。
通常抽出できなかった問題PDF763ページを日本語OCRしました。認識結果・画像・問題境界を保存しています。
公式正答表は文字層から読み取り、全問題の番号集合と照合しました。注記のある特殊扱い6件は画像確認も実施しました。

**初期監査合格であり、完成教材ではありません。** OCR本文、分類、仮要約は未校正・未査読。全問を要確認として残しています。
解説、難易度、優先度、統計、索引、main.tex、main.pdfは後工程です。

## 成果物

- `data/questions.csv`: 全問DB（正本）。原典ページ・正答・分類・確認状態を追跡可能。
- `data/answers_official.csv`: 公式正答と原典行・ページ・注記。
- `data/answer_exceptions.csv`: 複数正答・全員得点・訂正の6件。
- `data/classifications.csv`: 暫定分類と根拠の派生ビュー。
- `data/audit_report.csv`: 年度・科目別の48組の監査。
- `data/unresolved.csv`: 未校正・査読待ち・教材未作成の全問追跡。
- `extracted/text/`: ページ単位テキスト・OCR座標JSON。
- `extracted/pages/`: ローカル照合用PNGとOCR JSON。配布用教材には含めない。
- `extracted/questions/`: 問題単位の未校正OCR。
- `config/`: 暫定分類体系、境界と分類の手作業補正、スキーマ。
- `DATA_DESIGN.md`: 確認フラグの意味、データ設計、査読論点。
- `handoff/CHECKPOINT_1_FOR_ASTRA.md`: 次モデルへの指示。
- `WORKLOG.md`: 実施工程・検証・未解決事項。

## 再現

プロジェクト内で `make initial` を実行すると、保存済みOCRからS0〜S3のCSVを再構築・監査します（約数秒、ネット接続不要）。
Python 3とPopplerのpdfinfoが必要です。手作業補正はconfigのJSONから再適用されます。
CSVに直接追記した後工程の解説等は現行初期再構築では保存されません。査読1後は一括再構築を停止するガードを設けています。

OCRを再実行する場合はmacOSのVisionとSwiftコンパイラが必要です。

```sh
swiftc -module-cache-path /tmp/pe_exam_swift_cache scripts/ocr_pdf.swift -o scripts/ocr_pdf
python3 scripts/extract_pdf_text.py --ocr --workers 3
```

既存のページOCRは再利用します。通常テキストが存在するページにはOCRしません。
制限環境ではVisionの実行に許可が必要です。OCR本文を取得後、`make initial`を実行します。
`make all`は未実装の最終工程を成功と見せないため停止します。LuaLaTeX設定とPDFビルド用ターゲットのみ準備済みです。

公式サイトでは著作権の関係で一部省略・改変された問題があると説明されています。教材は本質を失わない独自要約と自作解説を中心とし、公式図版を再配布しません。
