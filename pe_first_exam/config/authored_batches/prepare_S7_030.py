# coding: utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')}
initial={r['question_id']:r for r in json.loads((ROOT/'config/authored_batches/S7_030_independent_answers.json').read_text())['questions']}
items=[]
def add(q,summary,values,reasons,solution,concept,labels,knowledge,ambiguity='',calculation=False,figure=False,cites=None):
 r=by[q];a=int(initial[q]['independent_answer']);assert len(values)==len(reasons)==5
 negative=q=='R04-REG-BASIC-1-2'
 items.append(dict(question_id=q,source_sha256=r['source_sha256'],stem=summary,summary=summary,
 conditions={'判断方向':'不適切な記述を選ぶ' if negative else '最も適切な記述又は組合せを選ぶ','原典照合':'14原典画像で16問の条件、数値、単位、表の列と全5候補を確認。','モデル':'独立性、正規性、一定発生率などの前提を個別に保持する。'},
 choices={str(i):dict(value=v,verdict=('不適切' if i==a else '条件を含めて検討') if negative else ('適切' if i==a else '不適切'),reason=w) for i,(v,w) in enumerate(zip(values,reasons),1)},
 figures='品質表・確率表・組合せ表を原典画像と照合。図表は独自の要約と計算へ変換する。',
 ambiguity=ambiguity,evidence=[initial[q]['source_image']],core_concept=summary,required_knowledge=knowledge,solution=solution,answer_reason=solution,
 independent_answer=initial[q]['independent_answer'],independent_solution_note='14原典画像の確認後、公式参照前の16解答を保存。'+initial[q]['reason']+'公式照合後も初回記録は保存する。',
 learning_points='変数の意味と単位を先に定め、平均・分散・確率・判定を順に分ける。品質の要求、工程の監視、ロットの受入れを区別し、成立条件のない一般化を避ける。',
 theory_references=labels,discipline_id=r['discipline_id'],concept_id=concept,cross_concepts=[],
 classification_reason='原典で品質保証、品質表、抜取検査、確率分布、統計推論を照合。既存の設計・計画及び技術に関する分類を維持し、共有する概念を追加する。',
 calculation=str(calculation).lower(),figure=str(figure).lower(),law='false',
 evaluation=dict(knowledge_novelty='2',reasoning_steps='2',calculation_load='2' if calculation else '0',figure_reading='2' if figure else '0',difficulty='3' if ambiguity or calculation else '2',difficulty_reason='数学自体は既知として扱う。品質の判断対象、組合せ表、モデル仮定を追加理解する負荷を別に評価する。'),
 citations=cites or ['stat_nist_normal','stat_psu_linear'],foundationality='high',transferability='high'))

add('H23-REG-BASIC-5-4','独立な製品質量の標本平均と総質量について、平均と標準偏差を求める。',
 ['平均20・偏差4・合計400・偏差10','平均80・偏差4・合計800・偏差7','平均80・偏差2・合計800・偏差10','平均20・偏差2・合計400・偏差7','平均80・偏差2・合計800・偏差7'],
 ['Aの標本平均の期待値は80gであり、標本数で平均を割らない。総質量の期待値も800gである。','平均の偏差は4gではなく2gである。合計の偏差も標準偏差をそのまま足した7gではなく10gである。','Aの4個平均の偏差は4/2=2g、合計の分散は4×16+4×9=100g²なので10gである。','平均と総質量の期待値がともに違い、合計の偏差も違う。','平均部分は合うが、合計の標準偏差は7gではない。独立成分の分散を足して最後に平方根を取る。'],
 r'各質量を独立正規変数とする。Aの標本平均は \(\bar A=(A_1+\cdots+A_4)/4\) で、期待値80g、分散 \(4(4^2)/4^2=4\,\mathrm{g^2}\) である。総質量は \(T=\sum_{i=1}^4A_i+\sum_{i=1}^4B_i\) なので期待値 \(4(80)+4(120)=800\,\mathrm g\)、分散 \(4(4^2)+4(3^2)=100\,\mathrm{g^2}\) となる。標準偏差はそれぞれ2gと10gで、3を選ぶ。平均を取る操作と、四つの値を合計する操作を混同しない。',
 'quality_normal_combinations',['theory:quality:variance','theory:quality:normal','theory:quality:sample_mean'],'独立変数の線形結合、平均の線形性、分散への係数の二乗、正規分布の閉性。',calculation=True,figure=True)

