# DB設計 — Review 1反映版

## 正本と所有
`data/questions.csv`が教材・索引の正本。`classifications.csv`とTeX問題ブロックは派生ビュー。
`classification_rules.json`は候補判定規則、`taxonomy.json`は学習分野・章の管理語彙、`concepts.json`は分野制約付き概念語彙である。実行中にtaxonomyを自動再生成しない。
`curated_examples.json`は原典ハッシュに束縛された新規執筆入力案で、既存CSVの手動編集を無条件に上書きする正本ではない。既に適用した内容は再適用で保持し、内容変更は競合として再確認を要する。

`build_question_db.py`と`classify_questions.py`は既定で候補を生成する。`--apply`で正本へ反映する。前者は原典・抽出・正答列のみを更新し、解説・校正文・評価などは保持する。後者は未確認の分類・仮要約だけを更新し、確認済み分類、独自の要約、校正済み依存フラグは保持する。
要旨を直接執筆する場合はsummary_status=draftとして仮要約と区別する。確認済みにする場合は証跡を伴わせる。
原典／抽出が変わった際は authored content を残して確認を失効させ、source_change_conflicts.csvへ記録する。

## 原子的更新と回復
共通のpublish_bundleは一時保存→検証→スナップショット→ファイル置換を行い、通常の例外では旧値を復旧する。snapshots/txn_*/journal.jsonに前後像と状態を保持する。
複数ファイルは同時のOS単一操作ではない。publication.lockのある間は読取りを停止し、プロセス強制終了で残ったロックは`recover_publication.py`で確認し、`--rollback`で明示回復する。
元のCHECKPOINT_1_FILES.csvは当時の証跡として保持する。S4開始前の全コード・設定・データもsnapshots/before_review1_*/へ保存した。

## 原典とOCR
source_sha256は公式PDF、raw_text_sha256は未校正問題抽出に結び付く。通常抽出が空でも既存の有効なOCRをno_textで上書きしない。
OCRキャッシュは原典ハッシュとエンジン・言語・DPI等の設定で識別する。既存57PDFの統合抽出は、元チェックポイントから原典が不変であることを確認して一度だけハッシュへ束縛した。これは再OCRや本文校正を意味しない。
生OCRは保持する。変更された問題抽出はcontent-addressedなextracted/questions_raw/へ保存する。
校正・独自要旨はextracted/corrected/{question_id}/{hash}.jsonで、問題幹、条件、①〜⑤の対応、図参照、確認範囲・疑義を保持する。原典の誤答を科学的に正しい記述へ書き換えない。

## 境界と番号
PDF物理ページは1起算、OCR行番号は0起算。bboxは正規化された左下原点。開始・終了のページ、行、bboxを保存する。
heading_candidates.jsonは公式正答との結合前に認識した全候補・採否理由を保存する。番号を認識し、読順と見出し書式で選んだ後に公式正答へ照合する。
printed_number_observedは問題原典から認識した番号、printed_number_expectedは正答表の印刷表記。見出し生文字列も保持する。番号集合が一致しても本文境界の目視保証とはしない。
H27の2件以外のboundary_verifiedは一括昇格していない。

## 分類の軸
official_group（基礎の公式群）、discipline_id（学習分野）、chapter_id（TeX章）、concept_id（主概念）を区別する。
従来の大中小分類は表示・既存CSV互換用。基礎の大分類は公式群、middle_categoryはその中の学習分野である。学習分野とファイルは常に1対1ではない。
question_topics.csvは主概念と横断タグの関連表。主分類の問題数と複数タグの延べ数を混ぜない。concept_statistics.csvに主タグ・横断タグ・重複を除いた問題数・延べタグ数を別々に保存する。
概念が未確定ならconcept_idは空、表示は未確定。一般語を架空の細分類の根拠にしない。語句一致はclassification_evidence、競合はclassification_candidatesへ保存する。
体系の版は1.0-review1として固定し、今後の分割・統合は影響IDと理由を記録して版を変更する。
原典画像で点検した48問の主分類・主概念だけを確認済みにした。その他と全横断タグを標本から一括確認済みにしない。
有機・高分子章12、技術社会政策章07、金属の強化機構を扱う材料物性章13を追加した。

