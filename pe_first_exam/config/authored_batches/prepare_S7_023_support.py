# coding: utf-8
import sys,json,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('modern_series','U.S. Environmental Protection Agency','Natural Gamma and Spectral Gamma Borehole Logging','https://www.epa.gov/environmental-geophysics/natural-gamma-and-spectral-gamma-borehole-logging','U/Th壊変系列が安定Pbへ至る公式公開本文を確認。自然放射線探査への利用と核種の終点を区別。'),
('si_cgpm2018','BIPM','Resolution 1 of the 26th CGPM (2018)','https://www.bipm.org/en/-/resolution-cgpm-26-1','2019-05-20発効と7定数・基本単位、原器等旧定義廃止の公式本文を確認。'),
('si_brochure9','BIPM','The International System of Units, 9th Edition','https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf','現在公開版4.01の基本単位・組立単位・歴史節の公開本文。全214頁通読ではない。cd含む7基本単位と540THz/683lm/W、定義と実現を分離。'),
('si_kelvin2007','BIPM','Resolution 10 of the 23rd CGPM (2007)','https://www.bipm.org/en/-/resolution-cgpm-23-10','出題前旧K定義は水三重点273.16K、同位体組成条件も明示。凝固点とは別。'),
('si_kelvin_realization','BIPM','Mise en pratique for the definition of the kelvin in the SI','https://www.bipm.org/documents/20126/41489682/SI-App2-kelvin.pdf/','2019文書PDF物理3頁：新K定義で三重点は最良推定273.16K、標準不確かさ0.1mK。R01再試験の0.01Cを厳密固定値にしない。'),
('si_nist811','NIST','Guide for the Use of the International System of Units, SP 811 (2008)','https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication811e2008.pdf','付録Bの公開本文でkgf/cm2=9.80665e4Pa、psi、標準atm、通常mmHg、St=1e-4m2/sを確認。旧基本単位定義を現行へ転用しない。'),
('modern_mit_nuclear','Massachusetts Institute of Technology','22.02 Introduction to Applied Nuclear Physics: Chapter 1','https://ocw.mit.edu/courses/22-02-introduction-to-applied-nuclear-physics-spring-2012/d0d046f78c917f107d925f11ac862ae4_MIT22_02S12_lec_ch1.pdf','物理14〜15頁の質量放物線、beta Q値、gamma核種不変の本文を確認。単一放物線近似と偶奇性を区別。'),
('modern_mit_mass','Massachusetts Institute of Technology','22.01 Mass Parabolas Continued, Stability, and Half Life (2016)','https://ocw.mit.edu/courses/22-01-introduction-to-nuclear-engineering-and-ionizing-radiation-fall-2016/070796817aacbd95389fc57d7d9ced35_mJ54DfN95Zo.pdf','講義記録物理13頁の偶偶/奇奇の対エネルギー・単純に下方へ遷移できないことを確認。全講義視聴ではない。'),
('modern_doublebeta','Brookhaven National Laboratory, NNDC','Double-Beta Decay Nuclear Data','https://www.nndc.bnl.gov/bbdecay/index.html','128/130Te等の観測された二重beta遷移を確認。現在の2025評価を2011出題値へ代入しない、精密半減期は引用しない。'),
('modern_fastfission','U.S. Nuclear Regulatory Commission','Fast Fission','https://www.nrc.gov/reading-rm/basic-ref/glossary/fast-fission','公式用語の公開本文、238U高速と235U熱中性子核分裂を区別。'),
('modern_alpha','U.S. Environmental Protection Agency','Radiation Basics','https://www.epa.gov/radiation/radiation-basics','alpha外部侵入は弱く、体内取込みでは影響が大きくなり得る。線量・経路等の条件を省いて全alphaに一定被害を割り当てない。'),
('modern_dose','IAEA','Radiation Protection and Safety of Radiation Sources: International Basic Safety Standards','https://nucleus.iaea.org/sites/nss-oui/Published%20Collections/m_3761d926-c16f-4477-a63b-741a9db1c16c/m_3761d926-c16f-4477-a63b-741a9db1c16c__50_0.Html','用語節のHT=sum wR DTR、E=sum wT HT、GyとSv、確定的影響の治療判断へ等価線量を転用しない注記を確認。法定限度は扱わない。'),
('modern_pv','U.S. Department of Energy','Solar Photovoltaic Cell Basics','https://www.energy.gov/cmei/systems/solar-photovoltaic-cell-basics','半導体への光吸収が電子へエネルギーを与える本文を確認。'),
('modern_oled','U.S. Department of Energy','OLED Basics','https://www.energy.gov/cmei/ssl/oled-basics','炭素系半導体に電極から電流を与えて発光、材質で色が決まる本文を確認。'),
('modern_led','U.S. Department of Energy','Cooling with Electroluminescent Semiconductors','https://stage.energy.gov/science/bes/articles/cooling-electroluminescent-semiconductors','公開研究概要のLEDキャリアによる光子放出、バンドギャップを確認。'),
('modern_superconduct','U.S. Department of Energy','DOE Explains: Superconductivity','https://www.energy.gov/science/doe-explainssuperconductivity','臨界温度以下でDC無損失・磁場排除の本文確認。電子対説明は関連DOE原著解説と併用。'),
('modern_pairs','U.S. Department of Energy','Cracking the Mystery of Perfect Efficiency: Investigating Superconductors','https://www.energy.gov/science/articles/cracking-mystery-perfect-efficiency-investigating-superconductors','電子対とBCS理論の公開研究説明を確認。全超伝導体の媒介機構を通常フォノンに固定しない。'),
('modern_laser','Nobel Foundation','Advanced Information on the Nobel Prize in Physics 2000','https://www.nobelprize.org/uploads/2018/06/advanced-physicsprize2000-3.pdf','半導体レーザーのヘテロ構造・発光活性層・共振器の公開説明を確認。刺激放出の一般原理は既存光電資料と接続。')]
p=ROOT/'references.bib';t=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',t))
for k,a,title,u,n in refs:
 if k not in keys:t+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+title+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(t)
d=ROOT/'extracted/reference_checks/S7_023';d.mkdir(parents=True,exist_ok=True)
(d/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=title,url=u,checked_claim=n) for k,a,title,u,n in refs],reused=['os_matter','os_photoelectric'],limitations=['PDF公開部分と全通読を区別。','SI定義は出題時・2019改定後を区別。','H23核問題のbeta安定の全称と内部被曝の条件を保持。']),ensure_ascii=False,indent=2)+'\n')
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
new=[('si_definitions','SI基本単位の定義・改定','基本単位|国際単位系|キログラム原器','physics_units'),('radiation_dosimetry','放射線量の物理量・防護量','吸収線量|等価線量|実効線量','physics_modern'),('optoelectronic_devices','光と電子励起を利用する素子','発光ダイオード|太陽電池|半導体レーザー|有機EL','physics_modern')]
if not all(k in ids for k,_,_,_ in new):
 snap=ROOT/'snapshots/config_before_S7_023_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,label,pat,disc in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pat,subjects=['APPLIED'],disciplines=[disc]))
 old=d['version'];d['version']='1.16-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/'config/concept_change_log_S7.json';log=json.loads(p.read_text());log.append(dict(time=now(),batch='S7_023_modern_units',previous_version=old,version=d['version'],added=[x[0] for x in new],reason='19原典で単位換算と歴史的定義を分離。線量を材料応力から、光素子を一般磁性から修正。既存原子核と物質波は再利用。152概念版保存。'));p.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print('references',len(refs),'concepts',len(d['concepts']))
