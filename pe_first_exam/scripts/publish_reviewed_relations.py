"""Publish explicitly source-compared relations; similarity scores are not approvals."""
import argparse,json
from common import ROOT,read_csv,csv_bytes,publish_bundle,digest
from validate_schema import validate_rows

def main():
 p=argparse.ArgumentParser();p.add_argument('input');a=p.parse_args()
 entries=json.loads((ROOT/a.input).read_text())['relations']
 questions=read_csv('data/questions.csv');by={r['question_id']:r for r in questions}
 rows=read_csv('data/question_relations.csv');keys={(*sorted((r['left_question_id'],r['right_question_id'])),r['relation_type']) for r in rows}
 for e in entries:
  if e.get('relation_type') not in ('same_concept','same_method','parameter_variant','near_repeat','exact_repeat'):raise ValueError('Invalid relationship type')
  left,right=e['left_question_id'],e['right_question_id']
  if left==right:raise ValueError('Self relation')
  for side,q in [('left',left),('right',right)]:
   r=by[q]
   if e['source_hash_'+side]!=r['source_sha256'] or digest(ROOT/r['source_file'])!=r['source_sha256']:raise ValueError('Stale source '+q)
   if not r['corrected_content_file']:raise ValueError('Unreviewed source '+q)
  if e['approval_status']!='verified' or not all(e.get(k) for k in ['shared_concept','shared_method','numerical_differences','negation_differences','choice_differences','figure_differences','temporal_differences','evidence']):raise ValueError('Incomplete comparison')
  key=(*sorted((left,right)),e['relation_type'])
  if key not in keys:rows.append(e);keys.add(key)
  for q,related in [(left,right),(right,left)]:
   old=set(filter(None,by[q]['related_question_ids'].split('|')));old.add(related);by[q]['related_question_ids']='|'.join(sorted(old))
 validate_rows(questions)
 publish_bundle({'data/questions.csv':csv_bytes(questions),'data/question_relations.csv':csv_bytes(rows)})
 print('Published reviewed relations:',len(entries),'total',len(rows))

if __name__=='__main__':main()