add('H24-REG-BASIC-1-3','要求品質の重みと対応の強さから、品質要素の重要度を積和で求める。',
 ['A>C>D','A>D>C','C>A>D','C>D>A','D>A>C'],
 ['C=53でA=49を上回るため、Aを先に置く順序は合わない。','Cは三要素のうち最大であり、最後に置けない。','重み付き合計はC=53、A=49、D=46なのでこの順序となる。','A=49はD=46より大きく、後二要素の順が逆である。','D=46は最小であり、最初にはならない。'],
 r'対応の強さを原典どおり◎5、○3、△1とし、空欄は加点しない。要求の重みは行順に5,5,4,3,4,3である。Aは \(5\cdot5+4\cdot3+4\cdot3=49\)、Cは \(5\cdot3+4\cdot5+3\cdot5+3\cdot1=53\)、Dは \(5\cdot5+4\cdot3+3\cdot3=46\) であり、3を選ぶ。各列に関係のある要求の重要度を反映する計算である。係数を一般的な別の尺度へ勝手に置き換えない。図中のBとEは今回の大小比較の対象ではない。',
 'quality_qfd',['theory:quality:qfd'],'要求品質と設計特性、対応行列、重要度の積和、問題固有の対応尺度。',calculation=True,figure=True,cites=['quality_qfd_scale'])

add('H24-REG-BASIC-5-4','最終検査と上流の品質保証を分け、プロセスの標準化と改善の関係を読む。',
 ['検査・三現管理・基準化・プロセス','検査・源流管理・標準化・プロセス','検査・三現管理・基準化・アウトカム','評価・源流管理・標準化・アウトカム','評価・三現管理・標準化・プロセス'],
 ['現場・現物・現実という三現の確認と、上流で不適合原因を抑える源流管理は同じ説明ではない。','要求適合を判定する検査、上流からの源流管理、方法を定める標準化、プロセスを管理する流れでつながる。','三現管理・基準化の対応に加え、ここで管理する対象は一連のプロセスである。','評価は広い概念だが本問の要求適合判定は検査である。末尾も成果だけを意味するアウトカムではなくプロセスである。','要求適合判定と上流の改善に対応する語が検査・源流管理になっていない。'],
 '完成品を検査して不適合品を隔離することと、不適合を生む工程を上流から改善することを分ける。設問の文脈ではアが検査、イが源流管理、ウが標準化、エがプロセスであり2となる。標準を設定して実施し、結果を確認して更新する循環が品質保証を支える。標準化は永久に方法を固定することではなく、改善結果を次の標準へ反映することを含む。',
 'quality_process_assurance',['theory:quality:assurance','theory:quality:pdca'],'検査と予防、上流工程、標準化、PDCA、プロセスと成果。',cites=['quality_process_jsqc','quality_iso_process'])

add('H25-REG-BASIC-1-6','工程能力指数、回帰分析、管理図、ヒストグラムを目的で区別する。',
 ['標準偏差・主成分分析・管理図・ヒストグラム','標準偏差・回帰分析・工程図・散布図','工程能力指数・回帰分析・管理図・ヒストグラム','工程能力指数・主成分分析・工程図・ヒストグラム','工程能力指数・回帰分析・工程図・散布図'],
 ['公差を工程のばらつき幅で割る値は標準偏差そのものではない。主成分分析も指定された応答モデルの評価と違う。','アの比は無次元の工程能力指数であり、異常監視は管理図、区間内度数の表示はヒストグラムである。','公差と工程能力の比、応答への説明変数のモデル、時間変動の監視、区間度数の図がそれぞれ対応する。','主成分分析は変数を合成して次元を減らす方法で、工程図も時間変動の統計監視とは異なる。','工程図は手順を示し、散布図は二変数の関係を示す。ここで求める監視と一変数の度数分布に対応しない。'],
 r'公差幅を工程のばらつき幅で規格化する値は工程能力指数である。正規かつ安定な工程の両側規格では \(C_p=(U-L)/(6\sigma)\) と表せる。応答変数と説明変数のモデルは回帰分析、工程の時間変動は管理図、測定値を区間に分け度数に比例する面積を並べる図はヒストグラムなので3である。管理図の管理限界と製品の規格限界、標準偏差と無次元の指数を混同しない。',
 'quality_tools_capability',['theory:quality:capability','theory:quality:charts','theory:quality:regression'],'安定工程と規格、Cp、回帰と主成分分析の目的差、管理図、度数密度。',cites=['quality_nist_capability','quality_nist_control','quality_nist_histogram','stat_psu_correlation'])

