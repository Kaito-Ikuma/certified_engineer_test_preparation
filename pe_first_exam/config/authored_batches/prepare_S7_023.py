# coding: utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')}
ini={r['question_id']:r for r in json.loads((ROOT/'config/authored_batches/S7_023_independent_answers.json').read_text())['questions']}
items=[]
def m(s):return r'\('+s+r'\)'
def add(q,summary,values,reasons,answer,solution,core,knowledge,concept,labels,cites,ambiguity='',direction='最も不適切なもの。',conditions=None,calc=False,figure=False,novel=0,steps=1,load=0,difficulty=1,verdicts=None):
 r=by[q];assert len(values)==len(reasons)==5
 units=r['discipline_id']=='physics_units'
 if verdicts is None:verdicts=['不適切' if i==answer else '適切' for i in range(1,6)]
 image='extracted/pages/'+r['source_year_directory']+'/17_applied_science/page_'+str(int(r['source_page'])).zfill(3)+'.png'
 items.append(dict(question_id=q,source_sha256=r['source_sha256'],stem=summary,summary=summary,
 conditions=conditions or {'方向':direction,'対象':'SIの定義・換算。定義の時点と指数を全肢画像で照合。' if units else '量子・原子核の性質。質量数、係数、否定と肢対応を画像照合。'},
 choices={str(i):dict(value=v,verdict=d,reason=w) for i,(v,d,w) in enumerate(zip(values,verdicts,reasons),1)},
 figures='問題幹・全5候補・単位指数・負号・核種・時点を画像照合。'+('ア〜エの対応表の全20セルを確認。' if figure else '設問固有図なし。'),
 ambiguity=ambiguity,evidence=[image],core_concept=core,required_knowledge=knowledge,solution=solution,
 independent_answer=ini[q]['independent_answer'],independent_solution_note='S7_023_independent_answers.jsonへ18原典画像を確認した後・公式前の初回を保存。'+ini[q]['reason']+' 初回を保持し一次資料で限定条件を追加。',
 answer_reason=solution,learning_points='定義の基準日を確定し、物理量の関係から指数と係数を導く。量子現象では運動量・エネルギー保存と観測対象を区別する。',
 theory_references=[('theory:units:' if units else 'theory:modern:')+x for x in labels],
 discipline_id='physics_units' if units else 'physics_modern',concept_id=concept,cross_concepts=['concept_043'] if concept=='si_definitions' else [],
 classification_reason='原典全肢の中心は'+core+'である。単位の換算と時点依存の定義、核種一般と量子物質波、線量の防護量と光素子を分離する。',
 calculation=str(calc).lower(),figure=str(figure).lower(),law='false',
 evaluation=dict(knowledge_novelty=str(novel),reasoning_steps=str(steps),calculation_load=str(load),figure_reading='1' if figure else '0',difficulty=str(difficulty),difficulty_reason='物理専攻読者に対し'+('既知の定義・指数又は一段代入で解ける。' if difficulty==1 else '定義改定・防護量等の新規性を含むか、複数段のエネルギー変換と単位を組み合わせる。')+'疑義は別軸で保持し難易度と混同しない。'),
 citations=cites,foundationality='high',transferability='high'))
