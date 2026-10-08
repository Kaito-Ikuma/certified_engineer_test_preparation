# 技術士第一次試験 全過去問体系化プロジェクト
## GPT-6.1 Sol 主力 + GPT-6 Astra 査読方式

あなたは VS Code 上の Codex エージェントとして、現在開いているローカルワークスペースを直接操作する。

本プロジェクトでは、

- **GPT-6.1 Sol：実作業・大量処理・執筆・コード実装の主担当**
- **GPT-6 Astra：重要な設計判断・難問・全体整合性の査読担当**

という役割分担を採用する。

重要：

**モデル切替を自分で実行できるとは仮定しないこと。**

モデル切替が必要なチェックポイントでは、指定された引継ぎファイルを生成し、作業状態を完全に保存したうえで停止すること。

ユーザーが手動でモデルを切り替えた後、同一リポジトリを読み直して続行する。

---

# 0. プロジェクトの目的

公益社団法人 日本技術士会が公開している技術士第一次試験について、

- 平成23年度
- 平成24年度
- 平成25年度
- 平成26年度
- 平成27年度
- 平成28年度
- 平成29年度
- 平成30年度
- 令和元年度
- 令和元年度再試験
- 令和2年度
- 令和3年度
- 令和4年度
- 令和5年度
- 令和6年度
- 令和7年度

を対象とし、

1. 基礎科目
2. 適性科目
3. 専門科目「応用理学部門」

の全問題を収集・解析・分類する。

その上で、

「年度別の過去問解説集」

ではなく、

**平成23年度〜令和7年度の全出題を、背景知識・理論・出題傾向・類似問題まで含めて体系的に理解できる日本語LaTeX教材**

を構築する。

最終的に、

```text
PDF
↓
問題DB
↓
分類
↓
頻度解析
↓
体系的教材
↓
年度別・テーマ別索引
↓
完全性監査
↓
LuaLaTeX PDF
```

まで一貫して構築する。

---

# 1. モデル運用方針

## GPT-6.1 Sol が担当するもの

以下は原則としてGPT-6.1 Solで実行する。

- ディレクトリ作成
- ファイル管理
- PDF一覧化
- PDFテキスト抽出
- PDFページ確認
- 問題分割
- CSV作成
- 正答データ登録
- 初期分類
- Pythonスクリプト作成
- 統計処理
- LaTeXファイル生成
- 本文大量執筆
- 年度別索引生成
- テーマ別索引生成
- 用語集生成
- 公式集生成
- `latexmk`
- コンパイルエラー修正
- Astra指摘事項の反映
- 完全性監査

大量の定型処理にAstraを浪費しない。

---

## GPT-6 Astra が担当するもの

Astraは次の3チェックポイントのみ原則使用する。

### ASTRA CHECKPOINT 1
**分類体系・データ設計の査読**

全問題DBの初期構築と初期分類が完了した直後。

### ASTRA CHECKPOINT 2
**難問・高リスク内容・教材品質の査読**

教材本文の初稿がある程度完成した段階。

### ASTRA CHECKPOINT 3
**最終全体査読**

全教材、索引、監査、PDFが完成した直後。

---

# 2. モデル切替プロトコル

Codexが自律的にモデル変更できるとは仮定しない。

Astraが必要になった場合、Solは必ず、

```text
handoff/
```

以下に引継ぎ文書を作成する。

例：

```text
handoff/
├── CHECKPOINT_1_FOR_ASTRA.md
├── ASTRA_REVIEW_1.md
├── CHECKPOINT_2_FOR_ASTRA.md
├── ASTRA_REVIEW_2.md
├── CHECKPOINT_3_FOR_ASTRA.md
└── ASTRA_REVIEW_3.md
```

Solはチェックポイントに到達したら、

1. 現在の作業を保存
2. `WORKLOG.md`を更新
3. 対象ファイル一覧を記録
4. Astraに確認させる論点を列挙
5. `CHECKPOINT_X_FOR_ASTRA.md`を生成
6. Git差分を確認
7. 作業を停止

する。

その際、チャットでは簡潔に、

```text
ASTRA CHECKPOINT X に到達しました。

次はモデルを GPT-6 Astra に切り替え、
「CHECKPOINT_X_FOR_ASTRA.md を読み、記載された査読を実施してください」
と指示してください。
```

と報告する。

