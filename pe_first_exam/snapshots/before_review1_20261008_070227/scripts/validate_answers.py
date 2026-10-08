"""Check question-to-official-answer joins and published exceptions."""
import json
import re
from common import ROOT, read_csv, write_csv

EXCEPTIONS={
    'H23-REG-APT-04':('1|5','multiple_accepted'),
    'H26-REG-BASIC-5-3':('5','single'),
    'H30-REG-APT-14':('ALL','all_awarded'),
    'R01-RET-APT-14':('ALL','all_awarded'),
    'R02-REG-BASIC-5-5':('4|3','multiple_accepted'),
    'R02-REG-APPLIED-10':('ALL','all_awarded'),
}
def main():
    official=read_csv('data/answers_official.csv'); questions=read_csv('data/questions.csv')
    byid={r['question_id']:r for r in official}
    if len(byid)!=len(official):raise ValueError('Duplicate official ID')
    assert set(byid)=={r['question_id'] for r in questions},'Question/answer ID sets differ'
    for row in questions:
        answer=byid[row['question_id']]
        assert re.fullmatch(r'[1-5](?:\|[1-5])*|ALL',answer['official_answer']),answer
        assert row['official_answer']==answer['official_answer'],row['question_id']
        assert row['answer_verified']==answer['answer_verified']=='true'
    for q,(answer,kind) in EXCEPTIONS.items():
        assert (byid[q]['official_answer'],byid[q]['answer_kind'])==(answer,kind),q
        assert byid[q]['official_note'],q
    special=[{'question_id':q,'official_answer':byid[q]['official_answer'],'answer_kind':byid[q]['answer_kind'],
              'source_file':byid[q]['source_file'],'source_page':byid[q]['source_page'],
              'official_note':byid[q]['official_note'],'visual_check':'true'} for q in EXCEPTIONS]
    write_csv('data/answer_exceptions.csv',special)
    report={'official_rows':len(official),'question_rows':len(questions),'join_mismatches':0,
            'unverified_official_answers':0,'exceptions':list(EXCEPTIONS),
            'verification_scope':'text-native official table parsing with structural checks; all six exception pages visually checked'}
    (ROOT/'extracted/logs/answer_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('Official answers validated:',len(questions),'including six published exceptions')
if __name__=='__main__':main()
