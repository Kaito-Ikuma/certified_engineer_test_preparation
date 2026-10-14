# coding: utf-8
"""Manually authored S7_049; original images and initial answers already reviewed."""
import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
S=json.loads((P/'extracted/logs/S7_049_analysis_selection.json').read_text())['records'];B={r['question_id']:r for r in S}
I={r['question_id']:r for r in json.loads((P/'config/authored_batches/S7_049_independent_answers.json').read_text())['records']}
Q=[]
def add(q,title,disc,cid,label,refs,opts,solution,ambiguity='',knowledge=None):
 r=B[q];choices={str(j):{'value':v,'verdict':ver,'reason':why} for j,(v,ver,why) in enumerate(opts,1)}
 Q.append(dict(question_id=q,source_sha256=r['source_sha256'],stem=title,summary=title,conditions={'原典確認':'S7_049の26原典画像で全五肢・否定・添字を確認。','対象':title},choices=choices,figures='図はない。原典画像は確認用で転載しない。',ambiguity=ambiguity,evidence=[f"extracted/pages/{r['source_year_directory']}/17_applied_science/page_{int(r['source_page']):03d}.png"],core_concept=title,required_knowledge=knowledge or solution,solution=solution,answer_reason=solution,independent_answer=I[q]['answer_initial'],independent_solution_note='公式前初回JSONを保持。'+I[q]['reason']+(' 再照合後の相違・読み違いは疑義欄に記録。' if ambiguity else ''),learning_points='測定対象と分離対象、定義の分母、絶対量と相対校正、全称と成立条件を分けて判断する。',theory_references=[label],discipline_id=disc,concept_id=cid,cross_concepts=[],classification_reason='原典全候補から主題を確認：'+title,calculation='false',figure='false',law='false',evaluation=dict(knowledge_novelty='3',reasoning_steps='2',calculation_load='0',figure_reading='0',difficulty='4' if ambiguity else '3',difficulty_reason='測定・物性・定義の区別と全称の例外を確認する。'),citations=refs,foundationality='high',transferability='high'))
Y='通常の条件で適切';N='不適切';L='条件付き・解釈留保'
add('H24-REG-APPLIED-16','多元素同時分析に向く方法を比較する。','chem_analysis','analysis49_xrf','theory:analysis:xray',['analysis49_xrf_ref'],[
('酸化還元滴定',N,'当量関係を使う濃度測定で、複数元素の特性線を一度に識別する方法ではない。'),('赤外吸収',N,'主に振動と官能基を調べる。通常の多元素同時定量の第一選択ではない。'),('キレート滴定',N,'金属イオンと錯形成する試薬の当量を使い、各元素を同時に独立識別する方式ではない。'),('吸光光度',N,'特定の吸収帯や呈色反応を用いる。ここでの全元素比較ではXRFが適する。'),('蛍光X線',Y,'元素ごとの内殻遷移エネルギーを分け、複数の元素の信号を一分析で得られる。')], '元素の種類を区別する観測量を探す。特性X線のエネルギー又は波長を検出するXRFなら、複数元素のピークを識別できる。各滴定の総当量だけでは混合元素を一度に分解できない。装置方式による同時・逐次検出の差はあるが、五方法の比較では5を選ぶ。')
add('H24-REG-APPLIED-27','ESRを核磁気共鳴と取り違えた略称を判断する。','chem_analysis','analysis49_acronyms','theory:analysis:acronyms',['analysis49_esr_ref'],[
('XRF／蛍光X線',Y,'X-ray Fluorescenceである。'),('SEM／走査型電子顕微鏡',Y,'Scanning Electron Microscopeである。'),('ICP-MS／誘導結合プラズマ質量分析',Y,'Inductively Coupled Plasma Mass Spectrometryで、プラズマで作ったイオンを質量分析する。'),('ESR／核磁気共鳴',N,'ESRはElectron Spin Resonance。核磁気共鳴はNMRである。'),('FTIR／フーリエ変換赤外分光',Y,'Fourier Transform Infraredで、干渉信号から赤外スペクトルを求める。')], '磁気共鳴で対象となるスピンを区別する。ESR/EPRは不対電子、NMRはスピンを持つ原子核の共鳴を扱う。電子と核を交換した4が不適切である。')
add('H24-REG-APPLIED-35','全地球水に占める氷・地下水を含む淡水の割合を選ぶ。','geo_groundwater','hydro49_global','theory:hydro:global',['analysis49_fresh_ref'],[(x,Y if j==1 else N,'全水量を分母とする代表推計約2.5%に最も近い。' if j==1 else '淡水総量の代表割合約2.5%より大きい。') for j,x in enumerate(['3%','5%','7%','9%','11%'],1)], '分母は河川水だけでも利用可能な淡水だけでもなく、海水を含む地球上の水全体である。USGSの2010年資料では淡水約2.5%なので、提示値で最も近い3%を選ぶ。氷河・永久雪や地下水を淡水の内訳から除かない。','水量は推計・対象範囲に依存する代表値。3%を厳密な物理定数とはしない。')
sep={
 'NMR':('核磁気共鳴',N,'共鳴周波数・化学シフト等を観測して構造を分析する。通常の装置は混合物を成分別に回収する分離器ではない。'),
 'MS':('質量分析',L,'イオンを質量電荷比で選別して測定する装置内の分離を含む。一方、元の中性混合物を大量に分取する手法とは異なる。'),
 'C':('遠心分離',Y,'回転場で密度・大きさに応じた沈降速度差を利用する。'),
 'E':('電気泳動',Y,'電荷と抵抗に依存する移動度差を利用して成分を分ける。'),
 'H':('高速液体クロマトグラフィー',Y,'固定相と移動相への分配等により保持時間が異なる成分を分ける。')}
