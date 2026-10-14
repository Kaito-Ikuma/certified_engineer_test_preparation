# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,digest
refs=[
('usgs_interior_structure','U.S. Geological Survey','The Interior of the Earth','https://pubs.usgs.gov/gip/interior/','取得HTMLの地殻・マントル節で地殻厚さの地域差、モホ、プレートが最上部マントルを含むことを確認。古い月・核組成の説明は利用しない。'),
('usgs_plate_boundaries','U.S. Geological Survey','This Dynamic Earth: Understanding Plate Motions','https://pubs.usgs.gov/gip/dynamic/understanding.html','取得HTMLの発散・収束・トランスフォーム節で海嶺生成、海溝沈み込み、横ずれを確認。旧衛星数や過度に単純なマグマ成因は転記しない。'),
('usgs_lithosphere2002','Walter D. Mooney and Claus Prodehl and Nina Pavlenkova','Seismic Velocity Structure of the Continental Lithosphere from Controlled Source Data','https://www.usgs.gov/publications/seismic-velocity-structure-continental-lithosphere-controlled-source-data','原研究の公式紹介本文で地殻と最上部マントルのリソスフェア、モホ、地域ごとの厚さを確認。2002年。'),
('umich_crust_teaching','University of Michigan','Whole Earth Structure and Plate Tectonics','https://psgt.earth.lsa.umich.edu/chapter/11/tectonics.html','授業本文の地殻節で面積約40\\%、上部と下部の平均組成、代表的厚さ、年代を確認。均質二層や全海洋底200Ma上限などの全称を転載しない。'),
('tokyo_crust_gallery','東京大学理学系研究科','マントルの岩石・大陸地殻の岩石','https://www.s.u-tokyo.ac.jp/ja/gallery/exhibits/eps001.html','公式研究展示で上部大陸地殻の花崗岩と大陸の約40億年の歴史を確認。大陸が全く沈み込まないという絶対表現を利用しない。'),
('kagoshima_plate2019','鹿児島大学理学部','南九州におけるプレート境界','https://www.sci.kagoshima-u.ac.jp/oyo/advanced/geology/plate.html','本文冒頭で日本付近の太平洋8〜9、フィリピン海4〜5 cm/年、組成区分と力学区分の差を確認。初出2019-09-07。北米固定の精密値を直接検証した資料とは扱わない。'),
('gsj_heat_flow1991','長尾年恭 and 山野誠','日本周辺の地殻熱流量分布とその特徴：第210回地質調査所研究発表会講演要旨','https://www.gsj.jp/data/bull-gsj/42-10_05.pdf','1991年地質調査所月報42巻10号、印刷550〜551頁（PDF8〜9頁）の文字層で東北日本太平洋側の低熱流量・日本海の高熱流量を確認。図の点値は読取っていない。'),
('jma_hyogo_history','気象庁','過去の地震津波災害：明治から平成7年','https://ds.data.jma.go.jp/eqev/data/higai/higai-1995.html','公式表の1995年兵庫県南部地震M7.3を確認。出題前の現象を例示し、気象庁MとMwを区別する。'),
('herp_longterm_intervals','地震調査研究推進本部','長期評価結果一覧・発生確率値の留意点','https://www.jishin.go.jp/evaluation/long_term_evaluation/lte_summary/','公式本文で活断層の間隔は数千年程度、過去の記録と間隔に幅があることを確認。2026年の確率値をH26年度へ遡及適用しない。1000年の全称下限は未検証。'),
('noaa_sea_salt','NOAA National Ocean Service','Why Is the Ocean Salty?','https://oceanservice.noaa.gov/facts/whysalty.html','本文で海水中の塩類約35‰、溶存イオン中のClとNaの約85\\%を確認。原典の分母の区別に使用。地球核から直接加熱という粗い説明は転載しない。'),
('noaa_nutrient_observations','NOAA Atlantic Oceanographic and Meteorological Laboratory','Nutrient Biogeochemistry','https://www.aoml.noaa.gov/ocd/ocdweb/nutrients.html','A16航海の自身の栄養塩観測を紹介する本文で表層取込みと深部再生、水塊ごとの差を確認。単調な全深度則とはしない。'),
('noaa_subtropical_ecco','NOAA Science On a Sphere and NASA','Sea Surface Currents and Temperature: ECCO2','https://sos.noaa.gov/catalog/datasets/sea-surface-currents-and-temperature-gray-land/','2012年登録の観測・モデル統合データ解説で五大亜熱帯環流、北半球時計回り・南半球反時計回りを確認。亜寒帯環流に拡張しない。'),
('noaa_overturning','NOAA National Ocean Service','The Global Conveyor Belt','https://oceanservice.noaa.gov/education/tutorial_currents/05conveyor2.html','公式本文の千年程度という循環尺度と北大西洋・南極の高密度水の説明を確認。原典の最大2000年を保証する資料ではない。'),
('noaa_tidal_patterns','NOAA National Ocean Service','How Many High Tides Are There per Day?','https://oceanservice.noaa.gov/facts/high-tide.html','公式本文で半日周・混合・日周潮の分類を確認。月と太陽の引力の機構はNOAA Tides公式本文でも確認。全地点2回ではない。'),
('usgs_ocean_water_volume','U.S. Geological Survey','Oceans and Seas and the Water Cycle','https://www.usgs.gov/water-science-school/science/oceans-and-seas-and-water-cycle','公式の地球水量推計表で海洋96.5\\%を確認。表面積比と区別し、精密な不変定数とはしない。'),
('feely_carbonate2004','Richard A. Feely and others','Impact of Anthropogenic CO2 on the CaCO3 System in the Oceans','https://www.pmel.noaa.gov/pubs/outstand/feel2633/feel2633.shtml','2004年原論文の本文で炭酸塩の飽和度、海域ごとの溶解と深海堆積を確認。溶解速度は深さに単調に増加しないため原典肢に疑義を保持。'),
('noaa_ccd_definition','NOAA National Centers for Environmental Information','Paleoenvironmental Standard Terms: Calcium Carbonate Compensation Depth','https://www.ncei.noaa.gov/access/paleo-search/cvterms?termId=4395','公式検索索引の定義で供給と溶解の釣合いによる補償深度を確認。ページ本文は動的で抽出なし。固定した水深値を与えない。'),
('noaa_carbon_chemistry','NOAA Ocean Acidification Program','What Is Ocean Acidification?','https://oceanacidification.noaa.gov/what-is-ocean-acidification/','公式本文の炭酸系・pH・全アルカリ度・溶存無機炭素の違いを確認。CO2吸収とpH低下はpH7未満になることと同義ではない。'),
('jamstec_deep_resources','海洋研究開発機構','STEAM教材4巻：深海探査の探究','https://www.jamstec.go.jp/steam/images/contents/04_text.pdf','取得PDF物理11頁（用語集17頁）文字層で4000m以深の団塊、ゆっくりした成長、海山クラストとの相違を確認。低堆積速度との関係は埋没と成長のモデル推論である。'),
('noaa_ultraslow2004','Edward T. Baker and Christopher R. German','On the Global Distribution of Hydrothermal Vent Fields: Ultraslow Ridges','https://www.pmel.noaa.gov/pubs/outstand/bake2544/ultraslow_ridges.shtml','2004年原研究の超低速海嶺節で低マグマ供給、マントル岩の露出、非一様性を確認。熱水がないという意味にしない。'),
('jma_tsunami_generation','気象庁','津波発生と伝播のしくみ','https://www.jma.go.jp/jma/kishou/know/jishin/tsunami/generation.html','公式本文で海底変位と発生、浅海増幅、V字湾の集中を確認。各地点の単調増幅の保証として使わない。'),
('jma_tsunami_prediction','気象庁','津波を予測するしくみ','https://www.jma.go.jp/jma/kishou/know/jishin/tsunami/ryoteki.html','公式本文で長波速度√(gh)、グリーンの法則を用いた沿岸換算と地形による誤差を確認。理論導出は独自に記述する。'),
('jma_tsunami_rivers','気象庁','津波から身を守るために','https://www.jma.go.jp/jma/kishou/know/jishin/tsunami_bosai/index.html','本文で海から離れていても川に沿う津波があることを確認。距離の全国共通値を与えない。')]
p=ROOT/'references.bib';s=p.read_text();added=0
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:
  s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n+'}\n}\n';added+=1
