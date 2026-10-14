# coding: utf-8
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('atm_noaa_composition','NOAA','The Atmosphere','https://www.noaa.gov/jetstream/atmosphere','本文組成表の乾燥空気N2/O2/Ar順序。CO2の現在表示値を出題当時へ遡及しない。'),
('atm_noaa_layers','NOAA','Layers of the Atmosphere','https://www.noaa.gov/jetstream/atmosphere/layers-of-atmosphere','本文の温度層序・界面高度の緯度差。温度と質量密度を別軸に扱う。'),
('atm_us1976','NOAA, NASA and USAF','U.S. Standard Atmosphere, 1976','https://www.ngdc.noaa.gov/stp/space-weather/online-publications/miscellaneous/us-standard-atmosphere-1976/us-standard-atmosphere_st76-1562_noaa.pdf','18MB原本をローカル取得。文字抽出は欠落が多く数表全体の読了ではない。標準モデルの6.5K/kmと静水圧を独立計算し10km密度約0.414/1.225=0.338と推定、原典1/4概数の疑義を保持。上層組成高度の数表目視は未完了。'),
('atm_nasa_budget','NASA','Earth’s Energy Budget','https://ntrs.nasa.gov/api/citations/20120002320/downloads/20120002320.pdf','公開検索図説明の入射342・反射107・潜熱78W/m2。直接web取得は容量超過で失敗、全文読了とはしない。'),
('atm_nasa_albedo','NASA','Measuring Earth’s Albedo','https://science.nasa.gov/earth/earth-observatory/measuring-earths-albedo-84499/','全球平均反射約30パーセントを公式観測解説から確認。31パーセントは問題採用の代表値。'),
('atm_nasa_transport','NASA Langley Research Center','What is Earth’s Energy Budget? Five Questions with a Guy Who Knows','https://www.nasa.gov/centers-and-facilities/langley/what-is-earths-energy-budget-five-questions-with-a-guy-who-knows/','緯度間放射不均衡を大気・海洋輸送が補うという研究者本人解説を検索本文で確認。'),
('atm_noaa_winds','National Weather Service','Prevailing Winds','https://www.weather.gov/source/zhu/ZHU_Training_Page/winds/Wx_Terms/Flight_Environment.htm','本文の気圧傾度力・地衡風・地表摩擦・海陸風・大循環を確認。'),
('atm_jma_dynamic','気象庁','総観気象学 理論編（2022）','https://www.jma.go.jp/jma/kishou/know/expert/pdf/textbook_synop_theory_20220318.pdf','公開検索式の地衡風とロスビー数。教材のベクトル方向と近似条件は独立に運動方程式から導出。全文読了ではない。'),
('atm_jma_enso','気象庁','よくある質問：エルニーニョ／ラニーニャ現象','https://www.data.jma.go.jp/cpd/data/elnino/learning/faq/faq3.html','本文で南方振動は数年ごとの東西気圧変動。数十年変動と区別。'),
('atm_jma_ozone','気象庁','オゾン層とは','https://www.jma.go.jp/jma/kishou/know/env/ozonehp/3-10ozone.html','公式公開検索本文：90パーセント成層圏・紫外線吸収と加熱。'),
('atm_noaa_ghg','NOAA Global Monitoring Laboratory','Measuring and Analyzing Greenhouse Gases: Behind the Scenes','https://gml.noaa.gov/ccgg/behind_the_scenes/gases.html','本文のCO2季節変動・多様なメタン源・N2O由来NOとオゾン。古い濃度/GWP数値は不使用。'),
('atm_jma_ghg2012','気象庁','気候変動監視レポート2012','https://www.data.jma.go.jp/cpdinfo/monitor/2012/pdf/ccmr2012_all.pdf','公開検索本文で水蒸気の大きな自然温室効果と人為起源の追加強制力の区別。全文読了ではない。'),
('atm_usgs_water','USGS Water Science School','How Much Water is There on Earth?','https://www.usgs.gov/water-science-school/science/how-much-water-there-earth?qt-science_center_objects=0','公開表の大気12900km3、日蒸発散1170km3、氷・地下水等の貯留。比を取った約11日の計算は自分で行い推定間差を明示。'),
('atm_usgs_cycle','USGS','Hydrologic Cycle','https://www.usgs.gov/centers/new-york-water-science-center/science/hydrologic-cycle','本文の氷雪長期貯留と水の移動。貯留・流量・滞留を区別。'),
('atm_mri_cloud','気象庁気象研究所・荒木健太郎','雲の微物理過程の研究','https://www.mri-jma.go.jp/Dep/typ/araki/cloud_microphysics.html','研究者本人本文の過冷却水滴・氷晶成長・融解と日本降水。模式図転載なし。'),
('atm_noaa_pwat','NOAA NESDIS','Atmospheric Moisture','https://www.nesdis.noaa.gov/news/atmospheric-moisture','公開検索本文で可降水量が柱中水蒸気の水相当量であることを確認。日降水量との差は連続の式から独立説明。'),
('atm_usgs_transmissivity','USGS','Hydraulic conductivity and transmissivity estimates from slug tests（2020調査）','https://pubs.usgs.gov/publication/sir20235101/full','公式研究報告の推定法：透水係数×帯水層厚さ。検索公開本文で照合。'),
('atm_usgs_perched','USGS','Selected Constituents in Perched Ground Water（1999–2001）','https://pubs.usgs.gov/sir/2006/5236/section3.html','公式調査の透水性の低い堆積層上に宙水が形成される機構。検索本文で確認。'),
('atm_jma_acid','気象庁','酸性雨に関する基礎的な知識','https://www.jma.go.jp/jma/kishou/know/env/acid/info_acid.html','本文のCO2平衡pH5.6・中和と酸性沈着影響。海水のpHと降水を混同しない。'),
('atm_jma_acid2014','気象庁','降水・降下じんの化学成分：日本での酸性雨の状況','https://www.jma.go.jp/jma/kishou/know/env/acid/topic_acid.html','本文の2014公表資料：2008–2012地点年加重平均4.48–5.37、全地点5年4.72。H27当時の定性的肢の根拠。現在各地点の値へ流用しない。'),
]
f=ROOT/'references.bib';s=f.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-10}\n}\n'
f.write_text(s)
d=ROOT/'extracted/reference_checks/S7_018';d.mkdir(exist_ok=True,parents=True)
(d/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],limitations=['10km密度の1/4と標準モデル約0.34の差を保持。','R02上層主要成分の高度は詳細一次数表未確認。','R02水資源肢は全球更新と地域枯渇の範囲を査読待ち。']),ensure_ascii=False,indent=2)+'\n')
new=[('atmospheric_composition','乾燥大気の組成と微量気体の循環','大気.*組成|アルゴン'),('atmospheric_vertical','大気の鉛直温度・密度構造','対流圏|成層圏'),('earth_radiation_budget','地球の受光幾何と放射収支','太陽定数|熱収支'),('atmospheric_circulation','大気循環と地衡風・局地風','地衡風|ハドレー'),('enso','大気海洋相互作用と南方振動','ENSO|南方振動'),('water_budget_residence','水収支・貯留・平均滞留時間','水循環|滞留時間'),('precipitation_chemistry','降水の酸塩基平衡と酸性沈着','降水.*pH|酸性雨')]
f=ROOT/'config/concepts.json';d=json.loads(f.read_text());ids={x['id'] for x in d['concepts']}
if not all(x[0] in ids for x in new):
 snap=ROOT/'snapshots/config_before_S7_018_concept.json';assert not snap.exists();snap.write_bytes(f.read_bytes())
 for k,label,pat in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pat,subjects=['APPLIED'],disciplines=['earth_weather']))
 old=d['version'];d['version']='1.11-S7-concept-additions';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 f=ROOT/'config/concept_change_log_S7.json';rows=json.loads(f.read_text());rows.append(dict(time=now(),batch='S7_018_atmosphere',previous_version=old,version=d['version'],added=[x[0] for x in new],reason='大気23原典の7中心概念を既存earth_weather内へ追加。124概念の前版保存。'));f.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