sampling_knowledge='計数値と計量値、ロットとサンプル、不適合品の数、OC曲線、生産者危険と消費者危険、検査の切換え。'
sampling_solution=r'合否を数で決める計数値検査では不適合品の数を数える。良いロットの拒否は生産者危険 \(\alpha\)、悪いロットの受入れは消費者危険 \(\beta\) である。サンプル数を固定して合格判定個数を増やすと、受入確率が増し、生産者危険が下がる一方で消費者危険が上がる。先行ロットの成績によるなみ検査・きつい検査の切換えと、一ロット内で複数の標本を取る多回抜取を区別する。'
sampling_ambiguity='原典の「抜取検査手順を固定」と「判定個数で調整」は、標本数を固定して閾値を変更するという意味に限定する。全(n,c)固定なら二つの危険も固定である。切換え規則の出題時JIS原文全体は未取得であり一般概念の照合と区別する。'
add('H26-REG-BASIC-1-3','抜取検査の測定量、危険の負担者、合否の閾値と検査切換えを対応させる。',
 ['個数・生産者・消費者・判定個数・なみ/きつい','平均・消費者・生産者・判定値・なみ/きつい','個数・消費者・生産者・判定個数・多回抜取','平均・生産者・消費者・判定値・多回抜取','個数・生産者・消費者・判定値・なみ/きつい'],
 ['計数値の個数と危険の負担者、個数の合否閾値、ロット間の切換えが対応する。','計数値を平均値へ、危険の負担者を逆へ取り違えている。','生産者と消費者の危険を逆にし、ロット間切換えを一ロット内の多回抜取と混同する。','計量値の平均と判定値、複数標本を取る手順は本問の指定と合わない。','本問は不適合品の個数と合否判定個数の組合せを問う。計量値に対応する判定値との用語差を保持する。'],
 sampling_solution+'本問の五項目の組合せは1である。',
 'quality_acceptance_sampling',['theory:quality:acceptance','theory:quality:oc','theory:quality:switching'],sampling_knowledge,ambiguity=sampling_ambiguity,cites=['quality_nist_sampling','quality_nist_oc'])
add('H28-REG-BASIC-1-2','計数値抜取検査の危険と、先行ロットの成績による検査の切換えを読む。',
 ['平均・消費者・生産者・多回','平均・生産者・消費者・なみ/きつい','個数・消費者・生産者・多回','個数・生産者・消費者・なみ/きつい','平均・消費者・生産者・なみ/きつい'],
 ['測定量と危険の負担者が違い、多回抜取は先行ロットを使う切換えではない。','危険の順序は合うが、計数値検査では平均値でなく不適合品の数を使う。','危険の負担者が逆で、切換えと多回抜取も違う。','個数、良品拒否の生産者危険、不良品受入れの消費者危険、なみ/きついの切換えが対応する。','平均値への置換と危険の負担者の逆転が不適切である。'],
 sampling_solution+'本問は合格判定個数が問題幹にあり、残る四項目の組合せは4である。',
 'quality_acceptance_sampling',['theory:quality:acceptance','theory:quality:oc','theory:quality:switching'],sampling_knowledge,ambiguity=sampling_ambiguity,cites=['quality_nist_sampling','quality_nist_oc'])

intervals=['0.2%未満','0.2%以上1%未満','1%以上5%未満','5%以上10%未満','10%以上']
add('H27-REG-BASIC-1-5','独立な二部材の長さを足し、規定長さを超える確率を標準化する。',intervals,
 ['z=3の上側確率0.13%はこの範囲に入る。','0.13%は下限0.2%より小さい。','0.13%は下限1%より小さい。','0.13%は下限5%より小さい。','0.13%は10%に届かない。'],
 r'全長 \(L=A+B\) は平均3500mm、分散 \(0.4^2+0.3^2=0.25\,\mathrm{mm^2}\) の正規変数である。標準偏差0.5mmにより \(z=(3501.5-3500)/0.5=3\) となる。原典表の上側確率0.13%を読み、1を選ぶ。標準偏差を0.7mmと足す方法は独立な確率変動に対して使わない。連続分布では「超える」と「以上」の確率は等しい。',
 'quality_normal_combinations',['theory:quality:variance','theory:quality:normal'],'寸法和、分散の加法、上側確率と標準化、連続分布。',calculation=True,figure=True)
