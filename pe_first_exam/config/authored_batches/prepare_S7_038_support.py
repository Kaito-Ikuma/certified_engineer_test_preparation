# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,digest
refs=[
('employment_power2012','厚生労働省','職場のいじめ・嫌がらせ問題に関する円卓会議WG報告（2012年1月30日）','https://www.mhlw.go.jp/stf/shingi/2r98520000021hkd-att/2r98520000021hlu.pdf','印刷4〜6頁で顧客等の脚注、専門知識を含む優位性、適正指導の除外と六類型を確認。'),
('employment_power_current','厚生労働省','パワーハラスメント防止指針（2026年10月1日適用版）','https://www.mhlw.go.jp/content/11900000/001701369.pdf','物理1〜2頁の三要素、知識への依存、適正な指導の除外を確認。出題時の法条番号へ遡及しない。'),
('employment_sexual_current','厚生労働省','セクシュアルハラスメント防止指針（2026年10月1日適用版）','https://www.mhlw.go.jp/content/11900000/001701366.pdf','物理1〜3頁の二類型、同性、派遣、患者家族等の行為者、措置義務を確認。'),
('employment_sexual2018','厚生労働省','職場におけるハラスメント対策：管理職向け研修テキスト（2018年）','https://www.mhlw.go.jp/content/11900000/000474784.pdf','当時の措置義務と妊婦の業務調整の相談を確認。物理17頁の配慮例は強要と区別。条番号は現在と異なる。'),
('employment_sexual2006','厚生労働省','改正男女雇用機会均等法の施行について（2006年通知、改正反映本文）','https://www.mhlw.go.jp/web/t_doc?dataId=00tb3219&dataType=1&pageNo=1','派遣先を事業主とみなす取扱いの本文を確認。掲載本文は後年の改正を含むため2006年原版と同一とは扱わない。'),
('employment_discretion2014','東京労働局','専門業務型裁量労働制（平成26年3月版）','https://jsite.mhlw.go.jp/tokyo-roudoukyoku/content/contents/000501876.pdf','物理2頁の全19業務、3〜6頁の説明を実画像で確認。技術士業務の列挙なし。H25との版差は査読対象。'),
('employment_discretion_current','厚生労働省','専門業務型裁量労働制とは（現行解説）','https://www.check-roudou.mhlw.go.jp/study/roudousya_tayou_senmon.html','20業務の全列挙、2024年4月の追加、本人同意と撤回の要件を確認。'),
('employment_industrial_physician','東京労働局','総括安全衛生管理者等のあらまし：産業医','https://jsite.mhlw.go.jp/tokyo-roudoukyoku/hourei_seido_tetsuzuki/anzen_eisei/a-kanri.html','産業医節で50人以上の選任、規模別人数と専属の要件を確認。その他の巡視頻度の古い説明は利用しない。'),
('employment_labor_three','東京労働局','東京地方労働審議会（平成25年11月26日）議事録','https://jsite.mhlw.go.jp/tokyo-roudoukyoku/news_topics/kyoku_oshirase/shingikai_gijiroku/shingikai/_120488.html','伝統的な労働三法の三法名を確認。委員の労調法の機能評価は教材へ採用しない。'),
('employment_overtime','厚生労働省','時間外・休日労働と割増賃金','https://www.check-roudou.mhlw.go.jp/study/roudousya_jikangai.html','36協定の締結と届出、対象範囲を確認。現在の上限値をH25へ無条件に遡及しない。'),
('employment_hours2017','長野労働局','労働時間の適正な把握のためのガイドライン（平成29年1月20日）','https://jsite.mhlw.go.jp/nagano-roudoukyoku/hourei_seido_tetsuzuki/roudoukijun_keiyaku/roudoujikan-guideline.html','本文で指揮命令下の時間、命令された学習、客観的記録と把握責務を確認。'),
('employment_manager2008','厚生労働省','労働基準法における管理監督者の範囲','https://www.mhlw.go.jp/bunya/roudoukijun/dl/kanri.pdf','物理4頁で深夜割増と年休の適用、名称だけで決まらない実態を確認。'),
('employment_reform2018','厚生労働省','働き方改革による改正後の労働基準法の施行について（2018年9月7日）','https://www.mhlw.go.jp/web/t_doc?dataId=00tc3655&dataType=1&pageNo=1','冒頭の清算期間1〜3か月への延長、施行日2019年4月1日、残業上限の趣旨を確認。'),
('employment_worklife2010','内閣府仕事と生活の調和推進室','ワーク・ライフ・バランスの実現に向けた三つの心構えと十の実践','https://wwwa.cao.go.jp/wlb/research/kouritsu/pdf/3point10jissen-1.pdf','物理3〜5頁の十項目と会議の目的・到達点を確認。第2版チェックリスト2010年9月発行も確認。強引な意思決定を一般則としない。'),
('employment_maternity_current','厚生労働省','働きながらお母さんになるあなたへ','https://www.mhlw.go.jp/content/11900000/000563060.pdf','物理8頁の産前請求・産後原則と例外、物理3頁の個別母性健康管理措置を確認。現在の給付金等は過去問へ転記しない。'),
('employment_maternity2014','厚生労働省','年金部会資料：産前産後休業の性格（2014年）','https://www.mhlw.go.jp/file/05-Shingikai-12601000-Seisakutoukatsukan-Sanjikanshitsu_Shakaihoshoutantou/0000063777.pdf','物理14〜15頁で雇用形態を問わない産休と請求条件を確認。育休の旧要件や年金の議論は使用しない。'),
('employment_telework2020','厚生労働省','令和2年版厚生労働白書資料編：テレワーク指針概要','https://www.mhlw.go.jp/wp/hakusyo/kousei/19-2/dl/all.pdf','物理178頁（印刷178頁）の平成30年指針概要で勤務場所、時間把握、中抜け、移動中の指揮命令作業を確認。'),
('employment_telework_current','厚生労働省','テレワークの適切な導入及び実施の推進のためのガイドライン','https://www.mhlw.go.jp/content/000759469.pdf','物理10〜13頁で労働時間把握、中抜け、就業場所間の移動、長時間化対策を確認。'),
('employment_paidleave','厚生労働省','年次有給休暇取得促進：事業主の方へ','https://work-holiday.mhlw.go.jp/kyuuka-sokushin/jigyousya.html','年10日付与対象、年5日の取得、本人取得と計画付与の算入、意見聴取を確認。'),
('employment_alternative2008','厚生労働省','改正労働基準法：代替休暇','https://www.mhlw.go.jp/topics/2008/12/dl/tp1216-1l-02.pdf','代替休暇の労使協定・本人意思、引上げ分を換算する説明と数値例を確認。2008年改正の原理のみ使用。')]
p=ROOT/'references.bib';s=p.read_text();added=0
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:
  s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n+'}\n}\n';added+=1
