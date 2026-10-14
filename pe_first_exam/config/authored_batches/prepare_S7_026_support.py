# coding: utf-8
import sys,json,re,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('saf_ra2006','厚生労働省','危険性又は有害性等の調査等に関する指針について（2006年3月10日）','https://www.mhlw.go.jp/web/t_doc?dataId=00tb3050&dataType=1&pageNo=1','公開本文の指針と解説：統括管理/職場参加、実施時期、軽微除外の限定、疲労、非数値化/行列/演算/グラフ、設計工学管理保護具順位、著しい不均衡と重大危害例外、暫定措置、記録を確認。'),
('saf_ra_effects','厚生労働省','リスクアセスメントとは・目的と効果','https://www.mhlw.go.jp/content/11300000/kagaku2-2.pdf','公開3頁の流れ、5効果、守るべき決め事の理由、職場全員参加の感受性を確認。専門家の分析一般の否定とリスト不一致を分ける。'),
('saf_guide51','ISO','ISO/IEC Guide 51:2014: Safety aspects','https://www.iso.org/standard/53940.html','公式メタデータで2014版・2025再確認を確認。本文公開リンクの移転先fetchは403で未読。規格全文照合済みとはしない。'),
('saf_iso31000','ISO','ISO 31000:2018: Risk management Guidelines','https://www.iso.org/standard/65694.html','公式公開説明・検索可視テキストで版2018、目的、特定分析評価対応・監視伝達を確認。規格有料本文全体は未読。'),
('saf_jis31010','日本規格協会','JIS Q 31010:2012 English preview','https://webdesk.jsa.or.jp/preview/pre_jis_q_31010_000_000_2012_e_ed10_i4.pdf','取得PDFの物理1頁画像を目視。対応はIEC/ISO31010:2009、Risk management—Risk assessment techniques。H28前文のISO31000対応と区別。5頁全規格の本文確認ではない。'),
('saf_aeha','家電製品協会','事業者の方へ：安全確保のための表示','https://www.aeha.or.jp/safety/maker/','公開ページで表示指針と危険/警告/注意の区分・第5版2020リンクを確認。ページ送り版は本文未読、2013出題当時の版未照合。'),
('saf_icrp103','ICRP','Publication 103: Free extract','https://www.icrp.org/docs/ICRP_Publication_103-Annals_of_the_ICRP_37%282-4%29-Free_extract.pdf','公開検索の主な変更(e)-(g)で低線量の線形応答を仮定する防護モデルを確認。全勧告の通読ではない。'),
('saf_icrpaedia','ICRP','Fundamental Principles of Radiological Protection','https://www.icrpaedia.org/index.php/Fundamental_Principles_of_Radiological_Protection','公式解説の103第203項の経済社会条件、線量/人数/確率、個人の制約と211項の3曝露状況の最適化を確認。'),
('saf_food2023','厚生労働省','食品中の汚染物質に係る基準値設定のための考え方（2023年12月11日）','https://www.mhlw.go.jp/content/11121000/001177201.pdf','公開3頁を読解。2008年方針とALARA、国内汚染/摂取の検討、国際基準と曝露の検証。2008年原方針全文は取得不能で未読。'),
('saf_fsc_psych','食品安全委員会','食品のリスクコミュニケーションと心理学（2007年1月12日講義資料）','https://www.fsc.go.jp/koukan/kouza190112/kouza190112_siryou2.pdf','該当公開頁の自発性と便益、相互作用、専門家の判断を受入れさせることだけが目的でない、関係者参加・透明性を確認。三乗・1000倍という経験値を普遍則として教材化しない。'),
('saf_fsc_glossary','食品安全委員会','用語集：リスクコミュニケーション','https://www.fsc.go.jp/yougoshu/kensaku_comu.html','公的用語集を確認、認識・意見・情報の交換として扱い、一方的説得や必ず合意する技術とはしない。'),
('saf_parliament2006','House of Lords Economic Affairs Committee','Fifth Report: ALARP and Gross Disproportion（2006）','https://publications.parliament.uk/pa/ld200506/ldselect/ldeconaf/183/18308.htm','第61-64段落で許容不能/条件付き/広く受容の3水準、著しい不均衡の概念と倍率の一律未定義を確認。委員会によるHSEの説明・批評でありHSE規格本文ではない。'),
('saf_welfare','厚生労働省','社会福祉施設の労働災害防止資料：ヒヤリ・ハット活動','https://www.mhlw.go.jp/file/06-Seisakujouhou-11300000-Roudoukijunkyokuanzeneiseibu/0000110463.pdf','ローカル物理8-9/印刷44-45頁画像を目視。1:29:300と報告者を責めない/保護、早期改善、共有を確認。Heinrich原著の同一人330や数千の集計条件までは未確認。'),
('saf_4s','厚生労働省','職場のあんぜんサイト：4S','https://anzeninfo.mhlw.go.jp/yougo/yougo61_1.html','公開本文で整理・整頓・清掃・清潔、しつけを加えて5S、維持する活動を確認。'),
('saf_chem2016','厚生労働省','労働安全衛生法の改正について（ラベル・リスクアセスメント関係）','https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000094015.html','2014公布・2016June1施行、関連政省令/指針の時点を公式メタデータと本文で確認。'),
('saf_chemqa','厚生労働省','化学物質対策に関するQ&A（リスクアセスメント関係）','https://www.mhlw.go.jp/stf/newpage_11389.html','公開該当Q4-1/5-1/6-1等（前コンテキスト）で指定対象、裾切り、業種規模、実施契機、一般消費製品等の適用除外を確認。全物質への無条件義務としない。'),
('saf_healthreport','群馬労働局','健康診断を実施しましょう','https://jsite.mhlw.go.jp/gunma-roudoukyoku/hourei_seido_tetsuzuki/anzen_eisei/anzen17/kenkoushindan.html','公的公開検索/本文で一般健診結果報告は常時50以上、特殊は規模にかかわらずとする範囲を確認。個々の現在の改正規則全条文の通読ではない。')]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t.replace('&',r'\&')+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
new=[('risk_acceptability','安全の許容性・残留リスクと社会条件','許容.*リスク|残留リスク'),
('workplace_risk','職場リスク調査の対象・実施・統括・措置','危険性又は有害性|リスクアセスメント'),
('risk_perception','リスク認識の心理・社会条件','リスク認識|認知バイアス'),
('risk_response','リスク回避・低減・移転・保有と説明','リスク回避|リスク保有'),
('risk_quantification','リスクの見積りモデルと数値化の限界','発生確率|リスクの見積'),
('product_safety_information','製品の警告・使用情報と予見可能な誤使用','警告表示|誤使用'),
('radiological_optimization','ALARAと防護の経済社会的最適化','ALARA|防護の最適化'),
('risk_definition','目的への不確かさと結果・起こりやすさ','不確かさの影響'),
('risk_reduction_hierarchy','設計・防護・管理・情報の優先階層','本質.*設計|優先順位'),
('risk_assessment_cycle','特定・見積り分析・評価・対応と反復','リスク.*プロセス|リスク.*評価'),
('workplace_safety_practices','職場安全の経験比・報告・4S・化学情報','ハインリッヒ|4S|SDS'),
('alarp_reasonableness','ALARPの水準・実行可能性・著しい不均衡','ALARP|キャロット')]
if not all(k in ids for k,_,_ in new):
 snap=ROOT/'snapshots/config_before_S7_026_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APT'],disciplines=['apt_3']))
 d['version']='1.19-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_026'
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.pdf')},limitations=['ISO_Guide51.pdfは136Bの移転案内テキストでPDFではない。移転先ISO fetchは通常/承認済みネットワークとも403。全文を確認した根拠には使わない。','JSA表紙、MHLW物理8-9の計3画像を実目視。規格原文未取得や集計母集団疑義は各問に残す。']),ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