add('R04-REG-BASIC-1-3','独立な引張力と圧縮力の差について、正の合力が閾値を超える確率を求める。',intervals,
 ['2.28%は0.2%未満ではない。','2.28%は上限1%を超える。','z=2の上側確率2.28%がこの範囲に入る。','2.28%は下限5%より小さい。','2.28%は10%より小さい。'],
 r'引張りを正として \(F=F_a-F_b\) と置く。期待値は300-200=100Nであり、独立な差の分散も \(30^2+40^2=2500\,\mathrm{N^2}\) と加える。したがって標準偏差50N、閾値200Nの標準化は \(z=(200-100)/50=2\) である。上側確率2.28%から3となる。力の平均では符号を反転するが、分散では係数を二乗するため圧縮成分の分散も正に加わる。',
 'quality_normal_combinations',['theory:quality:variance','theory:quality:normal'],'力の符号、正規差、分散と係数の二乗、上側確率。',calculation=True,figure=True)
add('R02-REG-BASIC-1-2','応力と強度の独立正規モデルで、強度が応力を下回る確率を比較する。',
 ['ウ→イ→エ→ア','ア→ウ→イ→エ','ア→イ→ウ→エ','ウ→ア→イ→エ','ア→ウ→エ→イ'],
 ['ウの次はイではなくアである。アの信頼性指標4/3はイの1より大きい。','ウの3/2はアの4/3より大きく、最小故障確率はウとなる。','ウをイより後に置くのが違い、ウは全ケース中で故障確率が最小となる。','信頼性指標を大きい順に並べると3/2、4/3、1、1/√2で、故障確率はこの順に小さい。','ウが最初でないことと、エがイより後であることに反する。'],
 r'限界状態 \(Z=R-S\) の平均は \(\mu_R-\mu_S\)、分散は \(\sigma_R^2+\sigma_S^2\) である。故障確率は \(\Phi(-b)\)、\(b=(\mu_R-\mu_S)/\sqrt{\sigma_R^2+\sigma_S^2}\) なので、大きい \(b\) ほど小さい。原典比のアは4/3、イは3/3=1、ウは3/2、エは1/√2である。故障確率の小さい順はウ・ア・イ・エとなり4を選ぶ。平均強度と平均応力の差だけで順位を決めず、その散らばりで規格化する。',
 'quality_stress_strength',['theory:quality:stress_strength','theory:quality:variance'],'独立な応力と強度、限界状態、信頼性指標、標準正規累積分布。',calculation=True,figure=True)
add('R06-REG-BASIC-1-6','独立正規寸法の和と差の分布を、平均と分散に分けて表す。',
 ['和は平均和/分散和、すき間も平均和/分散和','和は平均和/分散和、すき間は平均差/分散差','和は平均和/分散和、すき間は平均差/分散和','和は平均和/分散差、すき間は平均差/分散差','和は平均和/分散差、すき間は平均和/分散差'],
 ['接続長さは合うが、すき間の平均は内径から外径を引く。','すき間の平均は合うが、差の分散を引いてはいけない。','和の平均はμA1+μA2、すき間の平均はμB2-μB1で、どちらも独立成分の分散を足す。','独立な和でも差でも分散差にはならない。','接続長さの分散と、すき間の平均・分散の両方が違う。'],
 r'接続長さを \(L=A_1+A_2\)、すき間を \(G=B_2-B_1\) とする。独立正規変数の線形結合より、\(L\) は平均 \(\mu_{A1}+\mu_{A2}\)、分散 \(\sigma_{A1}^2+\sigma_{A2}^2\)、\(G\) は平均 \(\mu_{B2}-\mu_{B1}\)、分散 \(\sigma_{B2}^2+\sigma_{B1}^2\) である。3を選ぶ。原典の \(\mu_{B2}>\mu_{B1}\) は平均の順序であり、すべての個体で内径が外径より大きい保証ではない。分布の負側はしまりばめを表し得る。',
 'quality_normal_combinations',['theory:quality:variance','theory:quality:normal'],'独立正規寸法、平均和差、分散和、平均の順序と個体のすき間。',calculation=True,figure=True)

