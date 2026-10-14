from collections import defaultdict
from common import read_csv,publish_bundle
from tex_common import esc

def main():
    rows=read_csv('data/questions.csv');groups=defaultdict(list)
    for r in rows:groups[(r['subject'],r['middle_category'])].append(r)
    lines=[r'\chapter{分野別索引}',r'分類は確認済みと暫定を含む。概念タグの横断頻度は主分類の問題数と別に扱う。']
    for (subject,topic),rs in sorted(groups.items()):
        lines.extend([r'\section{'+esc(subject+'：'+topic)+'}', ', '.join(r'\hyperref['+r['tex_label']+']{'+esc(r['year']+('-再' if r['exam_session']=='RET' else '')+':'+r['question_number'])+'}' for r in rs)])
    publish_bundle({'generated/topic_index.tex':'\n'.join(lines)+'\n'})
if __name__=='__main__':main()
