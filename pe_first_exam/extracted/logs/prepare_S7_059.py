# coding: utf-8
"""Manually authored safety/consumer batch. No inference from official keys."""
import json,copy,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
R={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_059_selection.json').read_text())['records']}
I={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_059_initial_independent.json').read_text())['records']}
T=json.loads((P/'config/authored_batches/S7_052_engineering.json').read_text())['questions'][0]
Q=[];Y='条件内で適切';N='不適切';L='条件・時点を留保'
def add(q,title,cid,section,refs,opts,solution,knowledge,ambiguity='',discipline='basic_4_1',conditions=None,figure=False,law=False):
 r=R[q];e=copy.deepcopy(T)
 e.update(question_id=q,source_sha256=r['source_sha256'],stem=title,summary=title,
  conditions=conditions or {'原典':'問題文・否定・全五候補と組合せ表を保存原典18画像で確認。','時点':r['era_year']+'の本文表現を保持。後の制度改正を遡及しない。'},
  choices={str(i):dict(value=v,verdict=z,reason=t) for i,(v,z,t) in enumerate(opts,1)},
  figures='原典組合せ表の各行を独自要約。元画像は転載せず照合用に保存。' if figure else '文章の五肢。元画像は転載せず照合用に保存。',
  ambiguity=ambiguity,evidence=[f"extracted/pages/{r['source_year_directory']}/{Path(r['source_file']).stem}/page_{int(r['source_page']):03d}.png"],
  core_concept=title,required_knowledge=knowledge,solution=solution,answer_reason=solution,
  independent_answer=I[q]['independent_answer'],independent_solution_note='初回JSONと公式比較JSONを保存。'+I[q]['reason']+' 選択情報には公式メタデータも存在し、完全盲検とはしない。',
  learning_points='対象・責任主体・時点・要件を分け、文の否定と「全て」「不要」の範囲を点検する。知識を当てはめる前に何を証明する資料かを確かめる。',
  theory_references=[section],discipline_id=discipline,concept_id=cid,cross_concepts=[],
  classification_reason='原典の主題と全候補を照合：'+title,calculation='false',figure='true' if figure else 'false',law='true' if law else 'false',
  evaluation=dict(knowledge_novelty='2',reasoning_steps='2',calculation_load='0',figure_reading='1' if figure else '0',difficulty='3' if ambiguity else '2',difficulty_reason='定義と制度の時点を照合し、組織的な対応と全称表現を区別する。'),
  citations=refs,foundationality='high',transferability='high')
 if r['source_page_end'] and r['source_page_end']!=r['source_page']:
  e['evidence']=[f"extracted/pages/{r['source_year_directory']}/{Path(r['source_file']).stem}/page_{p:03d}.png" for p in range(int(r['source_page']),int(r['source_page_end'])+1)]
 Q.append(e)
def combo(values,target):
 # Explicit original-table rows; target is independently reasoned, not official.
 return [(v,Y if v==target else N,'各文又は定義の判定を先に行う。'+('全項目が一致する。' if v==target else '並びが判定 '+target+' と異なる。')) for v in values]

def cadd(q,title,cid,section,refs,values,target,solution,knowledge,ambiguity='',discipline='basic_4_1',conditions=None,law=False):
 add(q,title,cid,section,refs,combo(values,target),solution,knowledge,ambiguity,discipline,conditions,True,law)
def countopts(values,target,reason):
 return [(str(v)+'件',Y if v==target else N,reason+(' 集計と一致する。' if v==target else ' 判定を先に行った集計と一致しない。')) for v in values]

def numeric(values,target,reason):
 return [(str(v),Y if i==target else N,reason+(' 計算結果と一致。' if i==target else ' 計算結果に一致しない。')) for i,v in enumerate(values,1)]

def item(q,title,key,d,theory,values,answer,sol,knowledge,conditions,refs=None,ambiguity='',figure=False):
 # Five candidates manually transcribed from images; answer independently saved.
 add(q,title,'env58_'+key,theory,refs or [],numeric(values,answer,'解法の条件と結果を照合する。') if all(isinstance(v,(int,float)) for v in values) else combo(values,values[answer-1]),sol,knowledge,ambiguity,d,conditions,figure)
def detailed(q,title,key,d,theory,opts,sol,knowledge,conditions,refs=None,ambiguity=''):
 add(q,title,'env58_'+key,theory,refs or [],opts,sol,knowledge,ambiguity,d,conditions)

def env(q,title,key,values,a,sol,knowledge,refs=None,ambiguity='',d='basic_5_1',conditions=None,negative=False,reasons=None):
 opts=[]
 for i,v in enumerate(values,1):
  correct=(i==a)
  verdict=('不適切・選択対象' if correct else '条件内で適切') if negative else ('適切・選択対象' if correct else '不適切')
  opts.append((v,verdict,reasons[i-1] if reasons else ('判定と一致する。' if correct else '式・定義・対応の独立判定と一致しない。')))
 add(q,title,'env58_'+key,'theory:env:'+key,refs or [],opts,sol,knowledge,ambiguity,d,
  conditions or {'時点':R[q]['era_year']+'に指定された資料・制度。','照合':'原典18画像で否定・五肢・組合せ表を確認。後年値で置換しない。'},
  figure=any(x in key for x in ['balance','co2','order','history']))

env('H29-REG-BASIC-5-1','LCA・汚染者負担・拡大生産者責任。','principles',
 ['OOOX','XXXO','XOOX','OOXO','OXXX'],1,
 'Aは全過程の影響評価でLCA。Bは汚染の防止・回復費用を汚染者が負担するPPP。Cは廃棄・再利用まで生産者の責任を広げるEPR。Dは税務の処理を会計士が見る説明で、環境監査の定義ではない。OOOXの1。',
 'ライフサイクル、汚染者負担原則、拡大生産者責任、監査。',['env59_epr'],
 conditions={'列順':'A=LCA、B=汚染者負担、C=拡大生産者、D=税務監査。','O/X':'正/誤。'})
env('H29-REG-BASIC-5-2','パリ協定の削減目標は緩和に対応。','paris',
 ['五年ごと削減目標で適応を推進','2℃十分下方と1.5℃努力','情報の専門家レビュー','市場メカニズムの利用','森林減少・劣化抑制の支援'],1,
 '削減目標NDCの五年提出は緩和の取組であり、適応と呼ぶ1が不適切。適応は影響への備え。温度目標、透明性の情報・レビュー、協力的アプローチと市場、森林の吸収・排出抑制は条文の異なる要素を読む。パリ協定本文がJCMという日本の制度名を直接列挙したとの意味にはしない。',
 'NDC、緩和と適応、温度目標、透明性、協力。',['env59_ndc'],negative=True,
 ambiguity='取得UNFCCCはNDC五年と緩和の公式説明。協定2・5・6・13条の本文全体を通して照合する作業は未完了。')
env('H29-REG-BASIC-5-3','標準気体と液体の密度比からLNG体積比。','lng',
 ['1/1200','1/1000','1/800','1/600','1/400'],4,
 '1molのCH4は約16gで、0℃1気圧の体積22.4L。液体では.016/425=3.76×10^-5m³、気体.0224m³で比≈1/595。1/600の4が近い。平成23年度の候補順をそのまま使わない。',
 '理想気体、密度、同質量の体積比較。',d='basic_5_2',conditions={'標準状態':'0℃1気圧、純CH4理想気体。','液体':'425kg/m³一定。'})
env('H29-REG-BASIC-5-4','家庭エネルギーの用途と消費範囲。','home',
 ['給湯が約三割','冷房が暖房の約十倍','電気が約五割','冷蔵庫TV空調はトップランナー','電力約5%が待機'],2,
 '全国総和では冷房の年間消費は暖房より小さく、十倍とする2が不適切。電力だけと全燃料を含む家庭エネルギー、機器の効率と使用時間、総量と待機電力の比率を分ける。トップランナーは将来の効率目標の設定方式で、使用する一台ごとの達成義務と同じではない。',
 '用途別消費、エネルギー種、機器効率、待機。',['env59_energy2019'],d='basic_5_2',negative=True,
 ambiguity='原典「近年」の指定統計年が曖昧で、給湯三割・電気五割・待機五%の全原表は未取得。比率を現行値の普遍定数にはしない。')
env('H29-REG-BASIC-5-5','産業革命の担い手を大学主導へ一般化しない。','industrial',
 ['既存改良の積重ね','欧州大学研究者主導が多い','大工場への機械化','娯楽機構から転用例','児童労働等の社会問題'],2,
 '2が不適切。職人・発明家・企業家の改良と事業化を大学研究者主導へ一括置換できない。機械技術の利用、生産組織、労働制度という別の側面を合わせて整理する。',
 '産業革命、改良と普及、制度と労働。',['env58_steam'],negative=True,d='basic_5_0',
 ambiguity='個別の娯楽機構転用史料は未取得。大学との個別接点も無かったという全称にはしない。')
env('H29-REG-BASIC-5-6','人物の業績とサイクロトロンの発明者。','historydiscover',
 ['Volta電堆','Flemingリゾチームとペニシリン','RöntgenX線','Mendel遺伝法則','Edisonサイクロトロン'],5,
 'サイクロトロンはLawrenceらが開発した加速器で、Edisonという5が不適切。Voltaは定常電流を得る電堆、Flemingはリゾチームとペニシリン、RöntgenはX線、Mendelは形質の遺伝の規則性という対応。発明者名の誤りを、他の正しい加速原理の記述と混ぜて見落とさない。',
 '電池、抗菌物質、放射線、遺伝、加速器。',['env59_lawrence'],negative=True,d='basic_5_0',
 ambiguity='Lawrenceの公式授賞説明を確認。他の四人の全原報は未取得で業績対応は一次史料追加照合を要する。')
env('H30-REG-BASIC-5-1','SDGsの対象は先進国も含む。','sdgs',
 ['2015の2030アジェンダ中核','途上国だけの目標','17ゴール169ターゲット','多様主体の連携','日本2016実施指針'],2,
 'SDGsは普遍的で全ての国を対象とするので、途上国だけへ限定した2が誤り。17と169、環境・経済・社会の統合、各主体のパートナーシップを一組として読む。MDGsと同じ対象範囲へ戻さない。',
 '普遍性、統合、ゴールとターゲット、実施体制。',['env_sdgs_un','env_sdgs2016'],negative=True)
env('H30-REG-BASIC-5-2','環境会計の定義と他手法の誤対応。','accounting',
 ['グリーン購入はバイオマスのみ','環境報告は設備の自治体届出','会計は費用効果を金額物量','環境監査は税務監査','LCAは設備の更新周期'],3,
 '3の費用と効果を貨幣又は物量単位で表す仕組みが環境会計。グリーン購入は必要性と環境負荷全般、環境報告は社会への情報開示、環境監査は環境管理の評価、LCAは全過程の影響評価で、残る肢の限定が違う。',
 '目的・対象・単位による管理手法の区別。',['env58_accounting'])
env('H30-REG-BASIC-5-3','2017年の原油数量と輸入額比。','oil2017',
 ['67/マラッカ/クウェート/12','67/ホルムズ/サウジ/32','87/ホルムズ/サウジ/12','87/マラッカ/クウェート/32','87/ホルムズ/クウェート/12'],3,
 '指定年の中東依存は約87%、主要経路ホルムズ、最大相手サウジアラビア、石油・石油製品の総輸入額比約12%で3。依存度は数量、最後は金額であり、他の化石燃料を含む鉱物性燃料の比率へ拡張しない。',
 '統計年度・品目・数量と金額・経路。',['env59_energy2019'],d='basic_5_2',
 ambiguity='2019白書の公式検索本文で中東約87%を確認。2017財務省暦年の最大輸入先と金額12%の全原表を取得していない。')
env('H30-REG-BASIC-5-4','スマートメーターとHEMSの機能を分ける。','smart',
 ['系統需給のsmartgrid','地域の総合管理community','住宅機器を組み合わせるhouse','メーターが家庭需給を最適制御','smartはかしこい'],4,
 '家庭内の機器を管理・制御する説明はHEMSに対応。スマートメーターは通信機能を持つ電力量計であり、同じ装置として家庭全体の最適制御を定義した4が不適切。計測情報は管理システムの入力に使えるが、計測と制御の主体を分ける。',
 '計測、通信、家庭管理、地域と系統の範囲。',['env59_smart'],negative=True,d='basic_5_2')
env('H30-REG-BASIC-5-5','動力・通信・化学・核の技術成果の順。','historyorder',
 ['ウエオイア','ウオアエイ','オウエアイ','オエウイア','アオウエイ'],3,
 'Wattの改良が18世紀後半、Bellの電話1876、Hertzの電磁波実験1880年代、Haberのアンモニア合成基礎1909頃、Hahnらの核分裂1938。オ→ウ→エ→ア→イの3。Haberの基礎とBoschによる大規模工業化、核分裂発見と発電開始を分ける。',
 '科学的確認、技術発明、工業化の段階。',['env58_steam'],d='basic_5_0',
 ambiguity='五項目の初出全原報は未取得。HaberとHahnの単独人物表記は共同の貢献の全体を示すとはしない。')
env('H30-REG-BASIC-5-6','倫理責任は明文化の有無だけでは決まらない。','ethics',
 ['専門家は高い基準','職業で規範相違','力量超え仕事を引受けない','規範は変わる','規定なしなら責任なし'],5,
 '明文規定がなくても専門職の公益・安全・説明に関する責任は残るので5。力量の範囲を見極め、能力ある者との協働や引継ぎで適切に業務を処理する。',
 '公益、力量、責任、明文と倫理。',['ipej_ethics2011'],d='basic_5_0',negative=True)
env('R01-REG-BASIC-5-1','工業型から都市型の汚染と二次生成。','airhistory',
 ['SOx/Ox/SPM/CO2','NOx/Ox/CO2/SPM','SOx/NOx/SPM/Ox','NOx/SOx/CO2/Ox','SOx/NOx/SPM/CO2'],3,
 '工業地域の燃料硫黄によるSOx、自動車のNOxとSPM、NOxと炭化水素の光反応から生じる光化学オキシダント。SOx/NOx/SPM/Oxの3。最後の二次生成物をCO2とすると前駆物質と日射の条件に対応しない。',
 '発生源、硫黄酸化物、粒子、光化学反応。',['env58_pm25'],d='basic_5_4')
env('R01-REG-BASIC-5-2','排出原因を減らす緩和と影響への適応。','lca',
 ['JCMは貢献定量化と目標活用','適応は原因のガス排出削減','CFP全過程CO2換算','LCA全段階影響評価','環境基準は望ましい状態'],2,
 '原因の削減を適応と呼ぶ2が誤り。排出削減・吸収は緩和で、影響の被害回避が適応。CFPとLCA、環境基準の定義は対象量と境界を固定して判定する。JCMは削減・吸収への貢献を定量化する枠組みで、効果の無条件な認定ではない。',
 '緩和適応、LCA、CFP、JCM、環境基準。',['env59_ndc','env58_pmstandard'],negative=True,
 ambiguity='JCMの2019運用ルール全文とCFP規格は追加照合。')
env('R01-REG-BASIC-5-3','2015策定の2030比率で燃料名を点検。','energymix2015',
 ['原子力20–22','再エネ22–24','石油25–27','2013より最終消費減','自給率25程度と準国産'],3,
 '25–27%はLNG火力の目標であり、石油火力は約3%。燃料名の誤りの3を選ぶ。策定時点の他の比率・省エネ・自給率を保持し、後年の目標改訂値へ置換しない。',
 '策定年・目標年・実績と見通し・電源分類。',['env58_mix2015'],negative=True,d='basic_5_2',
 ambiguity='2015の7月最終PDF全図表をまだ取得していない。原典と公開骨子に基づく初稿として追加照合。')
env('R01-REG-BASIC-5-4','非エネルギー利用を除いた炭素量からCO2へ。','nationalco2',
 ['100Mt','300Mt','500Mt','1100Mt','1600Mt'],4,
 '石油は燃焼に使わない1600PJを引いて6231PJ。炭素排出は[5044×24+6231×19+4696×14]×1000=305189000t-C。PJ→TJの1000倍を忘れない。CO2は44/12倍で約1119Mt-CO2なので1100の4。炭素換算値305Mtをそのまま選ばない。',
 'システム境界、非エネルギー利用、PJ/TJ、分子量換算。',d='basic_5_2',
 conditions={'燃料PJ':'石炭5044、石油7831、天然ガス都市ガス4696。','非燃焼石油':'約1600PJ。','係数t-C/TJ':'石炭24、石油19、ガス14。','換算':'C12、CO2 44、PJ=1000TJ。'})
env('R01-REG-BASIC-5-5','応用が科学的発見より先行する例。','technologysequence',
 ['核分裂後に原子力発電','ウイルス発見後に種痘','望遠鏡後に土星環確認','量子力学後にトランジスタ','電磁波確認後にレーダー'],2,
 'Jennerの種痘は1796頃で、ウイルスの発見・概念形成は19世紀末。従って発見を種痘の前とした2が逆。実用的な方法が機序の科学的解明より先行する例であり、科学→技術の一方向の順序だけでは歴史を説明できない。',
 '経験的技術、機序解明、観測装置、時間順。',['env59_jenner'],negative=True,d='basic_5_0',
 ambiguity='他の四組の初出原報・開発年を全て取得したわけではない。土星の環は観測と環構造の解釈を分ける。')
env('R01-REG-BASIC-5-6','特許と基本法の定義、国の責務。','ip',
 ['発明は自然法則利用高度思想','特許保護利用と産業','知財には商標商号も','基本法は創造保護活用','国は施策責務なし'],5,
 '知的財産基本法は国の施策策定・実施責務を定めるので、無しとする5が誤り。発明の定義と知財全体の定義を区別し、商標や商号は特許発明の要件で排除しない。',
 '特許法1・2条、基本法2・5条、対象の広さ。',['ip_patent_statute','ip_broad_scope'],negative=True,d='basic_5_6')
env('R01-RET-BASIC-5-1','緩和・適応とEco-DRRの共便益。','ecodrr',
 ['緩和/適応/生態系/生物多様性','削減/対応/生態系/地域資源','緩和/適応/地域人材/地域資源','緩和/対応/生態系/生物多様性','削減/対応/地域人材/地域資源'],1,
 '排出原因を減らす緩和、避けられない影響に備える適応。湿原の遊水や森林の保全機能を使うEco-DRRは生態系を活用する減災で、生物多様性保全も共便益となる。四語を合わせる1。人材が不要という意味ではなく、略称が指す手法の核心を読む。',
 '緩和適応、地域特性、生態系の機能、共便益。',['env59_ecodrr'])
env('R01-RET-BASIC-5-2','家電小売の役割と循環制度の限定。','recyclelaw',
 ['家電小売の引取と製造者への引渡し','再利用ならバーゼル規制なし','容器三品目を販売者全費用','全工事の発注者に分別実施','基本法は再生最優先'],1,
 '1が家電小売の役割。再利用の有害廃棄物取引も規制対象となり得る。容器包装は三品目・販売者全費用ではなく、建設には対象条件と実施主体、循環の優先順には発生抑制がある。',
 '役割、対象と例外、優先順位、国境移動。',['env_circular_law','env_appliance'],d='basic_5_6',
 ambiguity='出題時バーゼル・建設の法令履歴と規模条件全文は追加照合。')
env('R01-RET-BASIC-5-3','LNG・原油・一般炭・絶乾材の質量発熱量。','heating',
 ['A>B>C>D','B>A>D>C','C>A>B>D','C>B>D>A','D>C>B>A'],3,
 '指定表の単位質量ではLNG、原油、輸入一般炭、絶乾廃材の順で3。平成24年度は気化ガスと原料炭という異なる指定なので同じ数値を転用しない。ここでも体積単位は密度換算が必要。',
 '燃料指定、乾燥状態、熱量単位と密度換算。',['env58_heating'],d='basic_5_2',
 ambiguity='指定時版の標準発熱量の全四値は未取得。後年改訂表を指定時表の代替確定にはしない。')
env('R01-RET-BASIC-5-4','一次供給の再エネ比率を境界に合わせる。','primaryshare',
 ['44%','22%','11%','2%','0.5%'],3,
 '2017指定統計と通常試験で与えた内訳を使うと、水力710+水力除く再エネ938+未活用596=2244PJ。全20095PJで割ると11.17%で3。これは一次エネルギー供給比であり発電量構成ではない。問題が指定する未活用を含む境界を保持する。',
 '一次供給、発電比との違い、境界、合計と百分率。',d='basic_5_2',
 ambiguity='再試験の本文には内訳がないため通常試験の2017内訳を補助として使った。総合エネルギー統計指定版の原表は追加取得。')
env('R01-RET-BASIC-5-5','同じ年表でも元の選択順へ戻す。','historyorder',
 ['アイエウオ','エアイウオ','アエオイウ','エアイオウ','アイエオウ'],4,
 'Halleyの周期性同定が18世紀初頭、Watt18世紀後半、Darwin–Wallace1858、Einstein1915、Fukui1952。エ→ア→イ→オ→ウの4。平成25年度の同型問題の正答1を番号だけ転用しない。',
 '初出の段階、時代順、候補の並べ替え。',['env58_steam'],d='basic_5_0',
 ambiguity='初出史料の全五項目照合は未完了。原典の彗星「発見」は周期性の同定として留保。')
env('R01-RET-BASIC-5-6','評価リスクと知覚リスクの隔たり。','risk',
 ['科学評価と費用技術を含む管理','情報と意見の相互交換','評価と知覚に隔たりなし','規制科学が信頼性と波及評価','規制と合意形成を支援'],3,
 '科学的評価と人の知覚は、経験・信頼・自発性・公平性等により隔たり得る。隔たりがないという3が誤り。相互の情報・意見交換によって理解し、評価の不確実性と管理の価値判断も説明する。レギュラトリーサイエンスは科学的根拠を政策等の判断へつなぐが、科学だけで価値判断を消すものではない。',
 'リスク評価・管理・対話、知覚、根拠と社会判断。',['eth54_riskcomm'],negative=True)
env('R02-REG-BASIC-5-1','海洋プラスチックの定義・流出・循環。','plastics',
 ['OOXOX','OXXOO','OOOXX','XXOOO','XOXXO'],2,
 '原典の主題判定はア正（概ね5mm以下）、イ誤（先進国だけ又は特に先進国由来へ一般化）、ウ誤（海外再生が半数以下という2017説明が違う）、エ正（3R+Renewable）、オ正（陸域の投棄や河川流出への対策）でOXXOOの2。ただし戦略の策定日は政府資料では2019年5月31日で、原典エの「6月」と一致しない。公式2を保持し、内容の判定と日付の疑義を分ける。',
 '粒径、陸域流出、資源循環、代替資源、日付。',['env59_plastic'],d='basic_5_1',
 ambiguity='原典の2019年6月は政府発表5月31日と相違。厳密に日付も判定すると想定組合せが崩れるためAstra重点査読。2017国内排出・海外再生の全原表も追加照合。')
env('R02-REG-BASIC-5-2','生物多様性保全と外来種防除。','biodiversity',
 ['組換え生物の国際枠組','外来種が在来種に影響','駆除は動物愛護で禁止','1992署名開放1993発効','保全持続利用利益配分'],3,
 '3の一律駆除禁止が不適切。防除制度と扱いへの配慮を併せて考える。CBDの三目的とCartagenaの組換え生物の扱いは対象が異なり、Nagoyaの利益配分とも区別する。',
 '条約と議定書、外来種、防除、倫理配慮。',negative=True,
 ambiguity='出題時の防除条項とCBD全三目的の原条文照合は追加確認。')
env('R02-REG-BASIC-5-3','部門別エネルギーの歴史的推移。','energytrends',
 ['最終消費2005ピーク後減','産業業務全体は省エネで同程度','GDP当たり日本は世界平均未満','家庭は震災後も継続増加','旅客2002ピーク後燃費等で減'],4,
 '家庭は省エネ機器・節電・世帯人員・気温等の影響で、震災後に継続増加したという4が誤り。2019統計の要因分解にも年ごとの増減があり、一様な増加ではない。総量、原単位、世帯数、産業部門の個別と合計を分ける。',
 '時系列、部門、GDP原単位、複数要因。',['env59_energy2019'],negative=True,d='basic_5_2',
 ambiguity='原典が参照する版のピーク年2005・2002と全五グラフの原表は未取得。後年の統計遡及改訂と区別して追加照合。')
env('R02-REG-BASIC-5-4','2010原子力比と複合サイクル・シェール。','energy2010',
 ['30/コンバインド/シェール','20/コンバインド/シェール','20/再熱再生/シェール','30/コンバインド/タイトサンド','30/再熱再生/タイトサンド'],1,
 '2010一般電気事業用原子力約30%、ガスタービンと排熱蒸気のコンバインド、米国非在来型シェールで1。原子力の指定時点と、輸出への期待から実際のLNG輸入へ変わった本文の時点を別々に読む。',
 '歴史的電源比、複合サイクル、ガスの供給。',d='basic_5_2',
 ambiguity='2010の指定分母の原表と米国由来輸入の開始資料は未取得。H24と同じ番号でないことを確認済み。')
env('R02-REG-BASIC-5-5','戦前技術史の曖昧な比較と公式複数正答。','japanindustrial',
 ['江戸手工業が西洋技術と発展','標準化技術を輸入し低賃金競争','学協会は欧米と異なり高学歴出身者','Taylorと同時に統計的品質管理導入','技術官僚の地位向上運動'],4,
 '独立の主な判断は4。日本で統計的品質管理が組織的に普及した節目は日科技連による1950のDeming講義等の戦後であり、戦前のTaylor導入と同時に普及したというまとめは不適切。ただし戦前の個別統計手法の利用まで無かったとはしない。公式は誤解を招く記述があったとして当初4に加え3も正答とした。3の「欧米とは異なり」という一般化は学協会の時期・構成の違いを落とす。独立解4、受理正答3と4をそれぞれ残す。',
 '技術移転、学協会史、科学的管理と品質管理、公式訂正。',['env59_juse'],d='basic_5_0',negative=True,
 ambiguity='公式の複数受理4|3を保持。独立解4は受理対象だが全受理集合を独立に列挙したものではない。3の欧米との差という一般化、戦前統計利用の個別例を追加史料で査読。')
env('R02-REG-BASIC-5-6','種痘・周期律・新元素・電子素子の順。','historyorder',
 ['イエアオウ','イエオウア','イオエアウ','エイオアウ','エオイアウ'],1,
 'Jenner1796、Mendeleev1869、Curie夫妻1898、De Forest三極管1906頃、トランジスタ1947。イ→エ→ア→オ→ウの1。観測された事実、法則化、装置の発明を同じ授賞年へまとめない。',
 '医療経験、元素周期、電子管から半導体。',['env59_jenner','env58_curie'],d='basic_5_0',
 ambiguity='全初出史料の取得は未了。電子管・トランジスタの共同貢献と特許の段階は追加照合。')

new={'principles','paris','home','historydiscover','sdgs','oil2017','smart','airhistory','nationalco2','technologysequence','ecodrr','primaryshare','risk','plastics','energytrends','japanindustrial'}
assert len(Q)==30 and set(R)=={e['question_id'] for e in Q}
for e in Q:
 key=e['concept_id'].split('_',1)[1]
 if key in new:e['concept_id']='env59_'+key
 e['learning_points']=e['required_knowledge']+' 集計対象・時点・法の主体・選択方向を固定し、同型でも元の五肢へ戻す。'
 e['law']='true' if key in ['paris','sdgs','ip','recyclelaw','biodiversity'] else 'false'
 e['calculation']='true' if key in ['lng','nationalco2','primaryshare'] else 'false'
 e['evaluation'].update(calculation_load='2' if e['calculation']=='true' else '0',difficulty_reason='原典時点・定義・集計境界・全称表現・特殊正答を確認する。')
out=P/'config/authored_batches/S7_059_environment_finish_middle.json';assert not out.exists()
out.write_text(json.dumps({'batch_id':'S7_059_environment_finish_middle','reference_date':'2026-10-14','questions':Q},ensure_ascii=False,indent=2));print('Prepared',len(Q),'partial',sum(bool(e['ambiguity']) for e in Q))
