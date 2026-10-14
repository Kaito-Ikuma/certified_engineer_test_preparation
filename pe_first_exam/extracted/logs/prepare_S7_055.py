# coding: utf-8
"""Manually authored safety/consumer batch. No inference from official keys."""
import json,copy,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
R={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_055_chemistry_selection.json').read_text())['records']}
I={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_055_initial_independent.json').read_text())['records']}
T=json.loads((P/'config/authored_batches/S7_052_engineering.json').read_text())['questions'][0]
Q=[];Y='条件内で適切';N='不適切';L='条件・時点を留保'
def add(q,title,cid,section,refs,opts,solution,knowledge,ambiguity='',discipline='basic_4_1',conditions=None,figure=False,law=False):
 r=R[q];e=copy.deepcopy(T)
 e.update(question_id=q,source_sha256=r['source_sha256'],stem=title,summary=title,
  conditions=conditions or {'原典':'問題文・否定・全五候補と組合せ表を保存原典26画像で確認。','時点':r['era_year']+'の本文表現を保持。後の制度改正を遡及しない。'},
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
acid=[
 ('酢酸＞炭酸＞フェノールの酸性度',Y,'水溶液の通常の比較ではこの順。炭酸は第一解離と、溶存CO2を含む見かけの扱いを区別する。'),
 ('同濃度の塩酸と酢酸のpHが等しい',N,'塩酸は強酸、酢酸は弱酸。同じ分析濃度でも水素イオン濃度は等しくならない。'),
 ('Na/K/Ca/Baの水酸化物は水で強塩基性',Y,'溶けた部分は強塩基として作用する。溶解度がすべて同じという意味ではない。'),
 ('炭酸カルシウムと希塩酸からCO2',Y,'炭酸イオンへの酸の作用でCO2と水を生じる。'),
 ('アンモニウム塩と強塩基からNH3',Y,'アンモニウムイオンからプロトンを取りアンモニアを生じる。')]
for q,order,salt in [('H23-REG-BASIC-4-1',[0,1,2,3,4],'硫酸アンモニウムとNaOH水溶液'),('H30-REG-BASIC-4-2',[0,2,3,4,1],'塩化アンモニウムとCa(OH)2の混合物を加熱'),('R04-REG-BASIC-4-1',[0,1,2,3,4],'塩化アンモニウムとCa(OH)2の混合物を加熱')]:
 opts=copy.deepcopy(acid);opts[4]=(salt+'からNH3',Y,acid[4][2])
 add(q,'酸の強さ、同濃度pH、ガス発生を区別する。','chem55_acid','theory:basicchem:acid',['purdue_acid_strength','chem55_hydrolysis'],[opts[i] for i in order],
 '誤りは同じ0.1 mol/Lの塩酸と酢酸のpHが同じという肢。弱酸の部分解離では水素イオン濃度が分析濃度より小さい。炭酸塩への酸の作用とアンモニウム塩への強塩基の作用は別のガス発生反応として判断する。',
 '強酸と弱酸、分析濃度と解離、水酸化物の溶解度、炭酸塩、アンモニウム塩。',
 '炭酸の見かけの解離と強塩基の溶解度の限定を保持。すべての条件で同じ酸性度や溶解度を保証しない。',
 conditions={'条件':'原典の常圧又は常温・常圧。','濃度':'塩酸・酢酸各0.1 mol/L。','アンモニア生成':salt})
add('H24-REG-BASIC-4-1','ヘスの法則で五つの反応の発熱・吸熱を判定。','chem55_hess','theory:basicchem:hess',['openstax_hess'],[
 (r'CO+H2→C+H2O(液)',Y,'ΔH=-286-(-111)=-175 kJ、発熱。'),
 (r'CO+H2O(液)→H2+CO2',N,'ΔH=-394-(-111-286)=+3 kJ、吸熱。水は液体。'),
 (r'CO2→CO+1/2 O2',N,'ΔH=-111-(-394)=+283 kJ、吸熱。'),
 (r'C+CO2→2CO',N,'ΔH=2(-111)-(-394)=+172 kJ、吸熱。'),
 (r'C+2H2O(液)→2H2+CO2',N,'ΔH=-394-2(-286)=+178 kJ、吸熱。')],
 '生成熱が発熱量として正に与えられているため、生成エンタルピーはCO=-111、CO2=-394、水(液)=-286 kJ/molと読む。生成物の総和から反応物の総和を引くと、五肢のΔHは順に-175、+3、+283、+172、+178 kJ。負の1のみ発熱。',
 '生成熱の符号、反応係数、元素の標準状態、生成エンタルピー差、相。',
 conditions={'温度圧力':'25°C、1気圧。','CO':'黒鉛+1/2 O2→CO+111 kJ。','CO2':'黒鉛+O2→CO2+394 kJ。','水':'H2+1/2 O2→H2O(液)+286 kJ。'})
for q,values in [('H24-REG-BASIC-4-2',['Cu2+','Ag+','Al3+','Mg2+','Fe3+']),('H29-REG-BASIC-4-1',['Ag+','Fe3+','Mg2+','Al3+','Cu2+'])]:
 why={'Al3+':'Al(OH)3を生じ、過剰OH−で[Al(OH)4]−となって溶解。','Cu2+':'Cu(OH)2を生じるが、通常の過剰NaOHによる再溶解に対応しない。','Ag+':'通常はAg2Oを生じる。Alと同じ両性の再溶解ではない。','Mg2+':'Mg(OH)2の沈殿はこの過剰NaOHの条件では再溶解しない。','Fe3+':'Fe(OH)3の沈殿はこの通常条件では再溶解しない。'}
 add(q,'過剰NaOHで再溶解する両性水酸化物。','chem55_ampho','theory:basicchem:amphoteric',['chem55_ampho'],
 [(v,Y if v=='Al3+' else N,why[v]) for v in values],
 '最初に水酸化物が沈殿し、過剰の水酸化物イオンで溶けるという二段階を読む。Al3++3OH−→Al(OH)3、Al(OH)3+OH−→[Al(OH)4]−。両性のAlを選ぶ。別の錯形成剤で溶ける性質をNaOH添加の条件へ移さない。',
 '両性水酸化物、沈殿と溶解平衡、ヒドロキソ錯イオン。')
thermal=[
 ('高純度金属の電子による熱輸送',Y,'通常の金属では自由電子の寄与が大きい。'),
 ('合金化で純金属より熱伝導率が低下',Y,'不純物や構造の乱れが輸送を散乱する一般的傾向。'),
 ('非晶質は結晶質より熱伝導率が低い',Y,'同系材料の通常比較では乱れによるフォノン散乱が大きい。すべての別組成の比較ではない。'),
 ('気孔率を増すと熱伝導率が増す',N,'低伝導の空隙を増す通常条件では有効熱伝導率は下がる。'),
 ('結晶化率が高い高分子の熱伝導率は高い',Y,'同じ物質で規則性が増す一般的傾向。方向性や構造条件は別に検討する。')]
for q in ['H24-REG-BASIC-4-4','H26-REG-BASIC-4-4']:
 add(q,'熱輸送の担い手と材料の乱れ・気孔。','chem55_thermal','theory:basicchem:thermal',['aist_metal_thermal','openstax_thermal_conduction','chem55_polymer'],thermal,
 '不適切4。金属は電子、絶縁性結晶は主に格子振動によって熱を運ぶ。乱れや不純物による散乱、低伝導の空隙は通常熱輸送を妨げる。高分子の結晶化率も構造の規則性に関わるが、任意の別物質間の大小へ拡張しない。',
 '電子とフォノン、散乱、気孔率、有効熱伝導率、結晶化と方向性。',
 '原典の合金・非晶質・結晶化率の記述は一般的傾向として限定。同組成・構造・温度の全称にはしない。',discipline='basic_4_3')
for q,values in [('H25-REG-BASIC-4-1',['高温・高圧','低温・高圧','高温・低圧','低温・低圧','変化なし']),('H28-REG-BASIC-4-1',['変化なし','低温・低圧','高温・高圧','低温・高圧','高温・低圧'])]:
 why={'低温・高圧':'発熱の生成側へ低温が有利。気体4→2molのため高圧も有利。','高温・高圧':'圧力の作用は有利だが、高温は平衡を吸熱の分解側へ。','高温・低圧':'温度・圧力とも生成側に不利。','低温・低圧':'低温は有利だが低圧は気体モル数の多い原料側へ。','変化なし':'温度は平衡定数、圧力は気体の平衡組成へ影響する。'}
 add(q,'発熱のアンモニア合成の平衡条件。','chem55_equilibrium','theory:basicchem:equilibrium',['chem55_equilibrium'],
 [(v,Y if v=='低温・高圧' else N,why[v]) for v in values],
 'N2+3H2→2NH3は指定の式で92 kJ発熱し、気体の総モル数が4から2へ減る。平衡収率は低温・高圧により増す。温度を下げると反応速度が遅くなるため、工業運転で単純に無限低温にすればよいという意味ではない。',
 'ルシャトリエの原理、発熱と平衡定数、分圧、反応速度と平衡収率。',
 '温度と圧力が平衡に及ぼす方向を扱う問題。原典の「できるだけ」等を、速度・相変化・非理想性を無視した実装指示にしない。',
 conditions={'式':'N2(g)+3H2(g)=2NH3(g)+92 kJ。','数量':'原料気体4molに対し生成物2mol。'})
add('H25-REG-BASIC-4-2','中和当量と残る酸・塩基、塩の加水分解。','chem55_neutral','theory:basicchem:neutralization',['chem55_hydrolysis'],[
 ('硫酸とNaOH',N,'酸2当量と塩基2当量が中和し硫酸ナトリウムとなる。通常の中性近似又は硫酸イオンの弱い塩基性で扱い、酸性の組合せではない。'),
 ('硫酸とアンモニア',Y,'H2SO4 1molとNH3 2molから硫酸アンモニウム。NH4+の酸性が支配する。'),
 ('NaOHと塩酸',N,'塩基2molに酸1molなのでOH−が過剰。'),
 ('NaOHと酢酸',N,'塩基2molに酸1molなのでOH−が過剰。'),
 ('アンモニアと酢酸',N,'NH3 2molに酢酸1mol。NH3とNH4+が残り塩基性の緩衝系。')],
 'すべて1 Lなので濃度からモル数を計算する。硫酸は2酸当量、塩酸・酢酸は1、NaOHは2塩基当量、アンモニアは2。硫酸とアンモニアだけは当量中和後に弱塩基の共役酸NH4+が残り、酸性となる2。他の肢は強塩基過剰又は非酸性の塩。',
 '酸塩基当量、強弱と加水分解、過剰量、緩衝溶液。',
 conditions={'各体積':'すべて1 L。','濃度':'H2SO4 1.0、NaOH 2.0、HCl 1.0、アンモニア水2.0、酢酸1.0 mol/L。','注記':'原典NH4OH表記を、実際の水中のNH3/NH4+/OH−の平衡と区別。'})
add('H25-REG-BASIC-4-4','不動態と海水の局部腐食を区別する。','chem55_corrosion','theory:basicchem:corrosion',['chem55_corrosion','nims_hydrogen2024'],[
 ('気体中の乾食と液体中の湿食',Y,'化学的又は電気化学的な環境との反応を区別する。'),
 ('表面酸化物による不動態化',Y,'強固な膜が反応の速度を抑える。イオン化傾向だけでは耐食性を決めない。'),
 ('不動態があるから一般に海水用途へ適する',N,'塩化物は孔食やすきま腐食等を生み得る。鋼種・温度・流動等によって選ぶ。'),
 ('腐食と引張応力で強さ以下でも割れる',Y,'応力腐食割れでは特定の材料・環境・引張応力が関わる。'),
 ('侵入水素が金属を脆化',Y,'水素の侵入・拡散・欠陥との相互作用が延性や破壊へ影響する。')],
 '不適切3。不動態の形成は耐食性の理由だが、海水の塩化物中で局部腐食や応力腐食割れが起こり得る。ステンレスを一括して海水に適すると結論しない。一方、海水用の適切な高合金鋼が存在しないという逆の全称もしない。',
 '不動態、塩化物、孔食・すきま腐食、応力腐食割れ、水素脆化。',
 '炭素鋼との相対適性は鋼種・環境・防食条件で変わるため原典の一般化を留保。全ステンレスが海水で使用不可とはしない。',discipline='basic_4_3')
for q,values in [('H30-REG-BASIC-4-3',['力学的減量','局部腐食なし','Al酸化膜で不動態化','Ni5%以上でステンレス','温度依存なし']),('R05-REG-BASIC-4-4',['Al酸化膜で不動態化','Cu5%以上でステンレス','温度依存なし','局部腐食なし','力学的減量'])]:
 why={'力学的減量':'力学的な摩耗と腐食の化学・電気化学的反応を区別する。','局部腐食なし':'孔食・すきま腐食などの局部腐食がある。','Al酸化膜で不動態化':'Al表面の酸化物が保護膜として働く。膜を壊す環境での腐食まで否定しない。','Ni5%以上でステンレス':'ステンレスの基本はCr含有量。Niをこの割合含むことが定義ではない。','Cu5%以上でステンレス':'Cuをこの割合含むことが定義ではない。基本となるのはCr。','温度依存なし':'温度は反応・拡散・皮膜の挙動へ影響する。'}
 add(q,'腐食の定義とアルミニウムの不動態。','chem55_corrosion','theory:basicchem:corrosion',['stainless_definition2022','chem55_corrosion'],
 [(v,Y if v=='Al酸化膜で不動態化' else N,why[v]) for v in values],
 '適切なのはAlの酸化膜による不動態化。腐食は摩耗と異なり、局部的にも進み、環境・温度に依存する。ステンレスの定義をNiやCuの5%へ置き換えない。',
 '化学的・電気化学的腐食、局部腐食、皮膜、Crを含むステンレス。',discipline='basic_4_3')
for q,oxy,ratio,values,target in [('H25-REG-BASIC-4-6',3,None,['1:1','1:2','1:4','1:6','1:7'],3),('R02-REG-BASIC-4-5',2,6,['3 mol','4 mol','6 mol','8 mol','12 mol'],3)]:
 solution=('好気呼吸のグルコースx、発酵のyとする。酸素消費6x=3よりx=0.5 mol。CO2総発生6x+2y=7よりy=2 mol。よってx:y=0.5:2=1:4の3。' if ratio is None else '好気呼吸のグルコースxは6x=2より1/3 mol。発酵は比1:6からy=2 mol。CO2は6x+2y=2+4=6 molの3。')
 add(q,'酸素と二酸化炭素から二つの代謝量を求める。','chem55_stoich','theory:basicchem:stoichiometry',['chem55_stoich'],numeric(values,target,solution),
 solution,'反応係数とモル量、二経路の物質収支、比と絶対量。',discipline='basic_4_1',
 conditions={'好気呼吸':'C6H12O6+6O2+6H2O→6CO2+12H2O。','発酵':'C6H12O6→2C2H5OH+2CO2。','指定量':('酸素3mol吸収、CO2 7mol発生。' if ratio is None else '酸素2mol吸収、グルコースの好気:発酵=1:6。')})
for q,mAl,mCu,vals,target in [('H27-REG-BASIC-4-3',96,4,['91.1 / 8.92','93.5 / 6.51','96.0 / 4.00','97.9 / 2.11','98.3 / 1.74'],5),('R01-REG-BASIC-4-3',95.5,4.5,['95.0 / 4.96','96.0 / 3.96','97.0 / 2.96','98.0 / 1.96','99.0 / 0.96'],4)]:
 nAl=mAl/27;nCu=mCu/63.5;x=nAl/(nAl+nCu)
 solution=f'合金100gを仮定し、Alは{mAl}/27.0={nAl:.6f} mol、Cuは{mCu}/63.5={nCu:.6f} mol。合計で割り、Al={100*x:.4f}%、Cu={100*(1-x):.4f}%。質量百分率をそのまま原子百分率として使わず、原子量で割ってから規格化する。'
 add(q,'合金の質量組成を物質量分率へ変換する。','chem55_fraction','theory:basicchem:fraction',['iupac_amount_fraction'],
 numeric(vals,target,solution),solution,'質量分率、物質量、原子量、物質量分率の規格化。',discipline='basic_4_3',
 conditions={'質量百分率':f'Al {mAl}%、Cu {mCu}%。','原子量':'Al27.0、Cu63.5。','答案列':'Al / Cuの百分率。'})
add('H27-REG-BASIC-4-4','金属の資源と製錬法を組み合わせる。','chem55_metallurgy','theory:basicchem:metallurgy',['chem55_kroll','chem55_crust'],
 combo(['Al Fe Zn Mg Ti','Al Mg Zn Fe Ti','Ti Fe Al Mg Zn','Ti Fe Al Zn Mg','Ti Mg Al Fe Zn'],'Al Fe Zn Mg Ti'),
 '地殻中はAlがFeより多いが生産量はFeが多い。Znは硫化鉱、Mgは炭酸塩鉱も用い、反応性の高いAlとMgは溶融塩電解による。TiCl4はMgで還元する。Al Fe Zn Mg Tiの1。',
 '地殻存在と生産量の違い、酸化鉱・硫化鉱・炭酸塩鉱、溶融塩電解、Kroll法。',
 '2015年の世界生産量・可採年数・価格の全統計と基準日は未確認。資源埋蔵量を不変の枯渇期限としない。',discipline='basic_4_3',figure=True)
for q,vals,target in [('H28-REG-BASIC-4-3',['ア イ エ','イ エ エ','イ オ ア','ウ ウ オ','ウ オ ア'],'イ オ ア'),('R02-REG-BASIC-4-3',['ア ウ オ','ア エ オ','イ エ ア','ウ イ ア','ウ イ オ'],'ウ イ ア')]:
 conditions=({'ア':'Fe>Cu>Al。','イ':'Cu>Fe>Al。','ウ':'Al>Fe>Cu。','エ':'Cu>Al>Fe。','オ':'Fe>Al>Cu。'} if q.startswith('H28') else {'ア':'Fe>Cu>Al。','イ':'Fe>Al>Cu。','ウ':'Cu>Fe>Al。','エ':'Cu>Al>Fe。','オ':'Al>Fe>Cu。'})
 add(q,'Fe・Cu・Alの密度・抵抗率・融点の順序。','chem55_properties','theory:basicchem:properties',['openstax_resistivity','chem55_properties','chem55_properties_al','chem55_properties_fe'],
 combo(vals,target),'20°Cで密度はCu>Fe>Al、抵抗率はFe>Al>Cu。1気圧で融点はFe>Cu>Al。各大小順を先に定め、その年度のア〜オの記号に戻す。同じ三元素でも記号の割当が異なる。',
 '密度と質量、電気抵抗率、融点、温度と純度、組合せ表。',
 '材料の純度・結晶状態・温度を変えた一般的大小へ拡張しない。原典は単体の通常値の比較。',discipline='basic_4_3',figure=True,
 conditions={**conditions,'比較条件':'密度と抵抗率20°C、融点1気圧。','列順':'密度 / 電気抵抗率 / 融点。'})
add('H29-REG-BASIC-4-2','溶質粒子数と沸点上昇。','chem55_colligative','theory:basicchem:colligative',['chem55_colligative'],[
 ('すべて100°Cより低い',N,'不揮発性溶質による沸点上昇の向きと逆。'),
 ('すべて高く同じ値',N,'分析濃度が同じでも電離後の粒子数が異なる。'),
 ('NaClが最低',N,'粒子数約2のNaClは非電解質のグルコースより上昇が大きい。'),
 ('グルコースが最高',N,'電離せず粒子数1のグルコースが最小の上昇。'),
 ('CaCl2が最高',Y,'理想的な電離でCa2+とCl−2個、粒子数3に相当。')],
 '各0.10 molを純水1.0kgへ溶かす。希薄の近似でΔTb=Kbi m、iはグルコース1、NaCl2、CaCl2 3。沸点上昇はこの順に大きくなり最高はCaCl2の5。',
 '質量モル濃度、束一性、電離、van’t Hoff係数。',
 '100°Cの比較には純水の沸点100°Cとなる圧力を前提とする。実溶液の非理想性を無視した厳密なi=整数の断定にはしない。',
 conditions={'量':'各0.10mol溶質、溶媒純水1.0kg。','濃度':'各0.10mol/kg。'})
for q,values,target in [('H29-REG-BASIC-4-4',['Zn Si Cu Fe','Zn Cu Si Fe','Fe Si Cu Zn','Si Zn Fe Cu','Si Zn Fe Si'],'Zn Si Cu Fe'),('R01-RET-BASIC-4-4',['Co Si Cu Zn','C Zn Fe Cu','C Zn Fe Si','Co Si Cu Fe','Co Cu Si Fe'],'Co Si Cu Fe')]:
 add(q,'材料の用途と構成元素を対応させる。','chem55_elements','theory:basicchem:elements',['openstax_batteries','chem55_fiber','chem55_duralumin','openstax_magnetism'],combo(values,target),
 ('乾電池負極はZn、シリカ光ファイバーはSi、Al-Cu系ジュラルミンはCu、代表的な永久磁石の候補はFe。Zn Si Cu Feの1。' if q.startswith('H29') else '設問のリチウムイオン二次電池正極の代表はCo系、シリカ光ファイバーはSi、ジュラルミンはCu、磁石はFe。Co Si Cu Feの4。全リチウム電池の正極がCoを必ず含むという意味ではない。'),
 '乾電池と二次電池の電極、シリカ、Al合金、磁性材料。',
 '材料の代表例と候補の対応。Coを含まないLi正極、プラスチック光ファイバー、Feを必須としない磁石などの例外を排除しない。',discipline='basic_4_3',figure=True,
 conditions={'列順':('乾電池負極 / 光ファイバー / ジュラルミン / 永久磁石。' if q.startswith('H29') else 'Liイオン二次電池正極 / 光ファイバー / ジュラルミン / 永久磁石。')})
add('R01-RET-BASIC-4-3','標準反応ギブズエネルギーの関係式。','chem55_gibbs','theory:basicchem:gibbs',['chem55_gibbs'],
 combo(['H−S','H−TS','H−T²S','TH−S','T²H−S'],'H−TS'),
 '標準反応量でもΔrG°=ΔrH°−TΔrS°。エントロピーの単位はエネルギー/温度なので、Tを掛けるとエンタルピーと同じ単位になる。H−TSの2。',
 'ギブズエネルギー、エンタルピー、エントロピー、絶対温度と単位。',
 conditions={'指定':'標準反応エンタルピーと標準反応エントロピーを用い、Tは絶対温度。'},figure=True)
add('R02-REG-BASIC-4-2','反応図から付加・脱離・置換を区別。','chem55_organic','theory:basicchem:organic',['chem55_organic'],combo(['a b','a c','a d','b c','b d'],'a d'),
 'aは1-プロパノールのOHをBrへ置換する。bは1-フェニルエタノールから水が脱離してスチレンとなる。cは1-ブテンの二重結合にHBrが付加。dは安息香酸とメタノールから安息香酸メチルを作る求核アシル置換。置換はa,dの3。',
 '結合の変化、置換、脱離、二重結合への付加、エステル化。',
 conditions={'a':'CH3CH2CH2OH+HBr→CH3CH2CH2Br+H2O。','b':'Ph-CH(OH)-CH3→Ph-CH=CH2+H2O、酸触媒。','c':'CH3CH2CH=CH2+HBr→CH3CH2CH(Br)CH3。','d':'Ph-COOH+CH3OH→Ph-COOCH3+H2O、酸触媒。'},figure=True)
add('R03-REG-BASIC-4-2','酸化数が変わらない反応式を選ぶ。','chem55_redox','theory:basicchem:redox',['iupac_oxidation_state'],[
 ('2Na+2H2O→2NaOH+H2',N,'Na0→+1、H+1→0。酸化還元。'),
 ('NaClO+2HCl→NaCl+H2O+Cl2',N,'Cl+1と−1が0へ変わる過程を含む。酸化還元。'),
 ('3H2+N2→2NH3',N,'H0→+1、N0→−3。酸化還元。'),
 ('2NaCl+CaCO3→Na2CO3+CaCl2',Y,'Na+1、Cl−1、Ca+2、C+4、O−2が変わらない。'),
 ('NH3+2O2→HNO3+H2O',N,'N−3→+5、O0→−2。酸化還元。')],
 '酸化数の増減があるかを各元素で追う。4の形式的な交換式では全原子の酸化数が保存される。他の四反応はいずれも増減を含む。水中で4の反応が実際に右へ進むかは溶解平衡などの別の問題である。',
 '酸化数、酸化・還元、反応の分類と進行条件。')
add('R03-REG-BASIC-4-4','鉄鉱石から鉄への還元と必要質量。','chem55_metallurgy','theory:basicchem:metallurgy',['chem55_crust','chem55_iron'],[
 ('Al・高炉・還元・1429kg',Y,'元素順位、製錬法、酸化数の方向、質量収支が全て対応。'),
 ('Al・電炉・還元・2857kg',N,'指定の鉱石とコークスは高炉。160/112の倍率であり2倍の質量ではない。'),
 ('Al・高炉・酸化・2857kg',N,'Fe3+からFe0は還元。質量倍率も誤り。'),
 ('Cu・電炉・酸化・2857kg',N,'地殻順位、炉、酸化還元、質量の各条件が異なる。'),
 ('Cu・高炉・還元・1429kg',N,'地殻の順位の空欄はAlでありCuではない。')],
 '地殻の主要元素はO,Si,Al,Feの順。高炉で酸化鉄を還元する。Fe2O3は式量2×56+3×16=160、その中のFeは112。1000×160/112=1428.571...kg、最低約1429kgの1。原典の純粋Feという理想化に従い、実操業の歩留まりや銑鉄の炭素を加えない。',
 '地殻存在量、酸化鉄、高炉、CO等の還元、式量と物質収支。',
  discipline='basic_4_3',conditions={'原料':'Fe2O3、石灰石、コークス。','生成量':'Fe1000kg。','原子量':'Fe56、O16。','理想化':'鉄鉱石と銑鉄に不純物なし。'})
add('R07-REG-BASIC-4-2','希薄水溶液での酸性度を四組比較。','chem55_acid','theory:basicchem:acid',['purdue_acid_strength','yale_hydrohalic'],combo(['ア イ','ア ウ','イ ウ','イ エ','ウ エ'],'イ ウ'),
 'アはHFがHClより強いとするので誤。イはCF3基の電子求引性によりトリフルオロ酢酸が酢酸より強く正。ウはエタノールが酢酸より弱く正。エはフェノールがエタノールより弱いとするので逆。正しいイ・ウの3。',
 '酸解離、結合強度、誘起効果、共役塩基の共鳴安定化。',
 conditions={'条件':'希薄水溶液。','ア':'HF>HClの主張。','イ':'CF3COOH>CH3COOH。','ウ':'エタノール<酢酸。','エ':'フェノール<エタノールの主張。'},figure=True)

assert len(Q)==29 and set(R)=={e['question_id'] for e in Q}
for e in Q:
 e['learning_points']=e['required_knowledge']+' 対象・単位・条件を定め、判断を選択肢の番号に戻す。'
 e['calculation']='true' if e['concept_id'] in ['chem55_hess','chem55_stoich','chem55_fraction','chem55_neutral'] or e['question_id']=='R03-REG-BASIC-4-4' else 'false'
 e['evaluation'].update(knowledge_novelty='2',reasoning_steps='2',calculation_load='2' if e['calculation']=='true' else '0',difficulty_reason='反応係数・酸性度・材料条件を区別して判断する。')
out=P/'config/authored_batches/S7_055_chemistry.json';assert not out.exists()
out.write_text(json.dumps({'batch_id':'S7_055_chemistry','reference_date':'2026-10-14','questions':Q},ensure_ascii=False,indent=2))
print('Prepared',len(Q),'partial',sum(bool(e['ambiguity']) for e in Q))
