# coding: utf-8
import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
cp=P/'config/concepts.json'
assert not (P/'extracted/logs/config_before_S7_055_concept.json').exists()
shutil.copyfile(cp,P/'extracted/logs/config_before_S7_055_concept.json')
c=json.loads(cp.read_text());assert c['version']=='1.47'
spec=[
('acid','酸の強さと同濃度pH','basic_4_1'),('hess','反応熱の符号とヘスの法則','basic_4_1'),
('ampho','両性水酸化物の過剰塩基への溶解','basic_4_1'),('thermal','材料組織と熱輸送','basic_4_3'),
('equilibrium','発熱気体反応の平衡条件','basic_4_1'),('neutral','中和当量と塩の加水分解','basic_4_1'),
('corrosion','不動態と環境による腐食','basic_4_3'),('stoich','呼吸と発酵の物質収支','basic_4_1'),
('fraction','合金の質量組成と物質量分率','basic_4_3'),('metallurgy','資源と製錬の反応・質量','basic_4_3'),
('properties','FeCuAlの密度抵抗率融点','basic_4_3'),('colligative','沸点上昇と溶質粒子数','basic_4_1'),
('elements','用途と材料構成元素','basic_4_3'),('gibbs','標準反応ギブズエネルギー','basic_4_1'),
('organic','有機反応の結合変化による分類','basic_4_1'),('redox','酸化数変化による反応分類','basic_4_1')]
for key,label,d in spec:c['concepts'].append({'id':'chem55_'+key,'label':label,'pattern':label,'subjects':['BASIC'],'disciplines':[d]})
c['version']='1.48';cp.write_text(json.dumps(c,ensure_ascii=False,indent=2))
refs=[
('hydrolysis','OpenStax','Chemistry 2e:14.4 Hydrolysis of Salts','https://openstax.org/books/chemistry-2e/pages/14-4-hydrolysis-of-salts','アンモニウムイオンの酸性と不活性な塩化物イオンの本文を確認。全章読了ではない。'),
('ampho','University of Washington Department of Chemistry','Amphoteric Nature of Aluminum Hydroxide','https://chem.washington.edu/lecture-demos/amphoteric-nature-aluminum-hydroxide','公開実演手順の酸・NaOHによる水酸化物の溶解を確認。'),
('corrosion','World Stainless Association','Corrosion properties','https://worldstainless.org/about-stainless/properties/corrosion-properties/','公式技術解説の塩化物による局部腐食の記述を確認。リンク先の全冊子は未読。'),
('polymer','Xiangfan Xu and Jie Chen and Jun Zhou and Baowen Li','Thermal Conductivity of Polymers and Their Nanocomposites','https://arxiv.org/abs/1805.06163','著者の公開要旨を読んだ。材料構造に依存する熱輸送の参考。24頁全文と全条件の検証ではない。'),
('equilibrium','OpenStax','Chemistry 2e:13.3 Shifting Equilibria','https://openstax.org/books/chemistry-2e/pages/13-3-shifting-equilibria-le-chateliers-principle','圧力と気体モル数の本文を確認。温度効果は原典発熱条件から独立に判断。全章読了ではない。'),
('stoich','OpenStax','Chemistry 2e:4.3 Reaction Stoichiometry','https://openstax.org/books/chemistry-2e/pages/4-3-reaction-stoichiometry','出版社の反応化学量論節を参照。グルコースの原典係数から収支を独立に計算した。'),
('kroll','東邦チタニウム','3分でわかる東邦チタニウム','https://www.toho-titanium.co.jp/about/','公式検索本文のTiCl4とMgによるクロール法を確認。2015資源・価格統計の照合ではない。'),
('crust','Royal Society of Chemistry','Aluminium: abundance and production','https://periodic-table.rsc.org/element/13/aluminium','地殻中で最多の金属Alと溶融塩電解の公開本文を確認。原典時点の生産統計は別の未解決項目。'),
('properties','Royal Society of Chemistry','Copper: element properties','https://periodic-table.rsc.org/element/29/copper','Fact boxの密度8.96と融点1084.62℃を確認。'),
('properties_al','Royal Society of Chemistry','Aluminium: element properties','https://periodic-table.rsc.org/element/13/aluminium','公開検索Fact boxの密度2.70と融点660.323℃を確認。'),
('properties_fe','Royal Society of Chemistry','Iron: element properties','https://periodic-table.rsc.org/element/26/iron','公開検索Fact boxの密度7.87と融点1538℃を確認。'),
('colligative','OpenStax','Chemistry 2e:11.4 Colligative Properties','https://openstax.org/books/chemistry-2e/pages/11-4-colligative-properties','沸点上昇の本文・式と1気圧の水の表を確認。電解質は理想的粒子数による試験モデルと実測を区別。'),
('fiber','Corning','Silicon: The Collaborator of the Periodic Table','https://www.corning.com/worldwide/en/innovation/materials-science/glass/periodic-table-elements/silicon.html','メーカー公開検索本文のシリカと光ファイバーを参照。全製品がシリカであるとの一般化には使わない。'),
('duralumin','日本アルミニウム協会','板材の区分：アルミニウム合金の種類','https://www.aluminum.or.jp/fields/kenchiku/kenzai/guide/b/','表3のAl-Cu系と2017・2024ジュラルミンを本文確認。規格全文読了ではない。'),
('gibbs','OpenStax','Chemistry Atoms First:12.4 Free Energy','https://openstax.org/books/chemistry-atoms-first/pages/12-4-free-energy','本文のG=H-TSと標準反応量の式12.33を確認。全章読了ではない。'),
('organic','OpenStax','Organic Chemistry:6.1 Kinds of Organic Reactions','https://openstax.org/books/organic-chemistry/pages/6-1-kinds-of-organic-reactions','出版社公開本文の付加・脱離・置換の定義と例を確認。エステル交換・加水分解の分類を反応の逆方向にも用いる。'),
('iron','日本製鉄','製銑工程','https://www.nipponsteel.com/company/tour/process01.html','メーカー公開本文のコークス・還元ガスと高炉の説明を確認。原典の理想質量収支は別に独立計算。')]
def esc(s):
 for a,b in [('&',r'\&'),('%',r'\%'),('_',r'\_')]:s=s.replace(a,b)
 return s
bib=P/'references.bib';s=bib.read_text();notes=[]
for key,org,title,url,note in refs:
 key='chem55_'+key;assert '@online{'+key+',' not in s
 s+='\n@online{'+key+',\n author={{'+esc(org)+'}},\n title={'+esc(title)+'},\n url={'+url+'},\n note={'+esc(note)+'},\n urldate={2026-10-14}\n}\n'
 notes.append({'key':key,'url':url,'reading_scope':note,'full_source_read':False})
bib.write_text(s)
(P/'extracted/logs/source_notes_S7_055.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
print('Added',len(spec),'concepts',len(refs),'references')
