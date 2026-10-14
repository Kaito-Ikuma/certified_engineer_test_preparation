"""Dual provisional/verified frequencies; unknown evaluations remain blank."""
from collections import defaultdict
from common import ROOT,YEARS,read_csv,csv_bytes,json_bytes,publish_bundle

def main():
    rows=read_csv('data/questions.csv');groups=defaultdict(list)
    for r in rows:
        for level in ('major_category','middle_category','minor_category'):
            groups[(r['subject'],level,r[level])].append(r)
    stats=[]
    for (subject,level,label),group in sorted(groups.items()):
        sessions=sorted({r['source_year_directory'] for r in group},key=YEARS.index);years=sorted({r['year'] for r in group},key=YEARS.index)
        confirmed=[r for r in group if r['classification_verified']=='true' and (level!='minor_category' or r['topic_verified']=='true')]
        cs={r['source_year_directory'] for r in confirmed};cy={r['year'] for r in confirmed}
        ds=[int(r['difficulty']) for r in group if r['difficulty']]
        stats.append({'subject':subject,'level':level,'category':label,'provisional_questions':len(group),'verified_questions':len(confirmed),'provisional_sessions':len(sessions),'session_denominator':16,'provisional_session_frequency':f'{len(sessions)/16:.6f}','provisional_years':len(years),'year_denominator':15,'provisional_annual_frequency':f'{len(years)/15:.6f}','verified_sessions':len(cs),'verified_years':len(cy),'exam_sessions':'|'.join(sessions),'exam_years':'|'.join(years),'latest_exam_session':sessions[-1],'difficulty_evaluated':len(ds),'mean_difficulty':f'{sum(ds)/len(ds):.2f}' if ds else '', 'status':'provisional_incomplete_verification'})
    tags=read_csv('data/question_topics.csv');concept_groups=defaultdict(list)
    for t in tags:concept_groups[t['concept_id']].append(t)
    concepts=[]
    for cid,ts in sorted(concept_groups.items()):
        primary={t['question_id'] for t in ts if t['role']=='primary'}
        cross={t['question_id'] for t in ts if t['role']!='primary'}
        concepts.append({'concept_id':cid,'primary_questions':len(primary),'cross_tag_questions':len(cross),'distinct_questions':len(primary|cross),'tag_assignments':len(ts),'verified_assignments':sum(t['status']=='verified' for t in ts),'status':'provisional_incomplete_verification'})
    relations=read_csv('data/question_relations.csv');counts={k:0 for k in ('same_concept','same_method','parameter_variant','near_repeat','exact_repeat')}
    for r in relations:
        if r['approval_status']=='verified':counts[r['relation_type']]+=1
    publish_bundle({'data/topic_statistics.csv':csv_bytes(stats),'data/concept_statistics.csv':csv_bytes(concepts),'extracted/logs/statistics_summary.json':json_bytes({'questions':len(rows),'sessions':16,'years':15,'verified_primary_classifications':sum(r['classification_verified']=='true' for r in rows),'verified_relationship_counts':dict(counts),'unknown_difficulty':sum(not r['difficulty'] for r in rows),'scope':'Provisional classification frequencies; verified subset separately reported'})})
    print('Frequency groups',len(stats),'provisional; verified subset separately')
if __name__=='__main__':main()