missing_cd='原典の導入は6基本単位だけを列挙し、光度のcdを欠いてその他全部を組立できるとする。SIは出題時も7基本単位である。選択肢内の指数誤りは特定できるが導入の全称を正しい記述として校正完了にしない。'
N='力F=maからN='+m(r'\mathrm{kg\,m\,s^{-2}}')+'である。'
Pa='圧力p=F/SからPa='+m(r'\mathrm{kg\,m^{-1}s^{-2}}')+'である。'
J='仕事は力と移動距離の積でJ='+m(r'\mathrm{kg\,m^2s^{-2}}')+'である。'
W='仕事率はエネルギーを時間で割りW='+m(r'\mathrm{kg\,m^2s^{-3}}')+'である。'
C='電荷Q=ItよりC=Asである。'
V='電位差は仕事/電荷からV=J/C='+m(r'\mathrm{kg\,m^2s^{-3}A^{-1}}')+'である。'
Ohm='抵抗R=V/IからΩ='+m(r'\mathrm{kg\,m^2s^{-3}A^{-2}}')+'である。'
add('H23-REG-APPLIED-06','放射能・力・磁束密度・仕事率・抵抗を基本単位へ分解し、指数の誤りを選ぶ。',
 [m(r'\mathrm{Bq=s^{-1}}'),m(r'\mathrm{N=m\,kg\,s^{-2}}'),m(r'\mathrm{T=m\,kg\,s^{-2}A^{-2}}'),m(r'\mathrm{W=m^2kg\,s^{-3}}'),m(r'\mathrm{\Omega=m^2kg\,s^{-3}A^{-2}}')],
 ['放射能は単位時間の壊変数なのでBqはsの-1乗。周期周波数と同じ次元でも意味は区別する。',N,'電流に働く磁気力F=IℓBからT=N/(A m)=kg s^-2 A^-1。原典は不要なmとAの指数-2を含む。',W,Ohm],3,
 '3が指数を取り違えている。'+m(r'F=I\ell B')+'より'+m(r'[B]=\mathrm{N/(A\,m)=kg\,s^{-2}A^{-1}}')+'である。長さを一つ消し電流指数を-1にする必要がある。Bq/N/W/Ωは各物理定義から導ける。導入のcd欠落は別の疑義として保持する。',
 '物理量の定義から組立単位を導く','F=ma、p=F/S、仕事Fℓ、P=E/t、Q=It、V=E/Q、R=V/I、磁気力IℓB。','concept_043',['derived','electrical','activity'],['si_nist811','si_brochure9'],ambiguity=missing_cd,direction='誤っているもの。')
add('H25-REG-APPLIED-04','周波数・力・圧力・仕事・電圧の組立単位を比較する。',
 [m(r'\mathrm{Hz=s^{-1}}'),m(r'\mathrm{N=m\,kg\,s^{-2}}'),m(r'\mathrm{Pa=m^{-1}kg\,s^{-2}}'),m(r'\mathrm{J=m^2kg\,s^{-2}}'),m(r'\mathrm{V=m\,kg\,s^{-3}A^{-1}}')],
 ['周期Tの逆数でHz=s^-1である。',N,Pa,J,V+'原典はmの指数が1であり2ではない。'],5,
 '5の長さ指数が不足している。電圧は1Cを移す仕事で'+m(r'V=J/C')+'、'+m(r'[V]=\mathrm{kg\,m^2s^{-3}A^{-1}}')+'となる。OCRのma等を文字通り使わず原典上付きと全7基本単位を確認した。',
 '電気量を力学的エネルギーへ接続する','Hz=1/T、N=ma、Pa=N/m²、J=Nm、C=As、V=J/C。','concept_043',['derived','electrical'],['si_nist811','si_brochure9'],direction='誤っているもの。')
add('H27-REG-APPLIED-04','電荷・力・圧力・仕事率・抵抗の基本単位指数を確認する。',
 [m(r'\mathrm{C=s\,A}'),m(r'\mathrm{N=m\,kg\,s^{-2}}'),m(r'\mathrm{Pa=m^{-1}kg\,s^{-2}}'),m(r'\mathrm{W=m\,kg\,s^{-3}}'),m(r'\mathrm{\Omega=m^2kg\,s^{-3}A^{-2}}')],
 [C,N,Pa,W+'原典は長さ指数1であり、仕事の移動距離が一つ不足する。',Ohm],4,
 '4が仕事率を誤っている。'+m(r'P=F\ell/t')+'から'+m(r'[P]=\mathrm{kg\,m^2s^{-3}}')+'でありm²が必要である。電荷と抵抗も電流と時間・仕事から同じ体系で導く。導入はcdを欠くため疑義を別に残す。',
 '仕事率の長さ指数と電気量の結合','F=ma、仕事Fℓ、P=仕事/t、Q=It、R=V/I。','concept_043',['derived','electrical'],['si_nist811','si_brochure9'],ambiguity=missing_cd)