---

# 3. Astra側の行動規則

Astraで再開された場合、最初に必ず、

```text
handoff/CHECKPOINT_X_FOR_ASTRA.md
```

を読む。

その後、指定された関連ファイルのみならず、必要に応じてプロジェクト構造全体を確認する。

Astraは原則として大量本文を直接書き換えない。

主な役割は、

```text
問題発見
↓
原因分析
↓
改善方針
↓
修正指示
```

である。

結果は、

```text
handoff/ASTRA_REVIEW_X.md
```

へ保存する。

各指摘には、

```text
Severity:
Critical / High / Medium / Low

Target:
対象ファイルまたは問題ID

Problem:
問題点

Reason:
問題である理由

Recommended fix:
推奨修正

Verification:
修正後に何を確認すべきか
```

を記載する。

Astraの査読完了後は、

```text
Astra査読が完了しました。

次は GPT-6.1 Sol に戻し、
「ASTRA_REVIEW_X.md を読み、全指摘を反映して続行してください」
と指示してください。
```

と報告して停止する。

---

# 4. ディレクトリ構造

最終的に最低限、

```text
pe_first_exam/
├── README.md
├── AGENTS.md
├── WORKLOG.md
├── Makefile
├── latexmkrc
├── main.tex
├── references.bib
│
├── sources/
│   ├── H23/
│   ├── H24/
│   ├── H25/
│   ├── H26/
│   ├── H27/
│   ├── H28/
│   ├── H29/
│   ├── H30/
│   ├── R01/
│   ├── R01_retest/
│   ├── R02/
│   ├── R03/
│   ├── R04/
│   ├── R05/
│   ├── R06/
│   └── R07/
│
├── extracted/
│   ├── text/
│   ├── pages/
│   └── logs/
│
├── data/
│   ├── source_files.csv
│   ├── questions.csv
│   ├── answers_official.csv
│   ├── classifications.csv
│   ├── topic_statistics.csv
│   ├── unresolved.csv
│   └── audit_report.csv
│
├── scripts/
│   ├── scan_sources.py
│   ├── extract_pdf_text.py
│   ├── build_question_db.py
│   ├── validate_answers.py
│   ├── classify_questions.py
│   ├── generate_statistics.py
│   ├── generate_year_index.py
│   ├── generate_topic_index.py
│   ├── audit_completeness.py
│   ├── audit_tex_labels.py
│   └── build_all.py
│
├── chapters/
│   ├── 00_exam_overview.tex
│   ├── 01_study_guide.tex
│   │
│   ├── basic/
│   │   ├── 00_overview.tex
│   │   ├── 01_design_planning.tex
│   │   ├── 02_information_logic.tex
│   │   ├── 03_analysis.tex
│   │   ├── 04_material_chemistry_biology.tex
│   │   └── 05_environment_energy_technology.tex
│   │
│   ├── aptitude/
│   │   ├── 00_overview.tex
│   │   ├── 01_engineer_act.tex
│   │   ├── 02_engineering_ethics.tex
│   │   ├── 03_compliance_accountability.tex
│   │   ├── 04_safety_risk.tex
│   │   ├── 05_environment_sustainability.tex
│   │   └── 06_research_information_ethics.tex
│   │
│   ├── applied_science/
│   │   ├── 00_overview.tex
│   │   ├── physics_chemistry/
│   │   ├── geophysics_geochemistry/
│   │   └── geology/
│   │
│   └── analysis/
│       ├── 01_frequency_analysis.tex
│       ├── 02_yearly_trends.tex
│       ├── 03_repeated_topics.tex
│       ├── 04_priority_topics.tex
│       └── 05_exam_strategy.tex
│
├── generated/
│   ├── yearly_index.tex
│   ├── topic_index.tex
│   ├── frequency_tables.tex
│   └── audit_summary.tex
│
├── appendix/
│   ├── formulas.tex
│   ├── glossary.tex
│   ├── all_questions.tex
│   └── methodology.tex
│
├── handoff/
│
└── build/
    └── main.pdf
```

を構築する。

---

# 5. 最重要設計原則

## CSVをSingle Source of Truthとする

教材本文を正本にしてはいけない。

全問題を、

```text
data/questions.csv
```

へ登録する。

最低限、

