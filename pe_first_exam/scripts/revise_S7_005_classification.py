"""Explicitly fix two wrongly typed discipline IDs, retaining superseded evidence."""
import json
from common import ROOT,read_csv,csv_bytes,json_bytes,publish_bundle,now,verification_payload_hash
from classify_questions import classification_view
from validate_schema import validate_rows

def main():
 qs=read_csv('data/questions.csv');checks=read_csv('data/verification_records.csv')
 targets={'H26-REG-BASIC-2-2','R05-REG-BASIC-2-2'}
 cat=next(c for c in json.loads((ROOT/'config/taxonomy.json').read_text())['categories'] if c['id']=='basic_2_8')
 changes=[]
 for r in qs:
  if r['question_id'] not in targets or r['discipline_id']=='basic_2_8':continue
  assert r['discipline_id']=='basic_2_7' and r['authoring_batch']=='S7_005_logic_sets_algorithms'
  before={k:r[k] for k in ['discipline_id','middle_category','classification_evidence']}
  r.update(discipline_id=cat['id'],middle_category=cat['middle'],classification_evidence='原典のユークリッド互除法の分岐・終了と最大公約数保存を確認。アルゴリズム・計算量が主分類である。S7_005で誤入力した情報セキュリティIDを訂正。')
  for c in checks:
   if c['question_id']==r['question_id'] and c['kind']=='classification' and c['status']=='verified':c['status']='superseded'
  checks.append(dict(question_id=r['question_id'],kind='classification',source_sha256=r['source_sha256'],content_sha256=r['corrected_content_sha256'],reviewer='GPT-6.1 Sol (user-declared)',reviewed_at=now(),status='verified',evidence=r['corrected_content_file'],notes='Explicit classification-only correction; immutable text correction and solution draft retained.',payload_sha256=verification_payload_hash(r,'classification'),payload_bound_at=now()))
  changes.append(dict(question_id=r['question_id'],before=before,after={k:r[k] for k in before},reason='Wrong discipline literal 2_7 corrected to taxonomy algorithm 2_8'))
 if not changes:print('Classification correction already applied');return
 validate_rows(qs,checks=checks)
 publish_bundle({'data/questions.csv':csv_bytes(qs),'data/classifications.csv':csv_bytes(classification_view(qs)),'data/verification_records.csv':csv_bytes(checks),'data/batch_changes/S7_005_classification_correction.json':json_bytes({'time':now(),'changes':changes})})
 print('Revised classification IDs with superseded and new evidence:',len(changes))

if __name__=='__main__':main()