add('R05-REG-APPLIED-13','SI組立単位と動粘度の非SI単位の換算を比較する。',
 [m(r'1\mathrm C=1\mathrm{A\,s}'),m(r'1\mathrm J=1\mathrm{kg\,m^2s^{-2}}'),m(r'1\mathrm{Pa}=1\mathrm{kg\,m^{-1}s^{-2}}'),m(r'1\mathrm{St}=10^{-4}\mathrm{m^2s^{-1}}'),m(r'1\mathrm{\Omega}=1\mathrm{m^2kg\,s^{-3}A^{-1}}')],
 [C,J,Pa,'Stは動粘度cm²/s。cm=10^-2mを二乗するので10^-4m²/sである。SI基本単位そのものとは呼ばない。',Ohm+'原典はA^-1であり抵抗に必要なA^-2を欠く。'],5,
 '5の電流指数が誤りである。'+m(r'R=V/I=(J/Q)/I')+'、'+m(r'Q=It')+'より'+m(r'[R]=\mathrm{kg\,m^2s^{-3}A^{-2}}')+'。4は非SI単位StをSIへ正しく換算した記述であり、「SIでないから換算も誤り」としない。',
 '組立単位の指数と非SI換算係数','C=As、J=Nm、Pa=N/m²、Ω=V/A、動粘度St=cm²/s。','concept_043',['derived','electrical','conversion'],['si_nist811'])
add('R06-REG-APPLIED-16','圧力の慣用単位をPaへ換算し、最も遠い係数を選ぶ。',
 [m(r'1\mathrm{atm}=1.01325\times10^5\mathrm{Pa}'),m(r'1\mathrm{bar}=10^5\mathrm{Pa}'),m(r'1\mathrm{kgf\,cm^{-2}}=9.80665\times10^2\mathrm{Pa}'),m(r'1\mathrm{mmHg}=133.322\mathrm{Pa}'),m(r'1\mathrm{psi}=6.894757\times10^3\mathrm{Pa}')],
 ['標準気圧の定義係数である。実際の当地大気圧が常にこの値とはしない。','barは10^5Paの単位定義である。','kgfは標準重力9.80665m/s²で1kgに働く力9.80665N。cm²=10^-4m²で割ると9.80665e4Pa、原典は100分の1である。','通常の水銀柱換算は133.322Pa程度、液柱の実測は密度・温度・重力条件を持つ。','psiはlbf/in²で約6894.757Pa。NIST通常換算と一致する有効桁である。'],3,
 '3が2桁遠い。'+m(r'1\mathrm{kgf\,cm^{-2}}=\frac{9.80665\mathrm N}{10^{-4}\mathrm{m^2}}=9.80665\times10^4\mathrm{Pa}')+'である。原典の10²と係数を比較する。kgfとkg、面積のcm²とcmを混同しない。',
 '力単位と面積換算の二乗','標準重力9.80665m/s²、kgf=9.80665N、1cm²=10^-4m²、Pa=N/m²、atm/bar/mmHg/psiの定義と慣用係数。','concept_043',['conversion','derived'],['si_nist811'],direction='圧力換算として最も遠い値。',calc=True,load=1,difficulty=2,steps=2)
oldK='2019改定前のKは同位体組成を規定した水三重点の熱力学温度の1/273.16。通常圧凝固点とは異なる。現在はボルツマン定数kを固定する。'
rad='平面角は弧長/半径で次元1、単位radを用いる。radは角度の意味を残す記号であり、角度でない任意の比と区別する。'
newM='真空光速cを299792458m/sに固定し、秒との関係からmを定義する。'
newKg='プランク定数h=6.62607015e-34Jsを固定する。Js=kg m²/sなのでmとsの既定義と結びkgを定義する。重力定数Gを固定しない。'
newA='素電荷e=1.602176634e-19Cを固定する。C=Asなので秒と電荷の関係でAを定義する。'
newMol='NA=6.02214076e23mol^-1を固定し、1molが含む指定要素粒子数を定める。粒子の種類を明示する。'
newCd='540THzの単色放射の視感効果度Kcd=683lm/Wを固定する。光度は方向当たりの量で、現在は黒体温度を定義基準としない。'
add('H28-REG-APPLIED-06','改定前のSI基本単位の定義から、温度基準の取り違えを見つける。',
 ['秒：Cs133超微細構造遷移に対応する放射の周期。','m：定めた時間に真空を進む光の距離。','kg：国際キログラム原器の質量。','K：水の凝固点を基準。','mol：.012kgの12C中の原子数と同数の要素粒子を含む物質量。'],
 ['出題当時はCs133基底状態の二超微細準位間の放射9192631770周期を秒とした。現行も同じ周波数定数を固定する。',newM,'2016当時のkgは原器定義で適切。2019-05-20後はh固定となり原器は定義ではない。',oldK,'2016当時のmolはこの炭素12基準で適切。現在はNAを固定し、12gの12Cを定義文として使わない。'],4,
 '4が水の凝固点と三重点を取り違える。'+oldK+'出題年は2016であるため、kg原器と12C基準のmolを現在の知識だけで誤答扱いしない。定義は測定手順と区別する。',
 '時点に応じたSI基本単位の基準','旧Kの水三重点273.16K、旧kg原器・mol炭素12基準、2019-05-20改定、現行h/e/k/NA固定。','si_definitions',['history','definition','temperature'],['si_nist811','si_kelvin2007','si_cgpm2018'],novel=1,difficulty=2)
