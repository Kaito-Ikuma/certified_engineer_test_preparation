# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,digest
refs=[
 ('mit_colligative2008','Massachusetts Institute of Technology','Thermodynamics and Kinetics: Lecture 23, Colligative Properties','https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/f48ecc8d62ef6e1d0e3c72317cb067a7_lec_23.pdf','4頁の文字層で希薄条件、質量モル濃度、化学ポテンシャル、凝固点降下の関係を確認。資料ヘッダはSpring 2007、公開講義は2008。'),
 ('nptel_distillation1','NPTEL, IITs and IISc','Mass Transfer Operation 1, Module 5: Distillation, Lecture 1','https://archive.nptel.ac.in/content/storage2/courses/103103035/module5/lec1.pdf','1・4〜7頁の文字層で蒸留の目的、相対揮発度、平衡曲線、共沸を確認。蒸気圧の量依存など原資料の粗い記述は教材へ一般則として転載しない。'),
 ('nptel_azeotrope','NPTEL','Vapour-Liquid Equilibria: Description of General VLE Behavior','https://archive.nptel.ac.in/content/storage2/courses/103101004/modules/chapter-7/sec-4/1.9.html','取得HTMLの本文で共沸の気液組成一致と蒸発時の濃縮不能を確認。式画像は数式の出典として使わない。'),
 ('iapws_supercooled2015','IAPWS','Guideline on Thermodynamic Properties of Supercooled Water','https://iapws.org/technical-guidance/release/Supercooled.download','2015年指針7〜8頁の文字層で準安定液体の適用範囲、大気圧近傍を確認。旧PDF URLはHTMLへリダイレクトしたため現行公式downloadを取得。'),
 ('iapws95_2018','IAPWS','Revised Release on the IAPWS Formulation 1995 for Ordinary Water Substance','https://iapws.org/technical-guidance/release/IAPWS-95.download','2018年改訂資料2〜3頁で温度尺度、臨界温度647.096 K、密度322 kg/m3を確認。旧mailホストは証明書エラー、現行公式URLで取得。'),
 ('leybold_cryopump','Leybold','How does a Cryopump work?','https://www.leybold.com/en/knowledge/vacuum-fundamentals/vacuum-generation/how-does-a-cryopump-work','公式本文の冷面捕捉、凝縮、低温吸着、再生を確認。吸着と凝縮の結合エネルギーを取り違えた一文は引用しない。'),
 ('openstax_colloids','OpenStax, Rice University','Chemistry 2e, 11.5 Colloids','https://openstax.org/books/chemistry-2e/pages/11-5-colloids','公式本文で分子イオン溶液との区別、チンダル効果、乳濁液、マヨネーズ、石けんの構造と乳化作用を確認。')
]
p=ROOT/'references.bib';s=p.read_text()
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n+'}\n}\n'
p.write_text(s)
concepts=[
 ('colligative_properties','束一的性質・凝固点降下','凝固点|不揮発性'),
 ('vapor_pressure_conditions','飽和蒸気圧・沸騰・密封条件','蒸気圧|沸騰'),
 ('distillation_equilibrium','蒸留・気液平衡比・共沸','蒸留|還流|共沸'),
 ('cryogenic_vacuum','真空排気・低温凝縮吸着','クライオ|真空ポンプ'),
 ('phase_state_thermodynamics','相状態・臨界・実在気体','臨界|化学ポテンシャル'),
 ('water_phase_metastability','水の相変化・過冷却','過冷却|三重点'),
 ('colloidal_dispersion','コロイド分散・会合・乳化','コロイド|チンダル')
]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
if not all(k in ids for k,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_034_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APPLIED'],disciplines=['chem_physical']))
 d['version']='1.27-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_034'
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=[dict(file=str(f.relative_to(ROOT)),sha256=digest(f)) for f in folder.iterdir() if f.is_file() and f.name!='source_notes.json'],limitations=['supercooled.pdfは名前に反してHTMLであり、PDF解析に失敗した。actual.pdfだけを指針の本文確認に用いた。','旧mail.iapws.orgでSSL検証失敗、証明書検証を無効にせず現行公式に切り替えた。','原典の容器条件、平衡定数、96%の基準等は部分校正に保存する。']),ensure_ascii=False,indent=2)+'\n')
print('Concepts',len(d['concepts']))
