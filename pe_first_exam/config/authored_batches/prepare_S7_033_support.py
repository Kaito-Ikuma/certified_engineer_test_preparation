# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,digest
refs=[
 ('iupac_greenbook2012','IUPAC','Quantities, Units and Symbols in Physical Chemistry, third edition, second printing','https://iupac.org/wp-content/uploads/2019/05/IUPAC-GB3-2012-2ndPrinting-PDFsearchable.pdf','印刷58・61・63〜65頁の定義表と注記を文字層で確認。印刷64〜65頁（物理78〜79頁）は画像でも確認。'),
 ('mit_kinetics2013','Massachusetts Institute of Technology','Atmospheric Chemistry: Lecture 2, Chemical Kinetics','https://ocw.mit.edu/courses/1-84j-atmospheric-chemistry-fall-2013/2ad7eaba000b770595a604bdb6a6f310_MIT1_84JF13_Lec2_kinetics1.pdf','速度式、障壁模型、衝突模型、遷移状態模型を確認。模型の省略は本文で区別する。'),
 ('mit_buffer2008','Catherine Drennan and Elizabeth Vogel Taylor','Principles of Chemical Science: Lecture 23 transcript','https://ocw.mit.edu/courses/5-111-principles-of-chemical-science-fall-2008/48fccce09a655f756fadde73892f57c1_5-111F08-L23.pdf','弱酸塩基の共役対、血液の緩衝、濃度と緩衝容量、中和後の全体積について該当段落を確認。'),
 ('iupac_catalyst','IUPAC','Gold Book: catalyst','https://goldbook.iupac.org/terms/view/C00876','本文の直接取得は403。公式検索索引に表示された定義の範囲で、速度増大・標準ギブズエネルギー不変・負触媒を用いない用語方針を確認。'),
 ('niosh_hf','NIOSH','Hydrogen Fluoride / Hydrofluoric Acid: Systemic Agent','https://www.cdc.gov/niosh/ershdb/emergencyresponsecard_29750030.html','公式本文のdescriptionで弱酸と有害性、ガラス腐食、40パーセント超水溶液の発煙を確認。医療解説には使用しない。')
]
p=ROOT/'references.bib';s=p.read_text()
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:
  s+='\n@online{'+k+',\n  author = {{'+a+'}},\n  title = {'+t.replace('&',r'\&')+'},\n  url = {'+u+'},\n  urldate = {2026-10-12},\n  note = {'+n+'}\n}\n'
p.write_text(s)
concepts=[
 ('chemical_catalysis','触媒・反応経路・平衡不変','触媒'),
 ('salt_hydrolysis','中和後の塩の加水分解とpH','中和|加水分解'),
 ('reaction_equilibrium_shift','反応商による化学平衡移動','アンモニア|四酸化二窒素'),
 ('solubility_product','溶解度積・pH・共通イオン','溶解度積|水酸化マグネシウム'),
 ('acid_base_definitions','酸塩基の定義と溶媒依存性','ルイス|酸化物イオン'),
 ('hf_properties','フッ化水素の物性と酸解離','フッ化水素'),
 ('collision_diffusion_kinetics','衝突・反応断面積・拡散律速','衝突頻度|拡散律速'),
 ('reaction_gibbs_equilibrium','反応ギブズエネルギー・活量・平衡定数','平衡定数|自由エネルギー'),
 ('buffer_equilibrium','共役酸塩基対・緩衝容量・pH','緩衝')
]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
if not all(k in ids for k,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_033_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APPLIED'],disciplines=['chem_inorganic'] if k=='hf_properties' else ['chem_physical']))
 d['version']='1.26-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_033'
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=[dict(file=str(f.relative_to(ROOT)),sha256=digest(f)) for f in folder.iterdir() if f.is_file() and f.name!='source_notes.json'],limitations=['QMUL版Green Bookの文字層は文字化けしたため、IUPAC公式の検索可能版に切り替えた。','Gold Book各項目と1996年速度論資料の直接取得は403等で失敗。全文取得済みと扱わない。','R02応用13の反応速度比と公式2の一意性、HF物性の一部、負触媒・pKa等の原典用語、模型の適用条件は個別の部分校正に残す。']),ensure_ascii=False,indent=2)+'\n')
print('Concept total',len(d['concepts']))