add('H29-REG-APPLIED-05','改定前の温度基準と電位・角度の単位関係を比較する。',
 ['Kは水三重点で定義。','水三重点は.01℃。','1C=As。','1V=1N C^-1。','平面角はradで無次元。'],
 [oldK,'2017の旧定義では三重点273.16KとCelsiusの273.15Kオフセットから.01℃。定義水組成条件を持つ。',C,'N/Cは電場の次元である。VはJ/C=Nm/Cなので長さが一つ不足する。',rad],4,
 '4が電位差と電場を取り違える。'+m(r'V=E_{\rm work}/Q')+'よりV=J/C=Nm/Cである。水三重点の1・2は出題時の旧K定義として読む。平面角は長さ比でrad=1の次元を持つが角の意味を保持する。',
 '温度の定義時点と電位のエネルギー基準','旧KとCelsiusオフセット、Q=It、V=仕事/Q、電場F/Q、rad=弧長/半径。','si_definitions',['history','temperature','electrical','angle'],['si_kelvin2007','si_nist811','si_cgpm2018'],novel=1,difficulty=2)
add('R01-RET-APPLIED-01','2019年5月改定後のSIを旧原器定義と区別する。',
 ['kgは国際キログラム原器の質量で定義。','水三重点は.01℃。','1C=1As。','1mは真空光が1/299792458秒に進む距離。','平面角はradで無次元。'],
 ['原器定義は2019-05-20に廃止。'+newKg,'最良推定は273.16Kすなわち.01℃であるが、新K定義では実測値と不確かさを持つ。ITS-90のT90固定点を真の熱力学温度の定義と混同しない。',C,newM,rad],1,
 '意図された誤りは1であり、2019年5月後はh固定である。2の.01℃は提示精度での約値としては整合するが、以前の厳密定義値ではない。公式1と初回1を保持し、2の精度・温度尺度の省略は別の疑義にする。',
 '定義定数と三重点の測定値の違い','新kgはh固定、秒と光速m、C=As、Celsiusオフセット273.15K、水三重点の定義から実測への変化、rad。','si_definitions',['history','definition','temperature','angle'],['si_cgpm2018','si_kelvin_realization','si_brochure9'],
 ambiguity='改定後を明記する原典の2は三重点.01℃を無条件に断定する。熱力学温度Tは改定後不確かさを持ち、ITS-90のT90と同じ厳密定義値ではない。提示桁の近似としては妥当、厳密さが未指定である。公式・初回1は維持し原器誤りと別に疑義を保持。',
 novel=1,difficulty=2,verdicts=['不適切','近似として適切・厳密さ疑義','適切','適切','適切'])
for q,vals,keys,ans in [
 ('R02-REG-APPLIED-09',['mは真空光速で定義。','kgは重力定数で定義。','Aは電気素量で定義。','Kはボルツマン定数で定義。','molはアボガドロ定数で定義。'],['m','kgwrong','A','K','mol'],2),
 ('R03-REG-APPLIED-09',['cdは黒体放射で定義。','mは真空光速で定義。','kgはプランク定数で定義。','秒はCs超微細遷移周波数で定義。','molはアボガドロ定数で定義。'],['cdwrong','m','kg','s','mol'],1),
 ('R07-REG-APPLIED-09',['mは真空光速で定義。','Aは素電荷で定義。','kgは重力定数で定義。','molはアボガドロ定数で定義。','cdは単色放射で定義。'],['m','A','kgwrong','mol','cd'],3)]:
 rs={'m':newM,'kgwrong':newKg+'原典の重力Gとの対応が誤り。','kg':newKg,'A':newA,'K':'k=1.380649e-23J/Kを固定し、エネルギー尺度と温度尺度を結ぶ。','mol':newMol,'s':'Cs133の摂動のない基底状態超微細遷移周波数9192631770Hzを固定する。','cd':newCd,'cdwrong':newCd+'黒体基準は1979以前の歴史的定義に関係する。'}
 add(q,'現行SIの基本単位と定義定数の対応を判定する。',vals,[rs[k] for k in keys],ans,
 ('黒体を使う1が誤り。'+newCd if ans==1 else str(ans)+'のkgと重力定数Gの対応が誤り。'+newKg)+' 定数一つが他単位から独立に一単位を定義するわけではない。既に固定された時間・長さ等の体系と結ぶ。',
 '基本単位の定数による定義','2019改定のh/e/k/NA、Cs周波数、c、単色540THz視感効果度、定義と実現の区別。','si_definitions',['definition','history','photometry'],['si_cgpm2018','si_brochure9'],novel=1,difficulty=2)