p.write_text(s)
concepts=[('crust_moho_structure','地殻とモホ','地殻|モホ',['earth_interior']),('lithostatic_pressure','静岩圧・上載荷重','静岩圧',['earth_interior']),('intraplate_crustal_earthquake','内陸地殻内地震','内陸地震|地殻内地震',['earth_seismic']),('relative_plate_velocity','相対プレート速度','相対運動速度',['earth_interior']),('continental_crust_composition','大陸地殻の組成・上下構造','大陸地殻',['earth_interior']),('ocean_continent_contrast','海洋底と大陸の比較','大洋底',['earth_interior']),('plate_boundary_kinematics','プレート境界の相対運動','トランスフォーム',['earth_interior']),('island_arc_heat_flow','島弧配置と熱流量','弧状列島',['earth_interior']),('lithosphere_asthenosphere','リソスフェアとアセノスフェア','アセノスフェア',['earth_interior']),('ocean_nutrient_remineralization','海洋栄養塩の取込みと再生','リン酸|ケイ酸',['earth_ocean']),('subtropical_gyre_direction','亜熱帯環流の方向','亜熱帯',['earth_ocean']),('ocean_reservoir_circulation','海洋水量・循環・炭素吸収','海水|NADW',['earth_ocean']),('tsunami_long_wave','津波の長波近似と変形','津波',['earth_ocean'])]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
if not all(k in ids for k,_,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_036_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat,disc in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APPLIED'],disciplines=disc))
 d['version']='1.29-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_036'
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=[dict(file=str(f.relative_to(ROOT)),sha256=digest(f)) for f in folder.iterdir() if f.is_file() and f.name!='source_notes.json'],limitations=['一般値と地域例外を区別。17問部分校正。','J-STAGE熱流束論文は取得失敗、代わりにGSJ1991年の原研究要旨を取得して確認。','中心温度・北米固定の精密速度・大洋底の花崗岩質岩石・循環時間最大・炭酸塩の単調溶解速度の疑義は未解決。']),ensure_ascii=False,indent=2)+'\n')
print('Concepts',len(d['concepts']),'references added',added)
