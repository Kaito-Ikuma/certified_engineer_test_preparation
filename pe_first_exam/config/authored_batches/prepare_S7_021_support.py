# coding: utf-8
import json, re, sys, shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('gc_water','U.S. Geological Survey',"Where Is Earth's Water?",'https://www.usgs.gov/water-science-school/science/where-earths-water?items_per_page=6&page=0&qt-science%3Acenter_objects=0','公式公開本文の貯留表。総量1386000000km3、海96.54%、淡水分母氷68.7%、河2120・大気12900・全地下水23400000km3。塩性地下水を含む陸水と淡水の分母を区別。'),
('gc_hem','John D. Hem','Study and Interpretation of the Chemical Characteristics of Natural Water, third edition','https://pubs.usgs.gov/wsp/wsp2254/pdf/wsp2254a.pdf','原本PDF取得・全テキスト抽出。物理45頁珪藻はケイ酸を取り込む、64頁Ca-HCO3水の呼称、各イオンの溶解・酸化還元・沈殿・伝導率。対象箇所を検索して確認した。原本全頁を通読したという意味ではない。'),
('gc_river1970','北野康 and 加藤喜久雄','元素の地球化学的収支からみた沿岸海洋','https://www.jstage.jst.go.jp/article/engankaiyo/8/2/8_22/_pdf/-char/ja','1970論文原本PDF取得。物理3頁／誌面24頁の表4を画像確認。小林1960とLivingstone1963比較：蒸発残渣74.8対100mg/L、SiO2比26.84対11.67%。積は20.07632対11.67mg/L。火山地質等を説明。時期・集計対象を付す。'),
('gc_debye','IUPAC','Debye--Huckel equation','https://goldbook.iupac.org/terms/view/D01534','公式公開本文。活量係数・イオン強度・価数・温度定数の式。風化抵抗の直接推定モデルではない。単一イオン活量の慣例も区別。'),
('gc_redox','U.S. Geological Survey','Oxidation/Reduction (Redox)','https://www.usgs.gov/mission-areas/water-resources/science/oxidationreduction-redox?page=1','公式公開本文。酸素の供給と、無酸素時の硝酸・Mn・Fe・硫酸・CO2電子受容順序、溶存FeMn生成を確認。酸素不在を全ての地質条件へ無条件に一般化しない。'),
('gc_redox2009','U.S. Geological Survey','Redox Conditions in Selected Principal Aquifers of the United States','https://pubs.usgs.gov/publication/fs20093041','2009一次報告の公式要旨。溶存Mn2+・Fe2+・H2S・CH4と酸化還元による移動性変化。'),
('gc_mine','U.S. Geological Survey','Coal Extraction: Environmental Prediction','https://pubs.usgs.gov/fs/fs073-02/fs073-02.html','公式公開本文。黄鉄鉱酸化が酸性鉱山排水の主要因。ただし岩石の中和能と動力学によって排水が異なる。'),
('gc_mine2015','D. Kirk Nordstrom and D. W. Blowes and C. J. Ptacek','Hydrogeochemistry and Microbiology of Mine Drainage: An Update','https://www.usgs.gov/publications/hydrogeochemistry-and-microbiology-mine-drainage-update','2015原著の公式要旨。酸性だけでなく中性・塩性排水も存在し、炭酸塩・水酸化物等の中和と二次沈殿を区別。'),
('gc_carbon','NASA','The Carbon Cycle','https://science.nasa.gov/earth/earth-observatory/the-carbon-cycle/','2011解説の公式公開本文。遅い風化・堆積・火山と速い生物循環を分離、平衡再調整は長期である。過去の排出量を現在値として転用しない。'),
('gc_crust','U.S. Geological Survey',"Composition of the Earth's Crust",'https://pubs.usgs.gov/pp/0440d/report.pdf','公式公開PDFの表18、D13頁。質量%O46.60Si27.72Al8.13K2.59Ti0.44Mn0.100Cl0.020。比較は試料・基準が異なっても頑健だが全地球の存在度へ拡張しない。'),
('gc_meteoric','IAEA','Isotope Methods for Dating Old Groundwater','https://www-pub.iaea.org/MTCD/Publications/PDF/TE-1723_web.pdf','公式公開本文の4頁式2。δ2H=8δ18O+10、局地線の傾き切片・蒸発の逸脱を明記。全陸水の同位体絶対比が厳密な比例という意味ではない。'),
('gc_conductance','U.S. Geological Survey','Chapter A6.3. Specific Conductance','https://pubs.usgs.gov/publication/tm9A6.3','公式書誌・要旨とHemの本文を併用。伝導率の科学的基礎、25℃補正、校正と現場測定を区別。'),
('gc_conductance1994','U.S. Geological Survey','Collecting and Processing Stream Water Samples','https://water.usgs.gov/nawqa/pnsp/pubs/ofr94-455/sw-t.html','公式公開本文。電気抵抗の逆数と伝導度、25℃に標準化した比伝導度、溶存量組成依存。'),
('gc_dispersion','Lynn W. Gelhar and Claire Welty and Kenneth R. Rehfeldt','A Critical Review of Data on Field-Scale Dispersion in Aquifers','https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/92wr00607','1992原著の出版社公開要旨。59現場、縦分散長と観測尺度に傾向があるが普遍直線不可。横分散データの限界も明記。'),
('gc_sulfur_denit','橋本ら','硫黄脱窒菌の集積と単体硫黄への馴養','https://www.jstage.jst.go.jp/article/jswe1978/12/7/12_7_431/_article/-char/ja','1989原著の公式公開要旨。HCO3-無機炭素源とS2O3還元硫黄、完全嫌気で集積。直接openはCache miss、検索公開要旨で限定確認。著者名は未確定のため暫定団体表記へ置換する。'),
('gc_diatom','Michael J. Knight and colleagues','Direct Evidence of the Molecular Basis for Biological Silicon Transport','https://www.nature.com/articles/ncomms11926','2016原著公開本文。珪藻のケイ酸取り込みと輸送体を実験。成長・死後殻溶解を分ける。著者詳細は未照合なので団体著者を用いる。'),
('gc_reverse','PNAS','Rapid Transformation of Biogenic Silica to Authigenic Clay: Mechanisms and Geochemical Constraints','https://pmc.ncbi.nlm.nih.gov/articles/PMC12571068/','2025原著の公開本文。逆風化はカチオン・アルカリ度消費しCO2生成。H27原典4の意図を証明した資料とはせず、単純風化と逆風化を区別する後年の科学補足とする。'),
('gc_arsenic2004','厚生労働省','水質基準の円滑な施行について：平成16年4月1日施行基準','https://www.mhlw.go.jp/topics/2004/bukyoku/kenkou/1-4.html','公式公開表7。ヒ素量0.01mg/L。2018前の基準と現在の表を別確認。'),
('gc_arsenic_current','環境省','水質基準項目と基準値','https://www.env.go.jp/water/water_supply/kijun/kijunchi.html','2026-10-11閲覧の公式公開表。ヒ素量0.01mg/L。表全体の項目数・他成分変更を2018へ遡及しない。'),
('gc_arsenic_hazard','CDC NIOSH','Pocket Guide to Chemical Hazards: Arsenic','https://www.cdc.gov/niosh/npg/npgd0038.html','公式公開本文に金属CAS7440-38-2、As単体と曝露限度・発がん注意を記載。「金属ヒ素に毒性はない」を無条件に支持しない。医療助言を提供する用途ではない。'),
('gc_cave','U.S. Geological Survey','Geology of Wind Cave National Park','https://www.usgs.gov/geology-and-ecology-of-national-parks/geology-wind-cave-national-park','公式公開本文。滴下時CO2を失って方解石堆積、鍾乳石・石筍形成。'),
('gc_clays','U.S. Geological Survey','Environmental Characteristics of Clays and Clay Mineral Deposits','https://pubs.usgs.gov/info/clays/','公式公開本文。岩種、水岩比、温度、有機物、期間、風化帯上部カオリナイトと下部複雑粘土を説明。気候だけで全試料の鉱物を決めない。'),
('gc_ccs','U.S. Department of Energy','Carbon Capture, Utilization and Storage','https://www.energy.gov/carbon-capture-utilization-storage','公式公開本文。塩水帯水層・油ガス層等の貯留と流動圧力化学変化の予測。'),
('gc_capture','NETL','Point Source Carbon Capture','https://netl.doe.gov/carbon-management/carbon-capture','公式公開本文。膜・溶媒・吸着・化学ループとアミン系。単にEORに使う全技術がCCSと同程度に直結するとは扱わない。'),
('gc_mea','NETL','Regenerable Non-Aqueous Basic Immobilized Amine Slurries','https://www.netl.doe.gov/node/5718','公式公開本文。従来比較基準のMEA吸収を確認。'),
]
# 未照合の個人名を推測して書誌へ入れない。
refs=[(k,'水環境学会' if k=='gc_sulfur_denit' else 'Nature Communications' if k=='gc_diatom' else a,t,u,n) for k,a,t,u,n in refs]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
d=ROOT/'extracted/reference_checks/S7_021';d.mkdir(parents=True,exist_ok=True)
for name in ['river','hem']:
 shutil.copyfile('/private/tmp/S7_021_'+name+'.pdf',d/(name+'.pdf'))
 shutil.copyfile('/private/tmp/S7_021_'+name+'.txt',d/(name+'.txt'))
