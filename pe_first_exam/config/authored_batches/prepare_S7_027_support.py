# coding: utf-8
import sys,json,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
 ('struct_mit_beam','David M. Parks','Euler-Bernoulli Beams: Bending, Buckling, and Vibration (MIT 2004)','https://ocw.mit.edu/courses/2-002-mechanics-and-materials-ii-spring-2004/bc25a56b5a91ad29ca5c7419616686f7_lec2.pdf','公開PDFの線形梁仮定、荷重/長さ、断面のひずみ、断面力、自重q=ρAg、端部拘束、座屈のEI/L2依存、共振の周波数の本文を確認。数式の画像読みと独自導出を併用する。'),
 ('struct_mit_buckling','Raul Radovitzky and Zachary Cordero','Buckling of Beams (MIT 2021)','https://ocw.mit.edu/courses/16-001-unified-engineering-materials-and-structures-fall-2021/mit16_001_f21_lec33lec34lec35.pdf','49頁資料の導入、初期不整/偏心、弾性臨界荷重、細長比と圧壊/遷移/座屈の条件を確認。全章通読とはしない。'),
 ('struct_mlit_limit','国土交通省航空局','空港土木施設設計要領（構造設計編）令和3年4月改訂','https://www.mlit.go.jp/koku/content/sekkeiyouryou_kouzou_R3.4kaitei.pdf','2.3.1の終局/使用/疲労/修復、疲労を終局に含める場合もあるが本基準では別、2.3.2の性能照査、3.1の作用分類と自重を実本文で確認。全151頁の規準適合を確認したとはしない。'),
 ('struct_nims_data','物質・材料研究機構','NIMS構造材料データシートの発行について（2020年4月1日）','https://www.nims.go.jp/press/2020/04/lecian00000bax6x-att/202004010.pdf','公開説明の高温荷重下の時間依存塑性変形、疲労の繰返し荷重/ひずみ、平均引張応力の試験条件を確認。各データシート本体や特定材料の寿命全域を確認したものではない。'),
 ('struct_nasa_mean','NASA','Fatigue Failure Analysis (2018)','https://ntrs.nasa.gov/api/citations/20180002396/downloads/20180002396.pdf','NASAの公開疲労解析の平均応力・振幅・修正Goodmanの適用例を確認。普遍材料法則やすべての塑性域に同じ寿命式を適用しない。'),
 ('struct_mlit_glossary','国土交通省中部道路メンテナンスセンター','用語集：比例限度・疲労・疲労設計','https://www.cbr.mlit.go.jp/chubumc/data/glossary/','項目205-207の線形比例条件と静的破壊応力未満の繰返し損傷、供用期間累積照査の公的用語を確認。')]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
new=[
 ('structural_limit_state','使用・終局・疲労の限界状態','限界状態'),
 ('structural_buckling','圧縮安定とオイラー座屈','座屈|オイラー'),
 ('structural_tensile_test','引張試験と公称応力・弾塑性','引張試験|引張強さ'),
 ('structural_reliability_probability','強度・荷重の同時分布と破壊確率','破壊確率'),
 ('structural_cost_optimization','安全率と費用モデルの最適化','安全率.*費用|費用.*安全率'),
 ('structural_failure_modes','崩壊・共振・圧壊と構造モデル','崩壊荷重|共振'),
 ('structural_fatigue_creep','疲労・クリープと局所応力集中','疲労限度|クリープ|ミーゼス'),
 ('structural_beam_scaling','断面二次モーメント・断面係数と寸法依存','たわみ|曲げ応力'),
 ('structural_specific_strength','比強度と材料価格当たり性能','比強度')]
if not all(k in ids for k,_,_ in new):
 snap=ROOT/'snapshots/config_before_S7_027_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['BASIC'],disciplines=['basic_1_3']))
 d['version']='1.20-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_027';folder.mkdir(exist_ok=True)
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],limitations=['数学的最適化と同時分布の反例は所与条件から独自導出。規準の全文適合・材料価格相場の検証ではない。']),ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