```text
question_id
year
era_year
exam_session
subject
question_number
source_file
source_page
major_category
middle_category
minor_category
topic
subtopic
question_type
requires_calculation
requires_figure
requires_law
difficulty
priority
official_answer
answer_verified
question_summary
core_concept
required_knowledge
solution_summary
wrong_choice_summary
related_question_ids
tex_label
tex_file
status
needs_manual_verification
notes
```

を持たせる。

---

# 6. 推測禁止

以下を推測で埋めない。

- 問題文
- 数値
- 正答
- 年度
- 問題番号
- 図表内容
- 法令
- 化学式
- 地質年代

確認不能なら、

```text
needs_manual_verification = true
```

とする。

---

# 7. Phase S0 — GPT-6.1 Sol
## プロジェクト初期化

現在のワークスペースを確認する。

既存データを破壊しない。

必要なディレクトリ、

```text
README.md
AGENTS.md
WORKLOG.md
Makefile
latexmkrc
```

等を作成する。

`AGENTS.md`には最低限、

- 対象年度
- 対象科目
- Sol/Astra分業
- CSVが正本
- 推測禁止
- 全問収録
- LuaLaTeX
- Astraチェックポイント
- 完全性監査

を記録する。

---

# 8. Phase S1 — GPT-6.1 Sol
## 原典収集・PDF解析

原則として、

**公益社団法人 日本技術士会の公式PDF**

のみを問題・正答の一次資料とする。

`sources/`内を走査する。

不足資料についてネットワーク利用可能なら公式資料を取得する。

不可能なら、

```text
sources/MISSING_SOURCES.md
```

を作成する。

PDF解析は通常テキスト抽出を優先する。

OCRは通常抽出不能部分に限る。

数式、図、化学式、グラフ等は必要に応じてページ画像も確認する。

---

# 9. Phase S2 — GPT-6.1 Sol
## 全問題DB構築

全年度・全対象科目について問題を登録する。

一問たりとも代表例扱いで省略しない。

一意なIDを作る。

例：

```text
H23-REG-BASIC-1-1
R01-RET-APPLIED-12
R07-REG-APT-09
```

公式正答も登録する。

---

# 10. Phase S3 — GPT-6.1 Sol
## 初期分類

### 基礎科目

大分類：

```text
設計・計画
情報・論理
解析
材料・化学・バイオ
環境・エネルギー・技術
```

### 適性科目

例：

```text
技術士法
技術者倫理
公益確保
守秘義務
信用失墜
資質向上
説明責任
安全
リスク
品質
知的財産
研究倫理
情報倫理
環境
持続可能性
コンプライアンス
```

### 応用理学

```text
物理及び化学
地球物理及び地球化学
地質
```

さらに中分類・小分類へ整理する。

---

# 11. ASTRA CHECKPOINT 1
## 分類体系とDB設計の査読

次の条件を満たしたらSolは停止する。

- 原典一覧作成済み
- questions.csv 初版完成
- 全問題の初期登録完了
- 初期分類完了
- 問題数の暫定監査完了

Solは、

```text
handoff/CHECKPOINT_1_FOR_ASTRA.md
```

を生成する。

内容：

```text
# Astra Checkpoint 1

## 目的
全問題DBと分類体系の査読。

## Astraに確認してほしい事項

1. 大分類・中分類・小分類が学問体系として妥当か
2. 分類粒度が過剰または粗すぎないか
3. 特に応用理学の分類が自然か
4. 同一テーマが複数カテゴリへ不自然に分裂していないか
5. information_logic の体系が情報工学学習にも有用か
6. questions.csv のスキーマで後工程に不足がないか
7. 難易度・優先度評価方式が妥当か
8. 類似問題検出方法が妥当か
9. 誤分類の可能性が高い問題ID
10. 後工程で問題になりそうな設計上の欠陥

## 出力先
handoff/ASTRA_REVIEW_1.md
```

ここでSolは停止する。

---

# 12. Astra Review 1

Astraは分類体系そのものを重点的に査読する。

特に、

- 物理と地球物理の境界
- 化学と地球化学の境界
- 地質と物理探査
- 基礎科目「解析」の分類
- 情報・論理

を厳密に確認する。

必要ならカテゴリ統合・分割を提案する。

全問題を再執筆する必要はない。

結果を、

```text
handoff/ASTRA_REVIEW_1.md
```

へ保存して停止する。

---

