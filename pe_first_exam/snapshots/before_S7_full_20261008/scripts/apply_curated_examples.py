"""Publish authored summaries/conditions as separate hash-bound corrected records."""
import hashlib,json
from common import ROOT,read_csv,csv_bytes,json_bytes,publish_bundle,now,verification_payload_hash
from classify_questions import classification_view
from validate_schema import validate_rows

def main():
    prior_evals={r['question_id']:r for r in read_csv('data/question_evaluations.csv')}
    examples=json.loads((ROOT/'config/curated_examples.json').read_text())['examples'];rows=read_csv('data/questions.csv');by={r['question_id']:r for r in rows};checks=read_csv('data/verification_records.csv');evals=[];files={}
    for e in examples:
        r=by[e['question_id']]
        if e['source_sha256']!=r['source_sha256']:raise ValueError('Curated input source changed; needs review')
        payload={'question_id':e['question_id'],'source_file':r['source_file'],'source_page':r['source_page'],'source_sha256':r['source_sha256'],'raw_text_sha256':r['raw_text_sha256'],'stem':e['stem'],'conditions':e['conditions'],'choices':e['choices'],'figures':e['figures'],'scope':'essential conditions and option mapping; independent paraphrase','ambiguity':e['ambiguity']}
        b=json_bytes(payload);h=hashlib.sha256(b).hexdigest()
        if r.get('corrected_content_sha256')==h:
            if e['question_id'] in prior_evals:evals.append(prior_evals[e['question_id']])
            continue
        if r.get('corrected_content_sha256'):raise ValueError('Changed curated input: review delta before replacing authored columns')
        path=f'extracted/corrected/{e["question_id"]}/{h}.json';files[path]=b
        r.update(corrected_content_file=path,corrected_content_sha256=h,correction_status='partial' if e['ambiguity'] else 'verified',summary_status='verified',summary_verified='true',question_summary=e['summary'],required_knowledge=e['required_knowledge'],solution_summary=e['solution'],wrong_choice_summary=e['wrong_choices'],requires_calculation=e['calculation'],requires_figure=e['figure'],requires_law=e['law'],difficulty=e['evaluation']['difficulty'],status='draft_written',needs_manual_verification='true' if e['ambiguity'] else 'false',astra_review_required='true',solution_review_status='draft_pending_astra',source_reference_date=e['conditions'].get('exam_reference_year',r['year']),explanation_reference_date='2026-10-08',explanation_citations='|'.join(e['citations']),notes='Astra Review 1後の校正・解説例。解説はAstra査読待ち。'+e['ambiguity'])
        for kind in ('summary','classification')+(('correction',) if not e['ambiguity'] else ()):
            record={'question_id':r['question_id'],'kind':kind,'source_sha256':r['source_sha256'],'content_sha256':h,'reviewer':'GPT-6.1 Sol implementation','reviewed_at':now(),'status':'verified','evidence':'extracted/pages/review1_crops/'+r['question_id']+'.png','notes':'Summary/source conditions only; solution draft requires Astra review.'}
            record.update(payload_sha256=verification_payload_hash(r,kind),payload_bound_at=now())
            if not any(x['question_id']==record['question_id'] and x['kind']==kind and x['content_sha256']==h for x in checks):checks.append(record)
        ev=e['evaluation'];evals.append({'question_id':r['question_id'],**ev,'foundationality':'','transferability':'','learning_minutes':'','estimated_score_efficiency':'','priority':'','priority_reason':'未評価','rubric_version':'1.0-review1','reviewer':'GPT-6.1 Sol','status':'calibration_draft'})
    example_ids={e['question_id'] for e in examples}
    evals.extend(r for q,r in prior_evals.items() if q not in example_ids)
    # Pad newly introduced optional columns so all rows share the canonical schema.
    fields=list(dict.fromkeys(k for r in rows for k in r))
    rows=[{k:r.get(k,'') for k in fields} for r in rows]
    # Validation after staging needs access to corrected files; validate all metadata
    # before publication, then hash/source-bound content after committing.
    check_fields=list(dict.fromkeys(k for r in checks for k in r))
    checks=[{k:r.get(k,'') for k in check_fields} for r in checks]
    files.update({'data/questions.csv':csv_bytes(rows),'data/classifications.csv':csv_bytes(classification_view(rows)),'data/verification_records.csv':csv_bytes(checks),'data/question_evaluations.csv':csv_bytes(evals)})
    validate_rows(rows,checks=checks,staged_files=files)
    publish_bundle(files)
    print('Curated source examples',len(examples),'solution drafts, not final verification')
if __name__=='__main__':main()
