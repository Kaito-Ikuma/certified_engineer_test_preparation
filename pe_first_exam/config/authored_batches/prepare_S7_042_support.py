# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,json_bytes,digest
epa='https://www.epa.gov/environmental-geophysics/'
refs=[
('epa_resistivity','US EPA','Electrical Resistivity',epa+'electrical-resistivity','本文の四電極・幾何係数・Ωm・配列・感度体積・非一意性を確認。図注のRと抵抗率の混同は採用しない。Wenner式は半空間から独自導出。'),
('epa_ip','US EPA','Induced Polarization (IP) and Complex Resistivity',epa+'induced-polarization-ip-and-complex-resistivity','本文の時間減衰・周波数位相・粒界分極・直流比抵抗との同時計測を確認。掲載式の電流/電圧の誤記は転記しない。IPは比抵抗と無関係とはしない。'),
('epa_gpr','US EPA','Ground-Penetrating Radar (GPR)',epa+'ground-penetrating-radar-gpr','本文の電気特性境界、往復走時・速度測定、導電減衰、周波数と分解能の交換条件を確認。速度式には比誘電率を明示し、探査深度の厳密反比例を主張しない。'),
('epa_sp','US EPA','Self-Potential (SP)',epa+'self-potential-sp','本文の非分極電極・基準点相対電位・流動/酸化還元機構・鉱体負異常とモデル依存の深度推定を確認。SPに深度推定能力が全くないとはしない。'),
('epa_gamma_density','US EPA','Gamma-Gamma Density Logging',epa+'gamma-gamma-density-logging','本文のガンマ線Compton散乱・電子密度からかさ密度・孔隙率・校正と孔壁接触の条件を確認。粒子密度の直接測定又はベータ線とはしない。'),
('epa_borehole_resistivity','US EPA','Borehole Resistivity',epa+'borehole-resistivity','本文のnormal/focused電極、裸孔と導電孔内流体、含水・粘土・塩分の影響を確認。誘導検層は電極検層と区別。本文の流体影響の全称は装置非依存の保証にしない。'),
('epa_fdem','US EPA','Frequency Domain Electromagnetic (FDEM)',epa+'frequency-domain-electromagnetic-fdem','本文のコイル・渦電流・振幅と位相・送受信間隔と低誘導数を確認。掲載skin depth説明を普遍的DOI境界へ転記しない。'),
('epa_tdem_archive','US EPA','Time-Domain Electromagnetic Methods','https://archive.epa.gov/esd/archive-geophysics/web/html/time-domain_electromagnetic_methods.html','旧サイト本文の遮断後過渡応答・central loop・時間と深部感度を確認。装置寸法・ノイズに依存し、送受信間隔によらず無限に深く探査できるとはしない。'),
('usgs_csamt2012','Jamie P. Macy and Levi Kryder and Jamieson Walker','Characterization of the Highway 95 Fault in Lower Fortymile Wash using Electrical and Electromagnetic Methods, Nye County, Nevada','https://pubs.usgs.gov/sir/2012/5060/sir2012-5060.pdf','SIR2012-5060。取得PDF表紙と印刷12--13頁のskin depth・平面波・送受信距離と近接場を確認。三skin depthはこの報告の目安で全装置の厳密閾値ではない。'),
('usgs_linear_filter1981','Ahmed Samir M. El Kahwagy','A TI-59 Calculator Program for Computation of Schlumberger Resistivity Sounding Curve for Models with as Many as 25 Horizontal Layers','https://pubs.usgs.gov/of/1981/0160/report.pdf','取得PDFのGhosh linear filterによる比抵抗変換からSchlumberger見掛比抵抗を計算する説明を確認。線形フィルタを電極配列そのものとはしない。表紙著者と1980年プログラム日付・81-160報告番号を別確認。'),
('geebec_ps','株式会社GEEBEC','PS検層','https://www.geebec.co.jp/service/exploration/ps-logging/','施工事業者の一次技術説明本文：孔壁へ密着した受振器は水位のない部分でもdownhole測定可能。全孔状態・全装置への非依存性は保証しない。'),
('oyo_suspension','応用地質株式会社','サスペンションPSロガー2i','https://www.oyo.co.jp/services/products-list/geological-survey/suspension-ps-logger/','メーカー本文と専用製品PDF要約の孔内振源と二受振器、地表起振不要を確認。製品深度を全探査法の限界へ一般化しない。'),
('schumann_mt2009','R. Chand and M. Israil and J. Rai','Schumann Resonance Frequency Variations Observed in Magnetotelluric Data Recorded from Garhwal Himalayan Region India','https://angeo.copernicus.org/articles/27/3497/2009/','Annales Geophysicae27(2009)3497--3507。出版社抄録のMT電磁記録でのSchumann共振観測を確認。全文の全読了ではない。'),
('naro_thermal2008','農研機構','1m深地温の逆解析によるため池堤体漏水の幅・深度推定法','https://www.naro.go.jp/project/results/laboratory/nkk/2008/nkk08-35.html','2008成果情報本文の温度差・測定季節・熱伝導逆解析を確認。1mは測温深度で地下水の上限深度ではない。'),
('landslide_thermal2007','竹内 篤雄 and 渡辺 知恵子 and 大谷 沙織 and 山田 晃','1m深地温の再現性と実施時期の再検討について：水ミチ探査結果の精度向上を目指して','https://www.jstage.jst.go.jp/article/jls/44/2/44_2_111/_pdf','日本地すべり学会誌44(2007)111--115。本文111・113--114頁の水温と平常地温の差・季節反転・測線試験を確認。特定地の適期を全国の固定月へ拡張しない。'),
('rion_vibration2016','リオン株式会社','ShakeHands Vol.4: 道路交通振動測定','https://www.rion.co.jp/shakehands/ShakeHands_vol4_%E5%8D%B0%E5%88%B7%E7%94%A8.pdf','メーカー一次資料の検索収録で振動感覚補正加速度レベルとJIS C1510、2014マニュアルを確認。規格本文は未取得、出題当時と現行の版差の断定はしない。')]
p=ROOT/'references.bib';s=p.read_text();added=0
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:
  author=a if ' and ' in a else '{'+a+'}'
  s+='\n@online{'+k+',\n author={'+author+'},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n.replace('%',r'\%').replace('_',r'\_')+'}\n}\n';added+=1
