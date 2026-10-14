# coding: utf-8
"""Manually authored safety/consumer batch. No inference from official keys."""
import json,copy,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
R={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_056_selection.json').read_text())['records']}
I={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_056_initial_independent.json').read_text())['records']}
T=json.loads((P/'config/authored_batches/S7_052_engineering.json').read_text())['questions'][0]
Q=[];Y='条件内で適切';N='不適切';L='条件・時点を留保'
def add(q,title,cid,section,refs,opts,solution,knowledge,ambiguity='',discipline='basic_4_1',conditions=None,figure=False,law=False):
 r=R[q];e=copy.deepcopy(T)
 e.update(question_id=q,source_sha256=r['source_sha256'],stem=title,summary=title,
  conditions=conditions or {'原典':'問題文・否定・全五候補と組合せ表を保存原典33画像で確認。','時点':r['era_year']+'の本文表現を保持。後の制度改正を遡及しない。'},
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
 add(q,title,'finish56_'+key,theory,refs or [],numeric(values,answer,'解法の条件と結果を照合する。') if all(isinstance(v,(int,float)) for v in values) else combo(values,values[answer-1]),sol,knowledge,ambiguity,d,conditions,figure)
def detailed(q,title,key,d,theory,opts,sol,knowledge,conditions,refs=None,ambiguity=''):
 add(q,title,'finish56_'+key,theory,refs or [],opts,sol,knowledge,ambiguity,d,conditions)

item('H23-REG-BASIC-1-4','利得表の最適反応と支配戦略。','game','basic_1_5','theory:design:game',
 ['A60/B60','A60/B65','A65/B60','A65/B65','決まらない'],1,
 'Aの行を比較するとB60では12>8、B65では15>10なのでAは60が支配戦略。Bの列を比較するとA60では13>7、A65では14>10なのでBも60。互いの最適反応が一致するA60/B60の1。両社の売上合計を最大にする協調案とは別の基準である。',
 '利得表の行列、支配戦略、最適反応、ナッシュ均衡。',
 {'行':'Aの定価60,65万円。','列':'Bの定価60,65万円。','利得(A,B)':'行A60：(12,13),(15,7)。行A65：(8,14),(10,10)。単位億円。'},figure=True)
item('H23-REG-BASIC-2-4','二段キャッシュの実効アクセス時間。','cache','basic_2_5','theory:information:cache',
 [1.9,6.45,11.45,15.4,19.95],1,
 '一次成功、一次失敗かつ二次成功、両方失敗を排他的に分ける。二次の90%は一次失敗時の条件付きヒット率と読む。0.95×1+0.05×0.9×10+0.05×0.1×100=1.9 nsの1。二次や主記憶の時間を各経路の総所要時間として扱う試験モデル。各段を逐次探索し、その時間を別々に加えるモデルなら1+0.05×(10+0.1×100)=2 nsとなる。',
 '条件付き確率、排他的経路、ヒット率、累積時間のモデル。',
 {'一次':'1ns、95%。','二次':'10ns、一次失敗条件下90%。','主記憶':'100ns。'},['info_cache'],
 ambiguity='原典はアクセス時間に上位段の探索時間を含めるか明示しない。候補に合う経路総時間モデルと逐次加算モデルを区別し、査読を要する。')
item('H23-REG-BASIC-4-3','放射線の実体・遮蔽と照射による変化。','radiation','basic_4_2','theory:basicchem:radiation',
 ['ア イ','ア ウ','ア エ','イ ウ','イ エ'],4,
 'アは同じ厚さで普通コンクリートの方が鉛よりγ遮蔽効果が高いという一般化が誤り。イは照射が材料特性を変え得るので正。ウはαがHe核、β−が電子で、αの強い電離と短い飛程が対応して正。エはβを中性子、γを電子とするので誤。イウの4。',
 '粒子線と電磁波、飛程・電離、γ減衰と材料、照射損傷。',
 {'比較':'同じ厚さ、コンクリート密度2.35g/cm3。','原典β':'電子の流れとして記述。'},['finish56_radiation'],
 ambiguity='βには陽電子を放出するβ+もある。原典の電子という通常のβ−表現を全βの定義へ広げない。γ遮蔽は光子エネルギーと材料の減衰係数を含む。',figure=True)
item('H24-REG-BASIC-1-5','資源制約から生産利益を最大にする。','lp','basic_1_5','theory:design:lp',
 [4,6,9,10,12],5,
 '生産個数x,y≥0に対し3x+y≤9、x+2y≤8、利益3x+2y。頂点(0,0),(3,0),(0,4),(2,3)の利益は0,9,8,12万円。交点(2,3)は整数でも実行可能で最大12万円、5。',
 '線形計画、制約交点、頂点比較、整数生産量。',
 {'製品X':'A3kg、B1kg、利益3万円。','製品Y':'A1kg、B2kg、利益2万円。','上限':'A9kg、B8kg。'},figure=True)
for q,vals,a in [('H25-REG-BASIC-2-6',['26ns','25μs','26μs','25ms','26ms'],3),('H29-REG-BASIC-2-6',['260ns','26μs','260μs','26ms','260ms'],2)]:
 item(q,'命令数とCPIからCPU実行時間を求める。','cpu','basic_2_5','theory:information:cpu',vals,a,
 '必要サイクル数は3500×6+5000×5+1500×4=52000。2.0GHzは2.0×10^9サイクル/秒なので時間は52000/(2.0×10^9)=26×10^-6秒=26μs。命令数10000だけを周波数で割らず、CPIで重み付けする。',
 'CPI、クロック周期、命令構成による重み付き平均、SI接頭辞。',
 {'命令':'転送3500×CPI6、算術5000×5、分岐1500×4。','周波数':'2.0GHz。'},figure=True)
item('H26-REG-BASIC-1-2','限界利益から必要な客席回転を求める。','economics','basic_1_5','theory:design:economics',
 [2,3,4,5,10],4,
 '一人当たり限界利益は500-200=300円。月の目標利益100万円と固定費50万円を賄う人数は1500000/300=5000人。20日×50席で割ると一席一日5人、4。売上高500円をそのまま利益としない。',
 '売上と変動費、固定費、限界利益、期間と席数の換算。',
 {'売上':'500円/人。','変動費':'200円/人。','固定費':'月50万円。','目標利益':'月100万円。','営業':'20日、50席。'},figure=True)
drawreason='幾何公差は形状・姿勢・位置等を管理し、高精度化で不要にはならない。寸法は現場で誤算が起きないよう製作に必要な情報を示す。はめあい又は限界ゲージは指定公差の管理・検査に対応する。通常の正投影は第一角又は第三角で、第二角ではない。表題・部品等の情報を示す。'
for q,vals,a,order in [
 ('H26-REG-BASIC-1-6',['OXOXO','XOOOX','XOOXO','OOXOX','XXXOO'],3,'角法/寸法/はめあい/幾何公差/表題'),
 ('H29-REG-BASIC-1-5',['XOOXO','XOOOX','OXOXO','OOXOX','XXXOO'],1,'幾何公差/寸法/はめあい/角法/表題'),
 ('R01-REG-BASIC-1-3',['XXXOO','XOOOX','OXOXO','OOXOX','XOOXO'],5,'幾何公差/寸法/限界ゲージ/角法/表題')]:
 item(q,'製作図の角法・寸法・公差・検査を区別。','drawing','basic_1_10','theory:design:drawing',
 vals,a,drawreason+' この年度の列順へ戻して'+vals[a-1]+'。O正、X誤。',
 '投影法、寸法公差と幾何公差、はめあい・限界ゲージ、図面情報。',
 {'列順':order,'O/X':'正/誤。','原典':'全五行を画像から転記。'},['design48_iso'],figure=True)
item('H29-REG-BASIC-1-3','決定と確率分岐を後ろから評価する。','decision','basic_1_8','theory:design:decision',
 ['4.5 状況対応','5.4 状況対応','5.7 状況対応','6.6 恒久','6.9 恒久'],2,
 '状態S1ではA1の期待損失は.5×5+.5×7=6億円、A2の8より小さい。S2はA1が.6×8+.4×10=8.8、A2の12より小さい。状況対応全体は.6×6+.1×8.8+.3×3=5.38億円。恒久6.5より小さく、最も近い5.4と状況対応の2。決定ノードでは平均せず小さい案を選び、機会ノードだけ確率で平均する。',
 '条件付き期待値、決定ノードの最適化、後向き評価。',
 {'状態':'S1 .6、S2 .1、S3 .3。','S1':'A1=(5,.5;7,.5)、A2=8。','S2':'A1=(8,.6;10,.4)、A2=12。','S3':'3。','恒久':'6.5、額は全て億円。'},figure=True)
item('H29-REG-BASIC-2-5','再帰文法の生成列の不変条件。','grammar','basic_2_10','theory:information:grammar',
 ['111110','111000','101010','000111','000001'],4,
 '基底は01。再帰規則は生成列の外へ0と1を一つずつ付け、0011、000111となる。一般形0^n1^n(n≥1)なので4のみ生成可能。数が等しいだけでなく全0が全1の前に並ぶ必要がある。',
 'BNF、基底と再帰、生成列の構造、不変条件。',
 {'規則':'S::=01 | 0 S 1。'})
item('H30-REG-BASIC-1-5','検査費用と期待損害の合計を最小化。','cost','basic_1_1','theory:design:inspection',
 [2,3,4,5,6],3,
 '万円でC(x)=30x+3240/(x+2)^2。Cprime=30-6480/(x+2)^3=0からx+2=6、x=4。二階微分19440/(x+2)^4>0なので最小。整数候補でもC(3)=219.6、C(4)=210、C(5)=216.122...万円で4回、3。',
 '期待損害、総費用、微分と凸性、整数候補の比較。',
 {'確率':'1/(x+2)^2。','検査費':'1回30万円。','不具合損害':'3240万円。'})
item('H30-REG-BASIC-2-2','エレベータの状態遷移のガード条件。','state','basic_2_15','theory:information:state',
 ['= = = = =','= > < = =','< = = > >','= < > = =','> = = < >'],3,
 '上昇を継続するaは現在階<目的階、停止へ戻るb,cはともに=。下降を続けるdと停止から下降を始めるeは現在階>目的階。a,b,c,d,e=<,=,=,>,>の3。矢印の始点・終点と比較を合わせて読む。',
 '状態、イベント、ガード、状態不変条件。',
 {'状態':'停止・上昇・下降のみ。扉・故障・別階呼出を除外。','a':'上昇自己遷移。','b':'上昇→停止。','c':'下降→停止。','d':'下降自己遷移。','e':'停止→下降。'},figure=True)
item('R01-REG-BASIC-1-1','線形・凸・整数計画の成立条件。','convex','basic_1_8','theory:design:convex',
 ['OOXX','OXOX','XOXO','XXOO','XOOO'],5,
 'アは目的だけ線形ならよいとするので誤りで、線形計画は制約も線形。イは二変数の図解法で正。ウは凸実行可能集合上の凸関数の最小化では局所最適が大域最適となり正。エは整数問題の困難さとヒューリスティック近似の利用で正。XOOOの5。ヒューリスティックが全問題の最適性を保証するわけではない。',
 '線形制約、凸最小化、局所と大域、整数計画と近似。',
 {'列順':'線形計画/図解法/凸計画/整数計画。','O/X':'正/誤。'},['finish56_convex'],figure=True)
item('R01-REG-BASIC-1-2','定常需要の経済的発注量。','eoq','basic_1_5','theory:design:eoq',
 [50,60,70,80,90],2,
 '年間費用C(q)=kd/q+hq/2。微分すると-kd/q²+h/2=0、q=sqrt(2kd/h)。指定値でsqrt(2×20000×1350/15000)=sqrt3600=60単位の2。q>0で二階微分2kd/q³>0、q≤dも満たす。購入単価はqによらず、最適qへ影響しない。',
 '一定需要、即時補充、発注回数、平均在庫、凸費用の最小化。',
 {'k':'20000円/回。','d':'1350単位/年。','h':'15000円/(単位・年)。','条件':'欠品なし、需要一定、即時一括補充、0<q≤d。'},['finish56_eoq'])
item('R01-REG-BASIC-1-6','展開・複素指数・不定形極限の三公式。','math','basic_1_9','theory:design:mathformulas',
 ['ロピタル/オイラー/フーリエ','マクローリン/フーリエ/オイラー','マクローリン/オイラー/ロピタル','フーリエ/ロピタル/マクローリン','フーリエ/マクローリン/ロピタル'],3,
 'アは0中心のf(x)=Σf^(k)(0)x^k/k!なのでマクローリン。イはe^(iπ)+1=0なのでオイラーの等式。ウは0/0又は∞/∞で微分比の極限を用いるロピタル。3。何回でも微分可能というだけで無限級数と関数が一致するとは限らず、原典の適当な条件を保持する。',
 'Taylor/Maclaurin、複素指数、ロピタルの適用条件。',
 {'ア':'0中心、適当な条件下の級数。','イ':'e^(iπ)+1=0。','ウ':'0/0又は∞/∞、gprime≠0、微分比の極限が存在。'},figure=True)
for q,vals,a,one,two,recv,send,dist in [
 ('R01-REG-BASIC-2-5',['5/1001010','5/0001010','5/1101010','7/1001010','7/1011010'],5,'1110001','0001110','1001010','1011010',7),
 ('R04-REG-BASIC-2-4',['4/0000010','5/1100010','4/1001010','5/1000110','4/1000011'],5,'1110101','1001111','1000010','1000011',4)]:
 item(q,'ハミング距離と一ビット誤り訂正。','hamming','basic_2_1','theory:information:hamming',
 vals,a,f'{one}と{two}の各位置を比較すると距離{dist}。受信{recv}について無反転と七通りの一ビット反転を調べ、三つの検査ビットが全て再計算値に合う{send}を選ぶ。'+('R01では第3位置を反転し、情報1011のパリティは010。' if q.startswith('R01') else 'R04では第7位置を反転し、情報1000のパリティは011。')+' 最小距離3なので、誤りが高々1という条件下で訂正が一意になる。',
 'XOR、ハミング距離、mod2の検査式、最小距離と訂正能力。',
 {'比較':one+' / '+two,'受信':recv,'検査式':'x5=x2+x3+x4、x6=x1+x3+x4、x7=x1+x2+x4、全てmod2。','仮定':'通信誤りは高々一ビット。'},figure=True)
detailed('R01-REG-BASIC-4-4','化学物質の製法・特性・用途。','substances','basic_4_4','theory:basicchem:substances',[
 ('炭酸NaはHaber-Bosch製造',N,'Haber-Boschはアンモニア合成。炭酸Naの代表はSolvay法。'),
 ('黄リンは毒性少ない',N,'黄リンは強い毒性がある。空気中発火と水中保管は毒性の低さの根拠でない。'),
 ('TiO2の一部は光触媒用途',Y,'光を受けて表面で反応を促し、抗菌・防汚等へ使われる。'),
 ('黒鉛は極めて硬く導電性悪い',N,'層状構造で軟らかく、電気を伝える。ダイヤモンドと混同。'),
 ('Pbは鉛電池正極、PbOガラス',N,'放電時の負極がPb、正極活物質はPbO2。後半のガラス用途と合わせても肢全体は誤。')],
 '3のみ適切。製法名、同素体、電極極性、毒性を個別に判定する。原典の「中には」「使われている」という範囲を保持し、全TiO2が可視光で同じ性能を出すとはしない。',
 'Haber-BoschとSolvay、同素体と構造、光触媒、鉛蓄電池の活物質。',
 {'原典':'五肢の前半と後半をともに判定。'},['finish56_titania','openstax_batteries'],
 ambiguity='黄リンの毒性分類とSolvayの詳細一次資料は追加照合対象。TiO2の組成・結晶相・照射条件により光触媒性能が異なる。')
item('R01-RET-BASIC-1-1','等号条件を含む三つの不等式。','inequality','basic_1_9','theory:design:inequality',
 ['≤ = =','≤ ≥ =','= ≤ <','< = ≥','≤ ≥ <'],5,
 '相加相乗は幾何平均≤算術平均で、全数が同じなら等号。sinは[0,π/2]で凹なので両端を結ぶ直線より上にありsinθ≥2θ/π、θ>0で割ってsinθ/θ≥2/π。π/2は等号を含む。fsecond>0の厳密凸では異なる二点の中点関数値が平均より厳密に小さい。≤,≥,<の5。',
 '相加相乗、凹関数と弦、端点、厳密凸性とJensen。',
 {'1':'非負実数n個。','2':'0<θ≤π/2。','3':'区間のfsecond>0、x1≠x2。'},figure=True)
detailed('R01-RET-BASIC-4-1','結合双極子のベクトル和と分子極性。','polarity','basic_4_4','theory:basicchem:polarity',[
 ('CO2',N,'直線対称で二つのC=O双極子が相殺。'),
 ('ジエチルエーテル',Y,'Oの周りが折れ曲がり、C-O結合の双極子は相殺しない。'),
 ('CH4',N,'正四面体対称で相殺。'),
 ('BF3',N,'平面三角形対称で相殺。'),
 ('CCl4',N,'正四面体対称で相殺。')],
 '結合が極性でも分子全体は対称性によって無極性になり得る。候補ではジエチルエーテルのO付近の折れ曲がり構造だけが双極子を残すので2。',
 '分子形、結合極性、双極子ベクトル和、対称性。',
 {'対象':'中性分子の通常構造の極性。'},['finish56_polarity'])
item('R01-RET-BASIC-4-2','塩酸・酢酸・フェノールの酸性度。','acid','basic_4_4','theory:basicchem:acid',
 ['a b c','b a c','c b a','b c a','c a b'],3,
 '水中の通常比較は強酸HCl、弱酸酢酸、さらに弱いフェノールの順。c,b,aの3。フェノキシドも共鳴するが、カルボキシラートの安定性を同じ強さとしない。',
 '強酸・弱酸、共役塩基と共鳴、酸性度比較。',
 {'a':'フェノール。','b':'酢酸。','c':'塩酸。'},['purdue_acid_strength'])
item('R02-REG-BASIC-1-5','投影図の配置と断面図の目的。','drawing','basic_1_10','theory:design:drawing',
 ['OOXXX','XOOXX','XXOOX','XXXOO','OXXXO'],5,
 'アの第三角の平面図上・右側面図右は正。イの第一角では平面図は下なので誤。ウは内部を切って示す断面図で、想像図との呼称が誤。エは投影法明記不要が誤。オは情報量の多い主投影図を使い単純な物体は一図で足りる場合があり正。OXXXOの5。',
 '第一角・第三角、主投影図、断面図、図面の解釈。',
 {'O/X':'正/誤。','列順':'第三角/第一角/想像図という名称/明記不要/主投影図。'},['design48_iso'],figure=True)
item('R04-REG-BASIC-1-6','便益の期待値から建設費を引く。','decision','basic_1_8','theory:design:decision',
 ['ア','イ','ウ','エ','オ'],2,
 '期待価値=0.7Ba+0.2Bb+0.1Bc-C。ア4.7-3=1.7、イ5.0-3=2.0、ウ4.0-3=1.0、エ5.5-4=1.5、オ6.2-6=.2億円。最大イの2。便益最大のオでも費用控除後は最大でない。',
 '期待値、一定費用の控除、最大純便益。',
 {'確率':'a.7,b.2,c.1。','便益(abc)':'ア(5,4,4)、イ(5,4,7)、ウ(3,6,7)、エ(6,5,3)、オ(7,4,5)。','費用':'ア3、イ3、ウ3、エ4、オ6、額は億円。'},figure=True)
item('R04-REG-BASIC-2-3','LRUで参照履歴を更新する。','lru','basic_2_5','theory:information:lru',
 ['7M+2H','6M+3H','5M+4H','4M+5H','3M+6H'],3,
 '古い→新しいの順で保持。2(M):[2]、1(M):[2,1]、1(H):[2,1]、2(H):[1,2]、3(M):[1,2,3]、4(M):1を追出し[2,3,4]、1(M):2を追出し[3,4,1]、3(H):[4,1,3]、4(H):[1,3,4]。外部5回・主記憶4回で5M+4Hの3。挿入の古さを使うFIFOとは違いヒットでも順序を更新する。',
 'LRU、ページフォールト、ヒット時更新、アクセス時間の原典モデル。',
 {'容量':'3ページ、初期空。','参照':'2,1,1,2,3,4,1,3,4。','時間':'ヒットH、外部M。原典例はミスに追加Hを計上しない。'})
detailed('R05-REG-BASIC-4-2','コロイドの分離・光散乱・移動と状態。','colloid','basic_4_4','theory:basicchem:colloids',[
 ('電解質で疎水コロイド凝析',Y,'粒子間の反発が弱まり集合・沈殿。'),
 ('半透膜で透析',Y,'小さい分子・イオンを透過させコロイド粒子と分離。'),
 ('光路が見えるTyndall',Y,'粒子による光散乱。'),
 ('直流電場で電気泳動',Y,'荷電粒子が電場に応じ移動。'),
 ('流動しない状態がゾル',N,'流動性のある分散系がゾル、網目等によって流動しにくい状態がゲル。')],
 '不適切5。凝析、透析、光散乱、電気泳動はそれぞれ電解質・膜・光・電場の作用。ゾルとゲルの状態を取り違えている。',
 'コロイド粒子、凝析、透析、Tyndall、電気泳動、ゾルとゲル。',
 {'対象':'原典の通常の液体中コロイドの用語。'},['openstax_colloids'])
item('R06-REG-BASIC-1-4','減速比と動力保存から出力トルクを求める。','gear','basic_1_6','theory:design:gear',
 ['入力1→出力30/トルク等倍','入力30→出力1/トルク等倍','入力30→出力1/トルク30倍','入力1→出力30/トルク30倍','入力30→出力1/トルク1/30'],3,
 '速度比ωin/ωout=30なので入力30回転に出力1回転。動力P=Tωと効率ほぼ1からToutωout≈Tinωin、Tout≈30Tin。両条件を満たす3。速度が減ってもトルクは同じとすると出力動力が不足する。',
 '角速度、動力とトルク、減速比、伝達効率。',
 {'速度比':'入力角速度/出力角速度=30。','効率':'ほぼ100%、滑りなし。'})
detailed('R07-REG-BASIC-1-4','平面応力と平面ひずみの拘束条件。','plane','basic_1_6','theory:design:plane',[
 ('薄板の面外応力無視=平面応力',Y,'自由表面と薄さから面外応力を小さいとする。'),
 ('長柱の軸応力無視=平面ひずみ',N,'無視するのは軸ひずみ、軸応力はPoisson結合で残り得る。'),
 ('長柱の軸ひずみ無視=平面応力',N,'その近似は平面ひずみ。'),
 ('薄板の面外ひずみ無視=平面ひずみ',N,'薄板は面外変形を許し、通常面外ひずみは0でない。'),
 ('長柱の軸応力無視=平面応力',N,'指定の長柱を軸方向変形の拘束モデルとして読むとひずみを無視。')],
 '適切1。平面応力ではσz,τxz,τyz≈0でもεzはPoisson効果で一般に0でない。平面ひずみではεz,γxz,γyz≈0でもσzは一般に0でない。長柱は端部から離れた一様部分の変形拘束という適用条件を確かめる。',
 '三次元Hooke則、Poisson効果、自由面、拘束と二次元近似。',
 {'薄板':'面内荷重。','長柱':'側面に長さ方向一様荷重。'},
 ambiguity='原典長柱の軸方向拘束は省略。平面ひずみの標準的適用を説明し、自由な端部・一様軸伸びがある一般化平面ひずみとは区別して査読。')
item('R07-REG-BASIC-1-5','M/M/1の系内時間と待ち時間を分ける。','queue','basic_1_1','theory:design:queue',
 [0,25,50,75,100],5,
 'λ=36/3600=.01人/秒、μ=1/50=.02人/秒、ρ=.5。系内人数L=ρ/(1-ρ)=1、滞在W=L/λ=100秒。処理50秒を含むので待ちだけなら50秒。5。到着人数とサービス率を同じ単位にし、平均処理時間50秒を率50としない。',
 'Poisson到着、指数サービス、ρ<1、Little則、系内と行列。',
 {'到着':'36人/時間。','処理':'平均50秒/人、指数分布。','窓口':'1、Poisson到着。','問':'並んでから処理終了まで。'},['design48_queue_ref'])

assert len(Q)==30 and set(R)=={e['question_id'] for e in Q}
for e in Q:
 e['learning_points']=e['required_knowledge']+' 条件を式又は判定にし、全候補を照合してその年度の番号へ戻す。'
 e['calculation']='true' if e['concept_id'].split('_',1)[1] in ['game','cache','lp','cpu','economics','decision','cost','eoq','hamming','lru','gear','queue'] else 'false'
 e['evaluation'].update(calculation_load='2' if e['calculation']=='true' else '0',difficulty_reason='表・係数・単位・成立条件を確認し、独立解法を全候補へ照合する。')
out=P/'config/authored_batches/S7_056_design_information_finish.json';assert not out.exists()
out.write_text(json.dumps({'batch_id':'S7_056_design_information_finish','reference_date':'2026-10-14','questions':Q},ensure_ascii=False,indent=2))
print('Prepared',len(Q),'partial',sum(bool(e['ambiguity']) for e in Q))