add('H23-REG-APPLIED-10','天然壊変・熱中性子核分裂・β安定・透過と内部影響・γ脱励起を区別する。',
 ['自然UとThはα・β壊変を経て安定Pbへ至る。','238Uへ熱中性子を当て核分裂連鎖反応で発電。','同質量数の核はその中の最小質量へ向けてβ壊変。','α線は紙で止まるが、放出核種を体内へ取り込むとダメージが大きい。','γ放出はエネルギー準位が変わり原子番号は変わらない。'],
 ['主要な天然U238/U235とTh232の壊変系列の終点は安定Pb同位体。原子番号を変えるα・βと核準位遷移を分ける。','通常の熱中性子連鎖反応では235U等の核分裂性核種を用いる。238Uは高速中性子核分裂や捕獲後Pu生成の役割を持ち、熱核分裂性とは区別する。','β壊変はエネルギー的に可能な隣接Zへ進む。偶数Aでは偶偶・奇奇質量が別放物線となり、単一βに安定な核が複数あり得る。最小質量へ必ず単一βで進む全称は不正確。','外部αの透過は弱いが内部取込みでは短い距離に高密度にエネルギーを与え得る。影響は量・核種・摂取経路・組織への分布等で変わるので無条件に一定被害を割り当てない。','γは同じ核種の励起準位からの電磁遷移で、AとZを保つ。α・β後に伴うγは先行壊変で変わったZと区別する。'],2,
 '2の238Uと熱中性子が取り違えである。235U等の熱核分裂、238Uの高速核分裂・中性子捕獲を分ける。3はβ安定へ質量が減る一般傾向を述べるが、偶奇性と隣接核のQ値を省いた全称では成り立たない。公式2・独立2を保持し3の文字通りの一意性は査読対象に残す。',
 '核反応のエネルギー条件と保存するA・Z','αでA-4/Z-2、βでA一定/Z±1、γで核種不変、熱核分裂と高速核分裂、質量放物線と対エネルギー、内部と外部の透過条件。','concept_044',['nuclear','stability','fission','dose'],['modern_mit_nuclear','modern_mit_mass','modern_doublebeta','modern_fastfission','modern_alpha','modern_series'],
 ambiguity='原典3は同質量数の最小質量核へβ壊変するという全称。単一β安定核が複数となる偶数Aの対エネルギーを省く。二重βの実在は単一β経路とは別である。原典4は内部取込みの量・経路条件を省く。公式・初回2を保持し、3の科学的排他性は未確定。',
 direction='誤っているもの。',novel=1,steps=2,difficulty=2,verdicts=['主要天然系列で適切','不適切','一般傾向・全称疑義','適切（影響条件付き）','適切'])
add('H25-REG-APPLIED-07','同じ速さを持つ粒子の物質波長を質量比から並べる。',
 ['陽子→α→電子','α→陽子→電子','電子→α→陽子','陽子→電子→α','電子→陽子→α'],
 ['電子は最軽量で最長波長なので最後にはならない。','質量の大きい順を波長の大きい順へ取り違えている。','電子は先頭だがαは陽子より重く、αの波長は短い。','陽子より軽い電子が最長であり最初の2者が逆。','静止質量は電子<陽子<α。同速ではγも共通、p=γmvは質量に比例、λはその逆なのでこの順になる。'],5,
 '5である。'+m(r'\lambda=h/p,\quad p=\gamma mv')+'。同じ速さではγとvは共通なので'+m(r'\lambda\propto1/m')+'、電子、陽子、αの順となる。非相対論近似ならp=mvで同じ結論であり、同運動エネルギーという別条件を混ぜない。',
 '物質波長を運動量で比較する','λ=h/p、同速のγ共通、電子・陽子・α核の静止質量の順、速度ゼロで波長比較をする極限は除く。','photon_matter_wave',['matter'],['os_matter'],direction='長い順番として適切。',verdicts=['誤順序']*4+['適切'],steps=2,difficulty=2)
