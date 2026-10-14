# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT
by={r['question_id']:r for r in json.loads((ROOT/'config/authored_batches/S7_035_independent_answers.json').read_text())['records']}
out=[]
T='適切'; F='不適切'; C='条件付きで適切'
def add(q,stem,cid,labels,solution,knowledge,opts,learning,cites,ambiguity='',calc=False,discipline='chem_physical'):
 r=by[q]
 out.append(dict(question_id=q,source_sha256=r['source_sha256'],stem=stem,summary=stem,conditions={'確認範囲':'問題幹、数値、式、否定、全5候補を原典画像で照合した。','成立条件':knowledge},choices={str(i):dict(value=v,verdict=t,reason=s) for i,(v,t,s) in enumerate(opts,1)},figures='図なし。リチウム電池の問題は本文の5下線部から選択する。',ambiguity=ambiguity,evidence=[r['image']],core_concept=stem,required_knowledge=knowledge,solution=solution,answer_reason=solution,independent_answer=r['independent_answer'],independent_solution_note='公式正答を参照する前に保存した初回解答を保持する。'+r['reason'],learning_points=learning,theory_references=['theory:electrochem:'+x for x in labels],discipline_id=discipline,concept_id=cid,cross_concepts=[],classification_reason='反応量・電荷・自由エネルギー又は熱電現象を決める関係式を中心に分類する。'+learning,calculation='true' if calc else 'false',figure='false',law='false',evaluation=dict(knowledge_novelty='2',reasoning_steps='3' if calc else '2',calculation_load='2' if calc else '0',figure_reading='0',difficulty='3' if q=='H26-REG-APPLIED-13' else '2',difficulty_reason='物理専攻の電荷保存・状態量の理解を利用し、化学反応の係数と材料知識を追加する。鉛蓄電池は電解液の分母質量まで更新するため三段階の計算となる。'),citations=cites,foundationality='high',transferability='high'))
def combustion(q,half=False):
 vals=[450,850,1250,1650,2050] if half else [900,1700,2500,3300,4100]
 sol=r'ベンゼンの生成式の右辺にある−49 kJは吸熱を表し、生成エンタルピーは+49 kJ/molである。燃焼式は \(\mathrm{C_6H_6(l)}+(15/2)\mathrm{O_2(g)}\to6\mathrm{CO_2(g)}+3\mathrm{H_2O(l)}\)。ヘスの法則で \(\Delta H=6(-394)+3(-286)-49=-3271\,\mathrm{kJ\,mol^{-1}}\) となる。'
 sol+=r'0.5 molでは放出熱量が \(0.5\times3271=1635.5\,\mathrm{kJ}\) なので1650 kJの4を選ぶ。' if half else '1 molの放出熱量は3271 kJであり、最も近い3300 kJの4を選ぶ。'
 why=['生成物のCO2六つと水三つの寄与を合計した値より大きく不足する。','炭素と水素の両方の酸化による発熱を正しく合計した値に達しない。','生成物と反応物のエンタルピー差から求めた値より小さい。','原典指定の量の放出熱量に最も近い。','原典の反応係数と指定物質量から求めた値より大きい。']
 add(q,'熱化学方程式を組み合わせ、指定量の液体ベンゼンの完全燃焼熱を求める。','hess_thermochemistry',['hess','heat_sign','combustion'],sol,'原典の水は液体、炭素は黒鉛、ベンゼンは液体。式に付く熱量の符号を反応エンタルピーへ変換し、指定物質量を最後に掛ける。',[(str(v)+' kJ',T if i==3 else F,why[i]) for i,v in enumerate(vals)],'反応を逆にするとエンタルピーの符号が逆転し、係数倍すると熱量も同じ倍率になる。放出熱量の正値と負の反応エンタルピーを区別する。',['openstax_hess'],calc=True)
