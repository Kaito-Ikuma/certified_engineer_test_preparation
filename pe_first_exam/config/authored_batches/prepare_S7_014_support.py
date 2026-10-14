# coding: utf-8
"""References and concept refinements for source-read S7_014."""
import json,re,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('gsj_rock_classification','産総研地質調査総合センター','岩石の分類','https://www.gsj.jp/geology/fault-fold/formation/r-classification/r-classification.html'),
('gsj_igneous2021','産総研地質調査総合センター','斑れい岩類：その種類・成因と特徴','https://www.gsj.jp/data/gcn/gsj_cn_vol10.no10_p235-241.pdf'),
('aist_crystal_colors','産総研マルチマテリアル研究部門','結晶構造ギャラリー：白雲母の色','https://unit.aist.go.jp/mmri/ja/organization/db-nomura/crystal_gallery.html'),
('usgs_rock_thesaurus','U.S. Geological Survey','Lithologic classification of geologic map units','https://apps.usgs.gov/thesaurus/thesaurus-full.php?thcode=4'),
('jma_magma1999','気象庁','地震・火山月報1999年5月：マグマの性質','https://www.data.jma.go.jp/eqev/data/gaikyo/monthly/199905/monthly199905.pdf'),
('gsj_fuji_units','産総研地質調査総合センター','富士火山地質図第2版の凡例一覧','https://gbank.gsj.jp/volcano/Act_Vol/fujisan/tbl/pdf/at1_pdf.pdf'),
('nelson_contact2011','Stephen A. Nelson','Contact Metamorphism (Tulane University)','https://www2.tulane.edu/~sanelson/eens212/contactmeta.htm'),
('nelson_assemblages2011','Stephen A. Nelson','Metamorphic Mineral Assemblages (Tulane University)','https://www2.tulane.edu/~sanelson/eens212/metaminerals.htm'),
('hokkaido_polymorph2012','北海道大学地球惑星科学','地学I 2012年第10回：高圧多形と準安定性','https://www.ep.sci.hokudai.ac.jp/~keikei/chigaku1/arch2012/No10.pdf'),
('gsj_metamorphic_words','産総研地質調査総合センター','用語解説：変成岩','https://gbank.gsj.jp/geowords/glossary/metamorphic.html'),
('nelson_regional2011','Stephen A. Nelson','Regional Metamorphism (Tulane University)','https://www2.tulane.edu/~sanelson/eens212/regionalmetamorph.htm'),
('aist_awa2021','産業技術総合研究所','中央構造線が走る阿波池田地域の地質','https://www.aist.go.jp/aist_j/press_release/pr2021/pr20210419_2/pr20210419_2.html'),
('tohoku_highpressure','東北大学東北アジア研究センター','日本海及びその周辺域の岩石','https://www.cneas.tohoku.ac.jp/labs/geo/10oldpage/ishiwata/ISHKZHP/Japansea/Japansea.htm'),
('gsj_highpressure2016','産総研地質調査総合センター','九州の変成岩類と地質帯：GSJ地質ニュース5巻6号','https://www.gsj.jp/data/gcn/gsj_cn_vol5.no6.pdf'),
('usgs_ash_density','U.S. Geological Survey','Volcanic Ash: Density and Hardness','https://volcanoes.usgs.gov/volcanic_ash/density_hardness.html'),
('usgs_tephra_sizes','U.S. Geological Survey','Kilauea lava fountaining episode tephra clast sizes','https://www.usgs.gov/media/images/kilauea-lava-fountaining-episode-tephra-clast-sizes'),
('usgs_pinatubo1996','U.S. Geological Survey','Fire and Mud: Pyroclastic-Flow Deposits (W. E. Scott and others)','https://pubs.usgs.gov/pinatubo/wescott/'),
('usgs_tephra_fall','U.S. Geological Survey','Pre-1980 Tephra-Fall Deposits, Mount St. Helens: Introduction','https://pubs.usgs.gov/pp/p1563/introduction.html'),
('usgs_bishop_tuff','U.S. Geological Survey','Bishop Tuff in Long Valley Caldera, California','https://www.usgs.gov/volcanoes/long-valley-caldera/science/bishop-tuff-long-valley-caldera-california'),
('aist_accretion2026','産業技術総合研究所','ここにどうして蛇紋岩？','https://www.aist.go.jp/aist_j/press_release/pr2026/pr20260724/pr20260724.html'),
('gsj_saganoseki1993','産総研地質調査総合センター','佐賀関地域の地質','https://cdn.gsj.jp/ld/zfk/zfkdoc/0672/0672.html'),
('mlit_masa','国土交通省中国地方整備局','広島県に土砂災害が多いのはなぜ：花崗岩のマサ化','https://www.cgr.mlit.go.jp/ootagawa/sand/west/page1/page1_04.html'),
('maff_shiras2017','農林水産省','シラス（火砕流堆積物）の特徴','https://www.maff.go.jp/j/nousin/seko/gizyutu/attach/pdf/index-1.pdf'),
('gsj_shiras1957','産総研地質調査総合センター','霧島山地域の地質：シラス・水成シラス','https://cdn.gsj.jp/ld/zfk/zfkdoc/0704/0704.html'),
('gsj_loess2002','産総研地質調査総合センター','関東平野の土壌中微量有害元素の地球化学的研究：土壌地球化学図の基礎研究（第3報）','https://www.gsj.jp/data/bulletin/53_11_02.pdf'),
('loess2003','東京地学協会','風成塵・レス：地学雑誌112巻5号794--799頁','https://www.jstage.jst.go.jp/article/jgeography1889/112/5/112_5_794/_pdf/-char/ja'),
('mlit_peat','国土交通省北海道開発局札幌開発建設部','泥炭地ってなに？','https://www.hkd.mlit.go.jp/sp/sapporo_kitanougyou/kluhh4000000d6vw.html'),
('jseg_engineering_faq','日本応用地質学会中国四国支部','応用地質Q＆A中国四国版','https://www.jseg.or.jp/chushikoku/faq/'),
('slaking1979','農業土木学会','スレーキング：農業土木学会誌47巻11号886頁','https://www.jstage.jst.go.jp/article/jjsidre1965/47/11/47_11_886/_pdf'),
('slaking2006','土木学会','地下水質と空気供給状況を考慮した堆積性岩石の新しいスレーキング試験方法','https://www.jstage.jst.go.jp/article/jscejc/62/2/62_2_335/_article/-char/ja'),
('kyoto_deep2018','京都大学防災研究所','九州の深層崩壊に関する資料：花崗岩・付加体の比較','https://www.dpri.kyoto-u.ac.jp/web_j/publication/other/20180330_kyusyu.pdf'),
('sabo_deep2014','砂防学会','深層崩壊研究で思うこと','https://www.jstage.jst.go.jp/article/sabo/66/6/66_1/_pdf'),
('jsce_swelling2010','土木学会','不撹乱粘土試料の一次元膨潤圧特性とその異方性','https://www.jstage.jst.go.jp/article/jscejc/66/2/66_2_264/_pdf'),
('serpentinite_mechanics2003','日本地すべり学会','神居古潭帯に分布する蛇紋岩の不撹乱状態および再構成粘性土試料の力学特性','https://www.jstage.jst.go.jp/article/jls2003/40/4/40_4_293/_article/-char/ja/')]
f=ROOT/'references.bib';s=f.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s));added=[]
for key,author,title,url in refs:
 if key in keys:continue
 s+='\n@online{'+key+',\n  author={{'+author+'}},\n  title={'+title+'},\n  url={'+url+'},\n  urldate={2026-10-10}\n}\n';added.append(key)
