"""Separate initial registration audit from final textbook completeness."""
import argparse
import json
import re
from collections import Counter
from common import ROOT, YEARS, SUBJECTS, read_csv, write_csv, qid

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--final',action='store_true');args=parser.parse_args()
    questions=read_csv('data/questions.csv');official=read_csv('data/answers_official.csv')
    sources={r['path']:r for r in read_csv('data/source_files.csv')}
    classification={r['question_id']:r for r in read_csv('data/classifications.csv')}
    counts=Counter(r['question_id'] for r in questions)
    expected={r['question_id'] for r in official};actual=set(counts)
    report=[];unresolved=[];integrity_errors=[];tex_missing=0
    for row in questions:
        q=row['question_id']; source=sources.get(row['source_file'])
        if not source or not (ROOT/row['source_file']).exists():integrity_errors.append(q+': missing source')
        elif not 1<=int(row['source_page'])<=int(row['source_page_end'])<=int(source['page_count']):integrity_errors.append(q+': invalid page range')
        if q!=qid(row['source_year_directory'],row['subject'],row['question_number']):integrity_errors.append(q+': inconsistent ID')
        if not (ROOT/row['question_text_file']).exists():integrity_errors.append(q+': missing extracted question')
        if q not in classification:integrity_errors.append(q+': missing classification row')
        else:
            for field in ['major_category','middle_category','minor_category','topic','tex_file']:
                if row[field]!=classification[q][field]:integrity_errors.append(q+': classification mismatch '+field)
        texpath=ROOT/row['tex_file'] if row['tex_file'] else None
        has_tex=bool(texpath and texpath.exists() and '\\label{'+row['tex_label']+'}' in texpath.read_text())
        if not has_tex:tex_missing+=1
        issues=[]
        if row['needs_manual_verification']=='true':issues.append('ocr_body_verification')
        if row['boundary_verified']!='true':issues.append('heading_visual_verification')
        if row['classification_verified']!='true':issues.append('classification_review')
        if row['summary_verified']!='true':issues.append('semantic_summary_review')
        if row['requires_calculation']=='unknown' or row['requires_figure']=='unknown' or row['requires_law']=='unknown':issues.append('dependency_flags_review')
        if not row['difficulty'] or not row['priority']:issues.append('difficulty_priority_pending')
        if not has_tex:issues.append('textbook_pending')
        if issues:unresolved.append({'question_id':q,'issue_types':'|'.join(issues),'source_file':row['source_file'],
                                   'source_page':row['source_page'],'phase':'S4_or_later','status':'open',
                                   'reason':'初期登録段階。原典OCR校正、専門分類確認、教材執筆は未完了。'})
    for year in YEARS:
        for subject in SUBJECTS.values():
            group=[r for r in questions if r['source_year_directory']==year and r['subject']==subject]
            exp={r['question_id'] for r in official if r['source_year_directory']==year and r['subject']==subject}
            got={r['question_id'] for r in group}
            independently_expected=(25 if year in ('H23','H24') else 30) if subject=='BASIC' else 15 if subject=='APT' else 35
            if len(exp)!=independently_expected:integrity_errors.append(year+'/'+subject+': official count mismatch')
            report.append({'year':year,'subject':subject,'expected_questions':len(exp),'registered_questions':len(group),
                'official_answers_verified':sum(r['answer_verified']=='true' for r in group),
                'initial_classified':sum(bool(r['major_category']) and bool(r['middle_category']) for r in group),
                'classifications_verified':sum(r['classification_verified']=='true' for r in group),
                'tex_planned':sum(bool(r['tex_file']) for r in group),'questions_with_tex_label':sum(bool(r['tex_file']) and (ROOT/r['tex_file']).exists() and '\\label{'+r['tex_label']+'}' in (ROOT/r['tex_file']).read_text() for r in group),
                'explained_questions':sum(r['status']=='explained_verified' for r in group),
                'unprocessed_questions':sum(r['status']!='explained_verified' for r in group),
                'missing_questions':len(exp-got),'extra_questions':len(got-exp),
                'duplicate_ids':sum(counts[q]-1 for q in got),
                'manual_verification_required':sum(r['needs_manual_verification']=='true' for r in group),
                'audit_scope':'initial_registration'})
    metrics={'expected_questions':len(expected),'registered_questions':len(questions),'missing_questions':len(expected-actual),
             'extra_questions':len(actual-expected),'duplicate_question_ids':sum(v-1 for v in counts.values()),
             'unclassified_questions':sum(not r['major_category'] or not r['middle_category'] for r in questions),
             'unverified_official_answers':sum(r['answer_verified']!='true' for r in questions),
             'questions_without_tex':tex_missing,'unexplained_questions':sum(r['status']!='explained_verified' for r in questions),
             'manual_verification_required':len(unresolved),'integrity_errors':integrity_errors,
             'initial_audit_passed':False,'final_audit_passed':False,'scope':'S0-S3'}
    metrics['initial_audit_passed']=not any(metrics[k] for k in ['missing_questions','extra_questions','duplicate_question_ids','unclassified_questions','unverified_official_answers','integrity_errors'])
    metrics['final_audit_passed']=metrics['initial_audit_passed'] and not any(metrics[k] for k in ['questions_without_tex','unexplained_questions','manual_verification_required'])
    write_csv('data/audit_report.csv',report)
    write_csv('data/unresolved.csv',unresolved,['question_id','issue_types','source_file','source_page','phase','status','reason'])
    (ROOT/'extracted/logs/audit_metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
    print(json.dumps(metrics,ensure_ascii=False,indent=2))
    if not metrics['initial_audit_passed'] or (args.final and not metrics['final_audit_passed']):raise SystemExit(1)

if __name__=='__main__':main()
