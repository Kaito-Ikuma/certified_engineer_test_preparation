# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,json_bytes,digest
refs=[
('scj_code2006','日本学術会議','科学者の行動規範（2006年声明）','https://www.scj.go.jp/ja/info/kohyo/pdf/kohyo-20-s3.pdf','取得PDFの印刷3--4頁、正直・相互評価・中立説明・改ざん禁止・利益相反を確認。2013年版とは区別。'),
('privacy_general','個人情報保護委員会','個人情報保護法ガイドライン（通則編）','https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/','定義・本人同意・政令第1条の七生体特徴の該当箇所を確認。現行条番号を2011--2021年へ遡及しない。'),
('privacy_consent2017','個人情報保護委員会','2017年2月10日資料3-2：個人情報保護法Q&A','https://www.ppc.go.jp/files/pdf/290210_siryou3-2.pdf','検索収録Q1-57の黙示同意は個別具体判断という説明を確認。カード照会の個別事例の直接資料ではない。'),
('privacy_consent_current','個人情報保護委員会','本人の同意：Q1-61','https://www.ppc.go.jp/all_faq_index/faq1-q1-61/','公開短文全文を確認。明示に限られず黙示同意は個別具体の判断である。調査依頼だけで第三者提供への同意を推定しない。'),
('privacy_delivery','個人情報保護委員会','個人情報保護法ガイドラインQ&A','https://www.ppc.go.jp/personalinfo/faq/APPI_QA/','Q7-34--35の宛名情報の委託と封入物の中身の取扱いの違いを確認。安全管理義務は残る。現行資料で当時版全文照合の代わりとはしない。'),
('privacy_small2017','高知県','全ての事業者が個人情報保護法の適用対象となりました','https://www.pref.kochi.lg.jp/doc/2017090700114/','2017年9月21日告知本文を確認。2017年5月30日施行で5000人以下の適用除外を廃止。旧制度の複数DB計数の全文までは確認していない。'),
('privacy_evacuation2013','内閣府','災害時要援護者対策','https://www.bousai.go.jp/taisaku/hisaisyagyousei/youengosya/','2013年改正と2013年8月指針の成立を確認。名簿作成と提供を分離。'),
('privacy_evacuation_scope','内閣府','避難行動要支援者名簿の制度（概要）','https://www.bousai.go.jp/taisaku/hisaisyagyousei/pdf/sanko2-02.pdf','検索収録の発災又は発生のおそれと必要範囲、平時同意原則を確認。2020年度の集計を2014年の値として採用しない。'),
('export_overview','経済産業省','安全保障貿易管理の概要','https://www.meti.go.jp/policy/anpo/gaiyou.html','官庁の制度目的と外為法に基づく管理を確認。現在ページを旧法の仕様そのものへ置換しない。'),
('export_cases','経済産業省','大学・研究機関向けヒヤリハット事例集','https://www.meti.go.jp/policy/anpo/daigaku/jireishu.pdf','検索収録19頁のロボット内蔵センサーの部分品特例と学内部署の確認を読んだ。PDF直接取得は403、全文読了ではない。'),
('export_scope2022','経済産業省','外為法に基づく安全保障貿易管理の対象範囲','https://www.meti.go.jp/policy/anpo/law_document/minashi/meikakukanitsuite.pdf','検索収録の外国為替令17条と公知・基礎科学例外を確認。直接取得403。2022年明確化の資料を2021年の規則へ遡及しない。'),
('export_current_updates','経済産業省','安全保障貿易管理','https://www.meti.go.jp/policy/anpo/index.html','2025年10月9日施行の補完的規制見直しの案内を確認。旧問題の対象地域や条件へ現行版を補わない。'),
('ai_use2019','総務省','AI利活用ガイドライン（2019年）','https://www.soumu.go.jp/main_content/000637097.pdf','取得PDF印刷5--6・9--10頁の対象者・十原則・目的文脈に応じた選定・ソフトローを確認。透明性は全ソース公開義務ではない。'),
('ai_society2017','内閣府','人工知能と人間社会に関する懇談会報告書','https://www8.cao.go.jp/cstp/tyousakai/ai/summary/aisociety_jp.pdf','取得PDF印刷11・13--15・17--18頁を実画像で確認。六論点、感情誘導、価値多様性、個人情報と萎縮、技術デバイドを確認。文字層の化けを画像で補った。'),
('mext_ai_whitepaper2024','文部科学省','令和6年版白書：AIがもたらす科学技術・イノベーションの変革','https://www.mext.go.jp/b_menu/hakusho/html/hpaa202401/1421221_00002.html','HTMLの対象本文を確認。知識集約・高付加価値化・医療・対話型の四空欄に対応する。2024年記述を現在の予測へ拡張しない。'),
('jaist_knowledge','梅本 勝博 and 妹尾 大','酒造りとナレッジ・マネジメント','https://www.jaist.ac.jp/ks/labs/umemoto/sake_km.html','大学研究室の著者による本文2--3節を確認。暗黙知と形式知・SECIの相互作用の説明。'),
('iso27000_2009','ISO','ISO/IEC 27000:2009 公開書誌と概要','https://www.iso.org/standard/41933.html','初版2009年5月という公開書誌を確認。規格全条項は未取得。現在の公開書誌は27000:2026後継版を案内する。'),
('singapore2010','World Conference on Research Integrity','研究公正に関するシンガポール宣言（JSPS公開訳）','https://www.jsps.go.jp/file/storage/general/j-kousei/data/singapore_statement_JP.pdf','2頁の4原則と責任を確認。説明責任・守秘・利益相反開示を含む。規制法令ではない。')]
p=ROOT/'references.bib';s=p.read_text()
for k,a,t,u,n in refs:
 assert '@online{'+k+',' not in s
 a=a if ' and ' in a else '{'+a+'}'
 s+='\n@online{'+k+',\n author={'+a+'},\n title={'+t.replace('&',r'\&')+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n.replace('&',r'\&')+'}\n}\n'
p.write_text(s)
concepts=[('privacy_information_scope','個人情報の定義・公開と識別','個人情報','apt_1'),('privacy_consent_purpose','本人同意・第三者提供・利用目的','同意|第三者','apt_1'),('privacy_biometric_codes','身体特徴の個人識別符号','個人識別符号','apt_1'),('security_cia_management','CIA三要素と方針・管理体系','情報セキュリティ','apt_1'),('knowledge_tacit_explicit','暗黙知・形式知の変換','ナレッジ','apt_1'),('export_control_screening','安全保障貿易の該非・取引・出荷審査','輸出管理','apt_4'),('ai_use_principles','AI利活用の十原則','AI.*原則','manual_80'),('ai_social_transformation','AIの社会的論点と知識集約社会','AI|人工知能','manual_80')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']};snap=ROOT/'snapshots/config_before_S7_043_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
for k,t,pat,disc in concepts:
 assert k not in ids
 d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APT'],disciplines=[disc]))
d['version']='1.36-S7-concept-additions';p.write_bytes(json_bytes(d))
(ROOT/'extracted/reference_checks/S7_043/source_notes.json').write_bytes(json_bytes(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_sources=[dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in (ROOT/'extracted/reference_checks/S7_043').glob('*.pdf')],limitations=['出題当時の法令版は全条項照合済みではない。','R03APT14初回2と公式5の相違は黙示同意の条件として査読対象へ残す。','特許必要最小限例外は当時条文直接未確認。'])) )
print('concepts',len(d['concepts']),'refs',len(refs))