(d/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],limitations=['検索公開本文・要旨と原本PDF確認を明示的に区別。','H27水質は珪藻の成長と殻溶解、逆風化の説明範囲を要査読。','H30の金属ヒ素無毒、R02化学合成と脱窒、Ca-HCO3名称と陸水の分母の疑義を保持。']),ensure_ascii=False,indent=2)+'\n')
new=[('water_quality_indicators','水質汚濁指標と起源トレーサー','水質汚濁指標|BOD|SS'),
('carbon_geochemical_cycle','炭素貯留・生物循環と岩石風化','炭素循環'),
('river_water_chemistry','陸水の主要イオン・地質と採水変化','陸水|河川.*水質'),
('crust_abundance','地殻元素存在度と比較基準','地殻.*元素'),
('natural_water_redox','天然水の電子受容体・酸化還元電位','酸化還元.*天然水|Eh|ORP'),
('groundwater_transport','溶質の移流・拡散分散と観測尺度','分散長|機械的分散'),
('water_conductivity','天然水の電気伝導率・温度と組成','電気伝導率'),
('water_mineral_equilibrium','鉱物水反応・活量と風化生成物','水.*鉱物反応|イオン強度'),
('nitrogen_geochemical_cycle','窒素固定・硝化脱窒と炭素源','窒素循環')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
if not all(n[0] in ids for n in new):
 snap=ROOT/'snapshots/config_before_S7_021_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,label,pattern in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pattern,subjects=['APPLIED'],disciplines=['earth_chem']))
 modified=[]
 for c in d['concepts']:
  if c['id'] in ['water_budget_residence','rock_weathering'] and 'earth_chem' not in c['disciplines']:
   c['disciplines'].append('earth_chem');modified.append(c['id'])
 old=d['version'];d['version']='1.14-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/'config/concept_change_log_S7.json';log=json.loads(p.read_text());log.append(dict(time=now(),batch='S7_021_geochemistry',previous_version=old,version=d['version'],added=[n[0] for n in new],modified_disciplines=modified,reason='22原典を物質収支・水質・鉱物反応の中心課題に分ける。貯留・風化の既存概念は統合して領域適用を追加。140概念版を保持。'));p.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
