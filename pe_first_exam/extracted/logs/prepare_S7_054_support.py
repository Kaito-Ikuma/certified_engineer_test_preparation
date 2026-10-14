# coding: utf-8
import json,re,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
cp=P/'config/concepts.json'
assert not (P/'extracted/logs/config_before_S7_054_concept.json').exists()
shutil.copyfile(cp,P/'extracted/logs/config_before_S7_054_concept.json')
c=json.loads(cp.read_text())
spec=[
('data','研究データの検証と期限','apt_1'),('public','公共責任と法の空白','apt_5'),
('precaution','予防的取組の十二の視点','apt_3'),('principles','功利・正義・義務の倫理視点','apt_5'),
('sr','組織の社会的責任と不正対応','apt_5'),('norms','規範の効力と専門職の責任','apt_5'),
('guideline','2014研究不正ガイドラインの措置','apt_1'),('riskcomm','リスク対話の視点と検証可能性','apt_3'),
('code','倫理綱領の公共優先と誠実','apt_5'),('whistlepurpose','旧公益通報保護法の目的','apt_4'),
('conflict','発言内容と利益関係の開示','apt_5'),('iso','ISO26000の七原則','apt_5'),
('information','技術情報と説明・記録の行動','apt_1'),('bcp','事業継続計画と重要業務','apt_3'),
('disclosurecase','構造の危険と情報開示','apt_5'),('energy','地域エネルギーと熱電併給・ZEH','apt_2'),
('publicmodel','公衆と情報に基づく同意','apt_5'),('diversity','多様性の属性・経験・働き方','apt_5'),
('pdca','PDCAの四段階','manual_78'),('society','Society5.0と人間中心の目的','manual_80'),
('cpd','CPDの実績証明と通常業務','apt_0'),('competency','2023コンピテンシーの八項目','apt_0'),
('code2023','2023倫理綱領の指針と協働','apt_5'),('profession','2007宣言の三つの責任','apt_5'),
('dei','DEIの多様性・公平性・包摂性','apt_5')]
assert c['version']=='1.46'
for key,label,d in spec:c['concepts'].append({'id':'eth54_'+key,'label':label,'pattern':label,'subjects':['APT'],'disciplines':[d]})
c['version']='1.47';cp.write_text(json.dumps(c,ensure_ascii=False,indent=2))
refs=[
('eea','European Environment Agency','Late lessons from early warnings: report22/2001','https://www.eea.europa.eu/en/analysis/publications/environmental_issue_report_2001_22/environmental_issue_report_2001_22/@@download/file','章16の十二見出しを検索・抽出本文で確認。211頁全文読了ではない。'),
('rio','United Nations Audiovisual Library of International Law','Rio Declaration: procedural history and legal character','https://legal.un.org/avl/ha/dunche/dunche.html','国連の宣言の歴史資料を参照。宣言を条約として批准したとしない。原典前文のサミット交渉史全体は未照合。'),
('globalcompact','United Nations Global Compact','The Ten Principles','https://unglobalcompact.org/what-is-gc/mission/principles','公式検索本文で四分野と十原則の構成を確認。全実施手引の確認ではない。'),
('university','東京大学','東京大学学生懲戒処分規程等','https://www.u-tokyo.ac.jp/content/400283132.pdf','公式検索本文の試験不正を懲戒対象とする規定を確認。直接web openは内部エラー。2014全大学の処分分布の証明ではない。'),
('riskcomm','文部科学省','2014リスクコミュニケーションの推進方策資料','https://www.mext.go.jp/b_menu/shingi/gijyutu/gijyutu2/066/shiryo/__icsFiles/afieldfile/2014/04/03/1346337_1_1.pdf','案と検討資料を含む55頁PDF。抽出本文の認知モデル、当事者と統治者、検証可能性の箇所を確認。原典採用版との全照合は未完。'),
('iso_brochure','International Organization for Standardization','Discovering ISO26000: Guidance on social responsibility','https://www.iso.org/files/live/sites/isoorg/files/store/en/PUB100258.pdf','公式公開冊子の抽出本文と検索された図の七原則を確認。Clause4の七原則とClause6の七中核主題を区別。106頁規格本文の全読ではない。'),
('bcp2013','内閣府','事業継続ガイドライン第三版：2013年8月','https://www.bousai.go.jp/kyoiku/kigyou/pdf/guideline03.pdf','公式旧版リンクとPDFを開いて版を確認。重要事業とBCMの枠組みに用いる。全55頁の読了とはしない。'),
('bcp2021','内閣府','事業継続ガイドライン：2021年4月','https://www.bousai.go.jp/kyoiku/kigyou/pdf/guideline202104.pdf','57頁のうち抽出本文の影響度分析・法令契約と重要業務・改善の箇所を確認。全文読了ではない。'),
('bcp_survey2018','内閣府','平成29年度企業の事業継続及び防災の取組実態調査','https://www.bousai.go.jp/kyoiku/kigyou/topics/pdf/h29_jittaichousa.pdf','2018年3月調査。検索本文とPDF抽出の策定済大企業64.0・中堅31.8%を確認。114頁全部と各母集団定義は未読。2019試験後の調査値を使わない。'),
('cogen2018','資源エネルギー庁','コジェネでエネルギーを効率的に使う：2018年','https://www.enecho.meti.go.jp/about/special/johoteikyo/cogeneration.html','公開検索本文で発電と廃熱利用を確認。CEMSの当時定義全文は追加照合対象。'),
('zeh2018','資源エネルギー庁','ZEHの定義：改定版','https://www.enecho.meti.go.jp/category/saving_and_new/saving/assets/pdf/general/housing/zeh_definition_kodate.pdf','2018改定版の公式索引と検索本文を確認。年間・一次エネルギーの評価境界を条件として扱い、全エネルギー無条件ゼロにしない。全文精読ではない。'),
('pdca2017','文部科学省','研究開発評価研修資料：2017評価指針への言及','https://www.mext.go.jp/component/a_menu/science/detail/__icsFiles/afieldfile/2018/12/11/1411583_02.pdf','検索本文で2017指針とPDCAへの言及を確認。2017指針全文の転載ではない。'),
('society2021','内閣府','Society5.0：2016提案と2021計画','https://www8.cao.go.jp/cstp/english/society5_0/index.html','本文の社会段階、2016の人間中心と2021の持続可能・強靱・well-beingの説明を読んだ。現在ページの後段の事業全体を当時へ遡及しない。'),
('competency2023','文部科学省掲載資料','2023コンピテンシーを収録するガイドブック','https://www.mext.go.jp/content/20230607-mxt_kiban02-000030294_7.pdf','62頁PDFの物理29・30頁の抽出本文で2014七項目から2023八項目への変化と全キーワードを確認。全ガイドブック読了ではない。'),
('profession2007','日本技術士会','技術士プロフェッション宣言：2007年1月1日','https://www.engineer.or.jp/c_topics/000/000029.html','公式本文の三つの行動原則と日付を読んだ。'),
('dei2025','日本技術士会','日本技術士会DEI推進宣言：2025年4月','https://www.engineer.or.jp/c_topics/010/010898.html','本文の目的・三方針・Diversity/Equity/Inclusion定義と3月14日策定を読んだ。2021問題には後年の補足である。')]
def esc(x):
 for a,b in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('_',r'\_')]:x=x.replace(a,b)
 return x
bib=P/'references.bib';s=bib.read_text();notes=[]
for key,org,title,url,note in refs:
 key='eth54_'+key;assert '@online{'+key+',' not in s
 s+='\n@online{'+key+',\n author={{'+esc(org)+'}},\n title={'+esc(title)+'},\n url={'+url+'},\n note={'+esc(note)+'},\n urldate={2026-10-14}\n}\n'
 notes.append({'key':key,'url':url,'title':title,'reading_scope':note,'full_source_read':key in ['eth54_profession2007','eth54_dei2025']})
bib.write_text(s)
(P/'extracted/logs/source_notes_S7_054.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
print('Added',len(spec),'concepts',len(refs),'references')
