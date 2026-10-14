# coding: utf-8
import sys,json,re,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('str_faultrocks','大鹿村中央構造線博物館','断層岩の分類','https://mtl-muse.com/study/faultrocks/classification/','固結性、細粒基質10-50/50-90/90-100割合の分類案、マイロナイト結晶塑性、シュードタキライト溶融急冷の公開本文。区分案の違いを明示。'),
('str_shear','大鹿村中央構造線博物館','剪断センスの判定','https://mtl-muse.com/study/faultrocks/shear-sense/','XZ面の非対称構造、S/C面、シアバンド、フィッシュと方位条件の公開本文。右雁行と右横ずれを同一視しない。'),
('str_source','国土地理院','活断層とは何か','https://www.gsi.go.jp/bousaichiri/explanation','地下震源断層と地表地震断層、活動時代の定義幅、写真判読と現地調査の公開本文。史料記録を地表変位一般の必要条件にしない。'),
('str_activity','地震調査研究推進本部','活動間隔、活動度','https://www.jishin.go.jp/resource/terms/tm_activity/','A:1-10、B:0.1-1、C:0.01-0.1m/千年、下端含む上端含まない公開定義。30年発生確率ランクとは別。'),
('str_coastal2017','産業技術総合研究所 地質調査総合センター','GSJ総合パンフレット2017：隠れた活断層を探す','https://www.gsj.jp/data/pamphlet/GSJ_Pamphlet-2017.pdf','ローカル物理16/印刷14頁を読解し画像照合。沿岸活断層の連続性/活動性調査で海陸の重力・空中磁気探査を利用。全冊通読ではない。'),
('str_pollen2014','杉山雄一ほか','野坂断層海域部の更新世末期以降の活動','https://www.gsj.jp/data/actfault-eq/h25seika/2014_057-108.pdf','ローカル物理7/印刷63頁4.3.7、物理9/印刷65頁4.6.4.1。花粉/珪藻は堆積環境変遷の目的で実施、群集から河口・内湾と温暖化を推定。直接変位測定と区別。全52頁通読ではない。'),
('str_fold','Jean-Pierre Burg, ETH Zurich','Folding (2017)','https://www.files.ethz.ch/structuralgeology/jpb/files/english/7folding.pdf','公開物理1-5頁層平行圧縮/曲げ・ランプ、7-8層面すべり、10-12キンク・不安定性を確認。強度中程度・剛性高という出題肢の量的条件はこの確認だけでは確定しない。'),
('str_fold_geometry','Jean-Pierre Burg, ETH Zurich','Folds (2020)','https://www.files.ethz.ch/structuralgeology/jpb/files/english/8folds.pdf','公開講義のヒンジ/軸面/翼、アンチフォームと背斜の年代条件の区別、線の沈下角を確認。全頁通読とはしない。'),
('str_orientation','Jean-Pierre Burg, ETH Zurich','Structural Analysis (2017)','https://www.files.ethz.ch/structuralgeology/jpb/files/English/11polypli.pdf','物理4-5頁走向は面内水平線、真傾斜は走向に直交する鉛直面、線のtrend/plunge、同方位が同世代とは限らない説明を確認。全15頁通読ではない。'),
('str_intrusion','U.S. Geological Survey','Our Dynamic Desert: Volcanic Features','https://pubs.usgs.gov/of/2004/1007/volcanic.html','公式HTMLをcurlで取得し該当本文を確認。sillは層間の貫入、laccolithは膨らんだ貫入体。web open内部エラーとローカル確認を区別。'),
('str_diapir','U.S. Geological Survey','Earthshots: Lisan Peninsula','https://eros.usgs.gov/earthshots/lisan-peninsula','低密度物質が上方へ押し上がったdiapirの公式説明を確認。全ダイアピールで断層との関連がないとはしない。'),
('str_listric','横山俊治','層理境界逆断層の断層運動と地すべり変動 (2007)','https://kochi.repo.nii.ac.jp/record/1845/files/yokoyama2007landslides214.pdf','ローカル物理6頁/論文219頁の図5b・説明の下に凸の正断層曲面と深部収束を画像照合。地すべり例を全断層機構へ過剰一般化しない。'),
('str_en2016','東北大学災害科学国際研究所','平成28年熊本地震に関する調査報告：地表雁行配列','https://irides.tohoku.ac.jp/media/files/earthquake/eq/2016_kumamoto_eq_report/2016_KumamotoEqReport_1-6_rev.pdf','ローカル物理38-39/印刷35-36頁全文・図10を確認。右横ずれの杉型left-stepping地表配列の実例。図キャプション右ステップと本文左ステップの表記差もあるため全配列名を一般則へ拡張しない。全93頁通読ではない。'),
('str_moraine','U.S. Geological Survey','Geology of Glacier National Park','https://www.usgs.gov/geology-and-ecology-of-national-parks/geology-glacier-national-park','Glaciation節の氷河岩屑運搬と側方/末端モレーン堆積を公開本文確認。氷河数の歴史値を現在値として教材へ転用しない。'),
('str_ryoke','産業技術総合研究所 地質調査総合センター','御油地域の地質 (2008)：領家変成コンプレックス','https://gbank.gsj.jp/ld/resource/zfk/facies/m1142_f037.html','GSJ公開HTML第4章冒頭の高温低圧型と研究史・鉱物帯記載を確認。足助は隣接図幅でありこの図幅名は御油。図幅全報告通読を称さない。プレート速度の参照系は未確定。'),
('str_culmination','Geoffrey I. Alsop and R. E. Holdsworth','Vergence and facing patterns in large-scale sheath folds (1999)','https://research-portal.st-andrews.ac.uk/en/publications/vergence-and-facing-patterns-in-large-scale-sheath-folds/','著者所属大学の公開要旨でculmination/depressionとantiform/synformの組合せ・非対称構造が位置に依存することを確認。論文全文は未読。')]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
d=ROOT/'extracted/reference_checks/S7_025';d.mkdir(exist_ok=True)
local={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in d.iterdir() if p.suffix in ['.pdf','.html']}
(d/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_sha256=local,limitations=['No282は取得したがテキストが438bytesのみで本文未読。根拠引用には使わない。','H30問23の初回5と公式4を保持。花粉と磁気両方の利用を確認し相対的関連順位は未確定。','ミ/杉の配列とセンスの条件、スランプ形成全称、プレート速度参照系は追加査読。']),ensure_ascii=False,indent=2)+'\n')
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
new=[('structural_orientation','面の走向・傾斜と線の方位・沈下角','クリノ|走向|傾斜'),
 ('fold_geometry','褶曲の形態・部位・軸と年代','褶曲|ヒンジ|アンチフォーム'),
 ('fold_mechanics','座屈・曲げ・層面すべりの形成力学','座屈|スランプ|キンク'),
 ('fault_kinematics','断層の相対変位と分岐・屈曲構造','正断層|横ずれ|地塁'),
 ('fault_rocks','断層岩の変形機構・組織・基質割合','カタクレーサイト|ガウジ|シュードタキライト'),
 ('fault_activity','活断層の履歴・活動度と地表/地下変位','震源断層|活断層|活動度'),
 ('fault_survey','活断層調査の観察量・年代・物性・古環境','活断層調査|花粉分析|磁気探査'),
 ('fault_landforms','断層変位地形と他の地形形成機構','閉塞丘|撓曲崖|モレーン')]
if not all(k in ids for k,_,_ in new):
 snap=ROOT/'snapshots/config_before_S7_025_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APPLIED'],disciplines=['geo_structure']))
 d['version']='1.18-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
