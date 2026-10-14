# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,digest
refs=[
 ('pl_statute','e-Gov法令検索','製造物責任法','https://laws.e-gov.go.jp/law/406AC0000000085','1〜6条。現行条文と過去の時効規定を区別する。'),
 ('pl_qa','消費者庁','製造物責任法の概要Q&A','https://www.caa.go.jp/policies/policy/consumer_safety/other/pl_qa.html','問3〜9、12〜22、24を確認。中古品の対象性と修理業者の責任を区別する。'),
 ('pl_definitions2018','消費者庁','製造物責任法逐条解説：第2条定義（2018年9月）','https://www.caa.go.jp/policies/policy/consumer_safety/other/product_liability_act_annotations/pdf/annotations_180907_0003.pdf','物理1〜5頁（印刷2〜6頁）を画像確認。単なる冷凍・冷蔵、付合、中古品、再生品の境界。'),
 ('pl_time2018','消費者庁','製造物責任法逐条解説：消滅時効（2018年9月）','https://www.caa.go.jp/policies/policy/consumer_safety/other/product_liability_act_annotations/pdf/annotations_180907_0006.pdf','改正後規定を原則として解説する資料であり、2018年の施行済み条文とは扱わない。'),
 ('pl_transition2020','消費者庁','製造物責任法の一部改正について','https://www.caa.go.jp/policies/policy/consumer_safety/other/product_liability_act_amendment/pdf/consumer_safety_cms206_200129_01.pdf','2020年4月1日施行。生命身体侵害の短期期間を3年から5年へ変更し経過措置を定める。'),
 ('pl_nuclear_statute','e-Gov法令検索','原子力損害の賠償に関する法律','https://laws.e-gov.go.jp/law/336AC0000000147','本則4条3項に製造物責任法の不適用を確認。'),
 ('pl_product_csr2016','経済産業省','平成28年度製品安全人材育成研修：東京','https://www.meti.go.jp/product_safety/producer/pdf/28fy_jinzai/28fy_tokyo.pdf','官公庁検索索引で製品安全の社会的責任の例を確認。全文は403により取得できていない。'),
]
p=ROOT/'references.bib';s=p.read_text()
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:s+='\n@online{'+k+',\n  author = {{'+a+'}},\n  title = {'+t+'},\n  url = {'+u+'},\n  urldate = {2026-10-12},\n  note = {'+n+'}\n}\n'
p.write_text(s)
concepts=[
 ('pl_scope','製造物の有体性・動産性・加工の境界','製造物|冷凍|冷蔵'),
 ('pl_defect','通常有すべき安全性と予見可能な使用','欠陥|予見可能'),
 ('pl_proof','欠陥・損害・因果関係の立証','製造物責任|過失'),
 ('pl_producer','輸入者・表示製造業者・OEMの責任','OEM|輸入'),
 ('pl_development','開発危険と部品原材料の免責','開発危険'),
 ('pl_time','製造物責任の期間制限と法改正','時効|十年'),
 ('pl_repair_recycle','修理・中古品・再生品の責任境界','修理|再生品'),
 ('product_csr','製品安全の社会的責任と予防','製品安全|社会的責任'),
]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
if not all(k in ids for k,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_032_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APT'],disciplines=['apt_3']))
 d['version']='1.25-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'extracted/reference_checks/S7_032';files=[dict(file=str(f.relative_to(ROOT)),sha256=digest(f)) for f in p.iterdir() if f.is_file()]
(p/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=files,limitations=['逐条解説の文字抽出には文字化けがあり、定義の物理1〜5頁は画像で確認した。','ISO26000原規格全文と研修資料全文は取得していない。CSRの規格引用は問題提示条件として保持する。','初回H25APT7は冷凍冷蔵を加工と誤判定した。原記録は保持し、画像で確認した逐条解説に基づく訂正を本文で明示する。']),ensure_ascii=False,indent=2)+'\n')
print('Added references',len(refs),'concept total',len(d['concepts']))