combustion('H24-REG-APPLIED-14');combustion('H28-REG-APPLIED-12');combustion('R01-RET-APPLIED-12',True)
add('H24-REG-APPLIED-17','リチウムイオン電池の材料と、金属リチウム負極の課題を5下線部で判定する。','lithium_intercalation',['lithium','electrodes'],
 '金属リチウムの析出によるデンドライトは内部短絡を起こし得る。実用化で負極にはリチウムイオンを取り込む炭素系材料が採用され、白金という下線4が不適切である。初期の石油コークスと後の黒鉛を歴史上同一材料としない。正極のコバルト酸リチウムはLiCoO2である。',
 '原典の下線4はOCRの「自金」でなく「白金」である。標準電極電位は通常の水溶液系還元電位の基準、負極は放電時の役割として読む。',
 [('卑な',T,'通常の標準還元電位でLi+/Liは非常に負である。金属リチウムを酸化させる高電圧電池の負極としての性質につながる。'),('小さい',T,'リチウムは金属元素で最も小さいモル質量を持つ。1 molあたりの移動電子数と合わせて質量当たり容量を考える。'),('負極',T,'放電時にリチウムを酸化させ、電子を外部へ供給する側である。'),('白金',F,'この実用化経路の負極は炭素系材料であり、白金ではない。白金の不活性電極としての別の用途と混同しない。'),('コバルト酸リチウム',T,'LiCoO2はリチウムイオンの出入りを利用する実用正極材料である。')],
 '高い標準電位差だけで実用電池は決まらない。可逆にイオンを取り込むホスト、電解液、界面、短絡の抑制を合わせて読む。',['nobel_lithium2019','openstax_batteries'],ambiguity='「最も卑」は電極反応・溶媒・標準状態を原典が明記しない。通常の水溶液標準還元電位の比較として扱い、全溶媒系への全称とはしない。')
add('H25-REG-APPLIED-11','反応前後の酸化数を求め、還元に当たる変化を選ぶ。','redox_electron_balance',['oxidation_number','half_reaction'],
 r'\(\mathrm{MnO_4^-}\) ではMnの酸化数が \(x+4(-2)=-1\) より+7である。\(\mathrm{Mn^{2+}}\) では+2なので5電子を受け取る還元であり1を選ぶ。他の変化は酸化数不変又は増加である。',
 '単体の酸化数は0、単原子イオンは電荷に等しい。この問題の通常の酸化物でOは−2、H2SでHは+1である。式は変化の概略であって全反応の釣合い式ではない。',
 [(r'\(\mathrm{MnO_4^-}\to\mathrm{Mn^{2+}}\)',T,'Mnは+7から+2へ低下し還元である。'),('NaCl→NaOH',F,'Naは両側とも+1であり、Naの還元ではない。ClはCl−として別に移るなど全反応の収支が省略された表示である。'),(r'\(2\mathrm{I^-}\to\mathrm{I_2}\)',F,'Iは−1から0へ増加し、2電子を放出する酸化である。'),('Mg→MgCl2',F,'Mgは0から+2へ増加し酸化である。'),('H2S→S',F,'Sは−2から0へ増加し酸化である。')],
 '酸素の付加だけで判定せず、対象元素の酸化数と電子の受け渡しを追う。酸化数は形式的な電荷であり、共有結合内の実電荷そのものではない。',['mit_redox2014'])
add('H25-REG-APPLIED-12','二価の銅イオンの析出量から必要電荷と通電時間を求める。','faraday_electrolysis',['faraday','copper'],
 r'析出した銅は \(1.27/63.5=0.0200\,\mathrm{mol}\)。\(\mathrm{Cu^{2+}}+2e^-\to\mathrm{Cu}\) に必要な電子は0.0400 molである。\(Q=n_eF=0.0400\times96500=3860\,\mathrm C\)、\(t=Q/I=3860/5.36=720.15\,\mathrm s\) である。60で割ると約12.0分となり4を選ぶ。',
 '電流5.36 A、Cu 1.27 g、モル質量63.5 g/mol、F=96500 C/mol。全電流が電気分解に使われるという原典指定により電流効率1とする。',
 [('2分',F,'必要電荷3860 Cに対し5.36×120=643.2 Cしか流れない。'),('6分',F,'1929.6 Cであり、Cu2+に2電子が必要なことを無視するとこの時間に近付く。'),('10分',F,'3216 Cであり、指定析出量に必要な3860 Cより不足する。'),('12分',T,'3859.2 Cとなり丸めた必要電荷と一致する。'),('20分',F,'6432 Cとなり、指定析出量に必要な電荷より大きい。')],
 '物質量→電子量→電荷→秒→分の順に単位をつないで計算する。Fを銅1 molの電荷とせず電子1 molの電荷として使う。',['mit_redox2014'],calc=True)
