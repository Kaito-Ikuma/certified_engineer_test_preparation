# coding: utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')}
ini={r['question_id']:r for r in json.loads((ROOT/'config/authored_batches/S7_022_independent_answers.json').read_text())['questions']}
items=[]
def m(s):return r'\('+s+r'\)'
def add(q,summary,vals,reasons,answer,solution,core,knowledge,concept,labels,cites,ambiguity='',verdicts=None,direction='最も不適切なもの。',conditions=None,calc=False,difficulty=3):
 r=by[q];assert len(vals)==len(reasons)==5
 if verdicts is None:verdicts=['不適切' if i==answer else '適切（条件付き）' for i in range(1,6)]
 image='extracted/pages/'+r['source_year_directory']+'/17_applied_science/page_'+str(int(r['source_page'])).zfill(3)+'.png'
 items.append(dict(question_id=q,source_sha256=r['source_sha256'],stem=summary,summary=summary,
 conditions=conditions or {'方向':direction,'対象':'同位体の標準・分別又は年代。番号・核種・旧標準名称を原典画像で確認。'},
 choices={str(i):dict(value=v,verdict=d,reason=w) for i,(v,d,w) in enumerate(zip(vals,verdicts,reasons),1)},
 figures='問題幹・5肢・否定・質量数・δ記号・標準名称・年度番号を原典画像で照合。設問固有図なし。',
 ambiguity=ambiguity,evidence=[image],core_concept=core,required_knowledge=knowledge,solution=solution,
 independent_answer=ini[q]['independent_answer'],independent_solution_note='S7_022_independent_answers.jsonへ原典画像確認後・公式参照前の初回判断を保存。'+ini[q]['reason']+' 初回を改変せず後続一次資料で条件・名称の疑義を追加。',
 answer_reason=solution,learning_points='核種の生成、試料への取り込み、移動・分別、閉鎖、壊変を順番に分ける。比の基準と時計の開始条件を特定し、測定値と解釈する年代を区別する。',
 theory_references=['theory:isotope:'+x for x in labels],discipline_id='earth_isotope',concept_id=concept,cross_concepts=['isotope_general'],
 classification_reason='原典全肢の中心は'+core+'であり、自然試料の組成・履歴又は年代を読む同位体地球化学に主分類する。核種一般則は既存共通概念へ横断参照。',
 calculation=str(calc).lower(),figure='false',law='false',
 evaluation=dict(knowledge_novelty='2' if difficulty==2 else '3',reasoning_steps='1' if difficulty==2 else '2',calculation_load='1' if calc else '0',figure_reading='0',difficulty=str(difficulty),difficulty_reason='壊変の数学は物理専攻読者に既知である。試料・標準・分別・混合の地球化学的前提が新規であり、'+('一つの対応又は時間範囲を選ぶ。' if difficulty==2 else '複数の前提を分けて各記述を判断する。')),
 citations=cites,foundationality='high',transferability='high'))
legacy='原典のSMOW/PDB/CDTは歴史的対応を問う旧名称である。1995年IAEA勧告は既にVSMOW/VPDB/VCDTと尺度の実現物質を区別しており、出題時に旧隕石・化石標準そのものを現在も測定用一次物質として使うとは説明できない。公式と初回の対応は保存し、尺度と物質・旧名称の省略を査読事項に保持。'
standard_rs={'H':'水の2H/1HはSMOW系列（現在のVSMOW-SLAP尺度）。水素をCDT系列としない。','C':'炭素13C/12CはPDB/VPDB系列である。CDTは硫黄の尺度の起源であり、炭素の標準という対応は誤り。','Owater':'水・ケイ酸塩等の18O/16OにはSMOW/VSMOW系列が使われる。対象により尺度を明記する。','S':'CDTはCanyon Diablo隕石のトロイライトFeSに由来する硫黄の歴史的基準。実際のVCDT実現は硫化銀IAEA-S-1等を使い、旧CDT物質を無条件に現行標準としない。','Ocarbonate':'炭酸塩酸素はPDB/VPDB系列でも表す。同じ18Oでも水のVSMOWと炭酸塩のVPDBは数値基準が異なる。'}
for q,vals,order,ans in [
 ('H23-REG-APPLIED-21',['HとSMOW','CとCDT','OとSMOW','SとCDT','OとPDB'],['H','C','Owater','S','Ocarbonate'],2),
 ('H30-REG-APPLIED-21',['SとCDT','OとSMOW','CとCDT','OとPDB','HとSMOW'],['S','Owater','C','Ocarbonate','H'],3)]:
 add(q,'元素と同位体比の歴史的標準の対応を比較し、炭素と硫黄の基準を取り違えた組合せを選ぶ。',vals,[standard_rs[x] for x in order],ans,
 '炭素はPDB/VPDB、硫黄はCDT/VCDT系列という対応なので、CとCDTの'+str(ans)+'が誤りである。水のHとOはSMOW系列、炭酸塩OはPDB系列を用いる。δ値は比の基準を変えると変わるため、元素だけでなく試料と尺度を明記する。原典旧名称の歴史的対応と、現在の標準物質の実現を分ける。',
 '同位体比の基準尺度と標準物質','δ=(R/Rstd−1)×1000の定義、H/OのVSMOW、炭酸塩C/OのVPDB、SのVCDT、尺度を実現する標準物質。','isotope_standards',['delta','standards'],['iso_standards1995','iso_vsmow2','iso_vcdt'],ambiguity=legacy,
 verdicts=['対応は意図適切・旧名称注意' if i!=ans else '対応不適切' for i in range(1,6)],difficulty=2)
