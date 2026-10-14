# 技術士第一次試験 全過去問体系化プロジェクト

日本技術士会の[過去問題](https://www.engineer.or.jp/c_categories/index02021.html)を保存し、基礎・適性・応用理学を学習分野別に整理するプロジェクトです。対象は平成23〜30年度、令和元〜7年度、令和元年度再試験の16回です。

## 現在の状態

Astra Review 1のHigh 5件・Medium 6件に対応し、S4の修正、S5の暫定統計、S6のTeX骨格を実装しました。S7の本文・解説執筆は進行中です。詳細は[査読への対応表](handoff/REVIEW_1_RESPONSE.md)と[次工程](handoff/SOL_PROGRESS_S7.md)を参照してください。

- 原典PDF361件（問題352件＋公式正答9件）。保存済み原典のハッシュ不一致0。
- 問題DB1,270問：基礎470、適性240、応用理学560。欠落・余剰・ID重複0。
- 主分類確認済み146問。未確認の分類は暫定。
- 公式正答の特殊6件を維持。通常表48ページ・320セルを独立の座標抽出でも照合。
- 要旨確認済み103問、校正完了100問、部分校正3問。解説103問はAstra査読待ちの初稿。
- 全1,270問の年度・分野索引を生成し、力学・技術士法・数値表現の共通理論を追記。作業版PDFを更新中です。

[作業版PDF](build/main.pdf)は登録項目と一部解説を閲覧するためのものです。本文又は解釈の確認待ちは1,170問、確認済み解説は0問です。初期監査合格と最終合格は別で、最終監査は未実装のため明示的に失敗します。Checkpoint 2の条件にはまだ到達していません。

## 保存と正本

- `sources/H23/`〜`H30/`、`R01/`〜`R07/`、`R01_retest/`：各回22問題PDF。応用理学は`17_applied_science.pdf`。
- `sources/answers/`：公式正答PDF。取得URL・SHA-256は`data/source_files.csv`。
- `data/questions.csv`：正本。原典・番号・公式正答・分類・校正・要旨・解説・確認状態。
- `data/classifications.csv`、`question_topics.csv`：主分類と概念タグの派生表。
- `data/review1_classification_changes.csv`：S4前スナップショットとの変更434件、旧新値・理由・原典頁。
- `data/review1_target_results.csv`、`verification_records.csv`：原典確認の範囲とハッシュに対応する証跡。
- `data/answer_exceptions.csv`、`answer_verification_records.csv`、`answer_coordinate_checks.csv`：特殊正答と確認証跡。
- `data/topic_statistics.csv`、`concept_statistics.csv`：暫定値と確認済み部分集合。主分類数とタグの延べ数を区別。
- `data/question_evaluations.csv`、`question_relations.csv`：難易度の校準初稿と承認済み類似関係。
- `data/review_queue.csv`、`review_coverage.csv`、`review_strata.csv`：年代・科目・分野別の確認計画と実績。
- `data/unresolved.csv`：境界・校正・分類・概念・要旨・評価・解説を別々に追跡。
- `extracted/text/`、`extracted/questions/`：未校正OCR。`extracted/corrected/`：独立した校正条件・選択肢対応・図参照。
- `chapters/`：手書きの本文。`generated/questions/`：CSVから作る問題ブロック。
- `snapshots/`：S4開始前と更新ごとの前後像・回復ジャーナル。

[DATA_DESIGN.md](DATA_DESIGN.md)に所有列・状態・分類語彙・証跡・更新規則を記載しています。原典画像はローカル確認用で、作業版PDFに転載していません。

## 再実行

Python 3.9以降、Poppler、LuaLaTeX、Biber、latexmkを使います。通常の再構築にはネット接続や再OCRは不要です。

```sh
# 候補のみ。questions.csvは更新しない
python3 -B scripts/build_all.py --phase reviewed

# 原典・抽出・分類の更新を検証して反映。既存の執筆・校正列は保持
make reviewed

# 暫定統計・類似候補・索引・問題ブロックと参照監査
make draft

# 隔離したコピーでの回帰検証
make test

# 作業版PDF（初期監査や本文査読の代用ではない）
make pdf
```

`make initial`は歴史的チェックポイントを保護するため停止します。`make all`と`audit_completeness.py --final`は最終品質検査が未実装であるため失敗します。校正・解説をCSVへ追記しても、通常の再構築が無条件に消すことはありません。確認済みの内容を変更する場合は、その内容のハッシュに対応する新しい確認記録が必要です。

既存の有効なOCRは`--ocr`なしでも保持します。原典ハッシュが変わったキャッシュは再利用しません。再OCR時はmacOS VisionとSwiftが必要で、`extract_pdf_text.py --ocr`を利用します。旧キャッシュへの一度限りの束縛は校正完了を意味しません。

更新中・中断した`data/publication.lock`がある場合、読み取りと次の更新は停止します。`python3 -B scripts/recover_publication.py`で記録を確認し、`--rollback`で旧正本へ復旧します。手書き本文とCSVの前後像は保存されます。

Gitリポジトリは未初期化です。元のチェックポイントとAstra査読文書は履歴として保持しています。