add('H26-REG-APPLIED-13','鉛蓄電池の放電反応から、硫酸量と電解液量の両方を更新して濃度を求める。','lead_battery_mass_balance',['lead','solution_mass','faraday'],
 r'放電の全反応は \(\mathrm{Pb+PbO_2+2H_2SO_4\to2PbSO_4+2H_2O}\) で、2 molの電子に対し硫酸2 molを消費し水2 molを生成する。通過電子は \(100\times965/96500=1.00\,\mathrm{mol}\)。硫酸98 gが減り水18 gが増える。硫酸は \(300-98=202\,\mathrm g\)、電解液全体は \(1000-98+18=920\,\mathrm g\) となる。質量百分率 \(100\times202/920=21.96\%\) に最も近い22%の4を選ぶ。',
 '30質量%の電解液1000 g、100 A、965 s、F=96500 C/mol。使用後を放電と読み、全電荷が主反応へ使われ、外部との液交換や蒸発がないモデルを用いる。',
 [('11%',F,'電子1 molに対する硫酸消費量1 molと水生成量1 molを使った質量収支に合わない。'),('16%',F,'硫酸の減少と水の生成を合わせた最終質量920 gに対する202 gの比ではない。'),('20%',F,'202/1000を約20%とするのは電解液全質量を初期値のまま固定する誤りである。'),('22%',T,'硫酸202 gを最終電解液920 gで割った約21.96%に最も近い。'),('25%',F,'反応による硫酸消費98 gを反映した最終比率より大きい。')],
 '電極上の固体PbSO4へ移る質量は液相の分母から除く。硫酸が水になるという言い換えだけで分母を1000 gのまま保たない。',['openstax_batteries','mit_redox2014'],ambiguity='電流効率と外部の水損失を原典は明示しない。「使用後」を放電と解釈した主反応のみのモデルで公式4と一致する。充電や副反応を含む一般条件へ広げない。',calc=True)
add('H26-REG-APPLIED-15','ボルン・ハーバーサイクルの各過程に符号を付けてNaClの生成エンタルピーを求める。','born_haber_cycle',['born_haber','heat_sign'],
 r'Na(s)の昇華+108、Na(g)のイオン化+502、Cl2(g)半molの解離+243/2、Cl(g)の電子獲得−354、気体イオンからNaCl(s)の生成−788を加える。\(108+502+121.5-354-788=-410.5\,\mathrm{kJ\,mol^{-1}}\)。最も近い−411 kJ/molの2を選ぶ。',
 '原典の電子親和力354と格子エネルギー788は正の大きさとして与えられている。電子獲得と結晶生成はエンタルピー低下であり負符号、Cl原子1 molにはCl2を半mol解離する。',
 [('−289 kJ/mol',F,'Cl2の解離熱243を半分にせず全量使うと−289になる。NaCl 1 molに必要なCl原子は1 molである。'),('−411 kJ/mol',T,'半molの塩素分子解離と吸熱・発熱の方向をすべて反映する。'),('−471 kJ/mol',F,'指定された5過程のエンタルピー和−410.5と合わない。'),('−597 kJ/mol',F,'原典の昇華、イオン化、半解離、電子獲得、格子形成の和と合わない。'),('−1166 kJ/mol',F,'吸熱の昇華・イオン化・解離を含めた生成エンタルピーより過剰な負値である。')],
 '電子親和力と格子エネルギーは文献で符号慣習が異なる。名称だけに符号を割り当てず、反応方向を書いてから足す。',['openstax_born_haber'],ambiguity='原典は「生成熱」を負の候補で表す一方、他の熱量は正の大きさで与える。現代的な生成エンタルピーと熱化学式の右辺の発熱量の符号を区別して説明する。',calc=True)
add('H29-REG-APPLIED-07','ゼーベック・ペルティエ・トムソン効果を、温度依存と電流依存で区別する。','thermoelectric_effects',['seebeck','peltier','thomson','joule'],
 r'温度勾配を持つ導体のトムソン熱は電流に一次であり、電流反転で吸熱と発熱が入れ替わる。\(I^2R\) に従い電流反転で符号が変わらないのはジュール熱である。したがって5が不適切である。開回路の熱起電力は材料と端点温度が同じなら熱電能の温度積分で決まり、長さ・断面積を含まない。',
 '熱起電力は開回路で同じ材料・同じ両端温度を比較する。端点温度と材料を固定した熱起電力と、負荷を接続した端子電圧を区別する。',
 [('ゼーベック効果は温度差測定に利用',T,'異種材料の接点温度差から生じる起電力を熱電対の測温に用いる。'),('ペルティエ効果は熱電冷却に応用',T,'異種材料の接合部で電流方向に応じて吸熱又は発熱が起こる。'),('熱電能は温度依存',T,'ゼーベック係数S(T)は一般に材料と温度に依存し、一定値とするのは限定した温度範囲の近似である。'),('熱起電力は長さや太さに無関係',C,'材料と端点温度を固定した開回路の起電力には幾何形状が直接入らない。電気抵抗や負荷時の端子電圧、温度分布まで形状に依存しないという意味ではない。'),('トムソン熱は電流の2乗に比例',F,'トムソン熱は電流と温度勾配に一次で可逆である。二乗依存はジュール熱の特徴である。')],
 '接合部のペルティエ熱、単一導体内のトムソン熱、散逸によるジュール熱の場所と電流反転時の符号を比べる。',['mit_thermoelectric2024'],ambiguity='候補4は材料・端点温度・開回路を省略している。起電力と負荷時の端子電圧の区別を付し、一般に形状が無関係とはしない。',discipline='physics_electro')