# 13. Phase S4 — GPT-6.1 Sol
## Astra Review 1反映

`ASTRA_REVIEW_1.md`を読み、

Critical → High → Medium → Low

の順で反映する。

分類変更時には全問題DBも一括更新する。

変更履歴をWORKLOGへ記録する。

その後、分類体系を原則凍結する。

---

# 14. Phase S5 — GPT-6.1 Sol
## 統計・類似問題解析

以下を生成する。

```text
data/topic_statistics.csv
```

最低限、

- 大分類別問題数
- 中分類別問題数
- 小分類別問題数
- 出題年度
- 出題頻度
- 最終出題年
- 類似問題
- 再出題
- 問題難易度

を集計する。

---

# 15. Phase S6 — GPT-6.1 Sol
## TeX骨格作成

LuaLaTeXを使用する。

`main.tex`から全章を読み込めるようにする。

教材は年度順ではなく、

```text
背景
↓
基本概念
↓
理論
↓
重要式
↓
技術的意味
↓
過去問での問われ方
↓
具体的過去問
```

の体系とする。

---

# 16. Phase S7 — GPT-6.1 Sol
## 本文大量執筆

対象読者：

**大学院理学研究科・物理学専攻程度**

とする。

数学・物理については過度に初歩へ戻らない。

一方、

- 化学
- 地球化学
- 地質
- 法律
- 倫理
- 情報工学

は背景から説明する。

---

## 各テーマ標準構成

```latex
\section{テーマ名}

\subsection{背景}
\subsection{基本概念}
\subsection{理論}
\subsection{重要な式}
\subsection{物理的・技術的意味}
\subsection{技術士第一次試験での出題ポイント}
\subsection{過去問}
\subsection{頻出ポイント}
\subsection{まとめ}
```

---

## 過去問

```latex
\subsubsection{令和○年度 問○}
\label{q:...}

\paragraph{問題の要旨}

\paragraph{問われていること}

\paragraph{必要知識}

\paragraph{考え方}

\paragraph{正答}

\paragraph{他の選択肢}

\paragraph{この問題から覚えること}

\paragraph{関連問題}
```

---

# 17. 重点的に詳しく説明する事項

特に、

- 地震波
- 地球内部
- 重力
- 地磁気
- プレート
- 火山
- 気象
- 同位体
- 鉱物
- 岩石
- 構造地質
- 地下水
- 物理探査

については、

**既知の物理学が地球科学へどう適用されるか**

を説明する。

---

# 18. 情報工学への接続

基礎科目「情報・論理」では必要に応じて、

```latex
\begin{tcolorbox}[title=情報工学への接続]
...
\end{tcolorbox}
```

を置く。

接続先：

- アルゴリズム
- 計算量
- データ構造
- OS
- コンピュータアーキテクチャ
- ネットワーク
- DB
- セキュリティ
- ソフトウェア工学
- AI
- データ分析

ただし第一次試験対策から逸脱しすぎない。

---

# 19. 難問フラグ

Astra Checkpoint 2に備え、

以下のいずれかに該当する問題に、

```text
astra_review_required = true
```

相当の管理を行う。

対象：

- difficulty = 4 または 5
- needs_manual_verification = true
- 法令問題
- 正答理由に曖昧さがある
- 高度な地球化学
- 高度な地質
- 高度な地球物理
- 複数解釈可能性
- 図表依存問題
- 説明に自信が低い
- 公式解答との整合理由が不明瞭

必要ならCSV列を追加する。

---

# 20. ASTRA CHECKPOINT 2
## 難問・高リスク内容査読

以下が成立した段階でSolは停止する。

- 基礎科目初稿完成
- 適性科目初稿完成
- 応用理学初稿完成
- 難問フラグ付与完了
- 頻度分析初稿完成

作成：

```text
handoff/CHECKPOINT_2_FOR_ASTRA.md
```

内容：

```text
# Astra Checkpoint 2

## 主目的

教材内容の専門的査読。

## 最優先対象

1. astra_review_required の全問題
2. difficulty 4–5
3. needs_manual_verification
4. 法令・制度
5. 地球化学
6. 地質
7. 地球物理の難問
8. 説明と公式正答が直感的に一致しない問題

## 章単位査読

以下も確認する。

- 理論説明に物理的誤りがないか
- 過度な一般化がないか
- 数式の成立条件が欠けていないか
- 地質用語説明が循環定義になっていないか
- 適性科目で現在制度と当時制度を混同していないか
- 情報工学への接続が誤っていないか
- 類似問題統合が過剰でないか

## 出力

handoff/ASTRA_REVIEW_2.md
```

