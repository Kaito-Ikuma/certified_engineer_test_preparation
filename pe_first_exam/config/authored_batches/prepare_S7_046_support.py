# coding:utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,json_bytes
concepts=[('atomic_crystal_geometry','格子・配位数と最近接距離','chem_atomic'),('atomic_crystal_density','単位胞質量・体積と密度','chem_atomic'),('atomic_intermolecular','分子間力・分散とLJのエネルギー','chem_atomic'),('atomic_ionic_structures','NaCl/CsClと格子・基底','chem_atomic'),('atomic_solubility_mass','溶液分母の溶解度と析出収支','chem_physical'),('atomic_natural_delta','自然試料のδ代表値と基準尺度','earth_isotope'),('atomic_lattice_vibrations','格子比熱・散乱と磁区応答','chem_atomic'),('atomic_optical_molecules','分子光吸収・選択則と光異性化','physics_optics'),('atomic_orbital_spin','空間軌道・スピンと結合対称性','chem_atomic'),('atomic_bond_order','結合次数と電子対配置のモデル','chem_atomic'),('atomic_light_devices','電子準位遷移と光素子','physics_modern'),('atomic_electron_configuration','電子配置・容量と原子データ','chem_atomic'),('atomic_bravais','Bravais格子・基底と逆格子','chem_atomic')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());snap=ROOT/'snapshots/config_before_S7_046_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes());ids={x['id'] for x in d['concepts']}
for k,t,scope in concepts:
 assert k not in ids;d['concepts'].append(dict(id=k,label=t,pattern=t,subjects=['APPLIED'],disciplines=[scope]))
