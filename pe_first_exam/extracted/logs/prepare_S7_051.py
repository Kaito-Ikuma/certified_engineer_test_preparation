# coding: utf-8
"""Manual authoring after original-image inspection and independent answers."""
import json,copy,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
R={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_051_electromagnetic_selection.json').read_text())['records']}
I={r['question_id']:r for r in json.loads((P/'config/authored_batches/S7_051_independent_answers.json').read_text())['records']}
T=json.loads((P/'config/authored_batches/S7_050_volcano_resources.json').read_text())['questions'][0]
Q=[];Y='代表的条件で適切';N='不適切';L='条件・語義を留保'
def add(q,title,cid,sections,refs,opts,solution,ambiguity='',discipline='physics_electro',law=False):
    r=R[q];e=copy.deepcopy(T)
    e.update(question_id=q,source_sha256=r['source_sha256'],stem=title,summary=title,
      conditions={'原典確認':'S7_051の11原典画像で13問の全五肢・指数・単位・否定を照合。','対象':title},
      choices={str(i):dict(value=v,verdict=z,reason=t) for i,(v,z,t) in enumerate(opts,1)},
      figures='図表問題ではない。原典画像は照合用で転載しない。',ambiguity=ambiguity,
      evidence=[f"extracted/pages/{r['source_year_directory']}/17_applied_science/page_{int(r['source_page']):03d}.png"],
      core_concept=title,required_knowledge=solution,solution=solution,answer_reason=solution,
      independent_answer=I[q]['answer_initial'],independent_solution_note='公式前の初回JSONを不変で保持。'+I[q]['reason'],
      learning_points='場・応答・担い手・材料・温度を区別し、数値の指数と単位、代表モデルの適用条件を確認する。',
      theory_references=sections,discipline_id=discipline,concept_id=cid,cross_concepts=[],
      classification_reason='全原典五肢から主題を確認：'+title,calculation='false',figure='false',law='true' if law else 'false',
      evaluation=dict(knowledge_novelty='2',reasoning_steps='2',calculation_load='0',figure_reading='0',difficulty='3' if ambiguity else '2',difficulty_reason='現象と定義を区別し、逆比例・巻数比・指数単位を照合する。'),
      citations=refs,foundationality='high',transferability='high')
    Q.append(e)
add('H23-REG-APPLIED-02','磁性の測定・模型と熱電輸送則の役割を区別する。','em51_magnetic_tools',['theory:em:magnetism'],['em51_mit_magnetic_readings','em51_wf'],[
 ('Wiedemann–Franz則',N,'金属の熱伝導率と電気伝導率の関係が中心。磁性との相対比較では最も関係が薄い。磁場の影響を受けないという意味ではない。'),
 ('Slater–Pauling曲線',Y,'合金の電子数・組成と磁気モーメントの関係を表す。'),
 ('Curie則',Y,'局在磁気モーメントの常磁性磁化率と温度の関係。'),
 ('Ising模型',Y,'離散的なスピン変数と相互作用で磁気秩序・相転移を扱う模型。'),
 ('中性子回折',Y,'中性子の磁気モーメントによる散乱で磁気秩序を調べられる。結晶構造の回折にも使われる。')],
 '輸送係数の関係である1と、磁気モーメントの模型・温度依存・磁気構造の測定を分ける。Wiedemann–Franz則はκ/(σT)=Lで、低温の弾性散乱などの条件でLorenz数を比較する。物質の磁性と全く無関係という排他命題へは変えない。')
rho={
 'warm':('300Kと100Kの抵抗',Y,'通常の金属では格子振動による散乱が高温ほど増え、室温側の抵抗が大きい。相転移や異常な材料を含む全温度の保証ではない。'),
 'cold':('−195℃と0℃の抵抗',Y,'それぞれ約78Kと273K。通常の金属の比較では0℃側が大きい。摂氏温度を比で使わない。'),
 'residual':('不純物・格子欠陥と残留抵抗',Y,'低温で格子振動の寄与が減っても不純物・欠陥による散乱は残る。組成・構造による寄与を考える。'),
 'length':('一定断面でRが長さに比例',Y,'均一な導線はR=ρL/A。同じ材料・温度・断面積を保つ条件が必要。'),
 'ohm':('電流が電位差に比例',Y,'オーム性・温度一定ならI=V/R。自己加熱でRが変わる高電圧域まで無条件には広げない。'),
 'cm':('室温の金属が10²〜10⁴Ωcm',N,'原典は正の指数でΩcm。Cuの代表値1.68×10⁻⁸Ωmは1.68×10⁻⁶Ωcm。元の範囲は1〜100Ωmに相当し、金属の典型抵抗率から大きく外れる。'),
 'm':('室温の金属が10²〜10⁴Ωm',N,'原典はΩmで、H26のΩcmと同じ数値扱いにはしない。一般的金属の代表値10⁻⁸〜10⁻⁶Ωm程度と桁が違う。'),
 'm5':('室温の金属が1〜10²Ωm',N,'原典は1〜100Ωm。一般的な金属の抵抗率の典型値より何桁も大きい。特定合金の値を全金属へ固定しない。')}
for q,order,bad in [
 ('H26-REG-APPLIED-05',['warm','residual','length','ohm','cm'],'5'),
 ('R01-REG-APPLIED-07',['length','ohm','m','warm','residual'],'3'),
 ('R05-REG-APPLIED-08',['residual','length','cold','m5','ohm'],'4')]:
 add(q,'金属抵抗の形状・温度依存と抵抗率の桁を照合する。','em51_resistivity',['theory:em:resistivity'],['openstax_resistivity','em51_resistance'],[rho[k] for k in order],
 '各回の誤りは肢'+bad+'の抵抗率の桁である。R=ρL/AとI=V/Rを、材料・断面・温度一定という条件から使う。残留抵抗と温度依存を分け、H26のΩcm、R01とR05のΩmを独立に校正した。通常金属の温度傾向を特殊な転移や全合金へ広げない。')
mag={
 'curie':('常磁性磁化率が温度とともに増加',N,'局在モーメントのCurie領域ではχ=C/Tで、絶対温度の上昇に対して減少する。伝導電子のPauli常磁性の弱い温度依存と混同しない。'),
 'neel':('反強磁性から常磁性へのNéel温度',Y,'反平行の長距離秩序が失われる温度。強磁性のCurie温度とは区別する。'),
 'elements':('Fe・Mn・Niが単体強磁性',N,'通常の室温の代表的強磁性元素はFe・Co・Ni。原典のMnをCoと読み替えない。Mnの相・温度依存は別に扱う。'),
 'demag':('反磁場が形状に依存しない',N,'磁化で生じる反磁場は試料形状と磁化分布に依存する。均一磁化した楕円体でHd=−NMと表せる。'),
 'graphite':('黒鉛は磁場中で全く力を受けない',N,'黒鉛は反磁性を持ち、不均一な磁場で力を受け得る。一様な理想場では正味の並進力がゼロでも、全条件で力がないという記述は誤り。')}
add('H27-REG-APPLIED-07','磁気秩序・残留磁化とCurie則の温度依存を区別する。','em51_magnetism',['theory:em:magnetism','theory:em:pauli'],['openstax_magnetism','em51_pauli'],[
 ('昇温で自発磁化が消えるCurie温度',Y,'通常の強磁性相は温度上昇で秩序が弱まり、Curie温度で自発磁化を失う。'),
 ('外場に反対向きの反磁性',Y,'線形応答の磁化率が負で、誘起磁化が外場と反対向きになる。'),
 mag['neel'],
 ('磁場ゼロで残る残留磁化',Y,'磁化履歴のある試料に、外場を取り去っても残る磁化。全強磁性試料が必ず大きな値を持つとは限らない。'),
 mag['curie']],
 '局在モーメントの通常のCurie常磁性でχ=C/Tとなるので5。自発磁化の消失、反磁性の符号、Néel温度、残留磁化の定義を分ける。',
 '原典の常磁性全体への表現は広すぎる。PauliやVan Vleck等を含む全常磁性に単一の温度法則を適用せず、局在モーメントのCurie領域として説明する。')
for q,order,best in [
 ('H29-REG-APPLIED-09',['curie','neel','elements','demag','graphite'],'2'),
 ('R06-REG-APPLIED-07',['curie','graphite','neel','elements','demag'],'3')]:
 add(q,'Néel温度・反磁場の形状依存・元素の磁性を照合する。','em51_magnetism',['theory:em:magnetism','theory:em:demag'],['openstax_magnetism','em51_pauli','em51_demag'],[mag[k] for k in order],
 '適切な肢'+best+'は反強磁性秩序を失うNéel温度。ほかはCurie領域の逆温度依存、MnとCoの違い、形状による反磁場、黒鉛に働き得る磁場勾配力を確認する。',
 '元素の分類は通常の室温・安定相を想定する。常磁性の全モデルへの逆温度則の一般化、黒鉛の一様場と勾配場の混同を避ける。')
add('R01-REG-APPLIED-08','Pauliのスピン応答と軌道反磁性を区別する。','em51_pauli',['theory:em:pauli'],['em51_pauli','openstax_magnetism'],[
 ('室温の鉄は強磁性',Y,'通常圧・通常の純Feは室温で強磁性。結晶構造転移と磁気秩序の転移を区別する。'),
 ('Meissner効果による完全反磁性',L,'Meissner状態では磁束を排除する。臨界磁場・温度以下の条件が必要で、II型の混合状態では量子化磁束が侵入する。'),
 mag['neel'],
 ('Curie点以上で常磁性',Y,'通常の強磁性物質ではCurie温度を超えると自発磁化秩序を失う。'),
 ('Pauli常磁性が原子核まわりの軌道運動',N,'伝導電子のスピンに外場が作用し、Fermi統計を反映した応答となる。自由電子の軌道応答はLandau反磁性として区別する。')],
 '誤りは5の起源の取り違え。局在スピンのCurie則と、Fermi準位近傍の伝導電子によるPauli常磁性を分ける。Meissner効果も超伝導の全磁場領域での完全排除へは広げない。',
 '肢2の完全反磁性はMeissner状態の条件付き。II型超伝導の混合状態を含めて全状態へ断定しない。')
add('R03-REG-APPLIED-03','誘電損失・渦電流と表皮深さを分けて高周波加熱を読む。','em51_rf_heating',['theory:em:heating'],['em51_heating','em51_skin','em51_plasma'],[
 ('誘電加熱の対象を導電体とする',N,'代表的な誘電加熱は誘電体の交流電場に対する損失を利用する。導電体を主対象とする誘導加熱と入れ替えている。有限導電率の試料で両方の損失が共存することはある。'),
 ('GHz帯の誘電加熱をマイクロ波加熱',Y,'マイクロ波電場で誘電損失を生じさせる方式。高周波誘電加熱の全周波数がGHzという意味ではない。'),
 ('誘導加熱で渦電流損・履歴損',L,'導電体に誘起された渦電流のJoule損が基本。磁化履歴による損失は強磁性体等で寄与し、すべての導電体が履歴損を持つわけではない。'),
 ('内部に侵入しない表皮効果',L,'電流・場は表面近傍へ集中するが、良導体半空間モデルでも深さに対し指数的に減衰し、数学的にゼロの侵入ではない。原典の近似表現を留保する。'),
 ('無極放電・融合プラズマの高周波加熱',Y,'プラズマにも高周波電磁場からエネルギーを供給できる。QST資料で融合プラズマのRF加熱を確認。トーチの具体的な無電極回路は別途照合する。')],
 '公式1は誘電体と導電体の入れ替えに対応する。誘電損失、導電電流のJoule損、磁化履歴損を別々に考える。表皮深さδが有限であるため、肢4の内部へ全く侵入しないという字義を正確な物理定義として教えない。',
 '公式1を保持するが肢3の全導電体への履歴損、肢4の厳密な侵入ゼロには疑義。無電極トーチの原回路も未照合でAstraへ残す。')
add('R05-REG-APPLIED-04','RLC共振・ソレノイド・理想変圧器の巻数比を照合する。','em51_transformer',['theory:em:rlc','theory:em:solenoid','theory:em:transformer'],['mit_em12','mit_em09','em51_transformer_ref','openstax_magnetism'],[
 ('直列RLCのf=1/(2π√LC)',Y,'交流電源で駆動する直列回路の電流共振ではωL=1/(ωC)。抵抗で減衰する自由振動周波数とは別である。'),
 ('ソレノイドBが巻数密度nに比例',Y,'長く端効果が小さい、電流・透磁率一定のモデルでB=μnI。飽和域でμを一定としない。'),
 ('E2=(N1/N2)E1',N,'理想変圧器は同じ時間変化磁束を共有し、E2/E1=N2/N1。原典は分子分母が逆。電圧の最大値同士でも同じ巻数比になる。'),
 ('弱い磁化が外場と同じ向きなら常磁性',Y,'通常の線形応答で小さな正の磁化率を持つ。外場なしの自発磁化を持つ強磁性と分ける。'),
 ('Fe・Ni・Co等の強磁性体をコアに利用',Y,'代表的な強磁性元素で磁束を集中できる。実際の交流コアの選定では透磁率だけでなく保磁力・渦電流損・周波数を考える。')],
 '誤りは3の逆比。各巻の起電力が共通の磁束変化に比例するので、二次の巻数が多ければ二次電圧も大きい。共振の駆動条件と長いソレノイドの近似条件も別々に確認する。')
add('R05-REG-APPLIED-09','光子波長・特性X線と電波法の周波数定義を区別する。','em51_spectral',['theory:em:spectral'],['em51_xray','em51_radio_law'],[
 ('γ線の放出・吸収の起源',Y,'核・素粒子のエネルギー変化、対消滅・対生成等に関係する。核準位の特定値はここでは使わない。'),
 ('赤外・可視・紫外の順で波長が短い',Y,'真空中でc=fλ、光子エネルギーE=hf。短波長側ほど高周波・高エネルギーとなる。'),
 ('特性X線は通常連続スペクトル',N,'原子の内殻準位差に対応する線スペクトルが特徴。X線管全体の連続成分は電子の制動放射で、特性線と共存する。'),
 ('マイクロ波は約1m以下で加熱・レーダー',Y,'用途とおおよその領域の記述。波長分類の境界規約と、法令での電波の定義を同一視しない。'),
 ('電波法は3THz以下',L,'e-Govで第二条の300万MHz以下を確認し、3THz以下へ換算できる。2023年施行版の直接取得は失敗したため当時版の時点照合は留保。')],
 '誤り3は特性線と制動放射の取り違え。エネルギー準位差の離散性と、減速する電子の多様な損失を区別する。法令の300万MHzは3×10¹²Hzで、以下の境界も保持する。',
 '令和5年の法令施行版を直接取得できていない。取得できた2024年版の第二条だけを当時版確認済みと扱わず、時点照合を要査読に残す。',discipline='physics_optics',law=True)
add('R06-REG-APPLIED-08','副殻容量・半導体の担い手とGeの四面体結合を区別する。','atomic_electron_configuration',['theory:atomic:orbital','theory:atomic:geometry','theory:em:pauli'],['atomic_quantum','em51_ge','em51_ge_structure','mit_semiconductor','em51_pauli'],[
 ('電池で自由電子が正極側へ動く',Y,'電子の負電荷による平均ドリフトは通常の電流方向と反対。各電子の熱運動を含む瞬間的な全軌道が正極へ直線的に進むわけではない。'),
 ('SiへBを添加するとp型',Y,'Bはアクセプターとして働き正孔が主要な担い手となる。結晶全体が単に正に帯電する意味ではない。'),
 ('s・p・d・fの収容数2・6・10・14',L,'同じ副殻に属する空間軌道の数1・3・5・7へ各2電子を入れた総容量。一個の空間軌道はどの種類も2電子なので原典の軌道という語を副殻群として説明する。'),
 ('Geの4s²4p²がsp²でダイヤモンド構造',N,'原典の電子配置は4s²4p²でNISTにも一致。通常のGeは四面体の4近接結合を持つダイヤモンド型で、教科書的混成モデルはsp³。sp²の三角平面と取り違え。'),
 ('Li・Naの不対スピンと常磁性',L,'孤立原子のs電子の軌道角運動量ゼロとスピンを区別する。ただしバルク金属のPauli応答はFermi統計を含み、孤立原子のCurie則をそのまま使わない。')],
 '4は四面体構造をsp²へ置き換えたことが誤り。原子の4s²4p²配置と結晶の共有結合モデルを分ける。副殻の総容量と一個の空間軌道の容量、孤立原子と金属の磁気応答も分離する。',
 '肢3の軌道という原典語は副殻群の総容量として条件を補う。肢5も孤立原子とバルク金属の常磁性機構が同じとはしない。',discipline='chem_atomic')
add('R07-REG-APPLIED-07','自発分極・圧電性と強誘電相転移の包含関係を読む。','em51_ferroelectric',['theory:em:dielectric','theory:em:ferroelectric'],['mit_ferroelectric','em51_quartz','em51_ferro_transition'],[
 ('外場なしで自発的な双極子',Y,'強誘電相の各分極ドメインに自発分極がある。多ドメイン試料で正味の分極が相殺されても局所の自発分極は否定されない。'),
 ('一般にCurie温度以上は常誘電相',Y,'典型的な強誘電体の相転移の説明。全物質の全温度経路の普遍的な単一転移へは広げない。'),
 ('圧電結晶はすべて強誘電体',N,'石英のように圧電性を持ちながら電場で反転する自発分極を持たない結晶がある。強誘電体は圧電性を持つという通常の関係の逆を保証しない。'),
 ('一次転移点で飽和分極が不連続',Y,'典型的な一次の強誘電相転移では秩序変数が不連続に変わる。有限電場での測定量や履歴の条件と熱力学の相境界を区別する。'),
 ('強誘電転移は構造相転移',Y,'通常の強誘電性ではイオン位置・配向秩序等の構造と分極が関係する。変位型と秩序無秩序型等の微視的機構を区別する。')],
 '3は包含関係を逆にした全称命題。圧電性は応力と分極・電場とひずみの結合、強誘電性は外場なしの分極とその電場反転を特徴とする。磁性のCurie温度と、分極のCurie温度も異なる秩序変数である。',
 '多ドメイン試料の正味分極、有限外場での飽和分極の測定条件を留保。一次転移の理論的秩序変数の不連続と無条件に同一視しない。')
assert len(Q)==13
out=P/'config/authored_batches/S7_051_electromagnetic.json';assert not out.exists()
out.write_text(json.dumps({'batch_id':'S7_051_electromagnetic','reference_date':'2026-10-13','questions':Q},ensure_ascii=False,indent=2)+'\n')
cfg=P/'config/concepts.json';c=json.loads(cfg.read_text());shutil.copyfile(cfg,P/'extracted/logs/config_before_S7_051_concept.json')
new=[
 ('em51_magnetic_tools','磁気模型・測定と熱電輸送則','physics_electro'),
 ('em51_resistivity','金属抵抗率・温度と単位桁','physics_electro'),
 ('em51_magnetism','磁気秩序・Curie/Néelと反磁場','physics_electro'),
 ('em51_pauli','局在スピン・Fermi統計とPauli応答','physics_electro'),
 ('em51_rf_heating','誘電損失・渦電流と表皮深さ','physics_electro'),
 ('em51_transformer','理想変圧器の電圧巻数比','physics_electro'),
 ('em51_spectral','特性X線と制動放射・電波定義','physics_optics'),
 ('em51_ferroelectric','自発分極・圧電と強誘電相転移','physics_electro')]
for cid,label,d in new:
 assert cid not in {x['id'] for x in c['concepts']}
 c['concepts'].append(dict(id=cid,label=label,pattern=label,subjects=['APPLIED'],disciplines=[d]))
c['version']='1.44-s7-051';cfg.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(Q),'questions and',len(new),'concepts')
