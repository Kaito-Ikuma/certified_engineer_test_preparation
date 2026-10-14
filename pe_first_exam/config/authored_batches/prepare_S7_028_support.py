# coding: utf-8
import sys,json,re,shutil,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
 ('reliability_nist_series','NIST','Reliability Handbook: Series model','https://www.itl.nist.gov/div898/handbook/apr/section1/apr182.htm','独立性、最初の部品故障で系故障、各寿命分布既知という三条件と信頼度の積を本文確認。'),
 ('reliability_nist_parallel','NIST','Reliability Handbook: Parallel or redundant model','https://www.itl.nist.gov/div898/handbook/apr/section1/apr183.htm','独立、少なくとも一つが稼働、各寿命分布既知という条件と故障確率の積を本文確認。'),
 ('reliability_nist_voting','NIST','Reliability Handbook: R out of N model','https://www.itl.nist.gov/div898/handbook/apr/section1/apr184.htm','同一信頼度・独立・任意のn-r故障を許す条件と二項和の式を確認。'),
 ('design_caa_pl1','消費者庁','製造物責任法逐条解説：第1条（平成30年9月）','https://www.caa.go.jp/policies/policy/consumer_safety/other/product_liability_act_annotations/pdf/annotations_180907_0002.pdf','文字層が文字化けするため物理1頁をレンダリングして目的条文、被害者の範囲、過失から欠陥責任の背景を確認。'),
 ('design_caa_pl2','消費者庁','製造物責任法逐条解説：第2条（平成30年9月）','https://www.caa.go.jp/policies/policy/consumer_safety/other/product_liability_act_annotations/pdf/annotations_180907_0003.pdf','物理5・6頁（印刷6・7頁）を実見。通常有すべき安全性、絶対安全性ではないこと、製造・設計・指示警告の欠陥を確認。全26頁通読ではない。'),
 ('design_mhlw_crane','厚生労働省','クレーン等安全規則：第213条','https://www.mhlw.go.jp/web/t_doc?dataId=74020000&dataType=0&pageNo=2','玉掛けワイヤロープの6以上と切断荷重/最大荷重の定義、平成10年の改正注記を確認。他のロープへ一般化しない。'),
 ('design_faa_2011','米国政府出版局','14 CFR 25.303: Factor of safety（2011年版）','https://www.govinfo.gov/content/pkg/CFR-2011-title14-vol1/pdf/CFR-2011-title14-vol1-sec25-307.pdf','2011年版の25.303本文、限界荷重に1.5を掛ける条件、例外と終局荷重既定の場合の扱いを確認。ロケット全般の規準ではない。'),
 ('design_fsc_adi','食品安全委員会','ADIの考え方について（2008年12月12日）','https://www.fsc.go.jp/fsciis/questionAndAnswer/show/mob07017000029','残留農薬等の無毒性量から通常100で割るADI算定と終生摂取の条件を本文確認。治療薬全般の安全率ではない。'),
 ('design_mlit_elevator','国土交通省','エレベーター強度検証法等：平成12年建設省告示第1414号（平成25年改正反映）','https://www.mlit.go.jp/notice/noticedata/pdf/201703/00006471.pdf','第二三の限定条件と物理3頁表を実見。主索の常時設置5.0/使用4.0、主索端部との区別を確認。2011当時版及び現行版の全改正履歴の検証ではない。'),
 ('maintenance_mlit_2013','国土交通省','国土交通省資料：適切な点検・保全（2013年）','https://www.mlit.go.jp/common/001026806.pdf','物理10頁の時間計画・状態監視・事後保全の対象別分類、経過年数の交換と動作値による劣化把握を本文確認。全32頁通読やJIS全版照合ではない。'),
 ('design_mhlw_foolproof','厚生労働省','職場のあんぜんサイト：フールプルーフ','https://anzeninfo.mhlw.go.jp/yougo/yougo39_1.html','人間特性と誤操作を災害へつなげない設計、ガードとインターロック例を本文確認。'),
 ('design_mhlw_failsafe','厚生労働省','職場のあんぜんサイト：フェールセーフ','https://anzeninfo.mhlw.go.jp/yougo/yougo38_1.html','故障時の安全側固定、影響限定、停止以外の代替機能の安全確保を本文確認。'),
 ('design_nasa_tolerance','NASA','Considerations for Software Fault Prevention and Tolerance（Technical Bulletin 23-06）','https://www.nasa.gov/centers-and-facilities/nesc/nesc-technical-bulletin-23-06considerations-for-software-fault-prevention-and-tolerance/','本文の飛行前の故障予防と飛行中のエラー検出・緩和を区別。NASAの技術用語全定義を通覧したものではない。'),
 ('design_mit_lp','MIT OpenCourseWare','Principles of Discrete Applied Mathematics: Linear Programming Notes（2013）','https://ocw.mit.edu/courses/18-310-principles-of-discrete-applied-mathematics-fall-2013/11d00f8f0f460a5e59b5e97322a218a9_MIT18_310F13_Ch8.pdf','単体法の基底交換、退化と循環対策、主/双対の式、弱・強双対の条件を該当本文で確認。全28頁の証明通読ではない。')]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
new=[
 ('design_reliability_network','直列・並列の信頼度と独立性','信頼度|直列.*並列',['basic_1_0']),
 ('design_reliability_voting','多数決冗長系の信頼度','多数決|冗長',['basic_1_0']),
 ('design_fault_tree','故障の木と論理ゲート','FTA|故障の木',['basic_1_0']),
 ('design_availability','修復系の定常稼働率','MTBF|アベイラビリティ',['basic_1_0']),
 ('design_maintenance','時間計画・状態監視・事後保全','保全',['basic_1_0']),
 ('design_fault_handling','故障時の安全・縮退・機能継続','フェール|フォールト|フールプルーフ',['basic_1_0']),
 ('design_safety_factor_scope','用途・基準時点ごとの安全係数','安全率|安全係数',['basic_1_3']),
 ('design_product_liability','製造物の欠陥と通常の安全性','製造物責任',['basic_1_4']),
 ('design_multiobjective','単体法・双対と多目的最適化','シンプレックス|パレート|双対',['basic_1_2'])]
if not all(k in ids for k,_,_,_ in new):
 snap=ROOT/'snapshots/config_before_S7_028_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat,ds in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['BASIC'],disciplines=ds))
 d['version']='1.21-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_028';folder.mkdir(exist_ok=True)
files=[]
for src in ['/tmp/S7_028_PL1.pdf','/tmp/S7_028_PL2.pdf','/tmp/S7_028_elevator.pdf','/tmp/S7_028_PL1_1.png','/tmp/S7_028_PL2_5.png','/tmp/S7_028_PL2_6.png','/tmp/S7_028_elevator_3.png']:
 target=folder/Path(src).name;shutil.copyfile(src,target);files.append(dict(file=str(target.relative_to(ROOT)),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=files,limitations=['IEC Electropedia 192-06各項目は403で未取得。IEC/JIS全文の一致を確認したとしない。','e-Gov現行製造物責任法は文字取得不能。平成30年逐条解説と各試験原典の条文を比較するが、全改正履歴を確認したとはしない。','安全率の一般的代表値を全材料・全用途の法定値としない。パレートの反例と稼働率はモデルから独自導出。']),ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