## 確認状態と証跡
answer_verifiedは互換の構造照合フラグで、解法確認を意味しない。answers_officialにparsed、structural_status、source_review_status、solution_review_statusを別々に持つ。
公式注記はpage_note_raw（全ページ注記）とofficial_note（当該問題への適用）を分ける。適用IDと訂正前値も保存する。
特殊6件の画像確認はanswer_verification_recordsから原典ハッシュ・ページが一致する場合にだけ導出する。通常の公式表は独立のbbox座標抽出でも48表・320セルを照合した。これも解法・全セル目視の保証ではない。

verification_recordsはquestion_id、確認kind、原典／内容ハッシュ、reviewer、reviewed_at、status、evidenceを保持する。校正JSON変更は内容ハッシュ、分類・要旨・解説列の変更はpayload_sha256によって旧確認が失効する。payload_bound_atは記録束縛日時で、過去のreviewed_atを変更しない。
summary_status=placeholder / draft / verified / staleを区別する。要旨・分類・校正・解法の確認は別kind。
needs_manual_verification=trueは本文条件または解釈に未確認がある状態。falseでも境界・解説・Astra査読の完了を意味しない。unresolved.csvは各未完了項目を独立に列挙する。
依存フラグのunknownをfalseと読まない。法令・制度・統計の出題時点と解説基準日を分ける。

## 難易度・優先度・類似関係
evaluation_rubric.jsonで、物理専攻大学院生を読者に固定する。専門知識の新規性、推論段階、計算負荷、図表読解を別評価し、実例と比較して総合1〜5の根拠を保存する。単純加算しない。
優先度は出題頻度、基礎性、転用性、学習時間、得点効率を別入力として承認する。未評価・学習時間未知は空欄。
校準例は基礎2・適性1・応用2。適性例には当時表現・他肢解釈の疑義があり、校準も初稿扱いである。
question_relations.csvで同概念、同解法、条件違い、近似再出題、完全再出題を区別する。数値・単位・否定・肢対応・図・時点差分と承認を保持する。OCR類似の候補157組から自動で再出題に昇格させない。

## 統計・教材・監査
topic_statistics.csvは16試験回と15年度の頻度を分け、全登録の暫定数と確認済み部分集合を並べる。未知の難易度を0にしない。少数の確認済み集合を全頻度の推定と読まない。
TeXの手書き章とgenerated/questionsのCSV所有ブロックを分ける。再生成は手書き本文を上書きしない。
S7開始時の作業版PDFは全問登録索引と5問の解説初稿を含んだ。最新処理数はREADME・SOL_PROGRESSとCSVで確認する。全問解説完成・Checkpoint 2条件達成を意味しない。
初期監査は件数・集合・正答・原典ハッシュ・スキーマ・参照・派生ビューを検査する。最終監査は未実装のため明示失敗する。make all、audit_completeness.py --finalが成功を出すことはない。
将来の最終条件は校正・全解説・誤答説明・参照／ラベル一意・引用・入力とPDFのビルド一致・専門査読証跡を束ねる。ラベルだけ／古いPDF／未解決参照を成功としない。

## S7執筆情報（既存設計の追加列）

questions.csvのchoice_reviewsは全5肢のvalue/verdict/reasonをJSONで持つ。answer_reason、learning_points、theory_references、authoring_batch、independent_answer、independent_solution_statusを追加した。公式と独立解答の相違はdiscrepancy_pendingで保存し、公式正答を保持する。原典照合はextracted/correctedの不変JSONとcontent/source/payloadハッシュへ結び付ける。classification/summary/correctionの検証と解説初稿の状態を別にする。

同じ解法がsolution_summaryとanswer_reasonに格納されている場合、表示だけを共通段落にまとめる。CSVの両列は保持する。手書き共通理論と問題固有生成ブロックを分離し、図・表の原典は転載せず独自の条件表現と検討を生成する。明示的な原典比較をした関係のみpublish_reviewed_relations.pyで登録する。類似スコアは承認根拠にしない。