d['version']='1.39-S7-concept-additions';p.write_bytes(json_bytes(d))
refs=[
('atomic_quantum','OpenStax / Rice University','Chemistry 2e 6.3: Development of Quantum Theory','https://openstax.org/books/chemistry-2e/pages/6-3-development-of-quantum-theory','本文の空間軌道3量子数と全電子のスピン、Pauli原理を確認。'),
('atomic_phi2014','Stefan G. Minasian and others','New evidence for 5f covalency in actinocenes determined from carbon K-edge XAS and electronic structure theory','https://laro.lanl.gov/esploro/outputs/journalArticle/New-evidence-for-5f-covalency-in/9916369894203761','2014年原研究の著者研究所公開要旨を読了。thoroceneのphi軌道相互作用を確認。単純二原子の純phi結合の証明とはしない。出版社全文は403。DOI 10.1039/c3sc52030g。'),
('atomic_nist2019','NIST','Periodic Table: Atomic Properties of the Elements, July 2019','https://www.nist.gov/system/files/documents/2019/12/10/nist_periodictable_july2019.pdf','PDF1頁を実画像で確認。O/Ne/Kr/Cu/Znの電子配置、Na/Mg/Ar/Krの原子番号・第一イオン化エネルギーを使用。定義定数を過去問指定値へ置換しない。'),
('atomic_nonbond','John McMurry / OpenStax','Organic Chemistry 2.12: Noncovalent Interactions between Molecules','https://openstax.org/books/organic-chemistry/pages/2-12-noncovalent-interactions-between-molecules','本文の瞬間双極子・誘起双極子と水素結合の供与受容を確認。代表的N/Oの説明を全水素結合の定義上限にしない。'),
('atomic_lj','OpenStax / Rice University','University Physics Volume 1, 15.2: Energy in Simple Harmonic Motion','https://openstax.org/books/university-physics-volume-1/pages/15-2-energy-in-simple-harmonic-motion','公開検索収録の12–6ポテンシャルの符号を確認。力の指数13/7は独自微分。'),
('atomic_cnt','Satoshi Ishii and Yoshihiko Takano / NIMS','Development of Carbon Nanotubes with High Electrical Conductivity','https://www.nims.go.jp/NFM/NIMS-NOW/NIMSNOW_2007V05No05P08E_HighConductiveCarbonNanotube.pdf','2007冊子1頁文字層全文を読了。巻き方による導電/半導体とホウ素ドープを確認。図の数値を読み取っていない。'),
('atomic_diamond','NIMS','Ultra-wide Bandgap Semiconductors Group','https://www.nims.go.jp/electr-opt/UWBG_e.html','公式研究紹介の検索収録で5.5eVのギャップを確認。半導体化技術と通常純結晶を区別。'),
('atomic_sulfate','IAEA','Reference Materials: NBS-127','https://analytical-reference-materials.iaea.org/nbs-127','公開本文の海水硫酸由来BaSO4とdelta34S約+20.3‰、旧CDT脚注を確認。全海水の厳密定数ではない。'),
('atomic_bravais_ref','International Union of Crystallography','Nomenclature for crystal families, Bravais-lattice types and arithmetic classes','https://www.iucr.org/who-we-are/commissions/commission-on-crystallographic-nomenclature/published-reports/bravais','1984受理の委員会報告公開要旨で3次元14種類を確認。'),
('atomic_phonon','MIT OpenCourseWare','5.62 Lecture Summary 21: Thermodynamics of Solids, Einstein and Debye Models','https://ocw.mit.edu/courses/5-62-physical-chemistry-ii-spring-2008/3a7d85a0544e4f24a16ae196566108b7_21_562ln08.pdf','PDF2頁の格子正規振動、公開検索収録のEinstein/Debyeと低温比熱を確認。全数式の文字層は乱れている。'),
('atomic_barkhausen','Pierre Cizeau and Stefano Zapperi and Gianfranco Durin and H. Eugene Stanley','Dynamics of a ferromagnetic domain wall and the Barkhausen effect','https://arxiv.org/abs/cond-mat/9709300','1997年原研究の要旨を読了。駆動磁区壁と不連続応答を確認。全本文の指数検証をしたとはしない。'),
('atomic_retinal','Olaf Strauss / Webvision','The Retinal Pigment Epithelium','https://www.ncbi.nlm.nih.gov/books/NBK54392/','公開検索収録の11cisレチナールと光子による活性化・異性化を確認。直接閲覧はCAPTCHAで、全章読了ではない。'),
('atomic_ir_raman','MIT OpenCourseWare','3.014 Materials Laboratory: Network Glasses','https://ocw.mit.edu/courses/3-014-materials-laboratory-fall-2006/4ec2a53dc99af235b1ec00f19d4a9b6e_g3_ntwrkglasses.pdf','PDF15頁のIR双極子変化とRaman分極率を確認。後続の実験操作や仮想準位の表現は使用しない。'),
('atomic_linewidth','NIST','MATS Summary','https://pages.nist.gov/MATS/MATS%20Summary.html','公開本文の温度・質量依存Doppler幅と衝突半幅を確認。'),
('atomic_photosynthesis','OpenStax / Rice University','Concepts of Biology 5.2: The Light-Dependent Reactions of Photosynthesis','https://openstax.org/books/concepts-biology/pages/5-2-the-light-dependent-reactions-of-photosynthesis','公開検索本文でクロロフィル光吸収とNADPからNADPHへの電子受容を確認。'),
('atomic_ir_co2','NASA','Climate and Earth’s Energy Budget','https://science.nasa.gov/earth/earth-observatory/climate-and-earths-energy-budget/','公開検索本文でCO2の熱赤外吸収と可視付近の入射太陽光を区別。')]
p=ROOT/'references.bib';s=p.read_text();esc=lambda x:x.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
for key,author,title,url,note in refs:
 assert '@online{'+key+',' not in s;s+='\n@online{'+key+',\n author={'+esc(author)+'},\n title={'+esc(title)+'},\n url={'+url+'},\n urldate={2026-10-12},\n note={'+esc(note)+'}\n}\n'
p.write_text(s)
p=ROOT/'extracted/reference_checks/S7_046/source_notes.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json_bytes({'reference_date':'2026-10-12','references':[dict(zip(['key','author','title','url','scope'],x)) for x in refs],'nist_visual':'extracted/reference_checks/S7_046_nist_periodic.png','retained_discrepancies':['R01-REG-APPLIED-14','R02-REG-APPLIED-10']}))
print('Added concepts',len(concepts),'references',len(refs))