for q,order in [('H25-REG-APPLIED-15',['NMR','MS','C','E','H']),('H28-REG-APPLIED-16',['NMR','MS','C','E','H']),('R01-REG-APPLIED-12',['MS','E','C','NMR','H'])]:
 add(q,'成分の分離とNMRによる観測を区別する。','chem_analysis','analysis49_separation','theory:analysis:separation',['analysis49_ms_ref'],[sep[x] for x in order], 'NMRは核の磁気共鳴を観測する分析法で、通常は成分を位置・経路別に分ける操作を行わない。遠心分離・電気泳動・HPLCは移動速度や保持の違いを利用する。MSは装置内でイオンをm/zで選別するという意味で分離を含む。候補番号の入替えを確認し、NMRを選ぶ。','質量分析でのイオン選別と、中性試料の調製・分取という分離の意味は同一でない。原典の広い成分分離の比較として公式のNMR選択を説明する。')
add('H25-REG-APPLIED-16','高分子分子量の相対GPC測定と浸透圧による数平均を比較する。','chem_analysis','analysis49_molar','theory:analysis:molar',['analysis49_gpc_ref'],[
('ゲルろ過の溶離時間',L,'サイズ排除クロマトグラフィーとして標準物質で校正すれば分子量と分布を測定できる。原典に絶対測定という限定はなく、一般の分子量測定法としても成立する。'),('中和滴定から解離度',N,'示されたpH・解離定数の式は電離状態を調べる。末端基の数など追加情報なしに一般の高分子分子量を与えない。'),('半透膜による浸透圧',Y,'希薄溶液の粒子数に依存する浸透圧から数平均分子量を求める。濃度ゼロへの外挿で相互作用の寄与を減らす。'),('ガラス転移点の測定',N,'分子量と相関することはあるが、化学構造・可塑剤等にも依存し、記述だけでは一意に分子量が決まらない。'),('円偏光二色性',N,'左右円偏光に対する吸収差を測り、立体構造や二次構造を調べる。一般の分子量直接測定ではない。')], r'質量濃度c、数平均分子量Mnなら希薄溶液でΠ/c=RT/Mn+O(c)となる。濃度を変えてゼロへ外挿すれば切片からMnを得るので公式は3。一方、1のGPCも標準試料による相対校正で分子量を測定する実用法である。絶対測定の優位性で3を説明できるが、原典の一般的な問いから1を排除する十分な限定はない。','公式3を保持。初回独立1|3を保存。1も校正されたGPCによる分子量測定として成立し、単一正答の排他性は未解決。')
add('H25-REG-APPLIED-29','Horton型地表流と飽和地表流の定義を分ける。','geo_groundwater','hydro49_flow','theory:hydro:flow',['analysis49_runoff_ref','analysis49_darcy_ref'],[
('降雨が浸透能を超える流れを飽和地表流とする',N,'これは浸透能超過型、すなわちHorton型。飽和型は土壌が飽和して追加の水を受け入れられなくなる場合である。'),('透水量係数T=Kb',Y,'水平流を扱いKを厚さ方向に一定とする場合の式。一般には厚さ方向のKの積分となる。'),('透水係数は媒体固有だけではない',Y,'Kは媒体の固有透過度に加え流体の密度と粘性に依存する。'),('得水河川は地下水から水を受ける',Y,'地下水の流入により河川流量が増す区間をいう。'),('絶対間隙率と有効間隙率の区別',Y,'総間隙体積の割合と、流れに有効な連結間隙の割合を分ける。')],'地表流の発生を浸透能と飽和状態の二つで整理する。降雨強度が浸透能を上回るものはHorton型であり1が誤り。Darcy流束q=−K dh/dlと河川への流入を区別する。K=kρg/μ、一定KでT=Kbである。',knowledge='浸透能超過と飽和超過、Darcy則、TとKと固有透過度の区別。')
add('H27-REG-APPLIED-12','無機気体の生成物を反応式で確認する。','chem_inorganic','analysis49_gases','theory:inorganic:gas_generation',['analysis49_co_ref','inorganic_halogen_ref'],[
('ギ酸の濃硫酸脱水でCO2',N,'脱水生成物はCOと水。CO2への変更では酸素・水素の収支が合わない。'),('NaClと濃硫酸でHCl',Y,'不揮発性の酸により塩化物から塩化水素を発生させる。温度・当量で硫酸塩の組成は変わる。'),('Znと希硫酸でH2',Y,'Znが酸化されH+が還元される。硫酸の濃度を濃硫酸へ置き換えない。'),('MnO2と濃塩酸でCl2',Y,'Mn(IV)を還元しCl−を酸化する。MnO2+4HCl→MnCl2+Cl2+2H2O。'),('Cuと濃硝酸でNO2',Y,'酸化性酸でCuが溶け、濃硝酸では代表的にNO2を生じる。希硝酸の代表生成物NOと区別する。')], 'HCOOH→CO+H2Oが脱水の物質収支である。1のCO2は脱水と別の反応を混同している。他の四肢は酸塩基又は酸化還元の標準条件として成立する。操作の実施手順を教材で補わず、濃度・加熱という原典条件と生成物を対応させる。')
bio={
 'enz':('酵素はすべてタンパク質',L,'タンパク質酵素が多数を占めるが触媒RNAであるリボザイムもある。すべてという全称は1989年以前の発見に照らしても成立しない。'),
 'aa':('アミノ基と水酸基がアミノ酸の定義',N,'必要な組合せはアミノ基とカルボキシ基。側鎖にOHを持つセリン等の例はあるが、全アミノ酸の要件ではない。カルボキシ基内のOHを遊離アルコール性水酸基と同一視しない。'),
 'pep':('アミノ酸がペプチド結合で連なるタンパク質',Y,'カルボキシ基とアミノ基の縮合に対応するアミド結合で主鎖を形成する。'),
 'pi':('等電点の差で電気泳動分離',Y,'pH勾配で正味電荷がゼロになるpIへ集中させる等電点電気泳動がある。'),
 'den':('高次構造変化による変性と活性喪失',L,'通常の変性の要点は主として二次・三次等の構造変化。全て不可逆、必ず全活性喪失、ペプチド鎖の分解という一般化はしない。')}
