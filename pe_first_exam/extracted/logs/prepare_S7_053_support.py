# coding: utf-8
"""Explicit scopes and primary-source reading notes."""
import json,re,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
cp=P/'config/concepts.json';shutil.copyfile(cp,P/'extracted/logs/config_before_S7_053_concept.json')
c=json.loads(cp.read_text())
spec=[
('ghs','GHSの分類・伝達と国内追加表示','apt_3'),
('machine','機械安全の方策とシステム境界','apt_3'),
('recall','リコールと安全規制・責任の区別','apt_3'),
('food_label','食品の期限・原産地・アレルギー表示','apt_4'),
('food_roles','食品リスク評価・管理・対話の役割','apt_3'),
('ad_evidence','不実証広告と客観的根拠','apt_4'),
('quality','品質不正の記録と組織・現場条件','apt_3'),
('security','CIAと不審メールの初動','apt_1'),
('product_accident','重大製品事故の報告・公表と時点','apt_3'),
('workplace','変更時のリスク調査と軽微例外','apt_3'),
('human','ヒューマンエラー発生要因の12分類','apt_3'),
('gmo','生物多様性と食品安全の別審査','apt_2'),
('whistle','公益通報の対象者・通報先別要件','apt_4'),
('ethic_whistle','倫理的告発の証拠・段階・改善見込み','apt_5'),
('maintenance2021','2021インフラ行動計画の七項目','manual_79')]
assert not any(x['id'].startswith('saf53_') for x in c['concepts'])
for key,label,d in spec:c['concepts'].append({'id':'saf53_'+key,'label':label,'pattern':label,'subjects':['APT'],'disciplines':[d]})
c['version']='1.46';cp.write_text(json.dumps(c,ensure_ascii=False,indent=2))
refs=[
('ghs_old','厚生労働省','改正労働安全衛生法（GHS関係）情報','https://www.mhlw.go.jp/topics/bukyoku/roudou/ghs/index.html','検索本文でJIS Z7251:2006/2010とモデルラベル・MSDSを確認。当時の全規格本文は未取得。'),
('ghs_notice','厚生労働省','化学物質等の表示通知促進指針：平成24年3月29日','https://www.mhlw.go.jp/web/t_doc?dataId=00tb8209&dataType=1&pageNo=1','検索本文のH24公示・Z7253と危険有害性分類の枠組みを確認。全JIS細目の通読ではない。'),
('machine2007','厚生労働省','機械の包括的な安全基準に関する指針：2007年7月31日','https://www.mhlw.go.jp/web/t_doc?dataId=00tb3487&dataType=1&pageNo=1','公開検索本文で本質的安全・安全防護・使用上の情報・製造使用側の役割を確認。2003 ISO規格全文の確認ではない。'),
('recall2010','経済産業省','リコールハンドブック2010','https://www.meti.go.jp/committee/materials2/downloadfiles/g100525a04j01.pdf','当時版候補URLの直接web取得は失敗。H25全追跡時の社告省略の厳密な細条件を追加照合対象として残す。取得済み全文と扱わない。'),
('medicine_recall','医薬品医療機器総合機構','医薬品等の回収に関する情報','https://www.info.pmda.go.jp/kaisyuu/menu.html?guid=ON','公開検索本文で2012年度以降の医薬品回収を確認。消安法対象除外と薬事制度の回収不存在を混同しない。'),
('food_notice','消費者庁','食品表示関連通知：2009期限・2013アレルギー通知','https://www.caa.go.jp/policies/policy/food_labeling/information/notice/','公式索引で2009期限・2013年9月20日アレルギー通知を確認。当時の全対象品目・各通知本文は未通読。'),
('food_loss2013','消費者庁','食品ロスについて知る・学ぶ','https://www.caa.go.jp/policies/policy/consumer_policy/information/food_loss/education/','検索本文の2013年4月18日公表と期限見直し関連案内を確認。全時点の期限設定方法の逐条照合ではない。'),
('food_expiry','消費者庁','食品の期限表示に関する情報','https://www.caa.go.jp/policies/policy/food_labeling/food_sanitation/expiration_date/','期限の科学的・合理的設定と旧資料へのリンクを確認。2015以降の食品表示基準を2013設問へ遡及しない。'),
('food_roles2007','食品安全委員会','リスク管理機関と食品安全委員会の役割：2007年Q＆A','https://www.fsc.go.jp/fsciis/questionAndAnswer/show/mob07001000005','官庁の公開検索本文で科学的評価と管理行政の独立性を確認。各役割の全原典文言の逐語照合ではない。'),
('ad2016','消費者庁','不実証広告規制の説明：2016年資料','https://www.caa.go.jp/policies/policy/representation/fair_labeling/pdf/fair_labeling_160801_0001.pdf','検索本文の客観性・表示対応・一般的専門家見解・原則15日を確認。20MB PDF直接web取得はサイズ制限で失敗、全冊通読ではない。'),
('ad_overview','消費者庁','表示規制の概要','https://www.caa.go.jp/policies/policy/representation/fair_labeling/representation_regulation/','公開説明で優良誤認・資料要求・不提出の効果を確認。現行7条等の番号を2014原典へそのまま置換しない。'),
('pile2015','国土交通省','基礎ぐい工事問題に関する対策委員会：2015年中間報告','https://www.mlit.go.jp/common/001114887.pdf','2015年12月25日公表ページと公式概要の責任・記録・支持層到達を確認。41頁全事案の通読ではない。'),
('quality2020','経済産業省','2020年ものづくり白書：製造業の企業変革','https://www.meti.go.jp/report/whitepaper/mono/2020/honbun_html/honbun/101031_2.html','検索本文で2017年以降の複数品質不正と部門間連携の課題を確認。2019の全個別事案の調査原報告を代替しない。'),
('ipa_cia','情報処理推進機構','中小企業の情報セキュリティ対策ガイドライン第3.1版','https://www.ipa.go.jp/security/guide/sme/ug65p90000019cbk-att/000055520.pdf','公式検索本文でCIAの資産評価を確認。定義を補足する資料で、2016年の版を確認済みと主張しない。'),
('ipa_mail','情報処理推進機構','組織における標的型攻撃メール訓練：2017年7月31日','https://www.ipa.go.jp/security/anshin/attention/2017/mgdayori20170731.html','2017公式本文の検索収録で報告から対応の体制と訓練目的を確認。送信者名だけで信用しない判断を補足。'),
('products2012','経済産業省','製品安全に関する事業者ハンドブック：2012年','https://www.meti.go.jp/product_safety/producer/jigyouhandbook.pdf','検索本文で重大事故の5類型・30日・10日報告を確認。直接web取得403、全文通読ではない。'),
('oldnine','経済産業省','長期使用製品安全点検制度の見直し：2021年3月','https://www.meti.go.jp/shingikai/shokeishin/seihin_anzen/pdf/018_06_01.pdf','公式資料検索収録で従来9品目と制度の見直しを確認。2017の指定を現行指定へ改変しない。'),
('productflow2013','消費者庁','重大製品事故の公表までのフロー図：2013年3月6日','https://www.caa.go.jp/policies/policy/consumer_safety/centralization_of_accident_information/product_accident_committee/pdf/130306_shiryo3.pdf','検索本文のガス石油機器・製品起因の疑いと直ちに／原則1週間の段階を確認。法定全案件一律期限としない。'),
('products2023','経済産業省','重大製品事故報告制度の事業者用ハンドブック','https://www.meti.go.jp/product_safety/producer/guideline/file/handbook_1.pdf','検索本文の知った日を含む10日を確認。2018当時施行版の府令全文の代用ではない。'),
('workplace2006','厚生労働省','危険性又は有害性等の調査等に関する指針：2006年3月10日','https://www.mhlw.go.jp/web/t_doc?dataId=00tb3050&dataType=1&pageNo=1','取得本文351–408の変更時・平坦歩行の明らかに軽微な例外・疲労、106の治療不要と偶然軽微の区別、271のALARPを確認。全添付図の確認ではない。'),
('human12','中小建設業特別教育協会','ヒューマンファクターとヒューマンエラー：教育本文','https://www.tokubetu.or.jp/text_shokuan/part9/text_shokuan9-1.html','本文199–223の12の発生要因を確認。9割以上の統計母集団はこの資料でも確認していない。'),
('cartagena','農林水産省','カルタヘナ法とは','https://www.maff.go.jp/j/syouan/nouan/carta/about/','公式検索本文の2003公布2004施行と第一種・第二種、生物多様性評価を確認。全生物の承認を保証するものではない。'),
('gmo_food2004','厚生労働省','遺伝子組換え食品Q＆A','https://www.mhlw.go.jp/topics/idenshi/qa/qa.html','旧公式検索本文で食品安全委員会の評価と審査の法的義務化を確認。2024以降の所管変更を2020へ遡及しない。'),
('gmo_standards2000','厚生労働省','組換え食品安全性審査：規格基準告示','https://www.mhlw.go.jp/topics/idenshi/anzen/kokuji.html','告示検索本文の組換え微生物利用食品等の審査公表条件を確認。全例外・手続を網羅した照合ではない。'),
('whistle_oldfaq','消費者庁','民間事業者向けQ＆A：平成29年2月版','https://www.caa.go.jp/policies/policy/consumer_partnerships/whisleblower_protection_system/faq/private','旧制度FAQ検索収録の20日・不正目的を確認。2012/2015施行版全文の対照ではない。'),
('whistle_oldpublic','消費者庁','公益通報者保護法の概要：2020年2月','https://www.caa.go.jp/policies/policy/consumer_system/whisleblower_protection_system/pr/pdf/pr_200221_0001.pdf','2020旧制度公式説明の労働者に公務員を含む記載を確認。改正後版の全条文は別資料と照合対象。'),
('infra2021','国土交通省','インフラ長寿命化計画第2次：2021年6月18日','https://www.mlit.go.jp/report/press/content/001409546.pdf','実際のPDF目次Ⅵの七項目と対象期間、本文の予算管理を確認。Ⅴの現状課題の八項目とは区別。全77頁通読ではない。')]
notes=[];bib=P/'references.bib';s=bib.read_text()
for key,org,title,url,note in refs:
 key='saf53_'+key;assert '{'+key+',' not in s
 esc=lambda v:v.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
 s+='\n@online{'+key+',\n author={{'+esc(org)+'}},\n title={'+esc(title)+'},\n url={'+url+'},\n note={'+esc(note)+'},\n urldate={2026-10-13}\n}\n'
 notes.append({'key':key,'title':title,'url':url,'reading_scope':note,'full_source_read':False})
bib.write_text(s)
(P/'extracted/logs/source_notes_S7_053.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
print('Added',len(spec),'concepts and',len(refs),'references')
