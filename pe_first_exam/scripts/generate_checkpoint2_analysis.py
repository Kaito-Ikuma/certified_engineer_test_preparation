"""Generate reproducible first-draft analysis from the canonical DB."""
import json
from collections import Counter, defaultdict
from common import ROOT, YEARS, read_csv, csv_bytes, json_bytes, publish_bundle, now
from tex_common import esc

def table(headers, rows, widths):
    lines=[r'\begin{longtable}{'+widths+'}', ' & '.join(headers)+r'\\\hline']
    lines += [' & '.join(esc(str(v)) for v in row)+r'\\' for row in rows]
    return '\n'.join(lines+[r'\end{longtable}'])

def main():
    rows=read_csv('data/questions.csv')
    assert len(rows)==1270 and all(r['solution_summary'] for r in rows)
    names={'BASIC':'基礎','APT':'適性','APPLIED':'応用理学'}
    by=defaultdict(list)
    for r in rows: by[(r['subject'],r['middle_category'])].append(r)
    records=[]
    for (s,c),group in sorted(by.items()):
        sessions={r['source_year_directory'] for r in group}
        years={r['year'] for r in group}
        recent=sum(r['source_year_directory'] in ('R03','R04','R05','R06','R07') for r in group)
        records.append(dict(subject=s,category=c,questions=len(group),sessions=len(sessions),
                            years=len(years),recent_questions=recent,
                            question_ids='|'.join(r['question_id'] for r in group),
                            scope='current primary middle-category assignment; not final Astra approval'))
    ranked={s:sorted([x for x in records if x['subject']==s],
                    key=lambda x:(-x['questions'],-x['sessions'],x['category']))
            for s in names}
    frequency=r'\chapter{全問初稿から読む出題頻度}'+'\n'
    frequency+='全1,270問の主分類から集計する。問題数は類似問も別々に数え、科目内の中分類は一問一所属である。16試験回と15年度を区別し、令和元年度再試験は回数では別、年度数では通常試験と同じ年度とする。分類は原典照合済みだが、教材解説の専門査読と分類体系の最終承認はこれからである。\n'
    for s in names:
        total=sum(r['subject']==s for r in rows)
        frequency+=r'\section{'+names[s]+'：'+str(total)+'問の構成}'+'\n'
        frequency+=table(['中分類','問数','試験回/16','年度/15'],
                         [(x['category'],x['questions'],x['sessions'],x['years']) for x in ranked[s]],
                         r'p{.57\linewidth}rrr')+'\n'
    frequency+='中分類間の粒度は同一ではない。物理探査等の大きな分類と個別の技法を同じ尺度で比較しない。概念タグの集計は主タグ・横断タグを分ける。複数タグの合計は問題総数と一致しない。\n'
    yearly=r'\chapter{年度推移と比較の分母}'+'\n'
    yearly+='平成23・24年度は基礎25問、それ以後は基礎30問である。適性15問、応用理学35問は各試験回で同じ登録範囲を使う。出題数の変化を概念の流行と判断する前に分母を確認する。\n'
    yr=[]
    for y in YEARS:
        group=[r for r in rows if r['source_year_directory']==y]
        if group:yr.append((y,*[sum(r['subject']==s for r in group) for s in names],len(group)))
    yearly+=table(['試験回','基礎','適性','応用理学','合計'],yr,r'lrrrr')+'\n'
    yearly+=r'\section{令和3〜7年度の五回と全期間の比較}'+'\n'
    yearly+='後期五回は基礎150、適性75、応用理学175問を分母にする。全期間の構成比と後期の構成比は、同じ主分類で比較する。数ポイントの差だけで単調な増減や次年度の出題を断定しない。\n'
    recent_totals={'BASIC':150,'APT':75,'APPLIED':175}
    trend=[]
    for s in names:
        total=sum(r['subject']==s for r in rows)
        for x in ranked[s][:6]:
            trend.append((names[s],x['category'],f"{100*x['questions']/total:.1f}",x['recent_questions'],
                          f"{100*x['recent_questions']/recent_totals[s]:.1f}"))
    yearly+=table(['科目','中分類','全期間\\%','後期問数','後期\\%'],trend,r'lp{.40\linewidth}rrr')+'\n'
    yearly+='再試験を通常年の傾向へ二重に算入する効果、分類境界の変更、主題が同じでも問い方が変わる効果を区別する。ここでは長期構成と後期構成の記述的比較までを行い、有意差や予測確率は計算していない。\n'
    relations=[r for r in read_csv('data/question_relations.csv') if r['approval_status']=='verified']
    counts=Counter(r['relation_type'] for r in relations)
    repeated=r'\chapter{類似問題は関係の種類で読み分ける}'+'\n'
    repeated+='原典を比較して承認した関係だけを集計する。同概念、同解法、条件違い、近似再出題、完全再出題は別の意味であり、OCR類似候補を再出題と認定しない。辺の数は比較した対の数であって出題された問題数ではない。一問が複数の辺に接続するため、辺数を総問題数へ加算しない。\n'
    repeated+=table(['関係','承認対数'],[(k,counts[k]) for k in ('same_concept','same_method','parameter_variant','near_repeat','exact_repeat')],r'p{.65\linewidth}r')+'\n'
    repeated+=r'\section{条件が同じでも番号を移さない}'+'\n'
    examples=[('H23-REG-BASIC-5-3','R05-REG-BASIC-5-4','標準メタンと液体密度から体積比。H29では候補順が異なる。'),
              ('H30-REG-BASIC-5-5','R03-REG-BASIC-5-5','WattからHahnまでの五業績。文字割当と候補順が異なる。'),
              ('R03-REG-BASIC-5-6','R07-REG-BASIC-5-6','1〜5期から2〜6期へ移り、ポスドクと総合知が入れ替わる。'),
              ('H28-REG-BASIC-5-1','R06-REG-BASIC-5-2','物質収支の方法は共通。値と不適切な命題は異なる。')]
    for l,r,reason in examples:
        repeated+=r'\paragraph{'+esc(l+'／'+r)+'} '+reason+r' \hyperref[q:'+l.lower()+r']{前の問題}と\hyperref[q:'+r.lower()+r']{後の問題}の各条件へ戻る。'+'\n'
    repeated+='主概念の名前が分かれている同型もあるため、概念タグの頻度だけでは再出題の全てを捉えない。未比較の対が多く、承認数は再出題総数の確定値ではない。完全再出題の承認が0でも、全資料に完全再出題が存在しないとの結論にはならない。\n'
    priority=r'\chapter{学習順序を頻度と転用性から組み立てる}'+'\n'
    priority+='大学院物理の背景がある読者は、既知の力学・熱・電磁気を原典の条件確認で回収し、情報・化学・地球科学・制度の新規概念へ時間を配分する。次の列挙は出題数による着手候補であり、習得時間を測ったS/A/B/Cの確定優先度ではない。難易度は校準初稿、学習時間と得点効率は未評価として残す。\n'
    for s in names:
        priority+=r'\section{'+names[s]+'の頻度上位に接続する基礎}'+'\n'
        priority+='、'.join(x['category']+'（'+str(x['questions'])+'問）' for x in ranked[s][:5])+'を最初の点検対象とする。\n'
    priority+='基礎は保存則、単位、論理、確率と待ち行列の成立条件を共通の道具にする。適性は技術士法の義務責務と、公益・安全・説明責任を別の根拠で整理する。応用理学は波の伝播・場・収支を物理探査へつなぎ、鉱物・岩石・地層・年代・同位体を用語と観測証拠から学ぶ。\n'
    priority+='頻度の低い問題も索引と解説から除外しない。高リスクの法令や歴史統計は解説の留保を先に読み、出題時点の原典と現在の参考説明を分ける。頻度だけで誤った初稿を反復学習しない。\n'
    strategy=r'\chapter{全問索引を使う学習と選択戦略}'+'\n'
    strategy+='一回目は年度順に原典条件と独立解法を確認し、二回目は概念索引で同型を比較する。既知の問題でも候補順、否定方向、図の境界条件、統計年を変えて確認する。公式正答の暗記だけで解法を再現できたと判定しない。\n'
    strategy+=r'\section{科目ごとの確認手順}'+'\n'
    strategy+='基礎では各年度の群別構成を原典で確認し、計算量・図の読解・新規知識を見積もって選ぶ。適性では五肢の全称表現と責任主体を点検する。応用理学では物理・化学・地球科学の全収録範囲を概観し、用語だけの選択と条件付きの計算を区別する。\n'
    strategy+='本書の登録数は公開問題の収録数であり、受験者が実際に回答する数と同じではない。過去の試験条件は各年の問題冒頭へ戻り、現在の受験案内の条件を遡及させない。学習時間・得点効率が未測定のため、分刻みの時間配分や次回出題確率は提示しない。\n'
    strategy+=r'\section{留保を解消する復習記録}'+'\n'
    strategy+='誤答した問題は、知識不足、条件の読み違い、計算、候補対応、資料時点のいずれが原因か記録する。公式複数正答では受理集合と自分が独立に求めた答えを別に残す。全員正解の公式措置は科学的命題が全て正しいことを意味しない。査読待ち問題を学習上の確定根拠にする前に未解決表を確認する。\n'
    files={'data/checkpoint2_frequency_analysis.csv':csv_bytes(records),
           'chapters/analysis/01_frequency_analysis.tex':frequency,
           'chapters/analysis/02_yearly_trends.tex':yearly,
           'chapters/analysis/03_repeated_topics.tex':repeated,
           'chapters/analysis/04_priority_topics.tex':priority,
           'chapters/analysis/05_exam_strategy.tex':strategy,
           'extracted/logs/checkpoint2_analysis_record.json':json_bytes({'time':now(),'questions':len(rows),'middle_groups':len(records),'approved_relation_pairs':len(relations),'relation_counts':dict(counts),'prediction_performed':False,'learning_time_evaluated':False,'status':'first_draft_pending_astra'})}
    publish_bundle(files)
    print('Published CP2 analysis first draft:',len(records),'groups',len(relations),'approved relation pairs')

if __name__=='__main__':main()