for q,order in [('H27-REG-APPLIED-16',['enz','aa','pep','pi','den']),('H30-REG-APPLIED-15',['enz','den','pi','pep','aa'])]:
 add(q,'アミノ酸の官能基と触媒RNAの例外を確認する。','chem_organic','analysis49_bio','theory:organic:biomolecules',['analysis49_amino_ref','analysis49_rna_ref'],[bio[x] for x in order], 'アミノ酸の定義はアミノ基とカルボキシ基であり、遊離の水酸基の有無ではない。公式はその誤定義を選ぶ。ただし酵素を全てタンパク質とする肢にも触媒RNAの反例があり、公式番号だけで他肢を正しいと確定できない。等電点の違いを利用する分離、ペプチド主鎖、通常の変性はそれぞれ構造・電荷・高次構造として整理する。', '公式単一正答は官能基の誤りH27=2/H30=5。酵素全称の肢1にもリボザイムの反例がある。H27初回理由で画像の水酸基をカルボキシ基と読み違えたが、再照合で水酸基を確認。初回JSONは不変で本文に訂正を明示。変性の活性喪失の一般化も留保。')
add('H28-REG-APPLIED-13','カルシウム塩の溶解・水和・潮解を比較する。','chem_inorganic','analysis49_calcium','theory:inorganic:calcium',['analysis49_gypsum_ref','inorganic_waterchem'],[
('CaCO3と塩酸でCO2',Y,'炭酸塩が酸で分解されCa2+・CO2・水となる。'),('CO2水に不溶で純水に易溶',N,'通常は逆。純水に難溶で、CO2の溶解で酸性となる水では炭酸水素イオンの生成を伴い溶解が促進される。'),('骨・歯の水酸アパタイト',Y,'Caを含むリン酸塩で骨や歯の無機成分の主成分をなす。'),('半水石膏は加水で硬化',Y,'CaSO4·1/2H2Oが二水石膏へ水和し、結晶が成長して固まる。'),('CaCl2の潮解性と吸湿',Y,'空気中の水分を取り込み、水溶液となり得るので乾燥用途に用いられる。')], '溶解度だけでなく化学平衡を確認する。CaCO3+CO2+H2O⇌Ca2++2HCO3−によりCO2水中での溶解が促進されるので2が不適切。半水石膏の硬化は水分が蒸発するだけでなく水和反応を含み、CaCl2の潮解とは機構が異なる。')
for q,beer in [('H29-REG-APPLIED-12','透過度の対数'),('R02-REG-APPLIED-11','吸光度')]:
 add(q,'分析信号と水銀温度計・天秤の環境依存を比較する。','chem_analysis','analysis49_metrology','theory:analysis:metrology',['analysis49_beer_ref','analysis49_thermo_ref','analysis49_buoy_ref','analysis49_sxes_ref'],[
 ('炎中の原子励起と発光',Y,'高い状態から低い状態への遷移による特性発光を測る。'),(beer+'の濃度比例',Y,'固定波長・光路長でBeer則A=−log10T=εcl。logTも係数の符号が負の比例関係となる。'),('水銀柱全部が同温度なら正しい',L,'全浸没用温度計ではその条件に対応する。一方、部分浸没型は指定浸没位置と露出柱の校正条件があり、全型に無条件の規則ではない。'),('XRF波長が化学結合状態で変わり得る',Y,'内殻の信号にも周辺電子状態に応じた小さいエネルギー差があり、高分解能では化学シフトを扱える。'),('天秤は温度・圧力・湿度で変化しない',N,'空気密度と浮力が変わる。試料と分銅の密度差があると見かけの比較が変わる。')],'天秤で下向きの有効力は概略mg−ρair Vg。空気密度は温度・圧力・湿度に依存し、試料と分銅の体積差によって浮力補正が必要となる。全く変わらない5を選ぶ。Beer則A=−log10 T=εclなのでH29のlog透過度も負の比例であり、R02の吸光度も正の比例となる。','水銀温度計の全浸没型という条件が原典に明記されていない。部分浸没型の校正まで全水銀柱同温と一般化しない。Beer則にも化学種・波長・散乱等の成立条件がある。')
