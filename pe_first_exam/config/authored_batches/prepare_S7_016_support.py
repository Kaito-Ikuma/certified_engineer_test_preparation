# coding: utf-8
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,digest
refs=[
('cabinet_npo_overview','内閣府','NPO制度の概要','https://www.npo-homepage.go.jp/about/npo-kisochishiki/nposeido-gaiyou','2012年改正施行、20分野、不特定多数の利益、支障のないその他の事業を本文確認。'),
('cabinet_npo_officers','内閣府',r'NPO法Q\&A：役員等','https://www.npo-homepage.go.jp/qa/ninshouseido/ninshou-yakuin','2-3-14で役員報酬人数3分の1以下と職員給与の区別を本文確認。'),
('cabinet_worklife','内閣府','仕事と生活の調和（ワーク・ライフ・バランス）憲章','https://wwwa.cao.go.jp/wlb/government/20barrier_html/20html/charter.html','憲章の目的、多様な選択、関係主体の取組。2007年策定・2010年改定と現在のウェブを分離。'),
('iso26000_project2010','International Organization for Standardization','ISO 26000 project overview','https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_26000_project_overview.pdf','2010年発行時の組織対象、持続可能な発展、認証用でないこと。ウェブPDF抽出本文で確認。'),
('iso_gri2014','International Organization for Standardization and Global Reporting Initiative','GRI G4 Guidelines and ISO 26000:2010: How to use the GRI G4 Guidelines and ISO 26000 in conjunction','https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso-gri-26000_2014-01-28.pdf','附属書Iの七原則と七中核主題を公式検索抽出で照合。政府の意向を法の支配へ加えない判断は原典と規範の区別に基づく独立分析。'),
('jp_constitution','衆議院','日本国憲法','https://www.shugiin.go.jp/Internet/itdb_annai.nsf/html/statics/shiryo/dl-constitution.htm','12条の権利保持・濫用・公共の福祉を国会本文で確認。'),
('jp_civil','e-Gov法令検索','民法','https://laws.e-gov.go.jp/law/129AC0000000089?occasion_date=20220220','1条の私権と公共の福祉。検索本文と条文、閲覧時点の版を区別。動的ページ全文の取得を意味しない。'),
('jp_national_public','e-Gov法令検索','国家公務員法','https://laws.e-gov.go.jp/law/322AC0000000120?occasion_date=20260325','100条の職務上の秘密・退職後の義務・許可を公式検索本文で照合。全ての服務条項の時系列監査ではない。'),
('ipej_associate_registration','日本技術士会','技術士補登録の手引','https://www.engineer.or.jp/c_topics/003/003820.html','認定課程修了者は技術士補となる資格を持つ。登録と区別。現在の手引を2015年の版とはしない。'),
('jabee_canberra','日本技術者教育認定機構','キャンベラ協定：UNESCO-UIAからの移行','https://jabee.org/international_relations/canberra-accord/','2012年正規認証、2014年暫定加盟、2019年正式加盟を本文確認。'),
('ipej_ipea2014','日本技術士会','第13回(C) EMF国際エンジニア審査申請書作成の手引','https://www.engineer.or.jp/emf/13C_tebiki.pdf','2015年4月1日の和文名称変更と登録要件を公式PDF検索抽出で確認。'),
('mext_international','文部科学省','技術士資格の国際的通用性について','https://www.mext.go.jp/a_menu/jinzai/gijutsushi/mext_01827.html','2003年10月1日日豪枠組み、共通称号と免許・登録、限定分野・受入国経験等を本文確認。現行対象分野表を2015年と同一とはしない。'),
('jaeic_mutual2010','建築技術教育普及センター','他エコノミーとの相互認証の状況について（平成22年6月）','https://www.jaeic.or.jp/international/apecarchitect-j/aa-dk/aa-sougoninsyou.html','2008年豪州・2009年NZ、固有事項審査を本文確認。日付の細部は他発表との差があるため解説は年単位。'),
('meti_secret_handbook2024','経済産業省','秘密情報の保護ハンドブック（第6版、2024年2月）','https://www.meti.go.jp/policy/economy/chizai/chiteki/pdf/handbook/full.pdf','公式検索抽出の3章3-4、複数人・単独時の事前事後確認、配置、紙削減を確認。ダウンロード403、全PDF読了でない。'),
('ncsu_ud1997','North Carolina State University, Center for Universal Design','The Principles of Universal Design, Version 2.0 (1997)','https://design.ncsu.edu/research/center-for-universal-design/','1997年4月1日版の七原則を公式本文で確認。ウェブ改修・PDFアップロード年と制定年を区別。'),
('court_jr2017','最高裁判所第二小法廷','平成27年（あ）第741号：平成29年6月12日決定','https://www.courts.go.jp/assets/hanrei/hanrei-pdf-86834.pdf','歴代3社長の事件、4頁末〜5頁の無罪第一審是認と主文の上告棄却を公式本文確認。単独の別社長事件と区別。'),
('jtsb_fukuchiyama2007','航空・鉄道事故調査委員会','鉄道事故調査報告書 RA2007-3-1：福知山線（本文）','https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf','保存PDFの本文229頁付近の曲線速照と243頁の原因、125頁付近の車上ATSをテキスト照合。全256頁の画像目視でない。'),
('mhlw_milk2002','厚生労働省','乳及び乳製品の規格基準の改正に関する食品衛生分科会報告について','https://www.mhlw.go.jp/shingi/2002/07/s0717-2.html','IIで停電時の菌増殖・エンテロトキシンA産生を本文・検索抽出照合。刑事判決資料ではない。'),
('milk_incident_company','雪印メグミルク','「2つの事件」の概要と「雪印八雲工場食中毒事件」','https://www.meg-snow.com/sustainability/esg/approach/incident/','当事企業による汚染原料と対応の振り返り。中立の判決認定としては使わない。'),
('muroran_ethics_cases','室蘭工業大学技術者倫理研究会','技術者倫理事例集','https://muroran-it.repo.nii.ac.jp/record/5154/files/EngEthics.pdf','保存PDF7章47頁以降、軽量化と変更、センサ・停止・慣性の検討をテキスト確認。独自の倫理分析資料、刑事判決一次文書ではない。'),
('caa_elevator2006','消費者庁消費者安全調査委員会','平成18年6月3日に東京都内で発生したエレベーター事故：報告書等','https://www.caa.go.jp/policies/council/csic/report/report_004/','2016年事故等原因調査と戸開走行、上昇・挟まれ。概要をウェブPDF本文で確認。'),
('mlit_sasago2013','国土交通省調査・検討委員会','トンネル天井板の落下事故に関する調査・検討委員会報告書（2013年）','https://www.mlit.go.jp/common/001001299.pdf','事故概要と接着系アンカー、設計・施工・維持管理、情報継承の提言をウェブ本文確認。刑事責任認定へ代用しない。')]
f=ROOT/'references.bib';s=f.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n  author={{'+a+'}},\n  title={'+t+'},\n  url={'+u+'},\n  urldate={2026-10-10}\n}\n'
f.write_text(s)
dest=ROOT/'extracted/reference_checks/S7_016';dest.mkdir(parents=True,exist_ok=True)
(dest/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=[dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in dest.glob('*.pdf')],limitations=['ISO/OECD 2019 PDFはウェブで容量超過、curl403。代わりにISO/GRI2014附属書を参照。未取得本文を読了として扱わない。','METIハンドブック403は検索抽出を使用し、現在版と出題当時の版を区別。','H30問14の1・3・4の刑事判決は一次裁判資料未確認。']),ensure_ascii=False,indent=2)+'\n')
new=[('npo_activity','非営利活動の公益目的・事業収入と報酬','NPO|特定非営利',['apt_5']),('work_life_balance','仕事と生活の調和・多様な働き方','ワーク・ライフ|仕事と生活',['apt_5']),('secret_management','秘密情報の接近制御・相互確認と持出し防止','単独作業|秘密情報',['apt_1','apt_4']),('international_registration','教育認定・国内登録・国際称号と業務資格','JABEE|APEC|IPEA',['apt_0']),('accident_learning','事故機構・設計運用と個別責任の区別','失敗事例|事故原因|刑事裁判',['apt_3'])]
f=ROOT/'config/concepts.json';d=json.loads(f.read_text());ids={x['id'] for x in d['concepts']}
if not all(x[0] in ids for x in new):
 snap=ROOT/'snapshots/config_before_S7_016_concept.json';assert not snap.exists();snap.write_bytes(f.read_bytes())
 for k,label,pat,disc in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pat,subjects=['APT'],disciplines=disc))
 old=d['version'];d['version']='1.9-S7-concept-additions';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 log=ROOT/'config/concept_change_log_S7.json';rows=json.loads(log.read_text());rows.append(dict(time=now(),batch='S7_016_ethics_institutions',previous_version=old,version=d['version'],added=[x[0] for x in new],reason='既存分類を保持し、非営利、仕事生活、秘密管理、国際登録、事故学習の5概念を適性へ追加。108概念の前版保存。'));log.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