add('H27-REG-BASIC-1-6','ISO 9001:2008を背景とするPDCAの順序を対応させる。',
 ['Plan Act Check Do','Plan Act Do Check','Plan Check Act Do','Plan Do Act Check','Plan Do Check Act'],
 ['実施前に改善を置き、実施を最後にする順序になっている。','実施より前に改善を置き、確認後に次の改善へ戻る対応がない。','計画の後に実施がなく確認へ進み、実施が最後になっている。','実施結果を確認する前に改善段階を置いている。','計画・実施・確認・改善の順で、結果を次の計画に反映する。'],
 'PDCAはPlanで目標とプロセスを定め、Doで実施し、Checkで目標・要求との対応を確認し、Actで改善する循環である。順序は5である。2008年版の実施ガイダンスもPlan-Do-Check-Actを用いる。一方、2015年版のプロセス解説は同じ循環をリスクに基づく思考とともに説明する。一般の循環の確認と、2008年規格の条文全体を照合したことは区別する。',
 'quality_pdca',['theory:quality:pdca','theory:quality:historical'],'計画、実施、確認、改善、フィードバック、規格の版。',
 ambiguity='ISO公式の2008実施ガイダンスでPDCA名称を確認したが、設問が参照するISO9001:2008/JISQ9001:2008の規格本文全体は未取得。現在版の説明を過去版の条文へ無条件に代用しない。',
 cites=['quality_iso2008_guidance','quality_iso_process'])
for q,values,reasons in [
 ('R03-REG-BASIC-1-3',['正誤正正','正正誤誤','正正正誤','誤正誤正','誤誤正正'],
 ['Doを誤とし、ChangeとAdjustを正としている。','PlanとDoは正しく、Check/Actに対応しないChange/Adjustは誤りである。','CをChangeとする説明を正としている点が違う。','Planを誤とし、Adjustを正としている点が違う。','PlanとDoを誤とし、ChangeとAdjustを正としている。']),
 ('R07-REG-BASIC-1-2',['誤誤誤正','誤正正正','正正正誤','正正誤誤','正正誤正'],
 ['PlanとDoは正しく、AchieveはActと違う。','Planを誤、ChooseとAchieveを正としている。','Chooseを正としている点が違い、CはCheckである。','PlanとDoが正しく、ChooseとAchieveはCheckとActに対応しない。','Achieveを正としている点が違い、AはActである。'])]:
 add(q,'PDCAの段階名と、それぞれの目的を照合する。',values,reasons,
 '計画を定めるPlanと実施するDoは正しい。Cは結果を監視・評価するCheck、Aは改善するActである。変更や達成などの一般語が意味として近くても、PDCAの指定された段階名への置換にはならない。正正誤誤の候補'+initial[q]['independent_answer']+'を選ぶ。',
 'quality_pdca',['theory:quality:pdca'],'Plan/Do/Check/Act、目標と評価、改善のフィードバック。',cites=['quality_iso_process'])

add('R04-REG-BASIC-1-2','一様・二項・ポアソン・指数・正規の分布と、現象をモデル化する前提を比較する。',
 ['サイコロの各面は一様分布','工業製品の不良個数はポアソン近似','災害間隔は指数近似','5年間の事故回数は正規近似','5回のコインの表数は二項分布'],
 ['公平なサイコロを前提に離散一様となる。偏ったサイコロまでは一様としない。','多数の独立機会と小さな一定不良確率を前提に二項分布をポアソンで近似できる。共通原因の不良連発には注意する。','一定率の独立発生モデルなら待ち時間は指数となる。災害全般の普遍法則ではない。','低頻度の回数を正規へ直接対応させるのは不適切という典型比較である。ただし平均回数が大きいポアソンには正規近似が成立するので、条件なしの不可能命題にはしない。','独立な試行と一定の表確率なら二項となる。公平性はp=1/2にするが、二項であること自体は一定pでも成立する。'],
 '初回は有限期間の事故回数の基本モデルをポアソンと読み、4を最も不適切とした。しかし原典は平均回数を指定しておらず、平均が十分大きいなら正規近似も可能である。2と3も小確率や一定率などの仮定を要する。したがって公式4を保持して典型分布の対応は説明するが、4だけがあらゆる条件で不適切という厳密な主張はしない。回数と間隔を区別し、分布名より先にモデルの前提を確認する。',
 'quality_probability_models',['theory:quality:models','theory:quality:poisson'],'離散/連続、二項の独立試行、ポアソンの希少事象、一定率と指数待ち時間、正規近似。',ambiguity='原典に平均事故回数がなく、ポアソンの大平均に対する正規近似を排除できない。災害間隔や不良個数にも仮定が省略される。公式/初回4を保持し、唯一不適切の厳密な成立範囲をAstra重点査読へ残す。',cites=['stat_nist_binomial','stat_nist_poisson','stat_nist_exponential','stat_nist_normal'])
