"""Candidate pairs, never auto-approve repeats from uncorrected OCR."""
from collections import defaultdict
from difflib import SequenceMatcher
import re,unicodedata
from common import ROOT,read_csv,csv_bytes,publish_bundle

def main():
    qs=read_csv('data/questions.csv');groups=defaultdict(list);text={}
    for r in qs:
        raw=(ROOT/r['question_text_file']).read_text();n=unicodedata.normalize('NFKC',raw);n=re.sub(r'^.{0,12}?\d+(?:[-ー]\d+)?','',n);text[r['question_id']]=re.sub(r'\s+','',n)
        groups[(r['subject'],r['discipline_id'])].append(r)
    out=[]
    for group in groups.values():
        for i,a in enumerate(group):
            for b in group[i+1:]:
                aa,bb=text[a['question_id']],text[b['question_id']]
                if min(len(aa),len(bb))/max(len(aa),len(bb),1)<.65:continue
                score=SequenceMatcher(None,aa,bb,autojunk=False).ratio()
                if score>=.78:out.append({'left_question_id':a['question_id'],'right_question_id':b['question_id'],'candidate_relation':'same_method_or_near_repeat','text_similarity':f'{score:.4f}','shared_discipline':a['discipline_id'],'negation_check':'pending','numbers_units_check':'pending','choice_mapping_check':'pending','figure_check':'pending','approval_status':'candidate','source_hash_left':a['source_sha256'],'source_hash_right':b['source_sha256']})
    publish_bundle({'data/similarity_candidates.csv':csv_bytes(out,'left_question_id right_question_id candidate_relation text_similarity shared_discipline negation_check numbers_units_check choice_mapping_check figure_check approval_status source_hash_left source_hash_right'.split())})
    print('Similarity candidates',len(out),'no automatic repeat approval')
if __name__=='__main__':main()