add('R03-REG-APPLIED-06','熱電現象の名称から光学現象を区別する。','thermoelectric_effects',['seebeck','peltier','thomson','kerr'],
 'ゼーベック、ペルティエ、トムソンと熱起電力はいずれも熱と電気の結合に関わる。カー効果は電場による複屈折又は磁気光学的な偏光変化などの光学現象の名称であり、列挙された熱電現象と区別して2を選ぶ。',
 '最も不適切な用語を選ぶ。カー効果には電気光学と磁気光学の用法があるが、いずれもこの熱電効果の名称ではない。',
 [('ゼーベック効果',T,'温度差により起電力が生じる熱電現象である。'),('カー効果',F,'光の屈折・偏光に関わる名称であり、温度差と電流の相互作用を表す熱電効果ではない。'),('ペルティエ効果',T,'異種材料接合部を流れる電流に伴う吸放熱である。'),('トムソン効果',T,'温度勾配を持つ材料内の電流に伴う可逆的な吸放熱である。'),('熱起電力',T,'温度差による起電力そのものを表す用語である。')],
 '似た人名の効果を、外部の原因と観測量で分類する。熱電は温度・電流・熱流、カー効果は電磁場と光学応答である。',['mit_thermoelectric2024'],discipline='physics_electro')
def gibbs(q,modern=False):
 opts=[('酸化電極をアノード、還元電極をカソードと呼ぶ',T,'反応による定義である。放電電池と電気分解では正負の対応が異なっても、酸化・還元による名称は変わらない。'),('電池反応全体が化学平衡なら電位差0',T,r'全反応の \(\Delta_rG=0\) から \(E=0\)。個別電極界面が局所平衡である開回路状態だけとは区別する。'),('電池起電力は反応ギブズエネルギーと無関係',F,r'可逆起電力は \(\Delta_rG=-nFE\) で結ばれる。nは釣合い全反応で移動する電子のmol数である。'),('標準水素電極を0とする基準',T,'標準電極電位はこの参照電極に対する相対値として表す。単独電極の絶対電位を直接測定する意味ではない。'),('標準電池電位は両標準電極電位の差',T,r'双方を還元電位として \(E^\circ=E^\circ_{\mathrm{cathode}}-E^\circ_{\mathrm{anode}}\)。反応の係数倍で電位を倍にしない。')]
 if modern:opts=[opts[2],opts[1],opts[0],opts[3],opts[4]]
 add(q,'電池の可逆起電力と反応ギブズエネルギー、平衡、標準電極電位の関係を判定する。','electrochemical_gibbs',['gibbs','nernst','electrodes'],r'反応1 molの進行で外部へ運ばれる電荷はnFであり、可逆に取り出す電気仕事の最大値は \(-\Delta_rG\) である。したがって \(\Delta_rG=-nFE\) であり、無関係とする'+('1' if modern else '3')+'が不適切である。全電池反応の化学平衡ではE=0となるが、個々の電極が局所平衡の開回路電池で起電力が0とは限らない。','可逆・開回路の起電力を扱う。標準電極電位は共通の還元電位表で比較し、全反応の平衡と個別界面の平衡を分ける。',opts,'起電力は示強量である。反応式を倍にすると反応エネルギーと電子数が共に倍になり、Eは変わらない。',['openstax_cell_gibbs','mit_redox2014'])
gibbs('R04-REG-APPLIED-15');gibbs('R07-REG-APPLIED-10',True)
assert len(out)==12
p=ROOT/'config/authored_batches/S7_035_energy_electrochem.json';assert not p.exists()
p.write_text(json.dumps(dict(batch_id='S7_035_energy_electrochem',reference_date='2026-10-12',questions=out),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(out),'partial',sum(bool(x['ambiguity']) for x in out))
