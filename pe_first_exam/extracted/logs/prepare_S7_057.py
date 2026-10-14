# coding: utf-8
"""Manually authored safety/consumer batch. No inference from official keys."""
import json,copy,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
R={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_057_selection.json').read_text())['records']}
I={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_057_initial_independent.json').read_text())['records']}
T=json.loads((P/'config/authored_batches/S7_052_engineering.json').read_text())['questions'][0]
Q=[];Y='条件内で適切';N='不適切';L='条件・時点を留保'
def add(q,title,cid,section,refs,opts,solution,knowledge,ambiguity='',discipline='basic_4_1',conditions=None,figure=False,law=False):
 r=R[q];e=copy.deepcopy(T)
 e.update(question_id=q,source_sha256=r['source_sha256'],stem=title,summary=title,
  conditions=conditions or {'原典':'問題文・否定・全五候補と組合せ表を保存原典55画像で確認。','時点':r['era_year']+'の本文表現を保持。後の制度改正を遡及しない。'},
  choices={str(i):dict(value=v,verdict=z,reason=t) for i,(v,z,t) in enumerate(opts,1)},
  figures='原典組合せ表の各行を独自要約。元画像は転載せず照合用に保存。' if figure else '文章の五肢。元画像は転載せず照合用に保存。',
  ambiguity=ambiguity,evidence=[f"extracted/pages/{r['source_year_directory']}/{Path(r['source_file']).stem}/page_{int(r['source_page']):03d}.png"],
  core_concept=title,required_knowledge=knowledge,solution=solution,answer_reason=solution,
  independent_answer=I[q]['independent_answer'],independent_solution_note='初回JSONと公式比較JSONを保存。'+I[q]['reason']+' 選択情報には公式メタデータも存在し、完全盲検とはしない。',
  learning_points='対象・責任主体・時点・要件を分け、文の否定と「全て」「不要」の範囲を点検する。知識を当てはめる前に何を証明する資料かを確かめる。',
  theory_references=[section],discipline_id=discipline,concept_id=cid,cross_concepts=[],
  classification_reason='原典の主題と全候補を照合：'+title,calculation='false',figure='true' if figure else 'false',law='true' if law else 'false',
  evaluation=dict(knowledge_novelty='2',reasoning_steps='2',calculation_load='0',figure_reading='1' if figure else '0',difficulty='3' if ambiguity else '2',difficulty_reason='定義と制度の時点を照合し、組織的な図・数式の成立条件を区別する。'),
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
 add(q,title,'finish57_'+key,theory,refs or [],numeric(values,answer,'解法の条件と結果を照合する。') if all(isinstance(v,(int,float)) for v in values) else combo(values,values[answer-1]),sol,knowledge,ambiguity,d,conditions,figure)
def detailed(q,title,key,d,theory,opts,sol,knowledge,conditions,refs=None,ambiguity=''):
 add(q,title,'finish57_'+key,theory,refs or [],opts,sol,knowledge,ambiguity,d,conditions)

def mech(q,title,key,values,answer,sol,conditions,knowledge,ambiguity='',d='basic_3_4',refs=None):
 item(q,title,key,d,'theory:analysis:'+key,values,answer,sol,knowledge,conditions,refs or [],ambiguity,True)

for q,vals,a in [
 ('H23-REG-BASIC-3-2',['(0,>3σ,0)','(>0,>3σ,0)','(0,>3σ,>0)','(0,<3σ,0)','(>0,<3σ,0)'],1),
 ('R01-RET-BASIC-3-6',['(0,<3σ,0)','(0,>3σ,0)','(0,>3σ,>0)','(>0,<3σ,0)','(>0,>3σ,0)'],2)]:
 mech(q,'楕円孔端で自由表面と応力集中を併用。','inglis',vals,a,
 'A(a,0)の孔縁の法線はx方向。外力を受けない孔面なのでσx=τxy=0。一方、接線方向のσyは自由表面でも消えない。Inglis解σy=(1+2a/b)σでa>bなので3σより大きい。三成分の順を元表に戻す。',
 {'孔':'x方向半軸a、y方向半軸b、a>b。','荷重':'遠方y方向一様引張σ>0。','地点':'A=(a,0)、列順σx,σy,τxy。'},
 '自由表面の応力ベクトル、法線と接線、楕円孔の応力集中。',
 'Inglis式は十分広い等方線形弾性板の理想化。有限幅・塑性・鋭い亀裂先端へそのまま数値を外挿しない。',refs=['analysis57_inglis'])

for q,vals,a in [
 ('H23-REG-BASIC-3-4',['fa<fb<fc','fa<fc<fb','fb<fa<fc','fb<fc<fa','fc<fa<fb'],3),
 ('H28-REG-BASIC-3-5',['fb<fa<fc','fa<fc<fb','fa<fb<fc','fb<fc<fa','fc<fa<fb'],1)]:
 mech(q,'梁の固有振動数は支持条件から比較。','beamfreq',vals,a,
 '一様Euler–Bernoulli梁のω1=β1²√(EI/(ρA))/L²。同じ梁なら共通係数が消える。片持ちbはβ1≈1.875、単純支持aはπ、両端固定cは≈4.730なのでfb<fa<fc。固定端を増やすと拘束が強くなるが、名称だけで判断せず境界条件の固有値を比較する。',
 {'a':'両端単純支持。','b':'片持ち。','c':'両端固定。','共通':'同じ長さ・材質・断面、最も低い曲げモード。'},
 '曲げ振動、変位と回転の境界条件、固有値。',
 '一様細長梁・線形小振動の標準モデル。せん断変形・回転慣性を含む短い梁へ厳密な値を一般化しない。')

for q,vals,a,ratio in [
 ('H24-REG-BASIC-3-5',['(0,−P)','(−P/4,−3P/4)','(−P/2,−P/2)','(−3P/4,−P/4)','(−P,0)'],4,3),
 ('H26-REG-BASIC-3-6',['(−P,0)','(−2P/3,−P/3)','(−P/2,−P/2)','(−P/3,−2P/3)','(0,−P)'],2,2),
 ('R07-REG-BASIC-3-4',['(−P,0)','(−4P/5,−P/5)','(−P/2,−P/2)','(−P/5,−4P/5)','(0,−P)'],2,4)]:
 mech(q,'両端固定棒の荷重点変位から反力を求める。','fixedbar',vals,a,
 '荷重点の右向き変位をuと置く。左区間の伸びuと右区間の縮みuから、反力はPA=−EAu/lleft、PB=−EAu/lright。釣合PA+PB+P=0と合わせる。左右剛性比'+str(ratio)+':1なのでPA=−'+str(ratio)+'P/'+str(ratio+1)+'、PB=−P/'+str(ratio+1)+'。短い区間の反力が大きく、どちらも図の正方向に対して負。',
 {'支持':'両端固定、荷重点の左長さ：右長さ=1:'+str(ratio)+'。','材料':'一様E,A、微小軸変形。','符号':'Pは右向き、両反力も右向きを正として記入。'},
 '軸剛性EA/l、変形適合、不静定棒、力の符号。',refs=['mit_material_elastic2000'])

mech('H25-REG-BASIC-3-1','三次元Hooke則のPoisson結合。','hooke',
 ['Eσx','E(σx+ν(σy+σz))','E(σx−ν(σy+σz))','(σx+ν(σy+σz))/E','(σx−ν(σy+σz))/E'],5,
 'x方向の引張応力はσx/Eの正ひずみを作る。y,z方向の引張は横収縮を通じて各−νσ/Eを加えるのでεx=[σx−ν(σy+σz)]/E。弾性係数を掛けるとひずみが無次元にならず、横応力の符号を正にすると収縮の向きも逆になる。',
 {'材料':'均質等方の線形弾性体。','記号':'垂直応力σx,σy,σz、E、Poisson比ν。'},'三次元構成則、横収縮、応力とひずみの次元。',refs=['mit_material_elastic2000'])

for q,vals,a in [
 ('H25-REG-BASIC-3-2',['aのみ','bのみ','cのみ','a,b','b,c'],3),
 ('H29-REG-BASIC-3-6',['a,b','b,c','aのみ','bのみ','cのみ'],5)]:
 mech(q,'同面積でも曲げ方向の断面高さが効く。','section',vals,a,
 'xy面内の曲げではz軸回りIz=bh³/12。aは幅d×高さ4dで16d⁴/3、bは2d×2dで4d⁴/3、cは幅4d×高さdでd⁴/3。cの曲げ剛性EIが最小なので撓みが最大。面積はいずれも4d²でも、曲げでは高さの三乗を使う。',
 {'断面':'a:幅z=d・高さy=4d、b:2d×2d、c:幅z=4d・高さy=d。','共通':'同じE、梁長さ、支持、荷重、断面積4d²。','曲げ':'xy面内。'},
 '断面二次モーメント、曲げ軸、曲げ剛性、撓み。',refs=['struct_mit_beam'])

mech('H25-REG-BASIC-3-5','軸伸びと弾性エネルギーの二分の一。','axialenergy',
 ['P=EAδ/l,U=EAδ²/l','P=EAδ/l,U=EAδ²/(2l)','P=EAδ/(2l),U=EAδ²/l','P=EAδ/(2l),U=EAδ²/(2l)','P=EAδ/(2l),U=EAδ²/(4l)'],2,
 'ε=δ/l、σ=Eε、P=Aσ=EAδ/l。線形に力を増す仕事U=∫0^δ(EA/l)x dx=EAδ²/(2l)=Pδ/2。最終荷重Pを全行程に掛けたPδでは仕事を二倍に数える。',
 {'棒':'長さl、断面積A、E一定。','伸び':'軸伸びδ、弾性域の準静的負荷。'},'応力・ひずみ、力変位線図、弾性ひずみエネルギー。',refs=['mit_material_elastic2000'])

for q,vals,a,layout in [
 ('H26-REG-BASIC-3-5',['a','b','c','a,b','b,c'],2,'a並列、b直列、c左右の壁'),
 ('R06-REG-BASIC-3-5',['a','b','c','a,b','b,c'],3,'a並列、b左右の壁、c直列')]:
 mech(q,'ばねの並列・直列と両側支持を区別。','spring',vals,a,
 '並列では同変位の力が加わりkeff=2k。直列では同じ力に対する伸びが加わりkeff=k/2。質点の両側を壁へつなぐ二本は、右へ動かすと左の伸びと右の縮みがともに左向き復元力を作り2k。ω=√(keff/m)が最小なのは直列。配置のa,b,cが年度で入れ替わるので番号を転用しない。',
 {'配置':layout,'共通':'ばね二本ともk、質点m、ばね質量・摩擦・減衰を無視。'},'等価ばね定数、復元力の符号、角振動数。',d='basic_3_0',refs=['analysis57_shm'])

mech('H27-REG-BASIC-3-2','偏微分で勾配を作ってから座標を代入。','gradient',
 ['(1,−4)','(4,−1)','√17','3','−3'],2,
 'ψ=2x−x²yの勾配は(∂ψ/∂x,∂ψ/∂y)=(2−2xy,−x²)。x=1,y=−1を入れると(4,−1)。√17はこのベクトルの大きさであって勾配そのものではない。先に点の値を代入してψを定数にすると微分情報が失われる。',
 {'関数':'ψ(x,y)=2x−x²y。','点':'(1,−1)。'},'偏微分、勾配、ベクトルとノルム。',d='basic_3_9')
mech('H27-REG-BASIC-3-4','薄板の垂直軸定理で慣性モーメントを比較。','inertia',
 ['Ixのみ','Iyのみ','Izのみ','Ix,Iy','Ix,Iz'],3,
 '重心を通る面内x軸はIx=M(2a)²/12=Ma²/3、y軸はIy=Ma²/12。面外z軸には垂直軸定理Iz=Ix+Iy=5Ma²/12を用いる。Ix>Iyでも和のIzがさらに大きいのでzのみ。',
 {'薄板':'一様な長方形、x方向a、y方向2a。','軸':'重心を通る直交三軸、zは面外。'},'質量慣性モーメント、垂直軸定理、重心軸。',d='basic_3_7')
mech('H27-REG-BASIC-3-5','異材両端固定棒の荷重点剛性。','compositebar',
 ['Pl/(2SE1)','Pl/(2SE2)','Pl/[2S(E1+E2)]','3Pl/[2S(2E1+E2)]','Pl/[2S(E1−E2)]'],3,
 '荷重点の左右はそれぞれl/2なので軸剛性は2SE1/lと2SE2/l。変位δに対し一方の伸びと他方の縮みがともに復元力を作る。P=[2S(E1+E2)/l]δ、従ってδ=Pl/[2S(E1+E2)]。E1=E2にしても分母が0にならず、均質な両端固定棒へ戻る。',
 {'棒':'全長l、各区間l/2、断面積S一定、左E1・右E2。','支持':'両端固定、中央に軸方向P。'},'異材の軸剛性、適合と釣合、極限検算。',refs=['mit_material_elastic2000'])
mech('H27-REG-BASIC-3-6','等しい片持ち撓みから形状比を求める。','cantilever',
 ['ad=0.5','ad=2.5','a/d=0.5','a/d=2','a/d=2.5'],4,
 '先端荷重撓みδ=PL³/(3EI)。梁1の正方形断面はI1=(l/4)^4/12=l⁴/3072。梁2は幅l/32、高さdなのでI2=ld³/384。等しい撓みからl³/I1=a³/I2、a³/d³=8、a/d=2。長さの積adは無次元の形状比とならない。',
 {'梁1':'長さl、正方形一辺l/4。','梁2':'長さa、断面幅l/32、高さd。','共通':'同じE、先端荷重P、片持ち梁、等しい先端撓み。'},'梁撓み、曲げ軸、断面二次モーメント、次元。',refs=['struct_mit_beam'])
mech('H28-REG-BASIC-3-6','平行な棒の共通伸びから応力比を求める。','parallelbar',
 ['AAEA/(ABEB)','ABEB/(AAEA)','ABEA/(AAEB)','EA/EB','EB/EA'],4,
 '両棒は等しい長さLで剛体端板に接続され、端板の回転が拘束されるため伸びδが共通。εA=εB=δ/Lで、σA/σB=EA/EB。軸力の比ならNA/NB=AAEA/(ABEB)だが、問は応力なので断面積は消える。',
 {'棒':'等長L、A棒のAA,EAとB棒のAB,EB。','端':'剛体板で共通軸変位、原典の平行配置。'},'共通ひずみ、応力と軸力の区別。',refs=['mit_material_elastic2000'])

orders=['Ra<Rb<Rc','Ra<Rc<Rb','Rc<Ra<Rb','Rc<Rb<Ra','Rb<Ra<Rc']
for q,a,lay in [('H29-REG-BASIC-3-4',2,'a菱形5辺、b3×3節点格子、c2×3節点梯子'),('R05-REG-BASIC-3-6',3,'a2×3節点梯子、b3×3節点格子、c菱形5辺')]:
 mech(q,'対称性と節点方程式で抵抗網を比較。','network',orders,a,
 '同長同断面の各辺をrとする。菱形は上下節点が同電位で中央の辺に電流が流れず、2rの二枝並列でr。3×3節点格子の対角端子は3r/2、2×3梯子の対角端子は7r/5。後二者は分岐があるので図の見た目で直列化せず、端子1Vで各内部節点にΣ(Vi−Vj)/r=0を立てる。有理数消去による別検算を保存。r<7r/5<3r/2を当該a,b,cへ戻す。',
 {'配線':lay,'端子':'原典で示す対角頂点A,B。','各辺':'長さL、同材料・同断面。交点の接続を原典で確認。'},'Ohm則、Kirchhoff則、等電位、グラフ。',d='basic_3_6',refs=['analysis57_resistors'])

mech('H29-REG-BASIC-3-5','トラスの軸力比と軸伸び比を分ける。','truss',
 ['A1/A2','√3A1/(2A2)','A2/A1','√3A2/(2A1)','√3A2/A1'],3,
 '節点Cの水平釣合からN1cos30°=N2cos60°、N1/N2=1/√3。幾何からl1/l2=√3。棒伸びδi=Ni li/(EAi)なのでδ1/δ2=(1/√3)×√3×A2/A1=A2/A1。軸力比だけを答えにしない。',
 {'形状':'A,C間の棒1は水平30°、B,C間の棒2は60°。A,B同じ水平高さ。','材料':'E共通、断面A1,A2、Cへ下向きP、ピン接合。'},'節点釣合、三角形の幾何、棒伸び。',refs=['mit_material_elastic2000'])
mech('R04-REG-BASIC-3-4','節点の水平釣合からトラス軸力比。','trussforce',
 ['1/2','1/√3','1','√3','2'],2,
 '荷重Pは鉛直なのでCの水平力和は0。N1cos30°=N2cos60°からN1/N2=(1/2)/(√3/2)=1/√3。棒の長さや断面積は、この静定トラスの力の釣合による比には不要。伸び比を問う別問題と混同しない。',
 {'形状':'棒1水平30°、棒2水平60°、Cに鉛直P。','接合':'ピン節点の二力部材。'},'二力部材、水平釣合、力の分解。')
mech('H30-REG-BASIC-3-5','安定平衡のポテンシャルは最小。','potential',
 ['ばねポテンシャルはku²/2','重力ポテンシャルは−mgu','平衡で全ポテンシャル最大','平衡変位mg/k','エネルギーの極値が保守系FEMの基礎'],3,
 '自然長から下向きuとしてΠ=ku²/2−mgu。Πprime=ku−mg=0でu=mg/k、Πsecond=k>0なので最小。最大とする3が不適切。他の式は同じ座標と基準で整合する。有限要素のエネルギー原理も保守系等の適用条件があり、あらゆる非保存力の問題へ無条件に一般化しない。',
 {'系':'鉛直ばねk、質点m、重力g。','座標':'自然長位置から下向きをu>0。','問':'不適切な記述を一つ。'},'ポテンシャル、停留と安定性、座標の符号。',d='basic_3_7',refs=['analysis57_shm'])
for q,vals,a,force,length,area,E,result in [
 ('H30-REG-BASIC-3-6',['.004mm','.04mm','.4mm','4mm','40mm'],3,4000,2000,100,200000,.4),
 ('R05-REG-BASIC-3-4',['.010mm','.020mm','.050mm','.10mm','.20mm'],5,2000,2400,120,200000,.2)]:
 mech(q,'SI接頭辞をそろえて軸伸びを計算。','extension',vals,a,
 'NとmmにそろえるとP='+str(force)+' N、L='+str(length)+' mm、A='+str(area)+' mm²、E='+str(E)+' N/mm²。δ=PL/(EA)='+str(result)+' mm。GPaをN/mm²にすると1GPa=1000N/mm²。長さだけmに残すと1000倍の誤差が生じる。',
 {'荷重N':str(force),'長さmm':str(length),'面積mm2':str(area),'弾性係数N/mm2':str(E)},'軸伸び、応力単位、接頭辞と長さ単位。',refs=['mit_material_elastic2000'])
mech('R01-REG-BASIC-3-3','線形抵抗を受ける落下の終端速度。','terminal',
 ['mg/k','2mg/k','√(mg)/k','√(mg/k)','√(2mg/k)'],1,
 '下向き正でm dv/dt=mg−kv。定常状態dv/dt=0からv∞=mg/k。解v=mg/k+(v0−mg/k)e^(−kt/m)もこの極限に収束する。速度の二乗に比例する抵抗なら平方根になるが、原典はkvなので使わない。',
 {'質点':'m>0、g>0。','抵抗':'速さに比例、係数k>0、運動と反対。','範囲':'原典は浮力を別項として与えない。'},'運動方程式、終端速度、一次微分方程式。',d='basic_3_7')
mech('R01-REG-BASIC-3-4','非圧縮条件を体積ひずみから読む。','incompressible',
 ['0','0.1','0.2','0.5','1'],4,
 '体積ひずみの一次近似はεx+εy+εz=(1−2ν)(σx+σy+σz)/E。任意の垂直応力に対して0とする非圧縮条件には1−2ν=0、ν=0.5が必要。特定の応力で和が0になる条件だけでは非圧縮材料を定義できない。',
 {'材料':'等方線形弾性、微小ひずみ。','要件':'任意の応力状態でも体積変化なし。'},'体積ひずみ、Hooke則、Poisson比。',
 'ν=0.5は非圧縮極限。K=E/[3(1−2ν)]は発散し、有限の体積弾性係数をもつ通常の構成則に数値代入して扱わない。',refs=['mit_material_elastic2000'])
mech('R01-REG-BASIC-3-5','荷重表示で棒のひずみエネルギー。','axialenergy',
 ['Pl','Pl/E','Pl²/A','P²l/(2EA)','P²/(2EA²)'],4,
 '軸伸びδ=Pl/(EA)をU=Pδ/2へ代入するとP²l/(2EA)。単位はN·mである。UがPに一次比例する候補は線形ばねのエネルギーの二次依存と整合しない。',
 {'棒':'長さl、断面A、E、弾性域で軸荷重P。'},'軸剛性、力変位面積、エネルギー単位。',refs=['mit_material_elastic2000'])
mech('R01-REG-BASIC-3-6','棒振子の質量慣性と重力トルク。','pendulum',
 ['2π√(l/g)','2π√(3l/(2g))','2π√(2l/(3g))','2π√(2g/(3l))','2π√(3g/(2l))'],3,
 '上端を支点とする一様棒のI=Ml²/3、重心距離l/2。小振幅ではIθsecond=−Mg(l/2)θなのでω²=3g/(2l)、T=2π√(2l/(3g))。全質量を棒端に集める単振子の式を使わない。質量は約分される。',
 {'棒':'一様細長棒、長さl、上端回転自由、重力g。','運動':'微小角振動、摩擦無視。'},'物理振子、慣性モーメント、線形化。',d='basic_3_0')
mech('R01-RET-BASIC-3-2','平面への垂足を法線方向射影で求める。','projection',
 ['(1,1,3)','(4,1,6)','(3,2,7)','(2,1,4)','(5,3,5)'],2,
 '法線n=(1,2,−1)、A=(6,5,4)、n·A=12、n·n=6。垂足H=A−[12/6]n=(4,1,6)。4+2×1−6=0で平面上にあり、A−H=(2,4,−2)=2nで垂直も確認できる。',
 {'点':'A=(6,5,4)。','平面':'x+2y−z=0。'},'法線、内積、正射影、二条件による検算。',d='basic_3_9')
mech('R01-RET-BASIC-3-5','通常の熱伝導と機械的振動を区別。','heat',
 ['振動数は材料特性だけで定まる','気柱の境界は振動数に影響しない','振子の振動数は質量平方根に反比例','通常の熱伝導の自由応答は振動しない','薄板には一つのモードだけ'],4,
 '通常のFourier熱伝導∂T/∂t=κ∇²T、κ>0では適切な固定温度又は断熱境界下の固有モードはe^(−κλt)で減衰し、慣性復元力による自由振動と異なる。材料だけでは形状・支持を落とし、気柱の開閉境界も重要。小振幅単振子の周期は質量によらず、薄板には複数モードがある。',
 {'問':'最も適切な記述。','熱':'通常の伝導を扱う原典のモデル。'},'時間微分、安定な熱拡散、モード、境界条件。',
 '時間一階微分だけでは非振動性を証明できない。一階の連立回転方程式は振動し得る。正の拡散係数とLaplacianの固有値を含む通常モデルとして限定して査読する。',d='basic_3_0')
mech('R02-REG-BASIC-3-5','傾斜と重力は平衡位置を変える。','springgravity',
 ['A=B=C','A>B>C','A<B<C','A=C>B','A=C<B'],1,
 '運動方向をばね軸に取り、平衡位置からの変位xを使う。重力成分は平衡条件に吸収され、どの配置もm xsecond=−kx。ω=√(k/m)なので三者同じ。鉛直で伸びが大きいことを振動数の違いへ直結させない。',
 {'A':'水平。','B':'45°の滑らかな斜面。','C':'鉛直。','共通':'質点m、同じばねk、摩擦無視、ばね軸方向運動。'},'平衡位置、一定外力、線形ばね振動。',d='basic_3_0',refs=['analysis57_shm'])
mech('R02-REG-BASIC-3-6','連続式とBernoulliで管内速度を求める。','bernoulli',
 ['(Ab/Aa)√((pb−pa)/ρ)','(Aa/Ab)√((pa−pb)/ρ)','√(2(pb−pa)/ρ)/√(1−Ab/Aa)','√(2(pa−pb)/ρ)/(1−Ab/Aa)','√(2(pa−pb)/ρ)/√(1−(Ab/Aa)²)'],5,
 '非圧縮の連続式Aa va=Ab vbからva=(Ab/Aa)vb。同じ高さのBernoulli式pa+ρva²/2=pb+ρvb²/2へ代入する。pa−pb=ρvb²[1−(Ab/Aa)²]/2を解くと5。面積比は速度へ一次で入り、速度エネルギーへ代入すると二乗になる。',
 {'管':'水平、a断面Aaからb断面Abへ、密度ρ。','モデル':'非圧縮・非粘性、定常として流線のエネルギー損失を無視。'},'質量保存、圧力エネルギー、Bernoulli、面積比。',d='basic_3_6')
mech('R03-REG-BASIC-3-4','固定棒の熱ひずみを圧縮応力が相殺。','thermal',
 ['2MPa引張','4MPa引張','4MPa圧縮','8MPa引張','8MPa圧縮'],3,
 '自由な熱ひずみαΔTに機械ひずみσ/Eを加え、両端固定の全ひずみ0とする。σ=−EαΔT=−(2.0×10³MPa)×(1.0×10^-4/K)×20K=−4MPa。温度上昇を妨げるので圧縮。Eを鋼の代表値へ置き換えず原典の2.0×10³MPaを使う。',
 {'材料':'E=2.0×10³MPa、α=1.0×10^-4/K。','拘束':'両端固定、温度20K上昇。'},'熱ひずみ、適合、応力の符号。',refs=['mit_material_elastic2000'])
mech('R03-REG-BASIC-3-5','ばねの全エネルギーは自然長から測る。','verticalenergy',
 ['0','ka²/2','ka²/2−mga','k(mg/k+a)²/2','ka²/2+mga'],4,
 '静止時の自然長からの伸びはmg/k。下端振幅位置ではさらにa伸びるのでばね単体のひずみエネルギーU=k(mg/k+a)²/2。平衡位置を中心とする振動エネルギーka²/2とは別の量。平衡時との差ならka²/2+mgaであり、問われた全量ではない。',
 {'系':'鉛直ばねk、質点m、振幅a、g。','問':'最下端でのばね自身の弾性エネルギー。'},'自然長、平衡位置、基準の違うエネルギー。',d='basic_3_7',refs=['analysis57_shm'])
mech('R03-REG-BASIC-3-6','四分円の重心を面積一次モーメントで求める。','centroid',
 ['(√3a/4,√3a/4)','(a/2,a/2)','(a/√2,a/√2)','(3a/(4π),3a/(4π))','(4a/(3π),4a/(3π))'],5,
 '第一象限の半径aの四分円は対称性でxbar=ybar。面積A=πa²/4、∫x dA=∫0^a x√(a²−x²)dx=a³/3。割るとxbar=4a/(3π)、同じくybar。弧だけの重心とは違い、面積全体を積分する。',
 {'領域':'第一象限、半径aの一様な四分円面。','問':'面積重心のx,y座標。'},'面積重心、対称性、一次モーメント。',d='basic_3_9')
mech('R04-REG-BASIC-3-5','角速度変化から慣性トルク。','torque',
 ['IΔω','IΔωT','IΔω/T','I(ω2²−ω1²)/2','I(ω2²−ω1²)T'],3,
 '一定角加速度α=(ω2−ω1)/T=Δω/T。運動方程式τ=Iαなので3。角速度の二乗差は回転運動エネルギーの差に関係し、所要トルクと単位も異なる。',
 {'円盤':'慣性モーメントI。','操作':'角速度ω1からω2へ時間Tで一定角加速度。'},'角加速度、回転運動方程式、次元。',d='basic_3_7')
mech('R04-REG-BASIC-3-6','張力の小振動剛性と長さ・質量の比。','stringmass',
 ['1:1','1:√2','1:2','√2:1','2:1'],5,
 'aの各半長Lで中央変位xが小さいと各張力の横成分はTx/L、合計2Tx/L。ωa²=2T/(mL)。bは各半長2L、質量2mでωb²=2T/[(2m)(2L)]=T/(2mL)。二乗比4なのでωa:ωb=2:1。',
 {'a':'全長2L、中央質量m。','b':'全長4L、中央質量2m。','共通':'一定張力T、原典の弦に直交する微小変位、他方向の変位無視。'},'張力の成分、小角近似、等価剛性。',d='basic_3_0')
mech('R05-REG-BASIC-3-5','減速機を介した円盤加速の入力トルク。','geartorque',
 ['IΔω/(n²T)','IΔω/(nT)','IΔω/T','nIΔω/T','n²IΔω/T'],2,
 '出力円盤の角加速度はΔω/Tで、出力トルクIΔω/T。入力/出力角速度比n、効率1なので入力トルクは出力の1/n。入力側換算慣性I/n²を使う場合も入力角加速度はnΔω/Tであり、積はIΔω/(nT)になる。',
 {'減速':'入力角速度:出力角速度=n:1。','円盤':'出力に慣性I、ω1→ω2を時間T。','効率':'1、損失無視。'},'動力保存、反射慣性、角加速度の基準。',d='basic_3_7')
mech('R06-REG-BASIC-3-4','Euler座屈の有効長で支持条件を比較。','buckling',
 ['Pa>Pb>Pc','Pa>Pc>Pb','Pb>Pa>Pc','Pb>Pc>Pa','Pc>Pa>Pb'],3,
 '臨界荷重Pcr=π²EI/(KL)²。a両端ピンはK=1、b固定・ピンはK≈0.699、c片持ちはK=2。EIとLは同じなので有効長が短いほど臨界荷重が大きく、Pb>Pa>Pc。',
 {'a':'両端ピン。','b':'一端固定・他端ピン。','c':'一端固定・他端自由。','共通':'同じL,E,I、理想的細長柱、軸圧縮。'},'Euler座屈、有効長、支持境界。',
 '真直・線形弾性の理想柱の比較。初期不整・残留応力・短柱の圧壊を含む実設計荷重としては使わない。')
mech('R06-REG-BASIC-3-6','交点接続を含む抵抗網の等電位を利用。','network',
 ['4/3Ω','1Ω','2/3Ω','1/3Ω','1/6Ω'],3,
 'a,b端子の中央に対する対称性から上、下、中央接続点が同電位。これらを結ぶ二抵抗には電流が流れない。残るaからbへの上・中央・下の三枝はそれぞれ1Ω+1Ω=2Ω、並列で2/3Ω。中央の黒点は交差線の接続を示し、未接続の交差へ読み替えない。',
 {'各抵抗':'全八個1Ω。','図':'菱形外周四辺と上下・左右の中央接続四辺、交点に接続点。','端子':'左右a,b。'},'等電位、節点接続、並列合成。',d='basic_3_6',refs=['analysis57_resistors'])
mech('R07-REG-BASIC-3-5','四面体の端子位置で合成抵抗は変わる。','tetra',
 ['Rb<Rc<Ra','Ra<Rc<Rb','Rc<Ra<Rb','Rc<Rb<Ra','Ra<Rb<Rc'],5,
 '一辺全体の抵抗をRとする。aは頂点間で直接Rと、残る二頂点を同電位にまとめた経路Rとの並列からR/2。bは頂点と対辺中点。対辺の両頂点をまとめると端子からそこまでR/2と3R/2の並列で3R/8、その節点から中点までR/4を足し5R/8。cは向かい合う二辺中点で各端のR/4と二頂点群間の四辺並列R/4を直列にし3R/4。従ってRa<Rb<Rc。節点方程式の有理数検算も一致する。',
 {'構造':'正四面体六辺、各辺同材料・同長L・同断面。','a':'二頂点。','b':'頂点とその対辺中点。','c':'互いに向かい合う二辺の中点。'},'対称な等電位群、中点での辺分割、直並列。',d='basic_3_6',refs=['analysis57_resistors'])
mech('R07-REG-BASIC-3-6','運動起電力と磁気制動から終端速度。','motional',
 ['MgR/(BL)²','(BL)²/(MgR)','MgR/(BL)','BLR/(Mg)','Mg/(BLR)'],1,
 '棒の起電力ε=BLv、回路電流I=ε/R。棒に働く磁気力F=IBL=B²L²v/RはLenz則で運動を妨げる。終端速度ではつり下げ質量の張力Mgと釣合うのでv=MgR/(BL)²。回路抵抗を増すと制動電流が減り、速度は増える。',
 {'回路':'レール間隔L、抵抗R、棒・レールの抵抗無視。','磁場':'面に垂直で一様B。','駆動':'滑車と糸で質量Mが落下、摩擦無視、定常速度。'},'運動起電力、Lenz則、磁気力、終端釣合。',d='basic_3_6')

assert len(Q)==43 and set(R)=={e['question_id'] for e in Q}
for e in Q:
 e['learning_points']=e['required_knowledge']+' 支持・接続・符号を原典図から確定し、式の成立条件を先に点検する。'
 e['calculation']='true'
 e['evaluation'].update(calculation_load='2',reasoning_steps='3',figure_reading='2',difficulty='3',difficulty_reason='原典の支持・接続・幾何を式へ変換し、単位・符号・極限で検算する。')
out=P/'config/authored_batches/S7_057_analysis_finish.json'
assert not out.exists()
out.write_text(json.dumps({'batch_id':'S7_057_analysis_finish','reference_date':'2026-10-14','questions':Q},ensure_ascii=False,indent=2))
print('Prepared',len(Q),'partial',sum(bool(e['ambiguity']) for e in Q))
