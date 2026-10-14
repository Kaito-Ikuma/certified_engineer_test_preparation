# coding: utf-8
import sys,json,re,shutil,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
 ('stat_nist_normal','NIST/SEMATECH','Engineering Statistics Handbook: Normal Distribution','https://www.itl.nist.gov/div898/handbook/eda/section3/eda3661.htm','密度・標準化・分布範囲と中心極限定理の本文を確認。中心極限定理は独立性・有限分散等の条件を補って説明する。'),
 ('stat_psu_linear','Pennsylvania State University','STAT 505: Linear Combinations of Random Variables','https://online.stat.psu.edu/stat505/Lesson02','ブラウズ失敗後curlで本文取得。Population Mean/Variance節の平均線形性、係数の二乗と共分散項を確認。全講義例の通読ではない。'),
 ('stat_psu_correlation','Pennsylvania State University','STAT 200: Correlation and Simple Linear Regression','https://online.stat.psu.edu/stat200/Lesson12','ブラウズ失敗後curl取得。相関、最小二乗回帰、R²=r²、外れ値と因果の節を確認。全例題の通読ではない。'),
 ('quality_qfd_scale','Jong-Seok Shin and Kwang-Jae Kim','Effect and Choice of the Weighting Scale in QFD (2000)','https://asq.org/quality-resources/articles/effect-and-choice-of-the-weighting-scale-in-qfd?id=626819a08f674ecaa9d19e42cad42821','ASQ掲載著者抄録を確認。関係尺度が技術重要度に影響する。全文は会員対象で未取得。試験固有5/3/1の積和は原典から独立計算。'),
 ('quality_process_jsqc','加藤省吾 and 伊藤怜史 and 飯塚悦功 and 下野僚子 and 水流聡子','病院における日常業務のプロセス管理標準を設計するための方法論 (2015)','https://www.jstage.jst.go.jp/article/quality/45/1/45_KJ00009750446/_article/-char/ja/','学会抄録全文で品質保証のプロセス設計・標準・QC工程表を確認。病院事例を全工程の実証へ一般化しない。'),
 ('quality_iso_process','ISO/TC 176/SC 2','The process approach in ISO 9001:2015','https://www.iso.org/iso/iso9001_2015_process_approach.pdf','物理1–2頁本文のプロセス定義、PDCA四段階と改善を確認。2008版原文の代用品とはしない。'),
 ('quality_iso2008_guidance','ISO/TC 176/SC 2','Implementation Guidance for ISO 9001:2008 (N836)','https://www.iso.org/iso/06_implementation_guidance.pdf','物理2頁の改定範囲と6頁のPlan-Do-Check-Actを文字層確認。規格本文全体は未取得。'),
 ('quality_nist_capability','NIST/SEMATECH','Engineering Statistics Handbook: What is Process Capability?','https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm','安定工程・正規前提、Cp/Cpkの定義を確認。規格限界と工程の変動を分ける。頁の他の推定式にある文字誤りは転載しない。'),
 ('quality_nist_control','NIST/SEMATECH','Engineering Statistics Handbook: What are Control Charts?','https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc31.htm','本文で時間・標本順、中心線と管理限界、偶然変動と異常、非ランダムパターンを確認。'),
 ('quality_nist_histogram','NIST/SEMATECH','Engineering Statistics Handbook: Histogram','https://www.itl.nist.gov/div898/handbook/eda/section3/histogra.htm','区間度数と密度正規化の本文を確認。異なる幅の区間では高さでなく面積を度数に対応させる。'),
 ('quality_nist_sampling','NIST/SEMATECH','Engineering Statistics Handbook: Lot Acceptance Sampling Plans','https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc22.htm','30行本文を確認。n,c、AQL/LTPD、第1種=良品拒否、第2種=不良品受入、多回と逐次を確認。JIS切換えの規格全文は未取得。'),
 ('quality_nist_oc','NIST/SEMATECH','Engineering Statistics Handbook: OC Curves','https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc243.htm','OCの二項累積式とα/β定義を確認。本文のc未満と以下の不統一、1-αを生産者危険とする誤記はpmc22の定義と数式で区別。教材はc以下とαを用いる。'),
 ('stat_nist_binomial','NIST/SEMATECH','Engineering Statistics Handbook: Binomial Distribution','https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm','二結果と一定p、質量関数、平均np/分散np(1-p)を確認。独立試行という成立条件を保持。'),
 ('stat_nist_poisson','NIST/SEMATECH','Engineering Statistics Handbook: Poisson Distribution','https://www.itl.nist.gov/div898/handbook/eda/section3/eda366j.htm','区間内回数、質量関数、平均と分散、歪度λ^(-1/2)を確認。小平均での非対称性と大平均近似を区別。'),
 ('stat_nist_exponential','NIST/SEMATECH','Engineering Statistics Handbook: Exponential Distribution','https://www.itl.nist.gov/div898/handbook/eda/section3/eda3667.htm','密度・生存確率と一定故障率を確認。全ての災害間隔が指数という普遍主張をしない。'),
 ('stat_nist_interval','NIST/SEMATECH','Engineering Statistics Handbook: Confidence Limits for the Mean','https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm','64行本文のt自由度n-1、有意水準、区間幅、1-αと反復被覆を確認。固定区間の事後確率と区別する。'),
]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={'+a+'},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
new=[
 ('quality_normal_combinations','独立正規変数の和差と標本平均','標準偏差|正規分布'),
 ('quality_qfd','品質要求の展開と重要度','品質表|要求品質'),
 ('quality_process_assurance','工程の品質保証と標準化','源流管理|品質保証'),
 ('quality_tools_capability','工程能力と統計的品質管理の図','工程能力|管理図|ヒストグラム'),
 ('quality_acceptance_sampling','抜取検査の二つの危険と切換え','抜取検査|生産者危険'),
 ('quality_stress_strength','正規応力強度モデルの故障確率','応力S|強度R'),
 ('quality_pdca','PDCAによるプロセスの継続改善','PDCA|9001'),
 ('quality_probability_models','事象回数と間隔の確率モデル','確率分布|ポアソン'),
 ('quality_correlation_regression','線形相関と回帰・因果の区別','相関係数|決定係数'),
 ('quality_hypothesis_inference','仮説検定と信頼区間','帰無仮説|統計的検定'),
]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
if not all(k in ids for k,_,_ in new):
 snap=ROOT/'snapshots/config_before_S7_030_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['BASIC'],disciplines=['basic_1_1','basic_5_3']))
 
 for c in d['concepts']:
  if c['id']=='quality_pdca' and 'basic_1_2' not in c['disciplines']:c['disciplines'].append('basic_1_2')
  if c['id']=='quality_correlation_regression' and 'basic_1_9' not in c['disciplines']:c['disciplines'].append('basic_1_9')
 d['version']='1.23-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_030';folder.mkdir(exist_ok=True)
files=[]
for src in ['/tmp/S7_030_psu_linear.html','/tmp/S7_030_psu_linear.txt','/tmp/S7_030_psu_correlation.html','/tmp/S7_030_psu_correlation.txt']:
 target=folder/Path(src).name;shutil.copyfile(src,target);files.append(dict(file=str(target.relative_to(ROOT)),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=files,limitations=['規格本文、JIS切換えは未取得。一般定義・公式の当時ガイダンス・原典記述を区別する。','検索で得たGamma/Weibull/Lognormal頁は今回の根拠へ代用しない。']),ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
