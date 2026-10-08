"""Join official values as sets; visual status is hash-bound evidence, never fixed."""
from common import ROOT,read_csv,csv_bytes,json_bytes,publish_bundle,digest
import re

EXCEPTIONS={'H23-REG-APT-04':('1|5','multiple_accepted'),'H26-REG-BASIC-5-3':('5','single'),'H30-REG-APT-14':('ALL','all_awarded'),'R01-RET-APT-14':('ALL','all_awarded'),'R02-REG-BASIC-5-5':('4|3','multiple_accepted'),'R02-REG-APPLIED-10':('ALL','all_awarded')}
def answer_set(value):return frozenset(value.split('|'))
def visual_verified(row,evidence):
    return any(v['question_id']==row['question_id'] and v['source_sha256']==row['source_sha256'] and v['source_page']==str(row['source_page']) and v['status']=='verified' and v['kind']=='official_answer_visual' and v['reviewer'] and v['reviewed_at'] and answer_set(v.get('verified_answer',''))==answer_set(row['official_answer']) and v.get('verified_answer_kind')==row['answer_kind'] for v in evidence)
def verify(official,questions,records=None,hash_check=True):
    by={r['question_id']:r for r in official}
    if len(by)!=len(official):raise ValueError('Duplicate official answer')
    ids=[r['question_id'] for r in questions]
    if len(ids)!=len(set(ids)) or set(ids)!=set(by):raise ValueError('Question/answer ID mismatch')
    hashes={}
    for r in official:
        if not re.fullmatch(r'[1-5](?:\|[1-5])*|ALL',r['official_answer']):raise ValueError('Unknown answer value')
        if hash_check:
            source=r['source_file']
            if source not in hashes:hashes[source]=digest(ROOT/source)
            if r.get('source_sha256')!=hashes[source]:raise ValueError('Stale official answer source')
    for r in questions:
        a=by[r['question_id']]
        if answer_set(r['official_answer'])!=answer_set(a['official_answer']) or r['answer_kind']!=a['answer_kind']:raise ValueError('Official answer mismatch '+r['question_id'])
    for q,(value,kind) in EXCEPTIONS.items():
        if answer_set(by[q]['official_answer'])!=answer_set(value) or by[q]['answer_kind']!=kind or not by[q]['official_note']:raise ValueError('Official exception lost '+q)
    return True

def main():
    official=read_csv('data/answers_official.csv');questions=read_csv('data/questions.csv');evidence=read_csv('data/answer_verification_records.csv');verify(official,questions,evidence)
    by={r['question_id']:r for r in official};special=[]
    for q in EXCEPTIONS:
        a=by[q];visual=visual_verified(a,evidence)
        special.append({'question_id':q,'official_answer':a['official_answer'],'answer_kind':a['answer_kind'],'source_file':a['source_file'],'source_page':a['source_page'],'source_sha256':a['source_sha256'],'official_note':a['official_note'],'original_answer':a['original_answer'],'visual_check':'true' if visual else 'false'})
    publish_bundle({'data/answer_exceptions.csv':csv_bytes(special),'extracted/logs/answer_validation.json':json_bytes({'official_rows':len(official),'question_rows':len(questions),'join_mismatches':0,'visual_exceptions_verified':sum(r['visual_check']=='true' for r in special),'verification_scope':'parsed/structurally checked; source review and independent solutions separately recorded'})})
    print('Official joins validated',len(questions))
if __name__=='__main__':main()
