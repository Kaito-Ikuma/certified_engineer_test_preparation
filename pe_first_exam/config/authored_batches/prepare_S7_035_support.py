# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,digest
refs=[
 ('openstax_hess','OpenStax, Rice University','Chemistry 2e, 5.3 Enthalpy','https://openstax.org/books/chemistry-2e/pages/5-3-enthalpy','ヘスの法則、逆反応と係数倍の符号・倍率、生成エンタルピーの差を公式本文で確認。過去問固有の数値は原典で確認し独自に計算。'),
 ('openstax_born_haber','OpenStax, Rice University','Chemistry 2e, 7.5 Strengths of Ionic and Covalent Bonds','https://openstax.org/books/chemistry-2e/pages/7-5-strengths-of-ionic-and-covalent-bonds','格子解離と形成の符号慣習の相違、半分子の解離、電子獲得の方向を本文で確認。NaClの数値は過去問指定を用いる。'),
 ('openstax_batteries','OpenStax, Rice University','Chemistry 2e, 17.5 Batteries and Fuel Cells','https://openstax.org/books/chemistry-2e/pages/17-5-batteries-and-fuel-cells','鉛蓄電池の全放電反応と半反応、LiCoO2と炭素負極を公式本文で確認。過去問の濃度計算は独自の液相質量収支。'),
 ('openstax_cell_gibbs','OpenStax, Rice University','Chemistry 2e, 17.4 Potential, Free Energy, and Equilibrium','https://openstax.org/books/chemistry-2e/pages/17-4-potential-free-energy-and-equilibrium','可逆起電力とギブズエネルギー、ネルンスト式、全反応平衡で起電力0を本文で確認。'),
 ('nobel_lithium2019','Royal Swedish Academy of Sciences','Scientific Background on the Nobel Prize in Chemistry 2019: Lithium-ion Batteries','https://www.nobelprize.org/uploads/2019/10/advanced-chemistryprize2019-2.pdf','6〜9頁文字層でデンドライト、LiCoO2、吉野の石油コークス負極、後の黒鉛と界面の歴史を確認。初期材料を黒鉛と同一視しない。'),
 ('mit_redox2014','Massachusetts Institute of Technology','5.111 Lecture Summary 25: Redox and Electrochemical Cells','https://ocw.mit.edu/courses/5-111sc-principles-of-chemical-science-fall-2014/7bfbd766cbfe78a2cf6b9a92b7e9b882_MIT5_111F14_Lecture25.pdf','1〜2・4〜5・7〜9頁文字層で酸化数、半反応の保存、Q=Itと電子mol、アノード酸化・カソード還元を確認。穴埋めや電圧計を電流測定とする粗い記述は出典として転記しない。'),
 ('mit_thermoelectric2024','Massachusetts Institute of Technology, Gian Paolo Beretta','2.43 Advanced Thermodynamics, Lecture 24: Thermoelectricity','https://ocw.mit.edu/courses/2-43-advanced-thermodynamics-spring-2024/mit2_43_s24_lec24.pdf','12・14・18頁の画像を実見し、開回路熱電能の積分、ペルティエ熱、トムソン係数と電流一次項を確認。14頁の不等号の誤記を転載しない。'),
 ('mit_kerr_calendar2005','Massachusetts Institute of Technology','6.161 Modern Optics Project Laboratory: Calendar','https://ocw.mit.edu/courses/6-161-modern-optics-project-laboratory-fall-2005/pages/calendar/','講義11の電気光学変調・複屈折・Kerr effectの分類を確認。熱電現象との分類の区別だけに使用し、係数値の出典としない。')
]
p=ROOT/'references.bib';s=p.read_text()
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n+'}\n}\n'
p.write_text(s)
concepts=[('hess_thermochemistry','反応熱・ヘスの法則','燃焼熱|熱化学',['chem_physical']),('born_haber_cycle','ボルンハーバーサイクル','生成熱|格子エネルギー',['chem_physical']),('redox_electron_balance','酸化数・電子収支','還元|酸化数',['chem_physical']),('faraday_electrolysis','ファラデーの法則・電気分解','ファラデー|析出',['chem_physical']),('lead_battery_mass_balance','鉛蓄電池・電解液質量収支','鉛蓄電池',['chem_physical']),('lithium_intercalation','リチウム電池・イオン挿入','リチウムイオン',['chem_physical']),('electrochemical_gibbs','電池電位・反応自由エネルギー','標準電極電位|電池電位',['chem_physical']),('thermoelectric_effects','熱電効果・可逆熱と散逸','ゼーベック|トムソン|熱電',['physics_electro'])]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
if not all(k in ids for k,_,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_035_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat,disc in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APPLIED'],disciplines=disc))
 d['version']='1.28-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_035'
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=[dict(file=str(f.relative_to(ROOT)),sha256=digest(f)) for f in folder.iterdir() if f.is_file() and f.name!='source_notes.json'],limitations=['一部MITノートは穴埋め式。空欄を確認済みの印刷本文と扱わない。','MIT thermoelectric講義の本文数式は文字層だけで読めず、12・14・18頁の実画像で確認。','原典の電流効率、熱起電力の幾何条件、符号慣習、標準電位比較の限定を部分校正へ保持。']),ensure_ascii=False,indent=2)+'\n')
print('Concepts',len(d['concepts']))
