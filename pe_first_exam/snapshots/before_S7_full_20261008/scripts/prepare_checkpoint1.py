"""Refresh stratified work queue without overwriting original checkpoint evidence."""
from collections import defaultdict
from common import ROOT,YEARS,read_csv,csv_bytes,json_bytes,publish_bundle
from validate_answers import EXCEPTIONS

def main():
    rows=read_csv('data/questions.csv');reasons=defaultdict(set)
    previous=read_csv('handoff/ASTRA_REVIEW_1_TARGETS.csv')
    for r in previous:reasons[r['question_id']].add('astra_impact_set')
    # Freeze original low-confidence/override sets so improved rules do not erase them.
    initial=read_csv('data/review_queue_checkpoint1.csv')
    for r in initial:
        if 'low_confidence' in r['review_reasons'] or 'manual_override' in r['review_reasons']:reasons[r['question_id']].add('original_high_risk')
    seen=defaultdict(int)
    for r in rows:
        q=r['question_id'];year=r['source_year_directory'];period='early' if year in YEARS[:5] else 'middle' if year in YEARS[5:11] else 'late'
        group=(period,r['subject'],r['discipline_id']);session=(year,r['subject'])
        if seen[group]<2:reasons[q].add('period_category_sample')
        if seen[session]<2:reasons[q].add('session_subject_sample')
        seen[group]+=1;seen[session]+=1
        if r['classification_confidence']=='low':reasons[q].add('low_confidence')
        if r['classification_method']=='manual_content_review':reasons[q].add('manual_override')
        if q in EXCEPTIONS:reasons[q].add('official_exception')
        candidates=__import__('json').loads(r['classification_candidates'])
        if len(candidates)>1:reasons[q].add('competing_rules')
    queue=[];strata=defaultdict(list)
    for r in rows:
        if reasons[r['question_id']]:queue.append({**{k:r[k] for k in ['question_id','source_year_directory','subject','discipline_id','middle_category','topic','source_file','source_page','question_text_file']},'review_reasons':'|'.join(sorted(reasons[r['question_id']])),'review_status':'pending'})
        year=r['source_year_directory'];period='early' if year in YEARS[:5] else 'middle' if year in YEARS[5:11] else 'late'
        strata[(period,r['subject'],r['discipline_id'])].append(r)
    coverage=[]
    for year in YEARS:
        for s in ('BASIC','APT','APPLIED'):coverage.append({'year':year,'subject':s,'queued':sum(r['source_year_directory']==year and r['subject']==s for r in queue),'verified':sum(r['source_year_directory']==year and r['subject']==s and r['classification_verified']=='true' for r in rows)})
    layers=[{'period':k[0],'subject':k[1],'discipline_id':k[2],'registered':len(rs),'queued':sum(bool(reasons[r['question_id']]) for r in rs),'classification_verified':sum(r['classification_verified']=='true' for r in rs),'summary_verified':sum(r['summary_verified']=='true' for r in rs)} for k,rs in sorted(strata.items())]
    publish_bundle({'data/review_queue.csv':csv_bytes(queue),'data/review_coverage.csv':csv_bytes(coverage),'data/review_strata.csv':csv_bytes(layers)})
    print('Stratified queue',len(queue),'session/subject cells',len(coverage))
if __name__=='__main__':main()