add('H27-REG-APPLIED-05','加速電子の運動エネルギーから連続X線の最短波長を求める。',
 [m(r'2.6\times10^{-11}\mathrm m'),m(r'3.5\times10^{-11}\mathrm m'),m(r'3.9\times10^{-11}\mathrm m'),m(r'9.1\times10^{-11}\mathrm m'),m(r'9.9\times10^{-11}\mathrm m')],
 ['求めた3.5357e-11mより小さく、本条件の電子エネルギー限界を超える。','3.5357e-11mへ最も近い提示値。','限界より長い波長の光子は放出され得るが最短値として2より遠い。','連続線にこの波長が存在し得ることと最短端であることは別、算出値から遠い。','この値も最短端ではなく、eVを全て一光子へ与える上限と一致しない。'],2,
 '初期運動エネルギーを無視する電子が電圧Vで得るK=eVを、一光子へ最大限移すと'+m(r'hc/\lambda_{\min}=eV')+'である。'+m(r'\lambda_{\min}=\frac{6.6\times10^{-34}\times3.0\times10^8}{1.6\times10^{-19}\times35\times10^3}=3.5357\times10^{-11}\mathrm m')+'より2。現行h/eの精密値へ置き換えず指定丸め値を使う。電子速度の非相対論近似は不要である。',
 '制動放射の端をエネルギー保存で求める','電圧仕事eV、光子E=hc/λ、全エネルギーを一光子へ渡す最短端、kV=10³V、指定h/e/c。','photon_matter_wave',['xray','duality'],['os_photoelectric'],
 direction='連続X線の最短波長に最も近い値。',conditions={'方向':'最短波長に最も近い値。','加速電圧':'35kV','h':m(r'6.6\times10^{-34}\mathrm{J\,s}'),'e':m(r'1.6\times10^{-19}\mathrm C'),'c':m(r'3.0\times10^8\mathrm{m/s}')},calc=True,load=2,steps=2,difficulty=2,verdicts=['不一致','最も近い','不一致','不一致','不一致'])
for q,half,t,values,answer in [
 ('H26-REG-APPLIED-09',30,90,['1/6','1/8','1/9','1/16','1/18'],2),
 ('H28-REG-APPLIED-09',8,30,['.20','.15','.07','.05','.03'],3),
 ('R04-REG-APPLIED-09',9,30,['.20','.10','.05','.03','.01'],2)]:
 unit='年' if q.startswith('H26') else '日'
 result=2**(-t/half)
 reasons=[]
 for i,x in enumerate(values,1):
  v=1/int(x[2:]) if x.startswith('1/') else float(x)
  reasons.append(('計算結果と一致する。' if q.startswith('H26') else '計算値へ5候補中で最も近い。') if i==answer else 'N/N0=2^(-t/T)で得る'+format(result,'.6g')+'と比較すると'+x+'は'+('小さすぎる。' if v<result else '大きすぎる。')+(' 適切肢より差が大きい。' if not q.startswith('H26') else ' 時間の比を線形に割るのではない。'))
 add(q,'半減期と経過時間の比から残存する親核種の割合を求める。',values,reasons,answer,
 '生成・流出入を除き一定壊変率なら'+m(r'dN/dt=-\lambda N')+'を積分して'+m(r'N/N_0=e^{-\lambda t}=2^{-t/T_{1/2}}')+'。'+m('t/T_{1/2}='+str(t)+'/'+str(half))+'から残存比は'+format(result,'.7g')+'、'+str(answer)+'の'+values[answer-1]+'を選ぶ。残った親核種量と壊変済み割合1−N/N0を区別する。',
 '半減期は指数減衰の時間尺度','一定壊変定数、T=ln2/λ、N/N0=2^(-t/T)、親核種量、指定時間の同単位化。','concept_044',['decay'],['modern_mit_nuclear'],
 direction='残存する元の核種量の割合に最も近い値。',conditions={'方向':'最も適切。' if q.startswith('H26') else '最も近い値。','半減期':str(half)+unit,'経過時間':str(t)+unit,'対象':'元の放射性核種の残存量、生成等なし。'},calc=True,load=1,verdicts=['適切' if i==answer else '不一致' for i in range(1,6)])