p.write_text(s)
concepts=[('workplace_sexual_harassment','職場のセクハラ・保護対象','セクシャル|セクシュアル'),('workplace_power_harassment','職場のパワハラ・優位性・指導','パワーハラスメント'),('workplace_harassment_judgment','職場のハラスメント判断','ハラスメント'),('labor_discretionary_scope','裁量労働制の対象業務','裁量労働'),('labor_worktime_management','労働時間と管理責務','労働時間'),('worklife_process_improvement','仕事と生活の調和・業務改善','ワーク・ライフ'),('labor_maternity_protection','産前産後休業と母性保護','産前|産後|産休'),('labor_telework_time','テレワークと労働時間','テレワーク'),('labor_reform_provisions','働き方改革の制度対応','働き方改革')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
if not all(k in ids for k,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_038_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APT'],disciplines=['apt_4']))
 d['version']='1.31-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_038'
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=[dict(file=str(f.relative_to(ROOT)),sha256=digest(f)) for f in folder.iterdir() if f.is_file() and f.name!='source_notes.json'],limitations=['H25APT04初回3は誤認で、19業務の原一覧から5に訂正。初回ファイルを変更しない。','旧テレワークPDF000545678はHTTP404。代わりに令和2年白書の指針概要を本文確認。','検索で業務改善資料と表示された0000056246は、取得すると平成25年の保健師育休資料であり主張に対応しない。worklife2014.pdfという暫定保存名の資料は引用に使用せず、内閣府の十の実践を確認した。','2026年10月1日版の法条番号や措置を過去年へ遡及適用しない。過去の全告示改正履歴を完了済みとはしない。','六問は全称・省略条件・初回不一致を部分校正として保持。']),ensure_ascii=False,indent=2)+'\n')
print('Concepts',len(d['concepts']),'references added',added)
