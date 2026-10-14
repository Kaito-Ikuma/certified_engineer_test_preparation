# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,digest,json_bytes
refs=[
 ('mit_signals2010','Alan V. Oppenheim and George C. Verghese','Signals and Systems: Chapter 2','https://ocw.mit.edu/courses/6-011-introduction-to-communication-control-and-signal-processing-spring-2010/4599f6cff8a3890477f4c4986db032a2_MIT6_011S10_chap02.pdf','本文のLTI畳み込みと帯域制限の標本化条件・理想再構成を確認。原典の線形性のみという省略と等号端点を区別する。'),
 ('mit_moving2012','Massachusetts Institute of Technology','6.02 Lecture 13: Frequency Response of Moving Average Filters','https://web.mit.edu/6.02/www/s2012/handouts/L13_slides.pdf','移動平均の周波数応答と零点のスライドを確認。窓長Mと周期の一致で正弦波が消える例は本教材の独自導出。'),
 ('scipy_notch','SciPy Developers','scipy.signal.iirnotch: Narrow Band-Stop Filter','https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.iirnotch.html','狭帯域阻止、有限幅、Qと阻止帯域の定義を現行公式文書で確認。過去問のAPI版についての主張はしない。'),
 ('scipy_fft','SciPy Developers','scipy.fft.fft: Discrete Fourier Transform','https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html','DFTを効率化するFFT、二のべき乗と他の標本数への算法、有限標本の周波数順を確認。'),
 ('scipy_coherence','SciPy Developers','scipy.signal.coherence: Magnitude Squared Coherence','https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.coherence.html','相互スペクトル絶対値二乗を自己スペクトル積で割る二乗コヒーレンスの定義を確認。'),
 ('usgs_processing2000','W. F. Agena and M. W. Lee and P. E. Hart','Reprocessing of Multi-channel Seismic-Reflection Data Collected in the Beaufort Sea','https://pubs.usgs.gov/of/2000/ofr-00-460/','取得HTML本文の静補正・NMO・CMP重合・migrationを確認。本文の特定規格化を普遍的算術平均の定義とはせず、平方根則は独自の分散計算で導出する。'),
 ('usgs_refraction2013','Alan Yong and Antony Martin and Kenneth Stokoe and John Diehl','ARRA-Funded VS30 Measurements Using Multi-Technique Approach at Strong-Motion Stations','https://pubs.usgs.gov/of/2013/1102/of2013-1102_text.pdf','取得65頁PDF本文の薄い層が初動に現れない例、低速度逆転との区別を確認。日本語のブラインド層の広狭を単一英語名へ固定しない。'),
 ('usgs_static2004','U.S. Geological Survey','Accurate Elevation and Normal Moveout Corrections of Seismic Reflection Data on Rugged Topography','https://www.usgs.gov/publications/accurate-elevation-and-normal-moveout-corrections-seismic-reflection-data-rugged','出版物索引の要約で地形と風化低速度層による走時ずれへの静補正を確認。本文全文は取得していない。'),
 ('epa_seismic_reflection','United States Environmental Protection Agency','Seismic Reflection','https://www.epa.gov/environmental-geophysics/seismic-reflection','本文の波速・密度による音響インピーダンス、走時深度対応、NMOとmigrationを確認。厚さ分解能等の一律値は採用しない。'),
 ('stanford_downward2001','Stanford Exploration Project','Downward Continuation and Imaging','https://sep.stanford.edu/sep/prof/waves/dwnc/paper_html/node9.html','本文と2001-03-01の表示を確認。地震波動場を地下へ外挿する下方接続とmigrationの関係を確認。ポテンシャル場専用とした初回誤認を訂正する根拠。'),
 ('rigid_boom2019','Christian von Hebel and others','Calibration, Conversion, and Quantitative Multi-Layer Inversion of Multi-Coil Rigid-Boom Electromagnetic Induction Data','https://pmc.ncbi.nlm.nih.gov/articles/PMC6864633/','一次論文の検索収録で送受信コイルによる電磁誘導の原理を確認。本文再取得はchallenge、MDPIは403、機関リポジトリPDF URLはHTMLを返し全文読了ではない。'),
 ('usgs_equivalent2007','Jeffrey D. Phillips','Geosoft eXecutables (GXs) Developed by the U.S. Geological Survey, Version 2.0','https://pubs.usgs.gov/of/2007/1355/pdf/of07-1355.pdf','取得PDFの印刷51頁USGS_MFDESIGNで磁気の双極子層・重力の密度層を等価層とする説明を確認。'),
 ('usgs_lateral_logging','U.S. Geological Survey','Circular 891: Geophysical Logs as a Source of Coal Bed Data','https://pubs.usgs.gov/circ/c891/geophysical.htm','取得HTMLのNORMAL AND LATERAL LOGS節で電極間隔と配置、抵抗の測定を確認。')]
p=ROOT/'references.bib';s=p.read_text();added=0
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:
  s+='\n@online{'+k+',\n author={'+a+'},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n+'}\n}\n';added+=1
p.write_text(s)
concepts=[('exploration_filter_types','探査信号のフィルタ選択','ノッチ|低域通過'),('exploration_stack_snr','探査の重合とS/N平方根則','スタック|S/N'),('exploration_moving_average','移動平均の雑音低減と周波数零点','移動平均'),('exploration_forward_inverse','探査の順問題・逆問題と対象雑音','順問題|逆問題'),('exploration_seismic_terms','地震探査の走時・画像化用語','CMP|静補正|ブラインド'),('exploration_wave_principles','探査波動の伝播原理','フェルマ|ホイヘンス|等価層'),('exploration_inverse_methods','逆問題の正則化・最適化と離散化','マルカート|共役勾配|平滑化拘束')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
if not all(k in ids for k,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_039_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APPLIED'],disciplines=['geo_exploration']))
 d['version']='1.32-S7-concept-additions';p.write_bytes(json_bytes(d))
folder=ROOT/'extracted/reference_checks/S7_039'
local={p.name:digest(p) for p in folder.iterdir() if p.is_file() and p.name!='source_notes.json'}
(folder/'source_notes.json').write_bytes(json_bytes(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_sha256=local,limitations=['rigid_boom.pdfは248バイトのHTML challengeでありPDFではない。成功取得と報告しない。','原典13実画像・17問を確認し公式前初回を保存。R01AP34初回5を訂正4と分離。','標本化端点、移動平均の周期消去反例、有限要素法の逆解析内利用は部分校正・査読待ち。'])))
followup=dict(time=now(),question_id='R01-REG-APPLIED-34',initial_answer_preserved='5',official_answer='4',followup_answer='4',reason='下方接続をポテンシャル場専用とした初回誤認。Stanford本文では地震波動場の地下外挿からmigrationを行う。rigid-boom EMI論文の一次検索収録は送受信コイルと導体の二次磁場を扱い、電磁探査の配置と分かる。',sources=['stanford_downward2001','rigid_boom2019'],limitation='rigid-boom論文全文PDFは取得できていない。初回5を改変せず当該検索収録の範囲を明示して最終査読を残す。')
(ROOT/'extracted/logs/S7_039_independent_followup.json').write_bytes(json_bytes(followup))
print('Concepts',len(d['concepts']),'references added',added)
