"""Manual image-reviewed geophysical observables; no official answers read here."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')}
items=[]
def add(q,stem,values,reasons,answer,solution,core,knowledge,theories,citations,discipline='geo_exploration',concept='concept_001',cross=None,conditions=None,correct=False):
 r=by[q]
 items.append(dict(question_id=q,source_sha256=r['source_sha256'],stem=stem,conditions=conditions or {'選択方向':'最も適切なもの' if correct else '誤り又は最も不適切・関係の薄いものを1つ'},choices={str(i):dict(value=v,verdict=('適切' if str(i)==answer else '不適切') if correct else ('不適切' if str(i)==answer else '適切'),reason=why) for i,(v,why) in enumerate(zip(values,reasons),1)},figures='図なし。否定方向と全5肢を原典ページ画像で照合。',ambiguity='',evidence=[f'extracted/pages/{r["source_year_directory"]}/17_applied_science/page_{p:03}.png' for p in range(int(r['source_page']),int(r['source_page_end'])+1)],summary=stem,core_concept=core,required_knowledge=knowledge,solution=solution,independent_answer=answer,answer_reason=solution,learning_points=core+'を、測定量・推定対象・基準面・近似条件に分けて理解する。名称だけで探査法を対応させない。',theory_references=theories,discipline_id=discipline,concept_id=concept,cross_concepts=cross or [],classification_reason='全5肢の原典を画像確認。'+core+'が判断の中心であり、観測量と理論の役割に従って主分類を確定する。',calculation='false',figure='false',law='false',evaluation=dict(knowledge_novelty='3',reasoning_steps='2',calculation_load='0',figure_reading='0',difficulty='3',difficulty_reason='物理原理は既習であるが、探査機器、補正と地球科学固有名称の対応を新たに学ぶ必要がある。'),citations=citations,foundationality='high',transferability='high'))

add('H23-REG-APPLIED-29','物理探査の観測対象と装置を比較し、海上音波探査の受振器を誤って説明した記述を選ぶ。',
 ['磁気から鉄類の有無と概略位置を探るが、細かな形状や製品種類は判別できない','MTは自然の地磁気・地電流から深部比抵抗を探る','相対重力計は吊った錘のばね伸びを利用する','地中レーダは概ね10 MHz以上の電磁波で極浅部を探る','ストリーマケーブルには防水加工した速度計を多数入れる'],
 ['通常の磁気異常だけでは磁化・形状・深度が非一意であり、細かな製品識別までは確定できないという探査上の限界を述べる。現代の補助情報を用いる識別可能性全般を否定する命題とは解さない。','自然変動の水平電場・磁場の応答から電気抵抗率を推定する方法である。','ばね定数と伸びの変化から重力の差を測る。絶対値を直接定める落下式とは区別する。','原典が述べる通常の浅部レーダの周波数帯と原理に対応する。到達深度は周波数だけでなく導電率や減衰にも依存する。','水中音波を測る受振器は通常ハイドロフォンであり、圧力変動を検出する。地上用速度計の防水化と同一ではない。'],
 '5','測定量を対照する。重力は加速度、MTは自然電磁応答、レーダは電磁反射である。水中の流体はせん断波を伝えず、海上の受振系では音圧を検出するハイドロフォンを用いる。速度計を防水加工するという第5肢の説明が誤りである。','観測量と受振器の対応','ハイドロフォンの圧力応答、地上速度計、相対重力計、MT、電磁波の反射。',['theory:exploration:observables','theory:exploration:electromagnetic','theory:gravity:measurement'],['usgs_marine_seismic','usgs_mt_metadata'],concept='concept_000',cross=['concept_001','concept_002'])

add('H27-REG-APPLIED-19','放射能・地温・電磁・レーダ・重力探査の推定対象を比べ、CSAMTの物性を誤る記述を選ぶ。',
 ['放射能探査は主にガンマ線強度から断層等の地質情報を得る','地温探査は温泉・地熱・地下水等の調査に用いる','CSAMTは遠方人工源の直交水平電場・磁場から磁化率を得る','レーダは誘電率や導電率の違う境界の電磁反射を捉える','重力は密度構造を求め、標高精度が重要である'],
 ['天然放射性核種の分布や移動の差を地質情報として利用する。ガンマ線の減衰により観測は主に表層からの寄与であり、深部核種をそのまま透視する意味ではない。','温度分布と熱の移流・伝導を手掛かりに熱水・地下水等を探る。','主要な推定対象は比抵抗である。水平電場と磁場の比を磁化率そのものと取り違えている。','電気特性の差が波の伝播と反射を変えることを利用する。','標高1 mの誤差は標準鉛直勾配で約0.3086 mGalに相当し、微小重力異常の解釈を妨げる。'],
 '3',r'CSAMTは人工源の遠方場を用いる電磁探査であり、電磁応答から比抵抗構造を推定する。均質・平面波近似なら見掛比抵抗は\(\rho_a=|E/H|^2/(\omega\mu)\)である。磁化率を主対象とする第3肢は物性の対応を誤っている。','電磁応答と比抵抗の対応','比抵抗と導電率、平面波インピーダンス、CSAMT遠方場、ガンマ線・温度・重力の観測。',['theory:exploration:electromagnetic','theory:exploration:observables'],['ochi_csamt_saijo','gsi_gravity_definitions'],concept='concept_002',cross=['concept_001'])

add('H27-REG-APPLIED-22','地形、無限水平層、潮汐、ばねドリフト、緯度の重力効果から誤りを選ぶ。',
 ['山・谷の地形効果はともに重力を小さくする','密度と厚さ一定の無限水平層は浅いほど重力が大きい','月と太陽の引力による潮汐補正が必要である','ばねの時間変化を一定と近似し閉合誤差を各点へ配分する','絶対重力と緯度から求めた正規重力との差をとるのが緯度補正である'],
 ['測点高まで無限平板があるというブーゲー基準に対する地形効果として読む。測点より上の山の引力は上向き、谷は基準平板の下向き引力を欠くため、いずれも下向き重力を減らす。任意の山と谷の絶対重力を比較する命題ではない。','無限平板の外部重力は2πGρtで深度に依存しない。有限の岩体では距離依存があるため、無限という条件が重要である。','月・太陽による時間変動を地下構造による異常と区別する必要がある。','同一点への戻り測定の閉合差から時間に比例するドリフトを近似して補正する操作を述べる。一定の伸びは測定区間のドリフトを一定率とする通常の近似として解釈し、あらゆる時間変化が必ず線形とはしない。','緯度に依存する理論基準を差し引き、基準地球の変化を除く操作である。'],
 '2',r'無限水平層の上に観測点がある場合、各薄層の寄与を積分すると\(g_z=2\pi G\rho t\)である。層と測点の距離は消えるので、浅いほど大きいという第2肢が誤りである。第1肢は無限平板に対する地形差、第4肢は短時間の線形ドリフト近似として条件を明示して読む。','無限平板の重力と重力補正の基準','ニュートン引力積分、無限平板と有限岩体の違い、地形補正の符号、潮汐、ドリフト、正規重力。',['theory:gravity:slab','theory:gravity:corrections','theory:gravity:measurement'],['gsi_gravity_definitions'])

add('H27-REG-APPLIED-33','測位衛星の時刻信号で位置を求める衛星測位システム全般の略称を選ぶ。',['GALILEO','GLONASS','GNSS','GPS','QZSS'],
 ['欧州の個別システム名であり、全般の総称ではない。','ロシアの個別システム名である。','Global Navigation Satellite Systemの略で、衛星測位システムの総称に対応する。','米国の個別システム名である。','日本の準天頂衛星システムである。GNSSに関連する地域的システムを含めた総称と、その一システムを区別する。'],
 '3','問われているのは測位を実現する国別の装置群ではなく、それらを含む名称である。米国GPS、ロシアGLONASS、欧州Galileo、日本QZSSを区別すると、総称はGNSSである。','衛星測位の総称と個別システム','GNSSとGPSの関係、電波到達時間と擬似距離、受信機時計誤差。',['theory:gravity:gnss'],['gsi_gnss'],discipline='earth_gravity',concept='gnss',correct=True)

add('H29-REG-APPLIED-31','重力探査で用いる補正名のうち、主に反射法地震探査に属するものを選ぶ。',['エトベス補正','ブーゲー補正','潮汐補正','フリーエア補正','静補正'],
 ['船や航空機の運動に伴う回転系の見掛加速度の差を補正する。','基準面と測点の間の岩石質量の引力を除く。','月・太陽による時間変動を除く。','基準面からの高さに伴う重力変化を補正する。','浅部低速度層や標高による地震波の走時差を、共通の基準面へ補正する地震探査の用語である。'],
 '5','補正の対象量を並べると、第1〜4肢は重力加速度の変化を扱う。静補正は主に地震探査の走時をそろえるもので、重力探査の標準的補正名としては該当しない。','重力補正と地震走時補正の区別','運動・質量・潮汐・標高の重力効果、浅部層による走時差。',['theory:gravity:corrections','theory:exploration:observables'],['gsi_gravity_definitions'],cross=['concept_000'])

definitions={'ジオイド':'基準となる重力等ポテンシャル面であり、重力場と標高の基準に関係する。','ケーニヒスベルガー比':'自然残留磁化の大きさと現在の場による誘導磁化の大きさの比であり、磁気異常の解釈に関係する。','プランク関数':'熱平衡放射のスペクトルを記述する関数であり、この候補群では重力・磁気探査の基本量に当たらない。','キュリー温度':'強磁性・フェリ磁性の自発磁化が消失する温度に対応し、磁性鉱物や磁気探査の解釈に関係する。','エトベス補正':'移動観測系の運動に伴う見掛重力の差を補正する。','AE（アコースティック・エミッション）':'微小破壊等に伴う過渡的な弾性波の放出・計測である。岩石研究にも用いるが、重力や磁化の測定とは異なる物理量を扱う。'}
for q,values,answer in [('H30-REG-APPLIED-32',['ジオイド','ケーニヒスベルガー比','プランク関数','キュリー温度','エトベス補正'],'3'),('R04-REG-APPLIED-35',['エトベス補正','ジオイド','キュリー温度','プランク関数','ケーニヒスベルガー比'],'4'),('R06-REG-APPLIED-34',['ケーニヒスベルガー比','ジオイド','AE（アコースティック・エミッション）','キュリー温度','エトベス補正'],'3')]:
 target=values[int(answer)-1]
 add(q,'重力・磁気探査の基準面、磁化特性、移動観測補正と、別の観測分野の語を区別する。',values,[definitions[v] for v in values],answer,'ジオイドとエトベス補正は重力、ケーニヒスベルガー比とキュリー温度は磁気に直接関係する。'+target+'は'+definitions[target]+'したがってこの肢を選ぶ。','重力・磁気探査の物理量と用語','等ポテンシャル面、残留磁化と誘導磁化、磁気秩序の温度依存、回転座標系。',['theory:gravity:corrections','theory:gravity:geoid','theory:geomagnetism:magnetization','theory:exploration:observables'],['gsi_gravity_definitions','kanaya_okuma2011']+(['sato_lei2009_ae'] if q.startswith('R06') else []))

add('R01-REG-APPLIED-27','令和元年度試験当時の日本周辺の偏角の方向と地域差から適切な記述を選ぶ。',
 ['全般的に北ほど偏角が小さい','沖縄本島の偏角は約5度','真北から東へ偏っている','同じ経度なら偏角は同じ','同じ緯度なら偏角は同じ'],
 ['当時の2015.0年磁気図では沖縄本島付近約5度西偏に対し、北海道では概ね9〜10度西偏であり、北ほど小さいという傾向と合わない。','当時参照可能な国土地理院の2015.0年磁気図で、沖縄本島付近は約5度の西偏を示す。概略値として適切である。','日本周辺は西偏であり、東西が逆である。偏角の符号規約と方位を区別する。','磁場は経度だけでは決まらず、同じ経度でも緯度に伴って偏角が異なる。','非軸対称な磁場があるため同緯度でも経度によって変わる。'],
 '2','偏角は水平磁場が真北となす角である。原典の「現在」を令和元年度時点とし、それ以前に公表された2015.0年磁気図を確認する。日本周辺は西偏で、沖縄本島の等偏角線は約5度である。緯度・経度の片方だけで同値になる量ではないので第2肢を選ぶ。','地磁気偏角の方向・分布・時点','真北と磁北、偏角の符号、二次元地理分布、地磁気永年変化、磁気図の元期。',['theory:geomagnetism:declination'],['gsi_declination2015'],discipline='earth_magnet',concept='geomagnetic_declination',conditions={'判断時点':'2019年度試験当時。最新2026年の偏角を遡及して代用しない。','裏付け資料':'国土地理院2015.0年磁気図、元期2015年1月1日、2016年12月作成。'},correct=True)

add('R07-REG-APPLIED-33','正規重力と各補正を区別し、密度差によるブーゲー異常の符号を誤る記述を選ぶ。',
 ['正規重力は地球の質量・自転・形状から導く理論値','ブーゲー補正は測点と海水準面の間の地殻物質の効果を除く','船・航空機の移動は遠心効果を変える','フリーエア補正は高さの違いの影響を補正する','高密度地域のブーゲー異常は小さく、低密度地域では大きくなる'],
 ['基準回転楕円体の外部重力ポテンシャルと自転による遠心ポテンシャルから定める。','標高差だけでなく、その間の岩石質量の引力を平板等で近似して除く。','地球自転と観測機の相対運動により見掛加速度が変わるためエトベス補正が必要である。','高さによる重力の鉛直勾配の影響をそろえる操作である。','形状等を同条件にした基準密度との差では、密度の過剰は正、欠損は負の重力異常を生む。第5肢は基本的対応を逆にしている。'],
 '5',r'測定重力から正規場・高さ・地表質量等の効果を取り除き、地下の密度差を評価する。同じ幾何条件なら重力の差は密度差\(\Delta\rho\)に線形であり、高密度は正の、低密度は負の異常を生む。第5肢はこの符号を逆に記述する。','基準密度と重力異常の符号','正規重力、フリーエア・ブーゲー・エトベス補正、密度差の引力積分。',['theory:gravity:slab','theory:gravity:corrections'],['gsi_gravity_definitions'])

assert len(items)==10
(ROOT/'config/authored_batches/S7_004_gravity_magnetism_gnss.json').write_text(json.dumps(dict(batch_id='S7_004_gravity_magnetism_gnss',reference_date='2026-10-09',scope='10問の全5肢を原典画像照合。重力補正、探査観測量、GNSS、試験当時の偏角を独立判断。',questions=items),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(items),'source-reviewed drafts; official answer values not accessed')