add('H30-REG-APPLIED-12','電子励起の発光・解離とKoopmans近似を比較する。','physics_optics','analysis49_photophysics','theory:analysis:photophysics',['analysis49_koop_ref','analysis49_pred_ref','atomic_ir_raman'],[
('無放射減衰後の発光をりん光とする',N,'発光の区別は減衰だけでなく始終の電子状態・スピン多重度で決まる。通常の一重項からの蛍光にも振動緩和は先行する。'),('系間交差後の通常発光を蛍光とする',N,'通常の一重項励起から三重項への系間交差を経る発光はりん光の説明である。遅延蛍光等までこの略記から断定しない。'),('自身の解離極限以上の分解を前期解離とする',N,'前期解離は離散的な状態が別の解離性状態との結合で非放射解離する場合を扱い、単にその状態の解離極限を超える直接解離と同一でない。'),('電子と核が同程度の速度で動く',N,'核は重く電子遷移の時間に大きく動けない。垂直遷移と振動波動関数の重なりが振動構造を与える。'),('イオン化エネルギーを軌道エネルギーの負号で見積もる',L,'凍結軌道のHartree–Fock近似でIE≈−εi。電子除去後の軌道緩和・電子相関などは近似に含まれない。')], '発光で蛍光とりん光を区別し、核が電子に比べて遅いことからFranck–Condonの垂直遷移を理解する。公式5はKoopmansの定理の凍結軌道近似を述べる。観測された全固体・全分子のイオン化エネルギーが無条件に厳密な単一軌道エネルギーと等しい、という主張へ拡張しない。','公式5は凍結軌道Hartree–Fockの適用条件つき。固体の全観測スペクトルへの厳密適用とはせず、りん光／遅延蛍光の例外も保持。')
ac={
 'EPR':('EPRの正式名',Y,'Electron Paramagnetic Resonance。電子常磁性共鳴でESRと同じ対象を扱う。'),
 'HPLC':('HPLCをHigh Precisionとする',N,'現在の通常名はHigh Performance Liquid Chromatography。高精度のPrecisionではない。'),
 'ESCA':('ESCAの正式名',Y,'Electron Spectroscopy for Chemical Analysis。XPSによる元素・化学状態の分析に用いられる。'),
 'CARS':('CARSの正式名',Y,'Coherent Anti-Stokes Raman Spectroscopy。コヒーレントな反Stokes Raman信号を観測する。'),
 'MALDI':('MALDIの正式名',Y,'Matrix-Assisted Laser Desorption/Ionization。マトリックス支援レーザー脱離イオン化を表す。')}
