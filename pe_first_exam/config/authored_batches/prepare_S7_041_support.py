# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,json_bytes,digest
base='https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/'
refs=[
('mit_material_elastic2000','David Roylance','Introduction to Elasticity',base+'e8b60e8a1efb6e7275372cc77f23ae9b_MIT3_11F99_elas_1.pdf','表紙2000年1月21日。単軸応力・公称ひずみ・Hooke則と強度対剛性の本文を確認。'),
('mit_material_stressstrain2001','David Roylance','Stress-Strain Curves',base+'d4ea545640f151bb66e6d8bc0ba55ed4_MIT3_11F99_ss.pdf','2001年8月23日。本文1--6頁の公称応力/ひずみ、現在面積と対数ひずみ、弾性と塑性を確認。全15頁の読了とはしない。'),
('mit_material_dislocations2001','David Roylance','Dislocation Basis of Yield and Creep',base+'339d0d74796cc35538c78bbed818b629_MIT3_11F99_dn.pdf','本文の転位移動、加工硬化、粒界障害、焼なまし・再結晶、Hall--Petch式を確認。単位胞と原子数の導出は教材独自である。'),
('mit_material_fracture2001','David Roylance','Introduction to Fracture Mechanics',base+'e5bca953e1dbd0cd0376f0f77033dc0d_MIT3_11F99_frac.pdf','2001年6月14日。き裂とGriffithエネルギーの本文、Cometの窓周辺リベット孔の説明を確認。全事故の起点の保証とはしない。'),
('mit_material_fatigue2001','David Roylance','Fatigue',base+'f678e01017186c53d45845ad93c07938_MIT3_11F99_fatigue.pdf','2001年5月1日。冒頭とS--N本文で繰返し損傷、き裂成長、疲労限度の材料依存を確認。'),
('mit_material_atomistic2001','David Roylance','Atomistics of Elasticity',base+'47b8bb075c947c20da6f30ac2fbb0719_MIT3_11F99_elas_2.pdf','本文の金属共通電子と結合ポテンシャル曲率、熱膨張、ゴムの異なる温度応答を確認。key年は教材識別名で表紙の年月を未確定とする。'),
('princeton_magnesium','Princeton University MAE324','Materials Glossary: Magnesium','https://www.princeton.edu/~maelabs/mae324/glos324/magnesium.htm','本文のE=45GPaとHCPを確認。代表値であり材種・温度・方位の全てを保証しない。'),
('princeton_tungsten','Princeton University MAE324','Materials Glossary: Tungsten','https://www.princeton.edu/~maelabs/mae324/glos324/tungsten.htm','本文のE=407GPaとBCCを確認。近接距離の誤植と熱膨張率の単位表記は採用しない。'),
('cambridge_unitcell','University of Cambridge DoITPoMS','Crystallography: Unit Cell','https://www.doitpoms.ac.uk/tlplib/crystallography3/unit_cell.php','一次大学教材の検索収録で原始/非原始胞・角/面の共有分率を確認。再取得403であり当日全文取得ではない。'),
('princeton_hcp','Princeton University MAE324','Materials Glossary: Hexagonal Close Packed','https://www.princeton.edu/~maelabs/mae324/glos324/hcp.htm','本文で六方格子に二原子基底、ABAB積層を確認。六角柱6原子との対応は共有分率から独自導出する。'),
('princeton_iron','Princeton University MAE324','Materials Glossary: Iron','https://www.princeton.edu/~maelabs/mae324/glos324/iron.htm','室温BCC、加熱FCC変態を本文確認。教材の910°Cは丸められた値であり精密な変態温度は独立資料と区別。'),
('princeton_aluminum','Princeton University MAE324','Materials Glossary: Aluminum','https://www.princeton.edu/~maelabs/mae324/glos324/aluminum.htm','室温FCCを本文確認。basis of one Ni atomという誤記をAlの原子種へ転載しない。'),
('princeton_copper','Princeton University MAE324','Materials Glossary: Copper','https://www.princeton.edu/~maelabs/mae324/glos324/copper.htm','本文のCuのFCCを確認。'),
('princeton_sodium','Princeton University MAE324','Materials Glossary: Sodium','https://www.princeton.edu/~maelabs/mae324/glos324/sodium.htm','本文のNaのBCCを確認。OpenStaxの無温度指定HCP例示と同一視しない。'),
('princeton_titanium','Princeton University MAE324','Materials Glossary: Titanium','https://www.princeton.edu/~maelabs/mae324/glos324/titanium.htm','室温TiのHCPを確認。本文の高温変態温度や合金強度の数値は採用しない。'),
('princeton_zinc','Princeton University MAE324','Materials Glossary: Zinc','https://www.princeton.edu/~maelabs/mae324/glos324/zinc.htm','室温ZnのHCPを本文確認。'),
('openstax_crystals','OpenStax','Chemistry 2e: Lattice Structures in Crystalline Solids','https://openstax.org/books/chemistry-2e/pages/10-6-lattice-structures-in-crystalline-solids','本文のBCC2/FCC4と最近接配位数8/12、面対角線4Rを確認。Naの無温度指定HCP例示は室温Naへ採用しない。原典図の転載はしない。'),
('openstax_magnetism','OpenStax','University Physics Volume 2: Magnetism in Matter','https://openstax.org/books/university-physics-volume-2/pages/12-7-magnetism-in-matter','本文でFe、Co、Niの強磁性と磁区の役割を確認。全元素・全温度の同一分類にしない。'),
('iron_curie1954','Proceedings of the Physical Society Section A','The Scattering of Slow Neutrons by Ferromagnetic Crystals','https://doi.org/10.1088/0370-1298/67/3/308','一次論文要約の鉄のCurie温度1043Kを検索収録で確認。再取得cache missであり全文読了ではない。約770°Cへの換算は教材独自。著者書誌は追加照合対象。'),
('iron_transform2023','David Hernández-Escobar and Alejandra Slagter and Julie Gheysen and Andreas Mortensen','Phase Transformation-Induced Interfacial Debonding of Silica Inclusions in Iron','https://link.springer.com/article/10.1007/s11663-023-02939-6','2023年オンライン/2024年巻。本文の912°C平衡温度、α→γ収縮と逆変態膨張の実験説明を確認。特定試料の歪みを全純鉄の定数へ採用しない。'),
('jogmec_nickel2014','JOGMEC','JOGMEC NEWS Vol.36: レアメタル供給リスクと取り組み','https://www.jogmec.go.jp/content/300376600.pdf','2014年3月、取得PDFの印刷6--7頁注4：日本のNiレアメタルと国際的ベースメタルの分類差を確認。めっき質量は原典値から独自計算。'),
('nist_fracture_history2010','Janet B. Quinn and George D. Quinn','A Practical and Systematic Review of Weibull Statistics for Reporting Strengths of Dental Materials','https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=901550','Dental Materials26(2010)135--147。取得PDF136頁のLiberty/Cometと破壊力学・欠陥の歴史説明を確認。事故報告原本の全照合とはしない。'),
('stainless_definition2022','American Institute of Steel Construction','Inside Stainless Steel: Modern Steel Construction January 2022','https://www.worldstainless.org/files/issf/non-image-files/PDF/Structural/january2022_MSC_Stainless_Steel_Article.pdf','印刷19頁のCr最低10.5質量パーセントとC最大1.2質量パーセントを確認。出題の10未満という十分条件を逆命題にしない。'),
('openstax_resistivity','OpenStax','University Physics Volume 2: Resistivity and Resistance','https://openstax.org/books/university-physics-volume-2/pages/9-3-resistivity-and-resistance','本文表9.1の20°CにおけるCu1.68/Au2.44/Fe9.71×10の負8乗Ωmを確認。純度と温度が変わる比較へ外挿しない。'),
('nims_hydrogen2024','物質・材料研究機構','耐水素脆化自動車用高強度鋼の開発：粒界炭素偏析の活用指針','https://www.nims.go.jp/rcsm/research/research-results/2401/details.html','2024Topic1本文の水素による脆化・機械特性と粒界破壊を確認。物性変化全般を水素脆化と定義しない。'),
('nims_diamond2007','物質・材料研究機構','NIMS21: Diamond Materials','https://archive.nims.go.jp/eng/publicity/publication/nims-accomplishments/hdfqf1000000betd-att/NIMS21_en.pdf','一次研究機関冊子の検索収録でdiamond cutting toolを確認。本文再取得timeoutであり全冊子読了ではない。key年は検索識別、正確な発行年は未確定。'),
('sulfur_machinability2004','服部 篤 and 狩野 隆 and 羽生田 智紀','低炭素硫黄快削鋼の硫化物形態と被削性に及ぼす脱酸の影響','https://www.jstage.jst.go.jp/article/denkiseiko/75/1/75_1_35/_pdf','電気製鋼75(2004)35--42。取得PDFの0.5S実験と本文MnS・形態・酸素・組織・工具寿命/粗さの条件を確認。出題の0.3対0.005の直接実験とはしない。'),
('nist_charpy','National Institute of Standards and Technology','Charpy Machine Verification Program','https://www.nist.gov/programs-projects/charpy-machine-verification-program','本文の高負荷速度と吸収エネルギーによる間接的衝撃靭性測定を確認。破壊靭性KICの直接測定とはしない。'),
('hall_petch_limits2020','Sneha N. Naik and Stephen M. Walley','The Hall--Petch and Inverse Hall--Petch Relations and the Hardness of Nanocrystalline Metals','https://link.springer.com/article/10.1007/s10853-019-04160-w','2019年オンライン/2020年巻。本文の通常Hall--Petch式とナノ領域の変形機構・硬度換算・加工条件を確認。逆Hall--Petchの全材料での保証はせず、実験証拠の未確定という著者の結論も保持。')]
p=ROOT/'references.bib';s=p.read_text();added=0
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:
  author=a if ' and ' in a else '{'+a+'}'
  s+='\n@online{'+k+',\n author={'+author+'},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n.replace('%',r'\%').replace('_',r'\_')+'}\n}\n';added+=1