f.write_text(s)
dest=ROOT/'extracted/reference_checks/S7_014';dest.mkdir(parents=True,exist_ok=True)
(dest/'source_notes.json').write_text(json.dumps({'checked_at':now(),'sources':[dict(key=k,author=a,title=t,url=u) for k,a,t,u in refs],'limitations':['一次資料の本文・検索抜粋を照合。全参考PDFの全頁目視を意味しない。','付加体問題の公式1を支持する排他的根拠は未確定。','白雲母の原典有色分類と通常分類の不一致を保持。']},ensure_ascii=False,indent=2)+'\n')
f=ROOT/'config/concepts.json';d=json.loads(f.read_text());new=[
('igneous_assemblage','火成岩組成・鉱物組合せ','火成岩|玄武岩|花崗岩|はんれい岩',['geo_petrology']),
('metamorphic_equilibrium','変成作用・鉱物組合せ・組織','変成|片岩|片麻岩|ホルンフェルス',['geo_petrology']),
('pyroclastic_deposit','火山砕屑物・堆積構造','火山砕屑|火砕流|軽石|アグルチネート',['geo_petrology']),
('accretion_rocks','付加体の構成岩・形成過程','付加体',['geo_petrology','geo_engineering']),
('soil_origin','特殊土の母材・成因','土壌|まさ土|しらす|泥炭|黄土',['geo_engineering']),
('rock_weathering','岩石風化・変質・スレーキング','風化|変質|スレーキング',['geo_engineering'])]
ids={x['id'] for x in d['concepts']}
if not all(x[0] in ids for x in new):
 snapshot=ROOT/'snapshots/config_before_S7_014_concept.json'
 if snapshot.exists():raise ValueError('Snapshot already exists but concepts incomplete')
 snapshot.write_bytes(f.read_bytes());d['version']='1.7-S7-concept-additions'
 for cid,label,pattern,disciplines in new:
  if cid not in ids:d['concepts'].append(dict(id=cid,label=label,pattern=pattern,subjects=['APPLIED'],disciplines=disciplines))
 f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 f=ROOT/'config/concept_change_log_S7.json';log=json.loads(f.read_text());log.append(dict(time=now(),added_ids=[x[0] for x in new],change='S7_014原典17問に基づき既存geo_petrology/geo_engineering内6概念を追加。93概念の前版保存。',reason='鉱物・岩石の大分類だけでは変成平衡・火成組成・土成因・風化機構を区別できないため。taxonomyの変更なし。'));f.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print('References added',len(added),'concepts',len(d['concepts']))
