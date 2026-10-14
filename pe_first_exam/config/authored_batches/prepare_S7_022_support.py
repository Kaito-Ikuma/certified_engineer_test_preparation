# coding: utf-8
"""Primary-source notes and small, versioned concept additions for isotope drafts."""
import sys,json,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('iso_standards1995','IAEA','Reference and Intercomparison Materials for Stable Isotopes of Light Elements, TECDOC-825','https://www-pub.iaea.org/MTCD/Publications/PDF/te_825_prn.pdf','1995年報告の検索公開本文。SMOW/PDBの旧名称廃止勧告、VPDBのNBS19尺度、硫黄CDTの不均一と枯渇、IAEA-S-1でVCDTを実現する勧告。全PDFを通読したとは扱わない。'),
('iso_vsmow2','IAEA','VSMOW2 Reference Material','https://analytical-reference-materials.iaea.org/vsmow2','公式公開本文。2009年リリース、VSMOW/SLAPへ直接校準するVSMOW2/SLAP2。物質と尺度、旧原典名称を区別。'),
('iso_vcdt','IAEA','IAEA-S-1 Reference Material','https://analytical-reference-materials.iaea.org/iaea-s-1','公式公開本文。1995年リリース、硫化銀IAEA-S-1でVCDTを定義実現、δ34S=-0.30‰。出題前からVCDTが使用されており単なる後年改訂ではない。'),
('iso_oxygen','NASA','Paleoclimatology: The Oxygen Balance','https://science.nasa.gov/earth/earth-observatory/paleoclimatology-the-oxygen-balance/','2005年本文の蒸発凝縮・氷床に16O隔離・低温で炭酸塩18Oが増える作用を確認。海水局所淡水入力と温度効果を分ける。'),
('iso_hydrothermal','地質調査所','酸素及び水素同位体によるカルデラ底熱水系の復元','https://www.gsj.jp/data/bull-gsj/29-10_05.pdf','講演要旨の検索公開本文。高温水岩反応で熱水が18Oに富み、天水起源熱水のOシフト、岩石側の18O減少を記述。全称として全熱水の同位体を固定しない。'),
('iso_tritium_clock','U.S. Geological Survey','Reston Groundwater Dating Laboratory: 3H/3He Dating Background','https://water.usgs.gov/lab/3h3he/background/','公式公開本文。1952年以降核実験・1963〜64ピーク、親娘比の時計、気液平衡・過剰空気・マントル/放射起源He等を分離する質量収支。旧半減期12.43と原典約12.3は有効数字を区別。'),
('iso_tritium2023','IAEA','IAEA Comprehensive ALPS Report, Annex 5: Tritium in the Environment','https://www.iaea.org/sites/default/files/iaea_comprehensive_alps_report.pdf','附属書5の検索公開本文で3H放射性・β壊変・半減期12.3年、自然/人工起源を確認。医療影響の説明には用いない。'),
('iso_groundwater','U.S. Geological Survey','Groundwater Age','https://www.usgs.gov/mission-areas/water-resources/science/groundwater-age?qt-science_center_objects=0','公式公開本文。若い水のトレーサー、14C約1000〜30000年、4HeのUTh起源、古い水と見かけ年代の区別。年代レンジは機器・試料条件に依存。'),
('iso_deadcarbon','U.S. Geological Survey','Age-Dating Ground Water Beneath Tinker Air Force Base, Midwest City, Oklahoma, 2003-04','https://pubs.usgs.gov/fs/2005/3099/','公式公開本文。14C物理半減期5730年、非放射性炭素が化学反応で加わると未補正見かけ年代が古くなる。若い有機炭素の混入は逆もあり得る。'),
('iso_radiometric','U.S. Geological Survey','Geologic Time: Radiometric Time Scale','https://pubs.usgs.gov/gip/geotime/radiometric.html','公式公開本文。14C約5万年範囲、親娘式、KArは条件により数千年も可能。長半減期だけを理由に若い年代を絶対不可としない。掲載Rb半減期等を現在の精密値へ転用しない。'),
('iso_zircon','U.S. Geological Survey','Uranium-Lead Geochronology of Proterozoic Rocks in Central New Mexico','https://pubs.usgs.gov/of/1997/0116/report.pdf','検索公開導入。ジルコンU-Pb結晶年代、変質抵抗、継承核と見かけ中間年代、粒子選択と解釈の必要。全本文未通読。'),
('iso_shell','産業技術総合研究所 地質調査総合センター','平成25年度沿岸域の地質・活断層調査研究報告','https://www.gsj.jp/data/coastal-geology/GSJ_INTERIMREP_065_2014_02.pdf','誌面16検索公開本文。貝殻等のAMS、CALIB6.0/MARINE09、地域的海洋リザーバー補正。2014年の使用例を最新の校準曲線とは称さない。'),
('iso_cl36','Scientific Reports','Fast Long-Term Denudation Rate of Steep Alpine Headwalls Inferred from Cosmogenic 36Cl Depth Profiles','https://www.nature.com/articles/s41598-019-46969-0','2019年原著公開本文Methods。Ca/K等核破砕、35Cl低エネルギー中性子捕獲、ミューオン。石灰岩はCaが主な核破砕標的だがCl捕獲経路も実在。R07肢4の科学的排他性を未確定に保持。'),
('iso_cl36_uw','University of Washington Cosmogenic Isotope Laboratory','STONE AGE: Cl-36 Exposure Age Calculator, Version 0.1','https://hess.ess.washington.edu/math/old/cl_input.html','研究室2002年公開実装説明。Ca/K/Fe/Ti核破砕、35Cl二次中性子捕獲、放射起源中性子捕獲を別項目。旧版計算機の精度を現在へ保証しない。'),
('iso_be10','Scientific Reports','Extreme Decay of Meteoric Beryllium-10 as a Proxy for Persistent Aridity','https://www.nature.com/articles/srep17813','2015年原著公開検索本文。大気N/Oの二次中性子核破砕、BeO/Be(OH)2のエアロゾル付着、湿性乾性沈着、閉鎖堆積物年代モデル。全本文通読とは扱わない。'),
]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
d=ROOT/'extracted/reference_checks/S7_022';d.mkdir(parents=True,exist_ok=True)
(d/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],reused=['gc_meteoric'],limitations=['公開本文、検索本文、旧研究報告を区別。','CDT/SMOW/PDB旧名称を原典から消さず、出題前から存在したV尺度と物質の対応を説明。','Cl36のCa主経路とCl中性子捕獲経路を両方保持し、公式4を科学的一意性へ昇格しない。']),ensure_ascii=False,indent=2)+'\n')
new=[('water_isotope_fractionation','自然水の同位体分別・気候と水岩反応','天水線|同位体分別'),
('water_isotope_age','水の放射性トレーサーと滞留時間','3H|3He|トリチウム'),
('cosmogenic_nuclides','宇宙線生成核種・露出と堆積年代','宇宙線.*核種|核破砕')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
if not all(n[0] in ids for n in new):
 snap=ROOT/'snapshots/config_before_S7_022_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,label,pattern in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pattern,subjects=['APPLIED'],disciplines=['earth_isotope']))
 modified=[]
 for c in d['concepts']:
  if c['id']=='isotope_general' and 'earth_isotope' not in c['disciplines']:
   c['disciplines'].append('earth_isotope');modified.append(c['id'])
 old=d['version'];d['version']='1.15-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/'config/concept_change_log_S7.json';log=json.loads(p.read_text());log.append(dict(time=now(),batch='S7_022_isotope',previous_version=old,version=d['version'],added=[n[0] for n in new],modified_disciplines=modified,reason='同位体15原典の標準・放射年代の既存概念を再利用。水分別、水時計、宇宙線核種のみを追加。149概念版保持。'));p.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