add('R05-REG-BASIC-1-6','ピアソン相関の線形性、端点、独立性、決定係数、因果の関係を区別する。',
 ['相関は常に-1<r<1','rが0から1へ近づくほど直線関係になる','r=0なら独立','決定係数は|r|','相関絶対値で因果が変わる'],
 ['完全な線形関係ではr=±1を取り得るため、厳密不等号で端点を除外できない。','正の相関が1へ近づくほど、正傾斜の直線の周りに集まる程度が強まるという意味である。','無相関は独立を含意しない。対称なXとY=X²では相関が0でもYはXに依存する。','切片あり一説明変数の最小二乗回帰ではR²=r²であり、|r|ではない。','相関は線形関連の強さを表し、共通原因などの交絡があるため、因果の有無や方向を決めない。'],
 r'相関係数は有限な非零分散の変数について \(\rho=\mathrm{Cov}(X,Y)/(\sigma_X\sigma_Y)\) と定義され、端点を含む[-1,1]にある。2は正の線形関連が強まるという典型的な説明である。無相関の反例として \(X\) を[-1,1]の対称一様、\(Y=X^2\) とすれば、\(\mathrm{Cov}(X,Y)=E[X^3]=0\) でもYはXに完全に依存する。決定係数は切片あり単回帰ならr²である。相関の大小から因果関係を結論しない。',
 'quality_correlation_regression',['theory:quality:correlation','theory:quality:regression'],'共分散、Cauchy–Schwarz、無相関と独立、切片あり単回帰、交絡。',cites=['stat_psu_correlation'])
add('R07-REG-BASIC-1-6','仮説検定の二種類の誤り、t統計量の自由度、信頼区間の意味を比較する。',
 ['成立を期待する帰無仮説から始める','有意水準は一般に30%','真H0棄却は第1種、偽H0不棄却は第2種','母分散未知の平均検定は自由度nのt','信頼度は危険率の逆数'],
 ['帰無仮説は基準となる命題であり、必ずそれが成立することを期待して設定するわけではない。棄却されないことも真の証明ではない。','有意水準は事前に定める。典型例は5%などであり30%を一般的とする記述は違う。','誤りの定義に合う。第2種の確率は対立仮説下の値に依存し、1-αと同じではない。','独立正規標本の通常の一標本t検定では平均の推定に一自由度を使い、自由度はn-1である。','信頼係数は1-αであり1/αではない。固定された一つの区間に固定母数が入る確率という事後解釈にも注意する。'],
 r'帰無仮説が真なのに棄却する誤りを第1種、偽なのに棄却しない誤りを第2種と呼ぶ3が正しい。独立正規標本で母分散が未知なら \(T=(\bar X-\mu_0)/(s/\sqrt n)\) はH0下で自由度n-1のt分布である。信頼係数1-αは同じ手順を反復したときに区間が母数を覆う割合であり、危険率の逆数ではない。観測後の固定された区間に対する確率と、観測前のランダムな区間の被覆率を区別する。',
 'quality_hypothesis_inference',['theory:quality:hypothesis','theory:quality:t_interval'],'H0と対立、第1種/第2種、有意水準、独立正規標本とt、頻度論的被覆。',cites=['stat_nist_interval','quality_nist_sampling'])

assert len(items)==16
out=ROOT/'config/authored_batches/S7_030_quality_statistics.json';assert not out.exists()
out.write_text(json.dumps(dict(batch_id='S7_030_quality_statistics',reference_date='2026-10-11',questions=items),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(items),'questions',sum(bool(x['ambiguity']) for x in items),'partial')
