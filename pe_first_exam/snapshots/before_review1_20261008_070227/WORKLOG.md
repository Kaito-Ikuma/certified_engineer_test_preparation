# 作業ログ

## 2026-10-08 JST — GPT-6.1 Sol（ユーザー申告）— S0
- 保存済みPDF352件のうち対象は48件（16回×3科目）。欠落なし。
- PROJECT_REQUEST.mdへユーザー指示全文を保存。AGENTS.mdと工程用ディレクトリを作成。
- Gitリポジトリは未初期化。既存PDFと取得元台帳を維持。
- pdftotext / pdftoppm / pdfinfo / Swift / latexmk利用可。Pythonのpdfplumber・pypdfは未導入。
- 48件の通常テキスト抽出を実施、すべて文字層なし。OCRが必要。
- 次工程: OCRと公式正答取得、問題境界・正答表の検証。

## 2026-10-08T01:01:38+09:00 — GPT-6.1 Sol（ユーザー申告）— S1
- 48件・763ページは通常抽出で文字なし。macOS Vision accurate ja-JP/en-USでOCRし、ページPNG、行テキスト、座標、信頼度を保存。OCR用バイナリは制限環境で失敗したため許可を得て実行。
- 公式正答一覧と9PDF（H23〜H30合冊＋令和8回）を取得。正答表352ページは文字層から抽出できた。原典台帳361件を更新。
- sourcesの既存問題PDFを保持。末尾のR07基礎20ページ目は画像で空白確認。

## 同日時 — S2
- 全1,270問を原典見出しと公式番号で初期登録。基礎470・適性240・応用理学560、R01再試験80。
- H27基礎4-5と応用理学8のOCR見出し欠損を画像で確認し、config/boundary_overrides.jsonに補正根拠を保存。見出し認識には年度別番号集合、読順、原典頁を使用。
- 公式正答1,270件を登録・照合。特殊扱い6件（複数正答2件、全員得点3件、正答訂正1件）の表と注記を画像確認。
- 正答は文字表抽出と構造チェック。問題本文・式・図表・法令の校正、解説は未完了。すべてneeds_manual_verification=true。

## 同日時 — S3 / Astra Checkpoint 1
- 全問の初期分類を付与。方法={'keyword_rules_initial': 1255, 'manual_content_review': 15}、信頼度={'medium': 1232, 'low': 38}。全分類はclassification_verified=false。15件を内容点検して補正。
- 一般キーワードの選択肢混入を防ぐため、丸数字をNFKC正規化する前に問題幹を区切った。分野固有の語句と手作業補正を優先。中分類・概念タグは暫定。
- 有機・高分子の独立章、適性の技術社会政策章を追加提案。専門分類の境界とタグの過剰分裂はAstra査読待ち。
- make initialで原典一覧→正答抽出→DB→分類→正答検証→監査を再現。欠落0、余剰0、重複0、初期未分類0、未照合正答0、整合エラー0。
- TeX実ラベルなし1,270、未解説1,270、要確認1,270。初期監査合格／最終監査未合格を区別。
- Git未初期化のためgit status/diffは実行不可。チェックポイント用ファイル一覧のSHA-256を保存する。remote操作なし。
- 対象変更: scripts/、config/、data/、extracted/、AGENTS.md、README.md、DATA_DESIGN.md、PROJECT_REQUEST.md、Makefile、latexmkrc、handoff/。
- 停止条件: S0〜S3完了。CHECKPOINT_1_FOR_ASTRA.mdを読みGPT-6 Astraで査読1を実施する。Solの統計・教材作成はその後。

## 2026-10-08 JST — Astra査読担当（ユーザー指定）— Checkpoint 1 Review
- handoff/ASTRA_REVIEW_1.mdへ査読結果を保存。Critical 0、High 5、Medium 6、Low 0。初期登録は受領、分類確定・統計・大量執筆の前に修正が必要。
- 原典361PDFと開始時チェックポイント34ファイルのSHA-256不一致0。1,270問、ID重複0。taxonomyに未登録の分類組合せ4行を確認。
- 分類タグの分野混同、固有振動・スタック・陽イオン分析等の分類、OCRの手順IV→I誤認を点検。主要例は公式問題の保存画像で照合。
- 隔離コピーでラベルと状態フラグだけの負例が最終監査に合格する欠陥を再現。元のdata/scripts/extracted/sourcesは変更していない。
- handoff/ASTRA_REVIEW_1_TARGETS.csvへ再点検集合48件を保存。全件誤り確定・全件画像確認済みを意味しない。
- 全問解答・OCR校正・全正答表セルの再目視は未実施。大量本文修正・再OCR・S4実装は行わず停止。
- 次工程: GPT-6.1 Solへ戻りASTRA_REVIEW_1.mdの全指摘を反映して続行。元チェックポイントのハッシュ一覧は開始時証跡として保持（WORKLOG追記分のみ差分）。