for q,order in [('H30-REG-APPLIED-13',['EPR','HPLC','ESCA','CARS','MALDI']),('R06-REG-APPLIED-14',['CARS','EPR','ESCA','HPLC','MALDI'])]:
 add(q,'HPLCのPerformanceとPrecisionを区別する。','chem_analysis','analysis49_acronyms','theory:analysis:acronyms',['analysis49_hplc_ref','analysis49_esr_ref','analysis49_maldi_ref','analysis49_cars_ref'],[ac[x] for x in order], 'HPLCのPを高精度のPrecisionへ交換した肢が不適切。通常はHigh Performance Liquid Chromatographyである。他の略称は観測又はイオン化機構を表す。MALDIはイオン源、TOF等は質量分析器であり、それぞれの機能を分けて覚える。')
ops={
 'D':('蒸留で気液組成は必ず違う',N,'共沸組成では気液の組成が一致し、通常の単純な蒸留を反復してもその組成を越えて分離できない。'),
 'G':('気体成分の液体への吸収',Y,'気体を液体と接触させ、溶けやすい成分を液相へ移す。表面への吸着と区別する。'),
 'L':('非混和液相への抽出',Y,'二相間の分配平衡を利用し、溶質を片方の相へ移す。'),
 'A':('活性炭・シリカゲル・ゼオライト',Y,'表面や細孔への相互作用により成分を保持する吸着剤として用いられる。'),
 'R':('逆浸透膜の水の選択透過',L,'溶媒を選択的に透過させ、浸透圧差に逆らう圧力で濃縮・脱塩する。実膜は全溶質を100%阻止する理想膜とは限らない。')}
for q,order in [('H30-REG-APPLIED-18',['D','G','L','A','R']),('R02-REG-APPLIED-17',['A','L','G','D','R'])]:
 add(q,'分離操作の原理と共沸による蒸留限界を判断する。','chem_physical','analysis49_operations','theory:analysis:operations',['phase_vle','inorganic_zeolite'],[ops[x] for x in order], '蒸留は気液平衡の組成差を使う。共沸点でy=xとなる例があるため、必ず異なるという全称が誤りである。吸収は液体内部への溶解、吸着は表面や細孔への保持、抽出は非混和液相間の分配として区別する。逆浸透は圧力で水を透過させる代表的操作だが、理想的な完全溶質阻止をすべての膜に保証しない。','逆浸透膜の全分子・イオンの完全阻止という記述は理想化。公式は蒸留の共沸例外を選ぶが、実膜の阻止率と対象化学種の条件を留保。')
