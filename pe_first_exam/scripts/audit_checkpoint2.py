"""Checkpoint 2 draft readiness; deliberately not final expert sign-off."""
import json,re
from collections import Counter
from common import ROOT,read_csv,csv_bytes,json_bytes,publish_bundle,now,digest
from tex_graph import input_graph

def main():
    rows=read_csv('data/questions.csv');errors=[]
    counts=Counter(r['subject'] for r in rows)
    if dict(counts)!={'BASIC':470,'APT':240,'APPLIED':560}:errors.append('unexpected subject totals')
    graph,graph_errors=input_graph();errors+=graph_errors
    text='\n'.join(graph.values())
    labels=set(re.findall(r'\\label\{([^}]+)\}',text))
    queue=[]
    for r in rows:
        q=r['question_id']
        for k in ('question_summary','core_concept','required_knowledge','solution_summary','answer_reason','learning_points','theory_references','independent_answer','choice_reviews'):
            if not r.get(k):errors.append(q+': missing '+k)
        if r['astra_review_required']!='true':errors.append(q+': unflagged draft')
        if r['solution_review_status']!='draft_pending_astra':errors.append(q+': unexpected solution state')
        if len(json.loads(r['choice_reviews'] or '{}'))!=5:errors.append(q+': not five option reviews')
        for label in r['theory_references'].split('|'):
            if label not in labels:errors.append(q+': missing theory label '+label)
        reasons=['all_solution_drafts']
        if r['needs_manual_verification']=='true':reasons.append('source_or_interpretation_pending')
        if r['difficulty'] in ('4','5'):reasons.append('difficulty_4_5')
        if r['requires_law']=='true':reasons.append('law_or_institution')
        if r['requires_figure']=='true':reasons.append('figure_dependent')
        if r['answer_kind']!='single':reasons.append('official_special_handling')
        if r['independent_solution_status']=='discrepancy_pending':reasons.append('independent_discrepancy')
        if r['independent_solution_status']=='accepted_official_member_draft':reasons.append('accepted_member_not_full_set')
        if r['subject']=='APPLIED' and ('geology/' in r['tex_file'] or 'geophysics_geochemistry/' in r['tex_file']):reasons.append('earth_science')
        queue.append({k:r[k] for k in ('question_id','subject','source_file','source_page','source_sha256','corrected_content_file','corrected_content_sha256','tex_file','tex_label','difficulty','needs_manual_verification','official_answer','answer_kind','independent_answer','independent_solution_status','explanation_citations','notes')}|{'review_reasons':'|'.join(reasons),'status':'pending_astra'})
    analysis=['chapters/analysis/'+n+'.tex' for n in ('01_frequency_analysis','02_yearly_trends','03_repeated_topics','04_priority_topics','05_exam_strategy')]
    for p in analysis:
        if p not in graph or len(graph[p])<400:errors.append('missing substantive analysis '+p)
    metrics={'time':now(),'registered_questions':len(rows),'subject_drafts':dict(counts),'all_five_choices':sum(len(json.loads(r['choice_reviews'] or '{}'))==5 for r in rows),'all_theory_connected':sum(bool(r['theory_references']) for r in rows),'astra_flags':sum(r['astra_review_required']=='true' for r in rows),'manual_required':sum(r['needs_manual_verification']=='true' for r in rows),'source_correction_states':dict(Counter(r['correction_status'] for r in rows)),'independent_states':dict(Counter(r['independent_solution_status'] for r in rows)),'difficulty_4_5':sum(r['difficulty'] in ('4','5') for r in rows),'law_questions':sum(r['requires_law']=='true' for r in rows),'figure_questions':sum(r['requires_figure']=='true' for r in rows),'analysis_chapters':len(analysis),'csv_sha256':digest(ROOT/'data/questions.csv'),'draft_readiness_passed':not errors,'final_expert_signoff':False,'errors':errors}
    publish_bundle({'data/checkpoint2_review_queue.csv':csv_bytes(queue),'extracted/logs/checkpoint2_draft_audit.json':json_bytes(metrics)})
    print(json.dumps(metrics,ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
