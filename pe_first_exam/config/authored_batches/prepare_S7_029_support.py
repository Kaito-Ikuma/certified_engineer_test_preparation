# coding: utf-8
import sys,json,re,shutil,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
 ('sed_gsj_slate','産総研地質調査総合センター','地質標本館：黒色粘板岩 GSJ R10562','https://www.gsj.jp/Muse/hyohon/rock/r10562.html','標本の堆積岩分類と登米層の記載を本文15行で確認。粘板岩を一律に未変成堆積岩とする根拠ではない。'),
 ('sed_mit_environment','John B. Southard / MIT OpenCourseWare','Depositional Environments, Chapter 10 (2007)','https://ocw.mit.edu/courses/12-110-sedimentary-geology-spring-2007/935e82faac10751572cd54f18531e17a_ch10.pdf','物理1–4頁の観察と解釈、8–12頁の河川、17–19頁の級化とBouma省略、22–23頁の潮流反転と断面効果を本文確認。33頁全文の通読ではない。'),
 ('sed_mit_cross','John B. Southard / MIT OpenCourseWare','Cross Stratification, Chapter 16 (2006)','https://ocw.mit.edu/courses/12-090-introduction-to-fluid-motions-sediment-transport-and-current-generated-sedimentary-structures-fall-2006/b76e182106487208fe4e449ccd40400e_ch16.pdf','物理24–25頁のHCSの振動流・複合流、成因の多様性と反砂堆例を確認。単一成因の絶対指標とはしない。'),
 ('sed_walther_oregon','Rebecca Dorsey / University of Oregon','Stratigraphy and Sequence Stratigraphy: Week 8','https://pages.uoregon.edu/rdorsey/geo334/334lect8.html','本文47行を確認。整合累重内のWalther、相対海水準と供給の競合、上昇中の通常海退、堆積シーケンスの境界を確認。'),
 ('sed_houston_structures','Daniel Hauptvogel and Virginia Sisson','The Story of Earth: Sedimentary Structures (2023)','https://uhlibraries.pressbooks.pub/thestoryofearthv2/chapter/chapter-4-sedimentary-structures2e/','4.2の移動リップル・斜交・級化・流痕・荷重痕と上下判定、4.4の生物擾乱を確認。画像は教材へ転載しない。'),
 ('sed_soft_deformation','Yi Gao and Zaixing Jiang and James L. Best and Jingong Zhang','Soft-sediment deformation structures: Upper Triassic Ordos Basin (2020)','https://experts.illinois.edu/en/publications/soft-sediment-deformation-structures-as-indicators-of-tectono-vol/','著者機関掲載の論文抄録のみ確認。火炎・荷重痕、未固結層の液状化・流動化・過荷重の関与を確認。全文取得・全成因照合ではない。'),
 ('sed_plumose_michigan','University of Michigan','Joints and Veins: Plumose Structure','https://psgt.earth.lsa.umich.edu/chapter/4/joints.html?zoom_highlight=row','羽毛状構造の節理起点・ハックル・停止線と割れ目伝播の節を本文確認。堆積面や上下指標と混同しない。'),
 ('sed_gsj_ec2011','内山美恵子 and 原未来也 and 竹内美緒 and 木村克己','東京低地と中川低地の沖積層堆積物で作成した懸濁液の水素イオン濃度指数及び電気伝導度 (2011)','https://www.gsj.jp/data/bulletin/62_01_full.pdf','物理88頁（印刷86頁）を実見。黄鉄鉱酸化・乾燥処理・ECの環境指標利用と単独識別の限界を確認。全116頁通読ではない。'),
 ('sed_xrf_jaea','日本原子力研究開発機構','ATOMICA: 蛍光X線分析の原理と応用 (2009)','https://atomica.jaea.go.jp/data/detail/dat_detail_08-04-01-26.html','概要と原理節の蛍光特性X線による元素の定性・定量、非破壊分析を確認。内部堆積構造の画像観察と区別。'),
 ('sed_sem_shimane','大久保雅弘 and 物種繁晴','地学試料の電子顕微鏡的観察（その1）：石英砂粒の表面構造 (1974)','https://ir.lib.shimane-u.ac.jp/3447','機関リポジトリ抄録の水成・風成砂の微細表面と溶食の区別を確認。本文PDF全6頁は未通読、SEMで単一履歴を一意決定するとはしない。'),
 ('strat_pollen_tokushima','日本地質学会','電気伝導度および花粉化石分析に基づく徳島平野・板東観測井コアの海成層の層序対比 (2021)','https://www.jstage.jst.go.jp/article/geosocabst/2021/0/2021_326/_article/-char/ja/','学会要旨の方法・結果を通読。海成層の花粉化石組成による対比と古地磁気の併用を確認。仮説年代を確定値へ変更しない。'),
 ('strat_gsj_tephra2013','山元孝広','栃木−茨城地域における過去約30万年間のテフラの再記載と定量化 (2013)','https://www.gsj.jp/data/bulletin/64_09_full.pdf','物理41頁の岩種・層厚・粒径を使う対比訂正と屈折率の併用を文字層で確認。全巻通読ではない。'),
 ('strat_gsj_atsumi','産総研地質調査総合センター','豊橋及び田原地域の地質：テフラ層序と対比','https://cdn.gsj.jp/ld/zfk/zfkdoc/1143/1143.html','2.5と7.7の中期更新世の海進泥層内テフラとMIS11・9対比を確認。局地/水域/古い地層を一律除外できない。'),
 ('strat_iu_unconformity','Indiana University','Unconformities','https://geol105b.sitehost.iu.edu/images/gaia_chapter_6/unconformities.htm','検索取得された一次機関本文抜粋で侵食・非堆積と三分類を確認。ブラウズ本頁・curlはSSL名不一致で取得できず、全頁の通読とはしない。'),
 ('sed_tsunami_fujino','藤野滋弘','陸上津波堆積物の多様な粒度，層厚，堆積構造 (2012)','https://www.jstage.jst.go.jp/article/jssj/71/2/71_102/_article/-char/ja','学会抄録全文を確認。塊状・葉理・正逆級化・複数ユニットの多様性と複数指標による認定を確認。'),
 ('sed_tsunami_usgs','Robert Peters and Bruce Jaffe','Identification of tsunami deposits in the geologic record (2010)','https://pubs.usgs.gov/of/2010/1239/of2010-1239.pdf','要旨及び堆積構造節を確認。近年のデータ集では構造が稀との記述があり「常に複雑」と一般化できない。全研究の単純/複雑頻度集計ではない。'),
 ('sed_tsunami_2002','重野聖之 and 七山太','津波堆積物 (2002)','https://www.jstage.jst.go.jp/article/agcjchikyukagaku/56/3/56_KJ00004409827/_pdf','物理1–2頁を実見。遡上/戻り流れの構造・海生遺骸・保存、隕石衝突及びストレッガー津波報告を確認。火山起源堆積物の個別報告は未確認。'),
 ('sed_tsunami_gsj_survey','産総研地質調査総合センター','津波堆積物データベース：調査方法','https://gbank.gsj.jp/tsunami_deposit_db/tsunami/survey.html','本文の湿地・堤間低地での保存、微化石・化学・分布・構造の複数判定を確認。岩礁の報告を不可能とはしない。'),
 ('volc_usgs_merapi','E. K. Abdurachman and J. L. Bourdier and B. Voight','Nuées ardentes of 22 November 1994 at Merapi volcano (2000)','https://www.usgs.gov/publications/nuees-ardentes-22-november-1994-merapi-volcano-java-indonesia','USGS掲載論文抄録全文を確認。ドーム崩落起源、谷埋積と希薄サージの分岐・非単純分布を確認。'),
 ('volc_usgs_msh_flow','U.S. Geological Survey','Mount St. Helens: Pyroclastic Flows','https://pubs.usgs.gov/gip/msh/pyroclastic.html','取得された一次本文抜粋の扇状・舌状・ローブ状分布を確認。頁open失敗のため全頁通読とはしない。'),
 ('volc_usgs_tephra','U.S. Geological Survey','Pre-1980 Tephra-Fall Deposits: Terminology','https://pubs.usgs.gov/pp/p1563/introduction.html','取得された一次本文抜粋でテフラの広義/狭義と本報告の降下限定を確認。頁open失敗、用語の範囲を全資料で一律としない。'),
]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={'+a+'},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
new=[
 ('sed_facies_system','堆積相と河川・デルタ・河口システム','堆積相|エスチュアリー',['geo_sediment']),
 ('sed_bedform_flow','流れ・波浪と斜交層理','ヘリンボーン|ハンモック|斜交',['geo_sediment']),
 ('sed_soft_deformation','未固結堆積物の二次変形','火炎構造|二次的堆積構造',['geo_sediment']),
 ('sed_way_up','形成時の上下と堆積構造','荷重痕|皿状|上下方向',['geo_sediment']),
 ('sed_proxy_methods','堆積環境指標と測定法の限界','電気伝導度|風成営力',['geo_sediment']),
 ('sed_tsunami_record','津波堆積物の形成・認定・保存','津波堆積物',['geo_sediment']),
 ('sed_facies_walther','堆積相の組合せ・累重とワルターの法則','ワルター|サクセション',['geo_sediment']),
 ('strat_tephra_correlation','テフラ同定・年代対比と再堆積','テフラ|テフロクロノロジー',['geo_stratigraphy']),
 ('strat_unconformity','不整合の時間間隙と三分類','不整合|無整合',['geo_stratigraphy']),
 ('volc_pyroclastic_distribution','火砕密度流の形成と地形に沿う分布','火砕流',['earth_volcano']),
]
if not all(k in ids for k,_,_,_ in new):
 snap=ROOT/'snapshots/config_before_S7_029_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat,ds in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APPLIED'],disciplines=ds))
 d['version']='1.22-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_029';folder.mkdir(exist_ok=True)
files=[]
for src in ['/tmp/S7_029_EC.pdf','/tmp/S7_029_MIT_env.pdf','/tmp/S7_029_MIT_cross.pdf','/tmp/S7_029_tsunami.pdf','/tmp/S7_029_tsunami_2002.pdf','/tmp/S7_029_tephra.pdf','/tmp/S7_029_EC_checked.png','/tmp/S7_029_tsunami2002_1.png','/tmp/S7_029_tsunami2002_2.png']:
 target=folder/Path(src).name;shutil.copyfile(src,target);files.append(dict(file=str(target.relative_to(ROOT)),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=files,limitations=['検索取得の一次本文抜粋・抄録・選択頁の確認範囲を個別に記録。全文通読や用語の全普遍性を確認したとはしない。','津波火山起源堆積物、PL型火砕流用語、逆級化の非一意性、HCSの多成因は個別疑義へ残す。']),ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
