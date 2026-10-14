"""Apply source-reviewed authored batches to the existing canonical question IDs."""
import argparse,hashlib,json,re
from common import ROOT,read_csv,csv_bytes,json_bytes,publish_bundle,now,digest,verification_payload_hash
from classify_questions import classification_view
from validate_schema import validate_rows
from validate_answers import answer_set

def padded(rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    return [{k:r.get(k,'') for k in fields} for r in rows]

def independent_comparison(answer, official, answer_kind):
    """Distinguish set equality from one accepted alternative; never expand a solve."""
    found, accepted = answer_set(answer), answer_set(official)
    if found == accepted:
        return 'matches_official_draft'
    if answer_kind in ('multiple', 'multiple_accepted') and len(found) == 1 and found <= accepted:
        return 'accepted_official_member_draft'
    return 'discrepancy_pending'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('input');args=parser.parse_args()
    batch=json.loads((ROOT/args.input).read_text());rows=read_csv('data/questions.csv');by={r['question_id']:r for r in rows}
    checks=read_csv('data/verification_records.csv');topics=read_csv('data/question_topics.csv');evaluations=read_csv('data/question_evaluations.csv')
    taxonomy={t['id']:t for t in json.loads((ROOT/'config/taxonomy.json').read_text())['categories']}
    concepts={t['id']:t for t in json.loads((ROOT/'config/concepts.json').read_text())['concepts']}
    changes=[];files={};processed=[];seen=set()
    for e in batch['questions']:
        q=e['question_id']
        if q in seen:raise ValueError('Duplicate batch ID '+q)
        seen.add(q);r=by[q]
        if e['source_sha256']!=r['source_sha256'] or digest(ROOT/r['source_file'])!=r['source_sha256']:raise ValueError('Changed source '+q)
        if set(e['choices'])!={'1','2','3','4','5'} or any(not c.get('reason') or not c.get('value') or not c.get('verdict') for c in e['choices'].values()):raise ValueError('Missing option review '+q)
        for key in ['stem','summary','core_concept','required_knowledge','solution','answer_reason','learning_points','theory_references','evidence']:
            if not e.get(key):raise ValueError('Missing authored field '+q+' '+key)
        if any(not (ROOT/p).exists() for p in e['evidence']):raise ValueError('Missing source image '+q)
        comparison=independent_comparison(e['independent_answer'],r['official_answer'],r['answer_kind'])
        match=comparison=='matches_official_draft'
        if not match and not e.get('ambiguity'):raise ValueError('Independent answer differs without documented ambiguity '+q)
        payload={k:e[k] for k in ['stem','conditions','choices','figures','ambiguity','evidence']}
        payload.update(question_id=q,source_file=r['source_file'],source_page=r['source_page'],source_sha256=r['source_sha256'],raw_text_sha256=r['raw_text_sha256'],scope='Source-image checked essential conditions and all options; independent paraphrase')
        content=json_bytes(payload);h=hashlib.sha256(content).hexdigest();path=f'extracted/corrected/{q}/{h}.json'
        if r.get('authoring_batch')==batch['batch_id']:
            if r.get('corrected_content_sha256')!=h:raise ValueError('Changed applied batch '+q)
            continue
        revision=bool(r.get('solution_summary') or r.get('corrected_content_sha256'))
        if revision:
            if (e.get('revision_of_content_sha256')!=r.get('corrected_content_sha256') or e.get('revision_of_batch')!=r.get('authoring_batch') or not e.get('revision_reason')):
                raise ValueError('Existing authored question needs explicit hash-bound revision '+q)
            for record in checks:
                if record['question_id']==q and record.get('kind') in ('classification','summary','correction','independent_solution','solution') and record.get('status') not in ('superseded','invalidated'):
                    record['status']='superseded'
            files[f'data/batch_changes/{batch["batch_id"]}_{q}_revision.json']=json_bytes({'question_id':q,'previous_row':dict(r),'revision_reason':e['revision_reason'],'replacement_content_sha256':h,'time':now()})
        files[path]=content
        old={k:r.get(k,'') for k in ['discipline_id','concept_id','major_category','middle_category','minor_category','topic','tex_file']}
        cat=taxonomy[e['discipline_id']];cid=e.get('concept_id','');label=concepts[cid]['label'] if cid else '未確定'
        r.update(discipline_id=cat['id'],major_category=cat['major'],middle_category=cat['middle'],tex_file=cat['file'],chapter_id=cat['file'].removeprefix('chapters/').removesuffix('.tex'),concept_id=cid,minor_category=label,topic=label,subtopic='',classification_method='manual_content_review',classification_confidence='high',classification_evidence=e['classification_reason'],classification_verified='true',topic_verified='true' if cid else 'false')
        r.update(corrected_content_file=path,corrected_content_sha256=h,correction_status='partial' if e['ambiguity'] else 'verified',summary_status='verified',summary_verified='true',question_summary=e['summary'],core_concept=e['core_concept'],required_knowledge=e['required_knowledge'],solution_summary=e['solution'],wrong_choice_summary=' '.join(f'{k}：{c["verdict"]}。{c["reason"]}' for k,c in e['choices'].items()),choice_reviews=json.dumps(e['choices'],ensure_ascii=False),answer_reason=e['answer_reason'],learning_points=e['learning_points'],theory_references='|'.join(e['theory_references']),requires_calculation=e['calculation'],requires_figure=e['figure'],requires_law=e['law'],difficulty=e['evaluation']['difficulty'],status='draft_written',needs_manual_verification='true' if e['ambiguity'] else 'false',astra_review_required='true',solution_review_status='draft_pending_astra',independent_solution_status=comparison,independent_answer=e['independent_answer'],source_reference_date=e.get('source_reference_date',r['year']),explanation_reference_date=batch['reference_date'],explanation_citations='|'.join(e.get('citations',[])),authoring_batch=batch['batch_id'],notes=e['ambiguity'] or '原典条件・5肢を画像確認。独立解法と各肢判断は初稿、Astra査読待ち。')
        if any(old[k]!=r[k] for k in old):changes.append({'question_id':q,'source_file':r['source_file'],'source_page':r['source_page'],'source_sha256':r['source_sha256'],'before':json.dumps(old,ensure_ascii=False),'after':json.dumps({k:r[k] for k in old},ensure_ascii=False),'reason':e['classification_reason']})
        for kind in ['classification','summary']+([] if e['ambiguity'] else ['correction']):
            checks.append({'question_id':q,'kind':kind,'source_sha256':r['source_sha256'],'content_sha256':h,'reviewer':'GPT-6.1 Sol (user-declared)','reviewed_at':now(),'status':'verified','evidence':'|'.join(e['evidence']),'notes':'Source conditions/classification/summary only. Textbook solution remains draft.','payload_sha256':verification_payload_hash(r,kind),'payload_bound_at':now()})
        checks.append({'question_id':q,'kind':'independent_solution','source_sha256':r['source_sha256'],'content_sha256':h,'reviewer':'GPT-6.1 Sol (user-declared)','reviewed_at':now(),'status':'draft_checked' if comparison!='discrepancy_pending' else 'discrepancy','evidence':args.input,'notes':e.get('independent_solution_note','Independent reasoning constructed from source conditions before answer comparison; not Astra review.'),'payload_sha256':verification_payload_hash(r,'solution'),'payload_bound_at':now()})
        topics=[t for t in topics if not (t['question_id']==q and (t['role']=='primary' or t.get('status')!='verified'))]
        for cross in e.get('cross_concepts',[]):
            if cross not in concepts:raise ValueError('Unknown cross concept '+q+' '+cross)
            if not any(t['question_id']==q and t['concept_id']==cross for t in topics):
                topics.append({'question_id':q,'concept_id':cross,'role':'cross','evidence':e['classification_reason'],'status':'verified','source_sha256':r['source_sha256']})
        if cid:topics.append({'question_id':q,'concept_id':cid,'role':'primary','evidence':e['classification_reason'],'status':'verified','source_sha256':r['source_sha256']})
        ev=e['evaluation'];evaluations=[v for v in evaluations if v['question_id']!=q]
        evaluations.append({'question_id':q,**ev,'foundationality':e.get('foundationality',''),'transferability':e.get('transferability',''),'learning_minutes':'','estimated_score_efficiency':'','priority':'','priority_reason':'習得時間・効率未評価','rubric_version':'1.0-review1','reviewer':'GPT-6.1 Sol','status':'calibration_draft'})
        processed.append(q)
    if not processed:print('Already applied; canonical authored columns preserved');return
    rows=padded(rows);checks=padded(checks);evaluations=padded(evaluations)
    validate_rows(rows,checks=checks,staged_files=files)
    files.update({'data/questions.csv':csv_bytes(rows),'data/classifications.csv':csv_bytes(classification_view(rows)),'data/verification_records.csv':csv_bytes(checks),'data/question_topics.csv':csv_bytes(topics),'data/question_evaluations.csv':csv_bytes(evaluations),f'data/batch_changes/{batch["batch_id"]}.csv':csv_bytes(changes,'question_id source_file source_page source_sha256 before after reason'.split()),f'extracted/logs/batches/{batch["batch_id"]}.json':json_bytes({'time':now(),'questions':processed,'source_conditions_checked':len(processed),'solution_drafts':len(processed),'final_verification':False})})
    publish_bundle(files);print('Published',batch['batch_id'],len(processed),'source-reviewed solution drafts')

if __name__=='__main__':main()
