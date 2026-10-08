# Astra Checkpoint 1

## 目的と状態
全問題DBと分類体系の査読。ユーザー申告のGPT-6.1 SolとしてS0〜S3を実施した。
ここでSol作業を停止する。Astraは大量本文の執筆・再OCRを開始せず、設計と分類の重要判断を査読する。

## 完了条件
- 原典一覧: 問題PDF352件を保持し、対象問題48件と公式正答9件を台帳で区別。
- 全問題初期登録: **1,270問**。基礎470／適性240／応用理学560。再試験80問。
- 全行に大・中・小分類、主題、執筆予定TeXパスを初期付与。
- 年度・科目48組で暫定監査済み。期待番号集合と原典見出し由来のDB番号集合が一致。
- 欠落0、余剰0、ID重複0、初期分類なし0、公式正答未照合0、原典・ページ・派生ビュー整合エラー0。
- `make initial`による再現確認済み。ネット接続なしで保存済みOCRから再構築できる。

## 未完了を混同しない
全問のOCR本文は未校正で`needs_manual_verification=true`。
全行の分類・仮要約は確認前（classification_verified / summary_verified=false）。
特殊な2見出しのみ画像確認して補正し、残りの境界は認識番号の照合を実施した。全1270見出しの画像目視は未実施。
公式正答のverifiedは公式文字表の抽出・構造照合で、解法確認ではない。特殊扱い6件の表・注記は画像も確認済み。
仮要約は「テーマ＋問題形式」に限定。正確な意味要約、数値・式・図表の校正、解説はこれから。
難易度・優先度・関連問題は未評価。TeXパスは計画だけで実ラベル・本文は未作成。
`questions_without_tex=1270`、`unexplained_questions=1270`、最終監査は未合格。main.pdfは未生成。

## Astraに確認してほしい事項
1. 大分類・中分類・小分類が学問体系として妥当か。公式基礎問題群と学問分類を二軸にすべきか。
2. 分類粒度が過剰または粗すぎないか。中分類に学習章、小分類に概念タグを割り当てる現案を評価する。
3. 応用理学の物理と地球物理、化学と地球化学、地質と物理探査の境界が自然か。
4. 同一テーマがカテゴリへ不自然に分裂していないか。特に同位体、相平衡、地殻、波動、鉱物の結晶構造。
5. information_logicの体系が情報工学学習にも有用か。OS・DB等の拡張を出題範囲に沿ってどう整理するか。
6. questions.csvスキーマ、原典座標、確認フラグ、未知値、複数正答・全員得点の表現に後工程の不足がないか。
7. DATA_DESIGN.mdの難易度・優先度評価案が対象読者に適切か。未評価の空欄を査読済み数値に置換しない。
8. 類似問題検出案が妥当か。主題・解法・条件・否定表現を分けて比較する方法を検討する。
9. 誤分類の可能性が高い問題ID。低信頼行と語句規則の弱点を調べ、修正指示を具体化する。
10. OCR本文未校正のまま要約や解説を自動生成する危険、再構築による後工程追記の消失、タグ正規化不足など、体系的な設計欠陥。
11. 有機・高分子の独立章`12_organic_polymer.tex`と適性の技術社会政策章`07_science_technology_society.tex`の追加提案の妥当性。
12. 初期監査と最終監査の条件が十分か。期待番号集合を公式正答表から得ることの限界と、独立の見出し/選択肢検証の追加を検討する。

## 読む順序と対象ファイル
1. `AGENTS.md` / `PROJECT_REQUEST.md` / `WORKLOG.md` / `README.md`
2. `DATA_DESIGN.md` / `config/question_schema.json`
3. `extracted/logs/audit_metrics.json` / `data/audit_report.csv` / `data/answer_exceptions.csv`
4. `config/taxonomy.json` / `scripts/classify_questions.py` / `config/classification_overrides.json`
5. `data/review_queue_checkpoint1.csv`から低信頼分類と境界問題を優先し、`data/questions.csv`と`extracted/questions/`の内容を確認。
6. 必要な箇所のみ原典PDF・`extracted/pages/`画像で照合。
7. `scripts/build_question_db.py` / `parse_official_answers.py` / `validate_answers.py` / `audit_completeness.py` / `build_all.py`の設計を確認。

全問を最初から再処理する必要はない。基礎解析と情報論理、応用理学の領域境界を層化して点検し、系統的な誤りがあれば影響する番号集合を示す。
`data/review_queue_checkpoint1.csv`は優先点検用であり、対象外の問題を捨てたものではない。全1270問はquestions.csvにある。

## 公式正答の特殊扱い
- H23-REG-APT-04: 1または5。
- H26-REG-BASIC-5-3: 当初3から5へ訂正。
- H30-REG-APT-14 / R01-RET-APT-14 / R02-REG-APPLIED-10: 全員得点。
- R02-REG-BASIC-5-5: 4または3。

## Gitと保存
ワークスペースはGit未初期化。git status / git diffによる差分確認はできない。
代わりに`handoff/CHECKPOINT_1_FILES.csv`へコード・CSV・引継ぎ文書のサイズとSHA-256を記録した。
既存PDFを保持し、remoteへのpushは行っていない。認識用バイナリはSwiftソースから再生成可能。

## 出力先と書式
`handoff/ASTRA_REVIEW_1.md`。
指摘ごとにSeverity（Critical/High/Medium/Low）、Target（ファイル・問題ID）、Problem、Reason、Recommended fix、Verificationを記す。
Critical→High→Medium→Lowの順でSolが反映できる具体的な修正指示とする。原則として大量本文を直接書き換えない。
査読結果を保存し、WORKLOGに記録したら停止する。

## 査読後の報告
「Astra査読が完了しました。次はGPT-6.1 Solに戻し、『ASTRA_REVIEW_1.mdを読み、全指摘を反映して続行してください』と指示してください。」