methods=['K-Ar法','Rb-Sr法','U-Pb法','14C法','フィッション・トラック法']
shell_rs=[
 'Kを含む鉱物等の40Kから生成した40Arを測る。2万年前の貝殻炭酸塩の生物由来炭素を直接測る方法としては選ばない。若い火山岩の測定まで絶対不可能という意味ではない。',
 'Rbを含む鉱物・岩石の87Rb→87Srを用い初生Srと閉鎖条件を検討する。提示の若い貝殻へは14Cほど直接的でない。',
 'ジルコン等のUを取り込む鉱物のU→Pb系列に適する。炭酸塩のU系列法一般とU-Pb法を混同せず、提示5法では14Cを選ぶ。',
 '生存中取り込まれた14Cが炭素交換停止後に減ることを使う。物理半減期5730年なら2万年後の残存率は約0.089であり測定時間範囲内である。海洋リザーバー・混入・再結晶・暦年校準を別途検討する。',
 'Uの自発核分裂による鉱物中の飛跡を用い、加熱で飛跡が消えるため熱履歴に依存する。若い貝殻の炭素を直接測る方法ではない。']
for q in ['H23-REG-APPLIED-24','H26-REG-APPLIED-31']:
 add(q,'2万年前の貝化石に対し、試料成分と時計の時間範囲に適合する測定法を選ぶ。',methods,shell_rs,4,
 '貝殻を形成した炭素の14Cを用いる4が提示中最も適切である。'+m('N/N_0=2^{-20000/5730}\\simeq0.089')+'であり、数万年の測定範囲に合う。他法の対象元素・鉱物と熱履歴はこの若い生物起源炭酸塩の時計に直接対応しない。貝が海生か淡水生か、リザーバー効果・再堆積・炭素交換を確認して暦年を推定する。',
 '試料と放射性時計の時間尺度の適合','閉鎖系の壊変N=N0exp(−λt)、14Cの物理半減期約5730年、生物炭素の交換停止、海洋・淡水リザーバー効果、校準。','radiometric_dating',['decay','radiocarbon','method'],['iso_radiometric','iso_shell'],direction='年代測定法として最も適切なもの。',conditions={'試料':'2万年前の貝化石。海生か淡水生かは原典に指定なし。','選択':'K-Ar、Rb-Sr、U-Pb、14C、フィッション・トラックの5法。','方向':'最も適切なもの。'},verdicts=['本試料では選ばない','本試料では選ばない','本試料では選ばない','最も適切（補正は別）','本試料では選ばない'],calc=True,difficulty=2)