add('R01-RET-APPLIED-29','Darcy則・異方性・井戸水位と自噴条件を比較する。','geo_groundwater','hydro49_flow','theory:hydro:flow',['analysis49_darcy_ref','inorganic_hydro_ref'],[
('Darcy則は被圧帯水層で成立する',L,'適切な層流・連続体近似のもとでは被圧帯水層にも成立する。原典に被圧だけ、のみという語はない。非被圧でも使えることは、この肢を直接否定しない。'),('水平・鉛直の透水性の違いは稀',N,'堆積層の配列や亀裂方向による異方性は一般的であり、等方性は近似条件である。'),('一定揚水の水位低下は厚さに比例',N,'均一な被圧帯水層の定常井戸モデルではs=Q ln(R/r)/(2πKb)。厚さbへの依存は反比例である。'),('漏水は常に下向き',N,'流れの向きは上下帯水層の水頭差で決まり、上向きも生じ得る。'),('扇状地下流の被圧層と自噴',L,'透水層を難透水層が覆い、水頭が地表より高い場合に自噴する。扇端等でその構造が成立する代表例であり、すべての扇状地に必ず起こるわけではない。')], '公式5は扇状地の地下構造と被圧水頭の代表的な説明である。1の原典は被圧の場合に成立するという文で、被圧の場合にのみという限定はない。Darcy則の一般性を指摘するだけでは1が誤りとは言えない。2～4は異方性、透水量係数の逆比例、水頭による流向から排除できるが、1と5の単一選択の整合は査読事項として残す。','公式5、独立初回1|5を保持。原典1にのみ／だけの限定を追加して公式へ合わせない。Darcy流速と実流速の意味及び扇状地の地質・水頭条件も確認が必要。')
add('R02-REG-APPLIED-12','分子光吸収の選択則とレチナールの光異性化を判断する。','physics_optics','atomic_optical_molecules','theory:atomic:optical',['atomic_ir_co2','atomic_ir_raman','atomic_retinal','atomic_linewidth'],[
('温室効果の振動吸収を可視とする',N,'水蒸気・CO2の代表的な温室効果は熱赤外の振動・回転吸収に関係する。'),('IRは分極率だけで双極子変化なら起こらない',N,'IR活性には振動による双極子変化、Raman活性には分極率変化が関係する。'),('cisレチナールの光異性化が視覚へ関与',Y,'11cisレチナールが光子を吸収して異性化し視物質の応答を引き起こす。'),('系間交差後の発光を蛍光',N,'通常の三重項を経る発光はりん光の説明。'),('選択則があるので衝突・運動で線幅不変',N,'Doppler幅・衝突幅があり、選択則と線幅の機構は異なる。')], '分子のどの自由度が光と相互作用するかを確認する。温室効果は主として熱赤外、IR活性は双極子変化、線幅には運動と衝突の影響がある。11cisレチナールの可視光吸収と異性化を述べる3が適切。')
add('R03-REG-APPLIED-16','内殻光電子の化学シフトと核・電子スピンを比較する。','chem_analysis','analysis49_xrf','theory:analysis:xray',['analysis49_xps_ref','analysis49_esr_ref','atomic_ir_raman'],[
('ESRと不対電子',Y,'不対電子の磁気共鳴を測る。'),('13Cはスピン1/2でNMR対象',Y,'13Cは核スピン1/2を持つ。豊富な12Cは核スピン0なので同じ測定対象ではない。'),('XPSは結合状態に鈍感で化学分析不向き',N,'周辺結合状態による内殻結合エネルギーの化学シフトを測定でき、元素と化学状態の分析に用いられる。'),('Ramanで振動・回転を調べる',Y,'非弾性散乱の周波数差が振動・回転遷移に対応する。'),('吸収端より短いX線でXRF',Y,'光子エネルギーが内殻電離の閾値を超えると空孔が作られ、その後の遷移から特性X線を放射し得る。')], '内殻の信号だから結合状態に無関係、という推論を避ける。XPSの結合エネルギーには化学シフトがあり3が不適切。励起X線はE=hc/λなので短波長ほど高エネルギーで、吸収端を超える内殻励起が蛍光X線を生む。')
ir={
 'N':('NMRは核スピンとラジオ波の共鳴',Y,'静磁場中でスピンを持つ核のエネルギー差に対応する高周波を用いる。'),
 'I':('IRは伸縮運動のみ',N,'結合角を変える変角・曲げ振動等も双極子を変えれば吸収する。'),
 'U':('UV–Visは電子遷移',Y,'光子吸収で分子の電子状態を励起する。'),
 'M':('強度と構造固有のモル吸光係数',L,'εは化合物の構造に関係するが、波長・溶媒・温度・化学種状態等も指定する必要がある。'),
 'F':('同じ官能基は近い吸収領域',Y,'局所的な結合の力定数と換算質量が似るため。共役・水素結合・環境によるずれはある。')}