停止する。

---

# 21. Astra Review 2

Astraは原則として、

**全問題を最初から再処理しない。**

高リスク項目を深く査読する。

ただし重大な体系的問題を発見した場合は、その影響範囲も確認する。

結果を、

```text
handoff/ASTRA_REVIEW_2.md
```

へ保存する。

---

# 22. Phase S8 — GPT-6.1 Sol
## Astra Review 2反映

全指摘を重要度順に処理する。

修正済み項目には、

```text
resolved
```

を記録する。

解決不能なら理由を残す。

---

# 23. Phase S9 — GPT-6.1 Sol
## 索引・付録

CSVから自動生成する。

```text
generated/yearly_index.tex
generated/topic_index.tex
generated/frequency_tables.tex
appendix/formulas.tex
appendix/glossary.tex
appendix/all_questions.tex
```

年度別索引により、

**全問題がどこで扱われているか追跡可能**

にする。

---

# 24. Phase S10 — GPT-6.1 Sol
## 学習戦略

以下を作成。

```text
chapters/analysis/04_priority_topics.tex
chapters/analysis/05_exam_strategy.tex
```

対象受験者：

- 物理学専攻大学院生
- 数学・物理が得意
- 化学・地質等は専門外
- 将来は情報工学系技術士も検討

とする。

テーマを、

```text
S
A
B
C
```

で優先順位付けする。

頻度だけでなく、

- 基礎性
- 他テーマへの波及
- 得点効率
- 学習時間

も考慮する。

---

# 25. Phase S11 — GPT-6.1 Sol
## 完全性監査

`scripts/audit_completeness.py`

で最低限、

```text
期待問題数
DB登録数
正答確認数
分類数
TeX割当数
解説済数
未処理数
```

を年度・科目別に確認する。

---

## 合格条件

```text
missing_questions = 0
duplicate_question_ids = 0
unclassified_questions = 0
questions_without_tex = 0
unverified_official_answers = 0
```

を目標とする。

---

# 26. Phase S12 — GPT-6.1 Sol
## LaTeXビルド

```bash
latexmk -lualatex main.tex
```

等を使用する。

エラーを修正する。

以下を残さない。

```text
Undefined control sequence
LaTeX Error
Missing $
Runaway argument
Duplicate label
Undefined reference
Undefined citation
```

軽微なOverfull boxも可能な範囲で修正する。

---

# 27. ASTRA CHECKPOINT 3
## 最終査読

次の状態でSolは停止する。

- PDFビルド成功
- 完全性監査成功
- 未処理問題ゼロまたは理由付き
- 全章完成
- 索引完成
- 学習戦略完成

作成：

```text
handoff/CHECKPOINT_3_FOR_ASTRA.md
```

内容：

```text
# Astra Checkpoint 3

## 目的

完成版の最終品質保証。

## 確認事項

1. 教材全体の体系性
2. 学問的誤り
3. 論理的不整合
4. 章間重複
5. 説明不足
6. 過剰説明
7. 分類の不自然さ
8. 学習優先度の妥当性
9. 物理学専攻者向けとして適切か
10. 情報工学への接続が妥当か
11. 完全性監査設計が十分か
12. 重大な見落としがないか

## 特に確認するファイル

- main.tex
- data/audit_report.csv
- generated/audit_summary.tex
- chapters/analysis/
- handoff/ASTRA_REVIEW_1.md
- handoff/ASTRA_REVIEW_2.md

## 出力

handoff/ASTRA_REVIEW_3.md
```

停止する。

---

# 28. Astra Review 3

Astraは完成物に対する査読者として振る舞う。

特に、

**Critical / High**

の問題発見を最優先する。

細かな文章美より、

- 誤答誘発
- 理論誤り
- 法令誤り
- 完全性不足
- 分類ミス
- 数式誤り

を重視する。

結果を、

```text
handoff/ASTRA_REVIEW_3.md
```

へ保存する。

---

# 29. Phase S13 — GPT-6.1 Sol
## 最終修正

Astra Review 3をすべて確認する。

CriticalおよびHighは必ず処理する。

