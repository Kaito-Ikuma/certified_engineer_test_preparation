# 技術士第一次試験 全過去問体系化プロジェクト

日本技術士会の[過去問題](https://www.engineer.or.jp/c_categories/index02021.html)を保存し、基礎・適性・応用理学を学習分野別に整理するプロジェクトです。対象は平成23〜30年度、令和元〜7年度、令和元年度再試験の16回です。

## 現在の状態

Astra Review 1のHigh 5件・Medium 6件に対応し、三科目の全1,270問の解説、共通理論、頻度分析5章の初稿を作成しました。全問に五肢別検討、共通理論参照、Astra査読フラグがあります。

- 原典PDF361件、問題DB1,270問（基礎470・適性240・応用理学560）。欠落・余剰・ID重複0。
- 主分類・要旨確認1,270問、原典条件校正771問・部分校正499問。解説は全問Astra査読待ち。
- 公式の複数受理・全員得点と訂正注記を維持。独立解と公式の相違24問、受理集合の一肢のみ独立確認1問を区別。
- 中分類80群の頻度・年度比較、原典比較済み374組の関係を集計。学習時間と得点効率は未評価。
- `make test`の30回帰、1,270ラベル監査、Checkpoint 2初稿監査が成功。最終専門査読と最終完成監査は未完了。

[Checkpoint 2査読依頼](handoff/CHECKPOINT_2_FOR_ASTRA.md)を作成し、Solの執筆工程は停止しました。[作業版PDF](build/main.pdf)は1,349頁の全問査読待ち初稿です。追加・分析等の63頁を表示確認し、未定義引用・参照、欠落文字、はみ出し0。[進捗と次工程](handoff/SOL_PROGRESS_S7.md)に状態を記録します。`extracted/logs/checkpoint2_draft_audit.json`と`data/checkpoint2_review_queue.csv`で初稿完成と未確認事項を別に確認できます。

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

# Checkpoint 2用分析と初稿監査
python3 -B scripts/generate_checkpoint2_analysis.py
python3 -B scripts/audit_checkpoint2.py

# 作業版PDF（初期監査や本文査読の代用ではない）
make pdf
```

`make initial`は歴史的チェックポイントを保護するため停止します。`make all`と`audit_completeness.py --final`は最終品質検査が未実装であるため失敗します。校正・解説をCSVへ追記しても、通常の再構築が無条件に消すことはありません。確認済みの内容を変更する場合は、その内容のハッシュに対応する新しい確認記録が必要です。

既存の有効なOCRは`--ocr`なしでも保持します。原典ハッシュが変わったキャッシュは再利用しません。再OCR時はmacOS VisionとSwiftが必要で、`extract_pdf_text.py --ocr`を利用します。旧キャッシュへの一度限りの束縛は校正完了を意味しません。

更新中・中断した`data/publication.lock`がある場合、読み取りと次の更新は停止します。`python3 -B scripts/recover_publication.py`で記録を確認し、`--rollback`で旧正本へ復旧します。手書き本文とCSVの前後像は保存されます。

Gitリポジトリは未初期化です。元のチェックポイントとAstra査読文書は履歴として保持しています。
