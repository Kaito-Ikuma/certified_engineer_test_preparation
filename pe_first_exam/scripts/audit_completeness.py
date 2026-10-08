"""Registration/correction diagnostics; final sign-off is deliberately unavailable."""
import argparse,json
from collections import Counter
from common import ROOT,YEARS,SUBJECTS,read_csv,csv_bytes,json_bytes,publish_bundle,digest
from validate_schema import validate_rows
from validate_answers import verify
from tex_graph import input_graph

def audit(questions,official,classification,sources,check_hashes=True):
    errors=[];counts=Counter(r['question_id'] for r in questions);expected={r['question_id'] for r in official};actual=set(counts)
    cls_count=Counter(r['question_id'] for r in classification)
    if any(n!=1 for n in cls_count.values()) or set(cls_count)!=actual:errors.append('classification duplicate/missing/extra IDs')
    try:validate_rows(questions,source_rows=sources)
    except ValueError as ex:errors.append(str(ex))
    try:verify(official,questions,hash_check=check_hashes)
    except ValueError as ex:errors.append(str(ex))
    bysource={r['path']:r for r in sources};cls={r['question_id']:r for r in classification}
    if check_hashes:
        for r in sources:
            path=ROOT/r['path']
            if not path.exists() or digest(path)!=r['sha256']:errors.append('source missing/changed '+r['path'])
    report=[];unresolved=[];tex_missing=0
    topics=read_csv('data/question_topics.csv') if (ROOT/'data/question_topics.csv').exists() else []
    pairs=[(r['question_id'],r['concept_id']) for r in topics]
    if len(pairs)!=len(set(pairs)):errors.append('duplicate question_topics key')
    allowed={r['id'] for r in json.loads((ROOT/'config/concepts.json').read_text())['concepts']}
    for r in topics:
        if r['question_id'] not in actual or r['concept_id'] not in allowed:errors.append('invalid question_topics FK')
    byquestion={r['question_id']:r for r in questions}
    relations=read_csv('data/question_relations.csv') if (ROOT/'data/question_relations.csv').exists() else []
    relation_keys=[]
    for r in relations:
        left,right=r['left_question_id'],r['right_question_id'];kind=r['relation_type']
        relation_keys.append((*sorted((left,right)),kind))
        if left==right or left not in actual or right not in actual:errors.append('invalid relationship FK')
        if kind not in ('same_concept','same_method','parameter_variant','near_repeat','exact_repeat'):errors.append('invalid relationship type')
        if r['approval_status']=='verified' and (left not in byquestion or right not in byquestion or r['source_hash_left']!=byquestion[left]['source_sha256'] or r['source_hash_right']!=byquestion[right]['source_sha256']):errors.append('stale relationship source')
    if len(relation_keys)!=len(set(relation_keys)):errors.append('duplicate relationship pair/type')
    for r in questions:
        q=r['question_id'];path=ROOT/r['question_text_file']
        if not path.exists() or digest(path)!=r['raw_text_sha256']:errors.append(q+': extraction hash mismatch')
        for k in ['major_category','middle_category','minor_category','topic','tex_file','discipline_id','concept_id']:
            if cls.get(q,{}).get(k)!=r.get(k):errors.append(q+': classification view mismatch '+k)
        meta=ROOT/'extracted/text'/r['source_year_directory']/(('basic' if r['subject']=='BASIC' else 'aptitude' if r['subject']=='APT' else '17_applied_science')+'.json')
        pages=json.loads(meta.read_text())['pages'];sp=int(r['source_page']);ep=int(r['source_page_end'])
        if int(r['heading_line_index'])>=len(pages[sp-1].get('lines',[])) or int(r['end_line_index'])>=len(pages[ep-1].get('lines',[])):errors.append(q+': line out of range')
        tex=ROOT/r['tex_file']
        if tex.exists():
            tex_files,tex_errors=input_graph(r['tex_file'])
            has_tex=not tex_errors and ('\\label{'+r['tex_label']+'}') in '\n'.join(tex_files.values())
        else:has_tex=False
        if not has_tex:tex_missing+=1
        issues=[]
        if r['needs_manual_verification']=='true':issues.append('ocr_body_verification')
        if r['boundary_verified']!='true':issues.append('boundary_verification')
        if r['classification_verified']!='true':issues.append('classification_review')
        if r.get('topic_verified')!='true':issues.append('concept_review')
        if r['summary_verified']!='true':issues.append('semantic_summary_review')
        if any(r[k]=='unknown' for k in ['requires_calculation','requires_figure','requires_law']):issues.append('dependency_flags_review')
        if not r['difficulty'] or not r['priority']:issues.append('difficulty_priority_pending')
        if not r['solution_summary'] or not r['wrong_choice_summary'] or r['status']!='explained_verified':issues.append('explanation_review')
        if not has_tex:issues.append('textbook_pending')
        if issues:unresolved.append({'question_id':q,'issue_types':'|'.join(issues),'source_file':r['source_file'],'source_page':r['source_page'],'phase':'S4-S7','status':'open','reason':'Remaining checks are explicitly separate from registration.'})
    for year in YEARS:
        for subject in SUBJECTS.values():
            group=[r for r in questions if r['source_year_directory']==year and r['subject']==subject];got={r['question_id'] for r in group};exp={r['question_id'] for r in official if r['source_year_directory']==year and r['subject']==subject}
            spans=sorted(group,key=lambda r:(int(r['source_page']),int(r['heading_line_index'])))
            for previous,current in zip(spans,spans[1:]):
                if (int(previous['source_page_end']),int(previous['end_line_index']))>=(int(current['source_page']),int(current['heading_line_index'])):errors.append('overlapping source spans '+previous['question_id']+' / '+current['question_id'])
            n=(25 if year in ('H23','H24') else 30) if subject=='BASIC' else 15 if subject=='APT' else 35
            if len(exp)!=n:errors.append(year+'/'+subject+': official count mismatch')
            report.append({'year':year,'subject':subject,'expected_questions':len(exp),'registered_questions':len(group),'missing_questions':len(exp-got),'extra_questions':len(got-exp),'duplicate_ids':sum(counts[q]-1 for q in got),'classifications_verified':sum(r['classification_verified']=='true' for r in group),'summaries_verified':sum(r['summary_verified']=='true' for r in group),'explained_questions':sum(r['status']=='explained_verified' for r in group),'manual_verification_required':sum(r['needs_manual_verification']=='true' for r in group),'audit_scope':'registration_and_provenance'})
    metrics={'expected_questions':len(expected),'registered_questions':len(questions),'missing_questions':len(expected-actual),'extra_questions':len(actual-expected),'duplicate_question_ids':sum(n-1 for n in counts.values()),'unclassified_questions':sum(not r['major_category'] or not r['middle_category'] for r in questions),'unverified_official_answers':sum(r['answer_verified']!='true' for r in questions),'questions_without_tex':tex_missing,'unexplained_questions':sum(r['status']!='explained_verified' for r in questions),'manual_verification_required':sum(r['needs_manual_verification']=='true' for r in questions),'unresolved_questions':len(unresolved),'integrity_errors':errors,'initial_audit_passed':False,'final_audit_passed':False,'final_status':'not_implemented','scope':'S4 registration/provenance'}
    metrics['initial_audit_passed']=not errors and not any(metrics[k] for k in ['missing_questions','extra_questions','duplicate_question_ids','unclassified_questions','unverified_official_answers'])
    return report,unresolved,metrics

def main():
    p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');a=p.parse_args()
    if a.final:raise SystemExit('Final quality/compile/citation checks are not implemented; final audit cannot pass.')
    report,unresolved,metrics=audit(read_csv('data/questions.csv'),read_csv('data/answers_official.csv'),read_csv('data/classifications.csv'),read_csv('data/source_files.csv'))
    publish_bundle({'data/audit_report.csv':csv_bytes(report),'data/unresolved.csv':csv_bytes(unresolved,'question_id issue_types source_file source_page phase status reason'.split()),'extracted/logs/audit_metrics.json':json_bytes(metrics)})
    print(json.dumps(metrics,ensure_ascii=False,indent=2))
    if not metrics['initial_audit_passed']:raise SystemExit(1)
if __name__=='__main__':main()
