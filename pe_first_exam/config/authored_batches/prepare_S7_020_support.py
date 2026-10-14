# coding: utf-8
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('env_paris','外務省','パリ協定の採択と日本の締結','https://www.mofa.go.jp/mofaj/ila/et/page24_000810.html','2015年12月12日採択、日本について2016年12月8日効力発生を公式本文で確認。原典の2016という年と採択を区別。'),
('env_circular_law','環境省','循環型社会形成推進基本法・条文','https://www.env.go.jp/recycle/low.html','第2条の再使用/再生利用/熱回収、第5〜7条の優先と技術経済・環境負荷の例外を本文確認。'),
('env_circular_outline','環境省','循環型社会形成推進基本法の概要','https://www.env.go.jp/recycle/circul/kihonho/gaiyo.html','公式公開本文で発生抑制から適正処分までの五段階を確認。'),
('env_waste2003','環境省','引越時に発生する廃棄物の取扱いについて（2003年）','https://www.env.go.jp/recycle/waste/hikkoshi/manual.html','本文3.2及び4.1で排出者責任、委託による責任消滅でないこと、管理票で運搬処分の確認を照合。旧法の項番号を現在へ移さない。'),
('env_appliance','経済産業省','家電リサイクル制度FAQ','https://www.meti.go.jp/policy/it_policy/kaden_recycle/faq/faq.html','公式検索本文Q4/Q5で過去販売又は同種買替、指定引取場所を確認。web本文取得失敗と区別。引取条件省略をH28疑義へ保持。'),
('env_appliance2024','経済産業省','家電リサイクル法の制度と対象機器','https://www.meti.go.jp/policy/it_policy/kaden_recycle/','公式公開本文で有機ELを含む現在の4群を確認。2016年の機器一覧へ新制度を逆投影しない。'),
('env_pollution','環境省','環境基準類型指定及び環境管理施策の現行制度について','https://www.env.go.jp/council/content/i_07/900430154.pdf','PDF物理1頁の環境基本法第2条3項抜粋で典型7公害を確認。e-Gov本文は0行で未取得、代用して読了としない。'),
('env_development','環境省','平成4年環境白書：持続可能な開発','https://www.env.go.jp/policy/hakusyo/h04/8265.html','1987年WCED報告と世代間公平、将来能力の保持を本文確認。'),
('env_biodiversity','環境省','平成8年環境白書：生物多様性とは','https://www.env.go.jp/policy/hakusyo/h08/10009.html','冒頭の遺伝子・種・生態系の3階層を本文確認。古い全種数などは教材へ利用しない。'),
('env_foodchain','中国四国環境局','猛禽類ミサゴと食物連鎖による濃縮（2013年）','https://chushikoku.env.go.jp/blog/2013/11/1209.html','公式公開本文の捕食者での蓄積性化学物質の濃度上昇を確認。全物質が同様とはしない。'),
('env_accumulation','環境省','ダイオキシン類挙動モデルハンドブック（平成16年）','https://www.env.go.jp/air/tech/kyodomoderuhandbookH16.pdf','公式公開検索本文で吸収・代謝・排出とBCFの関係を確認。全頁読了ではない。濃縮と毒性を別軸にする。'),
('env_zero2008','環境省掲載・環境人材育成事業報告','企業のゼロエミッションの定義例（2008年）','https://www.env.go.jp/chemi/kagaku/ecointernship/report/2008/symposium/pdf/symposium_murata.pdf','公式掲載の公開表で埋立ゼロ・再資源化99%以上等の対象/基準差を確認。H23の企業数増加という時系列は未確認。'),
('env_offset2008','環境省','G8環境大臣会合等におけるカーボンオフセット（2008年）','https://www.env.go.jp/press/10008.html','削減努力、残余排出認識、他所への削減投資という順と京都クレジットの利用例を確認。排出枠取引の制度自体と区別。'),
('env_neutral2011','環境省','カーボンニュートラル認証基準の公表（2011年）','https://www.env.go.jp/press/14187.html','全量をオフセットするニュートラルと従来のオフセットを本文確認。認証制度の現行運用を主張しない。'),
('env_offset_guideline','環境省','カーボンオフセットの取組に係る指針','https://www.env.go.jp/earth/ondanka/mechanism/carbon_offset/guideline/guideline-info.pdf','公式公開本文の削減困難量の全部又は一部を他所削減/吸収で埋め合わせる定義を確認。'),
('env_kyoto2005','環境省','平成17年環境白書：京都議定書','https://www.env.go.jp/policy/hakusyo/h17/21939.html','CO2/CH4/N2O/HFC/PFC/SF6の当初6種類を本文確認。後年のNF3等を原典へ加えない。'),
('env_sdgs_agenda','国連／外務省仮訳','我々の世界を変革する：2030アジェンダ（2015年）','https://www.mofa.go.jp/mofaj/files/000101402.pdf','前文、段落4/5/20、目標5.4等を確認。物理6頁は能力強化・雇用・リーダーシップ・意思決定。全文を長大転載しない。'),
('env_sdgs_un','United Nations DESA','Transforming our world: the 2030 Agenda','https://sdgs.un.org/2030agenda','原文前文のMDGs残課題・統合不可分・3側面・全stakeholderを確認。'),
('env_sdgs_binding','United Nations','United Nations sustainable development agenda','https://www.un.org/sustainabledevelopment/development-agenda-retired/page/10/','国連公式公開検索本文のnot legally bindingを確認。直接取得403。法的拘束力のある別の条約・国内法まで免除する説明ではない。'),
('env_sdgs2016','外務省','持続可能な開発目標実施指針（2016年決定、2017年冊子）','https://www.mofa.go.jp/mofaj/gaiko/oda/files/000252818.pdf','PDF物理3頁に感染症/開発途上国/環境/17。原典候補3の感梁症という誤植と区別。'),
('env_sdgs_pamphlet','外務省','持続可能な開発目標と日本の取組','https://www.mofa.go.jp/mofaj/gaiko/oda/sdgs/pdf/SDGs_pamphlet.pdf','公開本文で3側面・統合・普遍性を確認。人間の安全保障は別の外務省本文でも確認。'),
('env_humansecurity','外務省','人間の安全保障をめぐる国際潮流','https://www.mofa.go.jp/mofaj/gaiko/oda/bunya/security/index.html','人々を対象とし包括・統合して脆弱な個人へ対応する概念を確認。'),
('env_biosafety_qa','文部科学省',r'遺伝子組換えに関するQ\&A：第二種使用等','https://www.mext.go.jp/a_menu/lifescience/bioethics/mext_02733.html','HTML本文取得44966bytes。問3-7実験衣の質問への回答は付着感染防止の必要措置、3-9動物拡散防止、3-11教育にも法適用、廃棄前不活化を確認。服装をすべての使用に一律の条文要件としない。'),
('env_biosafety_school','文部科学省','高等学校などで遺伝子組換え実験を行う皆様へ','https://www.mext.go.jp/content/20250411-mxt_life-000035635_1.pdf','PDF2頁全本文を確認。2022年6月13日作成、2025年配置URL。P1拡散防止・不活化。2013年時点の制度と新資料の年を分ける。'),
('env_biosafety_law','環境省生物多様性センター','カルタヘナ法関連情報','https://www.biodic.go.jp/bch/bch_2.html','公式公開本文の第一種承認/第二種拡散防止を確認。'),
('env_renewable2022','資源エネルギー庁','エネルギー白書2022：一次エネルギーの動向','https://www.enecho.meti.go.jp/about/whitepaper/2022/html/2-1-3.html','公式公開検索本文で自然界熱、ヒートポンプの仕事による熱移送を確認。web直接取得失敗。2021年の概念の背景に用い性能統計は使わない。'),
('env_hydrogen2015','資源エネルギー庁','エネルギー白書2015：水素社会','https://www.enecho.meti.go.jp/about/whitepaper/2015html/3-8-3.html','公式公開本文で水素を二次エネルギー/輸送媒体と定義。原料・製造による排出は利用時排出と区別。'),
('env_biomass','資源エネルギー庁','バイオマス熱利用','https://www.enecho.meti.go.jp/category/saving_and_new/saiene/renewable/biomass/02.html','公式公開検索本文で発酵メタン利用を確認。直接本文未取得。再生可能性と利用時GHGゼロは同義でない。'),
('env_toprunner2019','資源エネルギー庁','トップランナー制度とLED照明（2019年）','https://www.enecho.meti.go.jp/about/special/johoteikyo/shoene_led.html','公式公開本文で商品化最良性能を基礎とする目標を確認。直接本文未取得。2024の法名は原本通り。'),
('env_planetary','Stockholm Resilience Centre','Planetary boundaries','https://www.stockholmresilience.org/research/planetary-boundaries.html','本文で境界超過は急激/不可逆的変化のリスクを増すが直ちに必ず発生とはしない。最新超過件数は試験解説に使わない。'),
('env_ar5','IPCC','Climate Change 2014: Synthesis Report','https://www.ipcc.ch/site/assets/uploads/2018/02/SYR_AR5_FINAL_full.pdf','公式公開検索本文2.2のall assessed emission scenariosを確認。本文PDF取得失敗。すべての想像可能な未来への普遍量化ではない。'),
('env_rain2017','気象庁','気候変動監視レポート2017 第2章','https://www.data.jma.go.jp/cpdinfo/monitor/2017/pdf/ccmr2017_chap2.pdf','PDF物理9頁の1901〜2017における100/200mm日数増加と1mm日数減少を確認。最新年の観測へ取り替えない。'),
('env_evac2021','内閣府','災害対策基本法改正関連資料（2021年）','https://www.bousai.go.jp/taisaku/hisaisyagyousei/horei_tsuchi/pdf/siryo56.pdf','物理26頁の旧準備/勧告/指示と新高齢者等避難/指示の対照、2021年5月20日から勧告廃止を確認。'),
('env_warning2026','気象庁','2026年5月29日から新たな防災気象情報を運用','https://www.jma.go.jp/jma/press/2604/14b/20260414_taikeiseiri.html','4月14日発表本文で名称に警戒レベル数字を付ける新運用を確認。市町村の避難情報と情報発表の主体を区別。')
]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
d=ROOT/'extracted/reference_checks/S7_020';d.mkdir(parents=True,exist_ok=True)
(d/'mext_qa.html').write_bytes(Path('/private/tmp/s7_020_mext_qa.html').read_bytes())
(d/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],limitations=['直接取得失敗と公式公開検索本文での限定確認を区別。','H23の企業数推移は未確認。H28引取条件、H30濃縮一般化、R03再エネGHG、R06不可逆の強い表現は疑義を保持。','R01再適性14は原典感梁症の誤植と公式全員得点。初回3の判断は保持する。']),ensure_ascii=False,indent=2)+'\n')
new=[('circular_resources','循環資源・再使用再生利用と処理優先','循環型|再使用|再生利用',['apt_2','basic_5_0']),('sdgs_integration','SDGsの普遍性・統合・人間の安全保障','SDG|2030|持続可能',['apt_2']),('carbon_accounting','排出削減・オフセットとニュートラルの境界','カーボン|オフセット|ニュートラル',['apt_2']),('biosafety_containment','組換え生物の拡散防止・第一種第二種使用','カルタヘナ|拡散防止',['apt_2','apt_1']),('renewable_carriers','再生可能資源・熱移送と二次エネルギー','再生可能|水素|空気熱',['apt_2']),('disaster_preparedness','災害リスク情報・避難制度と事前準備','避難|ハザードマップ',['apt_3'])]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
if not all(n[0] in ids for n in new):
 snap=ROOT/'snapshots/config_before_S7_020_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,label,pattern,disc in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pattern,subjects=['APT','BASIC'] if k=='circular_resources' else ['APT'],disciplines=disc))
 old=d['version'];d['version']='1.13-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/'config/concept_change_log_S7.json';log=json.loads(p.read_text());log.append(dict(time=now(),batch='S7_020_environment',previous_version=old,version=d['version'],added=[n[0] for n in new],reason='18原典から環境の広い旧概念を6中心課題に分ける。134概念版を保存。'));p.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
