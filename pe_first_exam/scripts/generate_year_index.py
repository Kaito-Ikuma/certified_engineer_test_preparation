from common import ROOT,YEARS,read_csv,publish_bundle,year_label
from tex_common import esc,qref

def main():
    rows=read_csv('data/questions.csv');lines=[r'\chapter{年度別索引}',r'全1,270問の登録索引。リンク先の校正・執筆状態を確認する。']
    for year in YEARS:
        lines.append(r'\section{'+year_label(year)+'}')
        for sub,title in [('BASIC','基礎'),('APT','適性'),('APPLIED','応用理学')]:
            group=[r for r in rows if r['source_year_directory']==year and r['subject']==sub]
            lines.append(r'\paragraph{'+title+f'（{len(group)}問）'+'} '+', '.join(qref(r) for r in group))
    publish_bundle({'generated/yearly_index.tex':'\n'.join(lines)+'\n'})
if __name__=='__main__':main()