add('H25-REG-APPLIED-27','U-Pb年代測定に適する鉱物を、Uの取り込み・初生Pb・閉鎖性から選ぶ。',
 ['黒雲母','ジルコン','白雲母','海緑石','カリ長石'],
 ['Kを含む雲母でK-ArやRb-Srの対象になり得るが、提示中のU-Pbの代表試料ではない。','ZrSiO4中でUがZr位置へ取り込まれ、通常初生Pbは少ない。抵抗性が高くU-Pb年代に適する。継承核・Pb損失・共通Pbは別途検査する。','Kを含む雲母でK-ArやRb-Sr等に利用するが、U-Pbの代表的選択肢はジルコンである。','Kを含む堆積性鉱物でK-Ar等の候補になり得る。生成・変質条件を要し、提示中のU-Pb最適鉱物ではない。','Kに富む長石で初生Pbを含み得る。Uを集めるジルコンのようなU-Pbの代表鉱物ではない。'],2,
 '2のジルコンを選ぶ。Uを取り込み、初生Pbが比較的少なく、結晶が地質過程を通じてU-Pb系を保ちやすいためである。238U→206Pbと235U→207Pbから独立な年代を比べ、同じ年代かどうかで閉鎖系の仮定を点検する。古い継承核を持つ粒子は岩体の定置年代と一致しない場合がある。',
 '放射性時計を保持する鉱物の選択','ジルコンZrSiO4、UとZrの置換、放射起源Pbと初生共通Pb、閉鎖系、U-Pb二系列と継承核。','radiometric_dating',['upb','closure','method'],['iso_zircon','iso_radiometric'],direction='U-Pbに最も適した鉱物。',verdicts=['代表試料ではない','最適','代表試料ではない','代表試料ではない','代表試料ではない'],difficulty=2)
for q,vals,ans in [('H28-REG-APPLIED-32',['14C法','K-Ar法','U-Pb法','Rb-Sr法','フィッション・トラック法'],1),('R01-RET-APPLIED-35',['K-Ar法','U-Pb法','Rb-Sr法','フィッション・トラック法','14C法'],5),('R04-REG-APPLIED-25',['U-Pb法','K-Ar法','14C法','Rb-Sr法','フィッション・トラック法'],3)]:
 rs={'14C法':'白亜紀の数千万〜億年の時間は、約5730年という半減期を何千回も超える。測定可能な14Cは背景・汚染に支配され、直接年代時計として不適切。','K-Ar法':'40Kの長い半減期と蓄積した放射起源40Arを使う。K含有鉱物を含む適切な岩石を選び、Ar損失や過剰Arを検査する。','U-Pb法':'白亜紀ジルコン等でU→Pbの二系列を使える。鉱物選択と初生Pb、Pb損失、継承核を検査する。','Rb-Sr法':'87Rb→87Srの比と複数の同源試料により初生Srを分ける。白亜紀の時間自体は適用候補だが、あらゆる試料に使えるとはしない。','フィッション・トラック法':'アパタイト・ジルコン等で238U自発核分裂の損傷を測る。白亜紀の冷却・熱履歴を測れるが、形成年代と必ず一致するとはしない。'}
 add(q,'白亜紀試料に対し、放射性時計の時間範囲が短すぎる方法を選ぶ。',vals,[rs[v] for v in vals],ans,
 '14Cの'+str(ans)+'が不適切である。数万年程度の時計を数千万〜億年の試料へ使うと、初生14Cは事実上失われる。他の4法は適切な鉱物・岩石と閉鎖条件を選べばこの時間尺度の年代又は冷却履歴を扱える。長半減期だけで万能とせず、何の出来事から時計が閉じたかを確かめる。',
 '年代範囲と時計の感度','壊変率λ=ln2/T、検出限界、14Cの数万年範囲、K-Ar/U-Pb/Rb-Srと飛跡法の試料・閉鎖条件。','radiometric_dating',['decay','method','closure'],['iso_radiometric','iso_zircon'],conditions={'対象':'白亜紀の地質試料。具体的鉱物は指定されていない。','方向':'測定方法として最も不適切。'},difficulty=2)
add('H29-REG-APPLIED-30','年代時計のうち、宇宙線で生成される親核種を使う方法を選ぶ。',
 ['U-Pb法','Rb-Sr法','14C法','フィッション・トラック法','熱ルミネッセンス法'],
 ['自然界の長寿命U核種の壊変を使い、通常の時計のUを宇宙線生成核種とはしない。','長寿命87Rbの壊変を使い、宇宙線による生成時計ではない。','大気14Nへ宇宙線の二次中性子が作用して14Cを作る。生物へ入った後の減衰を時計にする。','自然Uの自発核分裂の飛跡を使う。飛跡一般には宇宙線損傷もあるが、この年代法の時計はU核分裂。','放射線で生じた捕獲電荷の蓄積を発光として測る。宇宙線の線量寄与はあり得るが、宇宙線で作った核種の壊変比を用いる時計ではない。'],3,
 '3の14C法である。生成反応'+m('{}^{14}\\mathrm N+n\\to{}^{14}\\mathrm C+p')+'を、形成後の14Cのβ壊変とは区別する。提示中の他法は自然長寿命核種・核分裂飛跡・蓄積線量に基づく。宇宙線が線量に寄与することと、宇宙線生成核種を年代指標にすることを分ける。',
 '核種生成と壊変時計・蓄積線量の区別','宇宙線一次粒子と二次中性子、14N(n,p)14C、放射壊変と損傷・捕獲電荷の違い。','cosmogenic_nuclides',['cosmogenic','radiocarbon','method'],['iso_radiometric'],direction='宇宙線生成核種を利用する方法として最も適切。',verdicts=['該当しない','該当しない','該当する','該当しない','線量寄与と核種生成が別'],difficulty=2)