for q,order in [('R05-REG-APPLIED-15',['N','I','U','M','F']),('R07-REG-APPLIED-14',['N','U','M','I','F'])]:
 add(q,'IRの伸縮と変角を区別し分光法の対象を対応させる。','chem_analysis','analysis49_ir','theory:analysis:ir',['analysis49_ir_ref','analysis49_beer_ref'],[ir[x] for x in order], 'IRは伸縮だけでなく変角・曲げ等の振動も観測できる。したがってのみという限定の肢を選ぶ。NMRは核スピン、UV–Visは電子遷移を対象とする。官能基の吸収領域は近似的な構造指標であり、水素結合や共役で変わり得る。','モル吸光係数を構造だけの無条件定数とはしない。波長・溶媒・化学種等を指定する条件付きの説明として保持。')
add('R05-REG-APPLIED-22','クロマトグラフィーの保持・検出・検量線を区別する。','chem_analysis','analysis49_chrom','theory:analysis:chrom',['analysis49_chrom_ref','analysis49_library_ref','analysis49_hplc_ref'],[
('検出器は常に比例応答で成分同定不可',L,'一般の濃度検出器の略説には対応するがMS検出器は質量スペクトル等を得る。FPD硫黄モードのように応答が量の二乗となる方式もあり、検出器全ての性質ではない。'),('保持値一致で同一物質と推定',L,'同条件なら同定の手掛かりになるが、異なる成分が共溶出することもある。推定と確証を区別する。'),('絶対検量線は量とピーク面積の関係',Y,'既知濃度の標準試料から応答曲線を作り未知試料へ適用する。名称に反して測定値が校正不要という意味ではない。'),('内標準に重なるピークを選ぶ',N,'各対象ピークから分離される内標準を選び、面積比等で変動を補正する。重なると双方の信号を独立に測れない。'),('標準添加でマトリックス影響を考慮',Y,'同じ試料の分取へ既知量を添加することで試料環境での応答を校正する。直線性・加算性等は確認する。')], '内標準と対象成分のピークは分離される必要がある。比を取る二信号を分けて測れない4が公式の不適切肢である。ただし1も検出器を全称化するとMSや非線形検出器に合わない。2の保持一致は同一性の推定であって単独の厳密な証明ではない。','公式4を保持。肢1はMS等の成分識別情報とFPD硫黄の非線形応答に反例がある。一般濃度検出器という限定が原典になく、全五肢の排他性を査読。')
add('R06-REG-APPLIED-19','FTIRとフィッショントラックを区別する。','chem_analysis','analysis49_acronyms','theory:analysis:acronyms',['analysis49_ir_ref','analysis49_epma_ref','analysis49_naa_ref'],[
('FTIR／フィッショントラック',N,'FTIRはFourier Transform Infrared。フィッショントラックは核分裂飛跡を用いる別方法。'),('EPMA／電子線マイクロアナライザー',Y,'Electron Probe Microanalyzerで局所に電子線を照射し特性X線等を測る。'),('GC/MS／ガスクロマトグラフ質量分析',Y,'GCで分離した成分をMSで測定する複合方法。'),('NAA／中性子放射化分析',Y,'Neutron Activation Analysis。中性子照射後に生じる放射性核種等の信号から元素を分析する。'),('XRF／蛍光X線',Y,'X-ray Fluorescenceである。')], 'フーリエ変換赤外というFTIRと、年代測定等で使う核分裂飛跡を区別する。EPMAは電子線、XRFはX線、NAAは中性子を試料へ与える。GC/MSは分離器と検出分析器の組合せである。')
add('R07-REG-APPLIED-11','高分子の種類とセルロースの水への難溶性を判断する。','chem_organic','analysis49_polymer','theory:organic:biomolecules',['organic_physical','organic_step','analysis49_cellulose_ref'],[
('PEの熱可塑性',Y,'通常のポリエチレンは鎖状高分子で、加熱して軟化させ成形できる。架橋した材料の性質まで一律に拡張しない。'),('ナイロンは合成高分子',Y,'ポリアミドの代表例で、合成で作られる。'),('二種以上のモノマーによる共重合体',Y,'化学的に異なるモノマーを同じ高分子鎖へ取り込んだ場合をいう。単なる二種ポリマーの混合とは異なる。'),('タンパク質にペプチド結合',Y,'アミノ酸残基を結ぶ主鎖のアミド結合である。'),('セルロースはOH多数で水に易溶',N,'OHは水と相互作用できるが、鎖間相互作用・結晶性等が溶解を妨げる。通常のセルロースは水に難溶。')], '親水性官能基の存在だけで溶解の自由エネルギーは決まらない。セルロースは鎖間の結合と凝集を伴い通常水に難溶であり5を選ぶ。高分子の熱可塑性、合成・天然、共重合と混合をそれぞれ独立な分類として整理する。')
add('R07-REG-APPLIED-19','比貯留率と貯留係数の次元と厚さ依存を確認する。','geo_groundwater','hydro49_storage','theory:hydro:storage',['analysis49_storage_ref','analysis49_darcy_ref','inorganic_hydro_ref'],[
('空気侵入の負圧水頭',Y,'飽和から吸引を増して空気が入る閾値。正の吸引量として表す別の符号規約と区別する。'),('透水係数は媒体固有だけではない',Y,'K=kρg/μで、流体の密度と粘性の影響も含む。'),('含水比は水質量／乾燥固相質量',Y,'通常百分率で表す。体積含水率や湿潤総質量を分母とする割合とは異なる。'),('単位体積の貯留係数を厚さ倍して比貯留率',N,'単位体積・単位水頭の量は比貯留率Ss。厚さを掛けて無次元貯留係数S=Ss bとなり、名前と関係が逆。'),('透水量係数はKと厚さの積',Y,'一定Kの水平帯水層でT=Kb。SI次元は面積／時間である。')],'比貯留率Ssは単位体積・単位水頭の放出量で次元は長さの逆数、被圧帯水層の貯留係数S=Ss bは単位面積・単位水頭で無次元である。4は体積と面積の定義を入れ替え、厚さの掛け方も逆にしている。T=Kbの次元は長さの二乗／時間。次元の比較で名称暗記の取り違えを防げる。')
assert len(Q)==28
# Existing literature key for phase equilibria is checked below, never invented.
bib=(P/'references.bib').read_text()
import re
keys=set(re.findall(r'@\w+\{([^,]+),',bib))
for e in Q:
 e['citations']=[('phase_vle' if 'phase_vle' in keys else 'os_phase_diagrams') if k=='phase_vle' else k for k in e['citations']]
(P/'config/authored_batches/S7_049_analysis.json').write_text(json.dumps({'batch_id':'S7_049_analysis','reference_date':'2026-10-13','questions':Q},ensure_ascii=False,indent=2)+'\n')
concept_path=P/'config/concepts.json';conf=json.loads(concept_path.read_text());old={x['id']:x for x in conf['concepts']}
shutil.copy2(concept_path,P/'extracted/logs/config_before_S7_049_concept.json')
for e in Q:
 if e['concept_id'] not in old:
  c={'id':e['concept_id'],'label':e['core_concept'],'pattern':e['core_concept'],'subjects':['APPLIED'],'disciplines':[e['discipline_id']]};conf['concepts'].append(c);old[c['id']]=c
conf['version']='1.42';concept_path.write_text(json.dumps(conf,ensure_ascii=False,indent=2)+'\n')
print('Authored',len(Q),'concepts',len(conf['concepts']))
