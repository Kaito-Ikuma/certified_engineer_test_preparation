# coding: utf-8
import json,shutil,re
from pathlib import Path
P=Path(__file__).resolve().parents[2]
cp=P/'config/concepts.json'
assert not (P/'extracted/logs/config_before_S7_059_concept.json').exists()
shutil.copyfile(cp,P/'extracted/logs/config_before_S7_059_concept.json')
c=json.loads(cp.read_text());assert c['version']=='1.52'
q=json.loads((P/'config/authored_batches/S7_059_environment_finish_middle.json').read_text())['questions']
existing={x['id'] for x in c['concepts']};groups={}
for x in q:
 if x['concept_id'] not in existing:groups.setdefault(x['concept_id'],x)
for k,x in groups.items():
 c['concepts'].append({'id':k,'label':x['summary'].rstrip('。'),'pattern':x['summary'].rstrip('。'),'subjects':['BASIC'],'disciplines':sorted({y['discipline_id'] for y in q if y['concept_id']==k})})
c['version']='1.53';cp.write_text(json.dumps(c,ensure_ascii=False,indent=2))
refs=[
('epr','OECD','Extended Producer Responsibility: updated guidance 2016','https://www.oecd.org/content/dam/oecd/en/publications/reports/2016/09/extended-producer-responsibility_g1g6742c/9789264256385-en.pdf','検索本文の製品責任を使用後段階へ広げる定義を確認。全書の読了ではない。'),
('ndc','UNFCCC','Nationally Determined Contributions','https://unfccc.int/process-and-meetings/the-paris-agreement/nationally-determined-contributions-ndcs','公式検索本文で五年ごとの提出を確認。同機関のIntroduction to Mitigation検索で緩和との対応を確認。協定全条文未読。'),
('energy2019','資源エネルギー庁','エネルギー白書2019:一次エネルギー','https://www.enecho.meti.go.jp/about/whitepaper/2019html/2-1-3.html','公式検索本文の2017中東約87%を確認。家庭部門要因は同庁2019年度統計PDF検索を補助に用いた。全表・全四石油統計の確定ではない。'),
('lawrence','Nobel Prize Outreach','Physics1939 award ceremony speech','https://www.nobelprize.org/prizes/physics/1939/ceremony-speech/','公式検索本文の1930初期サイクロトロンとLawrenceらを確認。全授賞演説読了ではない。'),
('smart','資源エネルギー庁','省エネポータル:省エネって何','https://www.enecho.meti.go.jp/category/saving_and_new/saving/general/what/index.html','検索本文の計測器の遠隔検針等とHEMSの利用を確認。全機器仕様を確認したものではない。'),
('jenner','World Health Organization','Smallpox vaccines','https://www.who.int/news-room/feature-stories/detail/smallpox-vaccines','WHO公式検索本文のJenner1796を確認。個別接種原記録や医学助言の用途ではない。'),
('ecodrr','環境省','令和元年白書:我が国の適応に係る取組','https://www.env.go.jp/policy/hakusyo/r01/html/hj19010204.html','公式検索本文の緩和・適応と生態系を活用するEco-DRRを確認。白書全章読了ではない。'),
('plastic','環境省','プラスチック資源循環戦略について','https://plastic-circulation.env.go.jp/about/senryaku','公式本文索引で2019年5月31日と3R+Renewableを確認。原典R02の6月との差異を留保。2017輸出原表未読。'),
('juse','日本科学技術連盟','品質管理ナレッジ・歴史','https://www.juse.or.jp/faq_knowledge/knowledge/index.html','公式検索本文で1950Deming講義と統計的手法の普及を確認。同団体資料で1929の個別統計利用も確認し、戦前利用ゼロとはしない。')]
def esc(s):
 return re.sub(r'(?<!\\)%',r'\\%',s).replace('&',r'\&').replace('_',r'\_')
f=P/'references.bib';s=f.read_text();notes=[]
for k,a,t,u,n in refs:
 k='env59_'+k;assert '@online{'+k+',' not in s
 s+='\n@online{'+k+',\n author={{'+esc(a)+'}},\n title={'+esc(t)+'},\n url={'+u+'},\n note={'+esc(n)+'},\n urldate={2026-10-14}\n}\n'
 notes.append({'key':k,'url':u,'reading_scope':n,'full_source_read':False})
f.write_text(s);(P/'extracted/logs/source_notes_S7_059.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
print('Added',len(groups),'concepts',len(refs),'references')
