"""Generate CSV-owned question blocks; never overwrite authored chapter prose."""
import json
from collections import defaultdict
from common import ROOT,read_csv,publish_bundle
from tex_common import esc

def main():
    qs=read_csv('data/questions.csv');tax=json.loads((ROOT/'config/taxonomy.json').read_text())['categories'];groups=defaultdict(list);files={}
    for r in qs:groups[r['tex_file']].append(r)
    supplements={s['file']:s['title'] for s in json.loads((ROOT/'config/supplementary_chapters.json').read_text())['chapters']}
    order=('basic/','aptitude/','applied_science/physics_chemistry/','applied_science/geophysics_geochemistry/','applied_science/geology/')
    paths=sorted(set(t['file'] for t in tax)|set(supplements),key=lambda p:(next(i for i,k in enumerate(order) if k in p),p));inputs=[]
    for path in paths:
        titles=list(dict.fromkeys(t['middle'] for t in tax if t['file']==path));title=supplements[path] if path in supplements else PathTitle(path,titles)
        gen='generated/questions/'+path.removeprefix('chapters/');blocks=[]
        for r in groups[path]:
            blocks.append(r'\subsection{'+esc(r['era_year']+' 問'+r['question_number'])+'}\n'+r'\label{'+r['tex_label']+'}')
            blocks.append(r'\noindent\textbf{原典：} '+esc(r['source_file'])+'、PDF物理'+r['source_page']+'頁。')
            blocks.append(r'\textbf{公式正答：} '+esc(r['official_answer'])+'（'+esc(r['answer_kind'])+'）。')
            if r['summary_verified']=='true':
                for heading,key in [('問題の要旨','question_summary'),('必要知識','required_knowledge'),('考え方（査読待ち初稿）','solution_summary'),('他の選択肢（査読待ち初稿）','wrong_choice_summary')]:blocks.append(r'\paragraph{'+heading+'} '+esc(r[key]))
                if r.get('explanation_citations'):blocks.append(r'\par 参考：\cite{'+r['explanation_citations'].replace('|',',')+'}。')
                if r['related_question_ids']:blocks.append(r'\paragraph{関連問題} '+', '.join(r'\hyperref[q:'+x.lower()+']{'+esc(x)+'}' for x in r['related_question_ids'].split('|')))
                blocks.append(r'\par 難易度 '+esc(r['difficulty'])+'（校準初稿）、優先度未評価。')
            else:blocks.append(r'\par\textit{原典本文の校正と独自解説は未作成。分類のみの登録項目。}')
        files[gen]='\n\n'.join(blocks)+'\n'
        if not (ROOT/path).exists():
            note='補足の章骨格。現在のDBにこの章への主分類割当はなく、追加の出題実績を意味しない。本文は未執筆。' if path in supplements else '分野解説は執筆中。以下は登録問題と校正済み例の作業用一覧。'
            files[path]=r'\chapter{'+esc(title)+'}\n'+r'\noindent '+note+'\n'+r'\input{'+gen+'}\n'
        inputs.append(r'\input{'+path+'}')
    files['generated/chapter_inputs.tex']='\n'.join(inputs)+'\n'
    metrics=json.loads((ROOT/'extracted/logs/audit_metrics.json').read_text())
    files['generated/audit_summary.tex']=r'\chapter{作業状態と監査範囲}'+'\n'+f"登録 {len(qs)} 問、主分類確認済み {sum(r['classification_verified']=='true' for r in qs)} 問、要旨確認済み {sum(r['summary_verified']=='true' for r in qs)} 問。\n"+r'\par 解説は一部の初稿のみ。初期監査と最終監査を分け、最終完成は未判定。全問解説の完成教材ではない。'+'\n'
    stats=read_csv('data/topic_statistics.csv');lines=[r'\chapter{出題頻度（暫定集計）}',r'分類未確認を含む全登録値と、確認済みの部分集合を区別する。16試験回、15年度が分母。難易度未知を0として平均しない。',r'\begin{longtable}{p{.16\linewidth}p{.42\linewidth}rrr}',r'科目 & 大分類 & 暫定問数 & 確認済 & 出題回数\\\hline']
    for r in stats:
        if r['level']=='major_category':lines.append(esc(r['subject'])+' & '+esc(r['category'])+' & '+r['provisional_questions']+' & '+r['verified_questions']+' & '+r['provisional_sessions']+r'\\')
    lines.append(r'\end{longtable}');files['generated/frequency_tables.tex']='\n'.join(lines)+'\n'
    publish_bundle(files);print('Generated question blocks',len(qs),'chapter destinations',len(paths),'authored prose preserved')

def PathTitle(path,titles):
    if 'chapters/basic/' in path:return {'01':'設計・計画','02':'情報・論理','03':'解析','04':'材料・化学・バイオ','05':'環境・エネルギー・技術'}.get(path.split('/')[-1][:2],titles[0])
    return titles[0]
if __name__=='__main__':main()