frac_ice='氷期は16Oに富む水が陸上氷に隔離され、海水が18Oに富む。低温ほど炭酸塩と水の分別も殻18Oを増やす方向であり、有孔虫δ18Oは通常氷期に大きい。局所塩分・水温・生物効果・続成変質の補正は別に要する。'
sea='外洋海水は天水に比べ同位体組成の変動が小さいという一般的比較である。蒸発・降水・氷融解・河川流入で地域差はある。熱水も天水起源なら負値を取り得るが、水岩交換・マグマ性流体で変わるため全海水・全熱水の固定値とはしない。'
old='14Cに乏しい古い有機物又は炭酸塩から炭素が加わると、炭素量に対する14Cが薄まり未補正見かけ年代は古くなる。「ことがある」という原典の条件付き主張である。若い有機炭素なら若返る場合もあり、全有機物に一般化しない。'
evap='軽い水分子が蒸発しやすく、残った水はD（2H）・18Oに富む傾向となる。供給水や湿度・同位体交換による例外を分ける。蒸気が重くなるという説明へ逆転しない。'
add('H24-REG-APPLIED-32','自然水・地下水炭素・炭酸塩の同位体尺度と、蒸発・氷期の分別を比較する。',
 ['海水δ18Oの地域差は天水・熱水より小さく、後者は負値が多い。','有機物分解の炭素添加で地下水14C見かけ年代が古くなる場合。','水・珪酸塩岩・炭酸塩岩は全て酸素SMOWのみ。','蒸発残留水にDと18Oが濃縮。','有孔虫δ18Oは氷期の方が間氷期より大きい。'],
 [sea,old,'炭酸塩の酸素比はPDB/VPDB系列でも表示する。全対象にSMOWのみという限定は誤りである。異なる尺度のδ数値はそのまま比較しない。',evap,frac_ice],3,
 '3の「SMOWのみ」が不適切である。水・ケイ酸塩と炭酸塩では慣用尺度が異なり、炭酸塩酸素はPDB/VPDB系列を使う。他肢は蒸発残留、古い炭素による希釈、氷床と炭酸塩分別の作用を、それぞれ適用条件を付して理解する。海水が完全一様、全熱水が負値、全有機物が必ず老齢化という全称命題にはしない。',
 '同位体の基準・混合と気候分別','δの基準、水と炭酸塩の尺度、残留水の重同位体濃縮、氷床への軽同位体隔離、炭素混合と見かけ14C年代。','water_isotope_fractionation',['delta','standards','fractionation','climate','deadcarbon'],['iso_standards1995','iso_oxygen','iso_deadcarbon','iso_hydrothermal'])
add('H27-REG-APPLIED-25','水の同位体比の基準と天水線の軸、核実験トリチウムと分別を比較する。',
 ['各種同位体から土壌水・地下水・流出水の滞留を推定。','H/Oのδは標準比からの千分偏差、標準平均海水等。','δ18O対δ17Oを天水線と呼ぶ。','1952年以降核実験トリチウム増加から地下水涵養を推定。','蒸発凝縮の分別でδD・δ18Oが変わる。'],
 ['放射性同位体の壊変、安定同位体の入力変動と混合モデルを組み合わせ、適切な条件で滞留を推定できる。安定比だけが単調な年齢時計になるわけではない。','δ=(R/Rstd−1)×1000である。原典旧SMOW名称をVSMOW-SLAP尺度とその実現物質へ接続する。','天水線は水素δD（δ2H）と酸素δ18Oの関係である。酸素17/18の相関には別の意味があり、それを天水線と呼ばない。','核実験が作った1950年代以降の入力履歴を使う。減衰と混合を補正し、同じトリチウム濃度に複数涵養年が対応し得る。','質量差による平衡・速度論的分別が蒸発凝縮の履歴を残す。混合・蒸発線と地域天水線を分ける。'],3,
 '3が軸を取り違えている。天水線は'+m('\\delta^2\\mathrm H\\simeq8\\delta^{18}\\mathrm O+10')+'で、水素と酸素を結ぶ。δは千分率偏差であり濃度ではない。3Hの入力パルス・壊変は年代、安定H/O比は起源・分別を主に追い、両者を区別する。',
 '安定同位体の起源指標と放射性水時計','δ比の定義、全球・地域天水線、D=2H、核実験3H入力、壊変と混合。','water_isotope_fractionation',['delta','meteoric','tritium'],['gc_meteoric','iso_tritium_clock','iso_vsmow2'])