add('H27-REG-APPLIED-06','吸収エネルギーと防護上の重み付けを、線量名と単位の対応表へ結び付ける。',
 ['吸収線量／Bq／等価線量／Sv','等価線量／Gy／吸収線量／Bq','吸収線量／Sv／等価線量／Gy','等価線量／Sv／吸収線量／Gy','吸収線量／Gy／等価線量／Sv'],
 ['ア・ウ・エは対応するが吸収線量のイはGyでありBqは壊変率。','アとウが逆である。吸収線量にGy、等価/実効線量にSvを使うのでエBqも誤り。','アとウは適切だがGyとSvを逆にしている。次元が同じでも量の意味が違う。','Svが等価線量、Gyが吸収線量なのはよいが、原典のアは質量当たりエネルギーなので吸収、ウは放射線重み付け後なので等価。名称を逆にした。','アは吸収線量D、イGy、ウは等価線量HT、エSvである。実効線量EもSvだが組織重み付けをさらに持つ。'],5,
 '5である。質量当たり吸収エネルギー'+m(r'D=d\epsilon/dm')+'の単位はGy=J/kg。組織Tへの放射線Rの平均吸収線量に無次元重みwRを掛け'+m(r'H_T=\sum_Rw_RD_{T,R}')+'とするとSv。さらに'+m(r'E=\sum_Tw_TH_T')+'が実効線量でSvである。Bqは壊変/秒であってエネルギー/質量ではない。',
 'エネルギー量と生物影響を考慮する防護量','吸収線量D、Gy=J/kg、HT=sum wR DTR、E=sum wT HT、Sv、Bq=s^-1、重みは無次元。','radiation_dosimetry',['dose','activity'],['modern_dose','si_brochure9'],
 direction='ア・イ・ウ・エの組合せとして最も適切。',conditions={'ア':'単位質量当たりの吸収エネルギー','イ':'アの単位','ウ':'放射線荷重係数をアへ乗じた量（原典の名称）','エ':'ウと実効線量の単位','方向':'最も適切な組合せ。'},figure=True,novel=1,steps=2,difficulty=2,verdicts=['単位不適切','名称と単位不適切','単位逆','名称逆','適切'])
add('R05-REG-APPLIED-07','光と電子の励起・再結合を利用する素子と、超伝導の巨視的量子現象を比較する。',
 ['太陽電池','発光ダイオードLED','半導体レーザー','超伝導（超電導）','有機EL'],
 ['光吸収で電子・正孔を作り電流として取り出す。光から電気への変換であり光電子相互作用を利用する。','注入した電子と正孔の放射再結合で光を出す。電気から光への変換である。','活性層の電子励起と反転分布、光電磁場による誘導放出・共振器帰還を利用する。','超伝導は電子対等の巨視的な量子状態に伴う無抵抗・磁場応答の現象である。光吸収/放出素子とは主原理が異なる。光と超伝導体が相互作用しないという断言ではない。','有機半導体へ電荷を注入し、励起子等の放射緩和で光を出す。分子励起も電子励起に含む。'],4,
 '4がこの分類で最も不適切である。1は光吸収で電子励起を作り電流へ、2・3・5は励起された電子状態の放射緩和・誘導放出で光へ変換する。一方、超伝導は低温の凝縮量子状態の電気磁気応答が主原理である。光励起で超伝導を変化させる研究が存在し得ることとは別の比較である。',
 '光素子の吸収・自発放出・誘導放出の役割','光子E=hf、半導体の電子正孔、分子励起、光吸収と放射再結合、レーザーの反転分布/共振器、超伝導の凝縮状態。','optoelectronic_devices',['devices','superconduct','duality'],['modern_pv','modern_led','modern_laser','modern_oled','modern_superconduct','modern_pairs'],novel=1,steps=2,difficulty=2,
 verdicts=['該当','該当','該当','主原理が異なる','該当'])
assert len(items)==19
(ROOT/'config/authored_batches/S7_023_modern_units.json').write_text(json.dumps(dict(batch_id='S7_023_modern_units',reference_date='2026-10-11',scope='単位系11・現代物理8、18原典画像、19初回公式一致。導入cd欠落2・改定後三重点・beta安定全称の4疑義を保持。',questions=items),ensure_ascii=False,indent=2)+'\n')
print('prepared',len(items),'partial',sum(bool(e['ambiguity']) for e in items))