Mediumは原則処理する。

Lowは教材品質を損なわない範囲で処理する。

その後、

```text
make all
```

または同等処理を再実行する。

---

# 30. Final Audit

最終状態として、

```text
missing_questions = 0
duplicate_question_ids = 0
unclassified_questions = 0
questions_without_tex = 0
unverified_official_answers = 0
broken_tex_references = 0
undefined_citations = 0
latex_build_errors = 0
```

を確認する。

例外がある場合は、

```text
FINAL_EXCEPTIONS.md
```

へ、

- 問題ID
- 理由
- 影響
- 人間による確認が必要な点

を記録する。

---

# 31. コンテキスト管理

プロジェクト全体を会話履歴だけで保持しようとしない。

重要情報は必ずファイルに保存する。

特に、

```text
AGENTS.md
WORKLOG.md
questions.csv
ASTRA_REVIEW_X.md
```

を次セッションへの状態保存として利用する。

---

# 32. 使用量最適化ルール

Astraの利用量を節約するため、以下はAstraへ渡さない。

- ディレクトリ作成
- 単純CSV編集
- TeX形式統一
- 単純コンパイルエラー
- 年度別索引生成
- 表生成
- 重複除去
- 定型的説明

これらはSolで処理する。

Astraは、

**判断品質の差が教材全体へ波及する部分**

に集中させる。

---

# 33. Astra査読対象の優先順位

Astraの入力が巨大になりすぎる場合は、

```text
1. Critical候補
2. 未確認問題
3. difficulty 5
4. difficulty 4
5. 地質・地球化学
6. 法令
7. 体系設計
8. その他
```

の順に処理する。

内容を無断で捨てるのではなく、必要なら複数の査読バッチへ分割する。

---

# 34. 著作権

公式問題本文を大量にそのまま転載することを目的にしない。

問題内容は、

**本質を失わない正確な要約**

とする。

自作解説・数式・模式図を中心に教材化する。

元問題の図版は原則として再配布しない。

必要ならTikZ等で独自に再構成する。

---

# 35. 作業ログ

各Phase終了時に、

```text
WORKLOG.md
```

へ、

```text
日時
使用モデル
Phase
実施内容
変更ファイル
監査結果
未解決事項
次工程
```

を追記する。

---

# 36. Git

適宜、

```bash
git status
git diff
```

を確認する。

既存の無関係なファイルを変更しない。

ユーザーから明示されない限りremoteへpushしない。

---

# 37. 最終報告

最終完了時は長大な本文をチャットへ再掲しない。

以下のみ報告する。

```text
総問題数
基礎科目問題数
適性科目問題数
応用理学問題数
令和元年度再試験問題数
Astra査読3回の概要
監査結果
未解決事項
main.pdfのパス
主要成果物のパス
```

---

# 38. 開始時のモデル判定

このプロンプトを最初に実行しているモデルがGPT-6.1 Solである場合：

**Phase S0から開始する。**

Astraである場合：

`handoff/`内の未処理CHECKPOINTを探し、

```text
CHECKPOINT_X_FOR_ASTRA.md
```

が存在する場合のみAstra査読を行う。

チェックポイントが存在しない場合、Astraで大量作業を開始せず、

「通常作業はGPT-6.1 Solで開始してください」

と報告して停止する。

---

# 39. 最終原則

このプロジェクトでは、

**Sol = 実装者・執筆者**

**Astra = 査読者・設計レビュー担当**

とする。

Astraの能力を単純作業に消費せず、

- 分類体系
- 難問
- 高リスク内容
- 完成版品質

の判断へ集中させる。

一方でSolには、

- 大量処理
- 実装
- ファイル編集
- 執筆
- 自動化
- 修正

を徹底して担当させる。

---

# 開始指示

現在GPT-6.1 Solであるなら、ただちに

```text
Phase S0
```

から開始する。

まずワークスペースを調査し、必要なファイル・ディレクトリを構築する。

次に公式PDFの存在を確認し、

```text
S0 → S1 → S2 → S3
```

まで進める。

**Astra Checkpoint 1に到達するまでは、原則としてユーザーへモデル切替を要求しない。**

全問題DBと分類初版が完成した時点でのみ、

```text
CHECKPOINT_1_FOR_ASTRA.md
```

を生成して停止する。

作業を開始せよ。