for q,vals,order,ans in [('R02-REG-APPLIED-20',['蒸発残留水はDと18Oに富む。','地下水へ有機物分解炭素が加わると14C見かけ年代が古くなる場合。','有孔虫δ18Oは氷期より間氷期に大きい。','硫黄標準はCDTトロイライト。','海水δ18Oの変動は天水・熱水より小さく後者は負値が多い。'],['evap','old','ice','standard','sea'],3),
 ('R06-REG-APPLIED-21',['有孔虫δ18Oは氷期より間氷期に大きい。','有機物分解の炭素が地下水14C見かけ年代を古くする場合。','蒸発残留水はDと18Oに富む。','海水δ18Oの変動は天水・熱水より小さく後者は負値が多い。','硫黄標準はCDTトロイライト。'],['ice','old','evap','sea','standard'],1)]:
 rs={'evap':evap,'old':old,'ice':frac_ice+'原典はこの大小を逆にしている。','standard':standard_rs['S'],'sea':sea}
 add(q,'氷期と間氷期の有孔虫酸素比の大小を、蒸発・炭素混合・歴史的硫黄尺度から区別する。',vals,[rs[x] for x in order],ans,
 '氷期より間氷期のδ18Oが大きいとする'+str(ans)+'が意図された不適切肢である。氷床へ軽い水を隔離する作用と、低温で殻が重い酸素を取り込みやすい分別が、通常ともに氷期の殻δ18Oを増す。他肢の条件を分け、硫黄CDTは歴史的起源として説明しVCDT尺度の実現を併記する。',
 '氷床・炭酸塩分別と同位体尺度の時点','海洋と氷の同位体収支、温度依存の炭酸塩分別、古い炭素混合、CDTとVCDT・IAEA-S-1の違い。','water_isotope_fractionation',['climate','fractionation','deadcarbon','standards'],['iso_oxygen','iso_deadcarbon','iso_standards1995','iso_vcdt','iso_hydrothermal'],
 ambiguity='公式と初回は一致。原典の硫黄「国際標準物質CDTを用いて表記」は、出題前1995年のVCDT/IAEA-S-1勧告と物質・尺度の区別を省く。旧名称を現在の測定用標準物質へそのまま昇格しない。氷期δ大小の誤りは独立に説明できるが、硫黄肢の文字通りの妥当性は査読事項。',
 verdicts=['意図不適切（大小逆）' if x=='ice' else '旧尺度として意図適切・名称疑義' if x=='standard' else '適切（条件付き）' for x in order])
add('R05-REG-APPLIED-21','安定な重水素と放射性トリチウムを区別し、水の分別・天水線・熱水酸素シフトを読む。',
 ['重水素2Hは半減期約12.3年。','一般に降水・陸水は海水より重い同位体に乏しい。','反応で同位体組成の偏りが生じる作用は同位体分別。','δ2H=8δ18O+10が天水線。','熱水でδ2Hほぼ一定、δ18Oだけ高くなる場合。'],
 ['2H（D）は安定同位体である。約12.3年でβ壊変するのは3H（T）であり、核種の質量数を取り違えている。','海からの蒸発と降水の履歴により一般に陸水は重同位体に乏しい。蒸発湖等の例外を分け、全陸水の厳密不等式ではない。','同じ元素の同位体が反応・相変化で異なる比で配分されることである。核壊変で元素そのものが変わる作用とは区別する。','全球的な経験関係で、地域ごとの傾き切片・蒸発混合の逸脱がある。全水で厳密に成り立つ式ではない。','高温水岩交換で岩石の豊富なOと水のOが交換し、H変化よりO変化が目立つ例がある。マグマ性流体混合など他機構も検討する。'],1,
 '1が2Hと3Hを混同している。D=2Hは安定、T=3Hは半減期約12.3年で3Heへβ壊変する。安定H/Oの比は蒸発凝縮や水岩交換の履歴を追う指標であり、この壊変時計とは別である。天水線を基準にO側へのずれを見ると熱水反応を検討できる。',
 '核種の安定性と水の同位体分別','2Hと3Hの核構造・安定性、δ定義、天水線、蒸発凝縮・水岩同位体交換。','water_isotope_fractionation',['delta','fractionation','meteoric','hydrothermal','tritium'],['iso_tritium2023','iso_vsmow2','gc_meteoric','iso_hydrothermal'])