p.write_text(s)
concepts=[('material_strengthening','金属の粒径強化・加工硬化・再結晶','加工硬化|結晶粒|再結晶'),('material_fracture','材料の欠陥・脆性破壊・疲労','脆性|疲労|欠陥'),('material_elastic_modulus','ヤング率・弾性剛性と温度依存','ヤング率|フック'),('material_tensile_measures','公称応力・ひずみと真応力・対数ひずみ','公称|真応力|真ひずみ'),('material_crystal_cells','BCC/FCC/HCPと単位胞規約','体心|面心|六方'),('material_fcc_geometry','FCCの原子数・配位数・接触幾何','配位数|アルミニウム'),('material_coating_mass','被膜の体積・密度・質量百分率','めっき|ニッケル'),('material_iron_phases','純鉄の結晶変態と磁気転移','強磁性|コバルト|純鉄'),('material_property_selection','比強度・剛性・衝撃靭性と材料選択','比強度|シャルピー|水素脆化')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']};snap=ROOT/'snapshots/config_before_S7_041_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
for k,t,pat in concepts:
 assert k not in ids;d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['BASIC'],disciplines=['basic_4_1']))
d['version']='1.34-S7-concept-additions';p.write_bytes(json_bytes(d))
folder=ROOT/'extracted/reference_checks/S7_041';(folder/'source_notes.json').write_bytes(json_bytes(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_sources=[dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in folder.glob('*.pdf')],limitations=['14原典画像と公式前初回14一致。','13問の適用条件・歴史・単位胞規約を部分校正で保持。','原典の百分率計算・FCC幾何は独自導出。','原始胞の格子点数と原子基底、通常の胞の原子数を区別。','OpenStaxのNa例示、PrincetonのAl原子種誤記をそのまま採用しない。','Curie論文・Cambridge・NIMS21の検索収録を当日全文読了とはしない。'])))
print('concepts',len(d['concepts']),'new refs',added)