p.write_text(s)
concepts=[('exploration_dc_arrays','直流比抵抗の電極配置・見掛比抵抗','ウェンナー|シュランベルジャー'),('exploration_four_electrode','四電極と接地抵抗の分離','接地抵抗'),('exploration_ip_sp','人工分極と自然電位の信号機構','IP法|自然電位|SP法'),('exploration_archie','孔隙水導電とArchie式の適用条件','アーチー|孔隙水'),('exploration_nearfield','CSAMTの表皮深度・近接場・平面波','ニアフィールド|CSAMT'),('exploration_fd_td','周波数領域と時間領域電磁応答','スリングラム|TDEM|TEM'),('exploration_gpr_resolution','GPRの周波数・分解能・探査深度','レーダ|誘電率'),('exploration_borehole_signals','孔内検層の観測量・水位と接触条件','検層|VSP|サスペンション'),('exploration_multimethod','物理探査の複数手法と幾何・時間','物理探査|ジオトモグラフィ'),('engineering_strength_indices','岩石試験・岩盤強度の代理指標','RQD|圧密降伏')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']};snap=ROOT/'snapshots/config_before_S7_042_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
for k,t,pat in concepts:
 assert k not in ids;d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APPLIED'],disciplines=['geo_engineering'] if k.startswith('engineering_') else ['geo_exploration']))
d['version']='1.35-S7-concept-additions';p.write_bytes(json_bytes(d))
folder=ROOT/'extracted/reference_checks/S7_042';(folder/'source_notes.json').write_bytes(json_bytes(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_sources=[dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in folder.glob('*.pdf')],limitations=['29原典と21頁画像、公式前初回29一致を保存済み。','近接場とArchie式、GPR比例表現、SP深度推定は条件を留保。','原典の真空の誘電率μ、Ωmの三乗、F・m、ベータ線を誤答のまま保持。','検索収録・抄録・全文の確認範囲を区別。'])));print('concepts',len(d['concepts']),'new refs',added)
