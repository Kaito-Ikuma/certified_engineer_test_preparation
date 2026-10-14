# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,json_bytes,digest
refs=[
 ('jica_refraction2015','国際協力機構調査団','モーリシャス国地すべり対策プロジェクト：ファイナル・レポート（メイン）','https://openjicareport.jica.go.jp/pdf/12231320_01.pdf','取得PDF表紙2015年3月、印刷3-51〜3-52頁の萩原はぎとり法・トモグラフィ比較、直接波と屈折波、往復走時・原点走時の整合を本文確認。'),
 ('epa_surfacewaves','United States Environmental Protection Agency','Surface Wave Methods','https://www.epa.gov/environmental-geophysics/surface-wave-methods','本文の分散曲線・水平層のS波逆解析・波長と深度感度・高次モード及び横方向不均質の限界を確認。'),
 ('xia_rayleigh1999','J. Xia and R. D. Miller and C. B. Park','Estimation of Near-Surface Shear-Wave Velocity by Inversion of Rayleigh Waves','https://www.usgs.gov/publications/estimation-near-surface-shear-wave-velocity-inversion-rayleigh-waves','USGS一次論文要約でP波・S波・密度・層厚の依存、5Hz超のS波の強い感度、反復逆解析を確認。全文取得や全周波数での感度順位の保証とはしない。'),
 ('coastal_reflection2016','資源エネルギー庁','平成28年度沿岸部処分システム高度化開発報告書','https://www.enecho.meti.go.jp/category/electricity_and_gas/nuclear/rw/library/2016/28fy_enngannbu.pdf','一次報告の検索収録で浅層反射の最大オフセットと探査深度の目安を確認。原URL再取得は403であり全文・原図の読了ではない。目安を普遍的な必要条件へ拡張しない。'),
 ('seg_vertical_resolution','Society of Exploration Geophysicists','Seismic Data Analysis: Vertical Resolution','https://wiki.seg.org/wiki/Vertical_resolution','掲載専門書の検索収録で四分の一波長の目安は上下面反射の分離であり存在検出と異なる点を確認。再取得は403。'),
 ('seg_lateral_resolution','Society of Exploration Geophysicists','Seismic Data Analysis: Lateral Resolution','https://wiki.seg.org/wiki/Lateral_resolution','掲載専門書の検索収録で半波長の第一Fresnel zoneと横方向分解能、Ricker1953のwavelet論文への参照を確認。本文再取得は未達。'),
 ('moe_surface2004','土壌環境センター','埋設農薬調査における物理探査の適用性について','https://www.env.go.jp/water/report/h17-10/full.pdf','表紙2004年3月と物理57頁の表面波探査概要を確認。S波分散・一次元から二次元・通常20m程度という対象を読み、普遍的限界とはしない。'),
 ('segj_integrated2017','物理探査学会','統合物理探査調査研究委員会報告書','https://segj.or.jp/publication/pdf/IntegratedReport.pdf','一次報告の検索収録の対象別手法表を確認。トンネル・ダム・斜面の評価と強震動用S波構造を区別。keyの2017は検索時の識別名で書誌年月確定ではない。本文再取得未達。'),
 ('japansea_spac2017','日本海地震・津波調査プロジェクト','平成29年度報告：3.3.2 強震動予測','https://www.eri.u-tokyo.ac.jp/project/Japan_Sea/JSH29Report/PDF3/21_H29JSPJ-C3.3.2.pdf','本文のSPACによるRayleigh分散とS波モデル、強震動用モデルを確認。印刷361頁の検索収録で空間aliasingの最小波長を確認。全87頁の全文読了とはしない。'),
 ('array_limits2002','岩手大学機関リポジトリ（所蔵）','物理探査55巻5号363--373頁：微動アレーの推定波長限界（書誌要確認）','https://iwate-u.repo.nii.ac.jp/record/9867/files/bt-v55n5p363-373.pdf','一次論文の検索収録で数値実験及び実測のF-KとSPAC最大波長比較と条件依存を確認。PDF再取得503。題名・著者の確定と全文照合は査読対象として保持。'),
 ('epa_seismic_refraction','United States Environmental Protection Agency','Seismic Refraction','https://www.epa.gov/environmental-geophysics/seismic-refraction','本文のP波主体とS波例、初動・臨界屈折の増速条件・薄層と低速度層・飽和状態によるP波速度差の実例を確認。')]
p=ROOT/'references.bib';s=p.read_text();added=0
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:
  author=a if ' and ' in a else '{'+a+'}'
  s+='\n@online{'+k+',\n author={'+author+'},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n+'}\n}\n';added+=1
p.write_text(s)
concepts=[('exploration_refraction_interpretation','屈折初動のはぎとり・相反走時・連続勾配','はぎとり|全走時|ミラージ'),('exploration_refraction_properties','地震速度境界・地質と地盤状態','速度層|地質境界|地下水'),('exploration_reflection_resolution','反射分解能・薄層分離と存在検出','分解能|レイリー|フレネル'),('exploration_depth_limits','探査深度の目安と観測条件','探査深度'),('exploration_reflection_geometry','反射走時の双曲線・局所近似・配置','双曲線|放物線|オフセット'),('exploration_method_observables','探査の観測量と物理手法の対応','地震探査|ブーゲ'),('exploration_refraction_applications','屈折法の地山評価と主用途','ダム|地山|のり面'),('exploration_array_wavelength','微動アレイの長短波長限界','SPAC|F-K|エイリアシング'),('exploration_surfacewave_inversion','表面波分散・S波感度と統合逆解析','位相速度|S波速度')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
if not all(k in ids for k,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_040_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APPLIED'],disciplines=['geo_exploration']))
 d['version']='1.33-S7-concept-additions';p.write_bytes(json_bytes(d))
folder=ROOT/'extracted/reference_checks/S7_040';folder.mkdir(exist_ok=True)
(folder/'source_notes.json').write_bytes(json_bytes(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_sources=[dict(path='extracted/reference_checks/S7_039/jica_refraction.pdf',sha256=digest(ROOT/'extracted/reference_checks/S7_039/jica_refraction.pdf')),dict(path='extracted/reference_checks/S7_039/refraction.pdf',sha256=digest(ROOT/'extracted/reference_checks/S7_039/refraction.pdf'))],limitations=['15問14原典画像と公式前初回を保存し15一致。','反射の放物線局所近似は独自Taylor導出として保持。','PDF取得未達の一次検索収録を全文読了と呼ばない。','array_limits2002の題名・著者と当該全文照合を未確定として追跡する。'])))
print('Concepts',len(d['concepts']),'new refs',added)