add('R07-REG-APPLIED-22','水時計と宇宙線生成核種の標的元素・輸送を区別して各測定法の前提を検討する。',
 ['3Hのβ壊変で生じる3Heの蓄積と3H/3Heから水塊年代。','古い地下水14Cは地化学反応の無機炭素値変化を補正。','大気N/Oの核破砕で作る10Beがエアロゾルに付着し堆積速度へ利用。','カルサイト中Clへ宇宙線が照射して36Clを作り石灰岩削剥を推定。','岩石U/Thのα壊変で作る4Heが地下水に蓄積し滞留推定。'],
 ['大気との交換停止後、3Hから生じる放射起源3Heを分けて親娘比から見かけ年代を求める。初生大気He、過剰空気、地殻・マントルHe、混合とガス損失を補正する。','炭酸塩溶解等の古い炭素が14Cを希釈し、反応・交換・混合で年代指標が変わるため補正が必要。測る炭素の見かけ年代と水の移動時間は同一とは限らない。','大気宇宙線核破砕で作った10Beが粒子に付着し湿性・乾性沈着で堆積物へ入る。初期入力、混合・再移動と閉鎖性を検討して堆積履歴を推定する。','石灰岩ではカルサイトの主成分Caの核破砕が主要な36Cl生成経路であり、原典Cl標的は意図上取り違えと考えられる。ただし微量35Clへの二次中性子捕獲でも36Clを作る実在経路がある。原典を「Ca」に訂正せず、Cl経路を不可能とも断定しない。','α粒子は4He核で、U/Th系列由来Heが溶存水へ供給される。生成供給速度・地殻深部流束・拡散漏れ・混合等のモデルを要し、濃度だけから常に一意な年代を得るわけではない。'],4,
 '公式4と初回4は一致する。石灰岩表面の36ClではCa核破砕が主要経路であり、原典がClをカルサイトの標的として挙げる点が意図された誤りと考えられる。一方、35Cl(n,γ)36Clという二次中性子捕獲は実在する。微量Clを含む試料まで含めた原典の広い表現に科学的一意性を与えず、公式と疑義を併記する。他の方法も閉鎖・混合・生成入力の補正を条件とする。',
 '自然水の親娘時計と宇宙線標的反応','親娘3H/3Heの質量収支、炭素反応補正、10Be大気生成と沈着、Ca核破砕と35Cl中性子捕獲、UThα壊変由来4Heの供給。','water_isotope_age',['tritium','deadcarbon','helium','cosmogenic','cl36'],['iso_tritium_clock','iso_groundwater','iso_deadcarbon','iso_be10','iso_cl36','iso_cl36_uw'],
 ambiguity='初回・公式4を保持。原典はカルサイトに含まれるClへの宇宙線照射による36Cl生成と書く。石灰岩主要経路はCa核破砕だが、微量35Clの二次中性子捕獲経路も存在する。ClをCaへ原典校正せず、Cl経路を不可能とも説明しない。一意な科学的誤り肢かは査読待ち。',
 verdicts=['適切（補正・閉鎖条件）','適切（反応補正）','適切（入力・閉鎖条件）','意図不適切・生成経路疑義','適切（供給モデル条件）'])
assert len(items)==15
(ROOT/'config/authored_batches/S7_022_isotope.json').write_text(json.dumps(dict(batch_id='S7_022_isotope',reference_date='2026-10-11',scope='同位体地球化学15問、原典15画像を公式前に確認し初回保存、15公式一致。旧標準名4問とCl36生成1問を疑義に保持。',questions=items),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(items),'partial',sum(bool(e['ambiguity']) for e in items))
