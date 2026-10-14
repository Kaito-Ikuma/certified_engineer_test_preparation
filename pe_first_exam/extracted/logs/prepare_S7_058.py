# coding: utf-8
"""Manually authored safety/consumer batch. No inference from official keys."""
import json,copy,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[2]
R={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_058_selection.json').read_text())['records']}
I={r['question_id']:r for r in json.loads((P/'extracted/logs/S7_058_initial_independent.json').read_text())['records']}
T=json.loads((P/'config/authored_batches/S7_052_engineering.json').read_text())['questions'][0]
Q=[];Y='条件内で適切';N='不適切';L='条件・時点を留保'
def add(q,title,cid,section,refs,opts,solution,knowledge,ambiguity='',discipline='basic_4_1',conditions=None,figure=False,law=False):
 r=R[q];e=copy.deepcopy(T)
 e.update(question_id=q,source_sha256=r['source_sha256'],stem=title,summary=title,
  conditions=conditions or {'原典':'問題文・否定・全五候補と組合せ表を保存原典21画像で確認。','時点':r['era_year']+'の本文表現を保持。後の制度改正を遡及しない。'},
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
 add(q,title,'env58_'+key,theory,refs or [],numeric(values,answer,'解法の条件と結果を照合する。') if all(isinstance(v,(int,float)) for v in values) else combo(values,values[answer-1]),sol,knowledge,ambiguity,d,conditions,figure)
def detailed(q,title,key,d,theory,opts,sol,knowledge,conditions,refs=None,ambiguity=''):
 add(q,title,'env58_'+key,theory,refs or [],opts,sol,knowledge,ambiguity,d,conditions)

def env(q,title,key,values,a,sol,knowledge,refs=None,ambiguity='',d='basic_5_1',conditions=None,negative=False,reasons=None):
 opts=[]
 for i,v in enumerate(values,1):
  correct=(i==a)
  verdict=('不適切・選択対象' if correct else '条件内で適切') if negative else ('適切・選択対象' if correct else '不適切')
  opts.append((v,verdict,reasons[i-1] if reasons else ('判定と一致する。' if correct else '式・定義・対応の独立判定と一致しない。')))
 add(q,title,'env58_'+key,'theory:env:'+key,refs or [],opts,sol,knowledge,ambiguity,d,
  conditions or {'時点':R[q]['era_year']+'に指定された資料・制度。','照合':'原典21画像で否定・五肢・組合せ表を確認。後年値で置換しない。'},
  figure=any(x in key for x in ['balance','co2','order','history']))

env('H23-REG-BASIC-5-1','2008年度の温室効果ガスと国際枠組。','climate',
 ['CO2が九割以上','産業の次は家庭','条約の濃度安定は2050期限','1997パリ議定書','2009途上国に基準年削減数値義務'],1,
 'CO2換算の2008年度総量の九割以上がCO2で、1。部門別では家庭が第二位という組合せが違う。UNFCCCの究極目的に2050という一律期限はなく、1997採択は京都議定書。2009コペンハーゲンの合意を全途上国に法的数量削減義務を課す議定書と扱わない。',
 'CO2換算、部門の定義、条約と議定書、採択年。',['env58_ghg2008'],
 '当時白書の全ガス内訳・部門図と2009合意の条文の追加照合が必要。CO2九割以上は当時確定値公表表の検索本文でも確認。')
env('H23-REG-BASIC-5-2','排出抑制から適正処分までの優先順。','wasteorder',
 ['生活環境/再資源化/適正処理/半分','公衆衛生/再使用/適正処分/半分','生活環境/再資源化/適正処分/1/3','公衆衛生/再資源化/適正処理/1/3','生活環境/再使用/適正埋立/1/3'],2,
 '旧来の廃棄物行政の公衆衛生と公害対策に、循環型社会形成が加わる。優先は排出抑制→再使用→再生利用→熱回収→残るものの適正処分。2001基本方針の最終処分目標は1997基準の概ね半分なので2。処分を埋立の一方式だけへ狭めない。',
 '3R、循環利用と処分、基準年度と目標年度。',['env_circular_law','env58_wastegoal'],
 '取得した2001資料は基本方針案と施策実績であり、2010白書の引用箇所全文の一致は追加照合。')
env('H23-REG-BASIC-5-3','気液の同質量比較からLNGの体積比。','lng',
 ['1/400','1/600','1/800','1/1000','1/1200'],2,
 '同じ物質量を比べる。0℃1気圧で1molの理想気体は約22.4L、メタン質量16g。液体体積は0.016kg/(425kg/m³)=3.76×10^-5m³、気体は.0224m³。比は.00168≈1/595なので最も近い1/600。密度比ρgas/ρliquidでも同じ。冷却の温度条件を気体標準状態と混同しない。',
 '理想気体モル体積、分子量、密度と体積、単位。',d='basic_5_2',
 conditions={'気体':'0℃1気圧、純CH4の理想気体。','液体':'密度425kg/m³一定とする原典モデル。'})

histpairs=['Galileo/天体望遠鏡で観測','Huygens/振子時計','Arkwright/水力紡績機','Becquerel/ラジウム発見','Eastman/写真用フィルム乾板']
for q in ['H23-REG-BASIC-5-5','H27-REG-BASIC-5-6']:
 env(q,'人物と業績：放射能とラジウムを区別。','historypairs',histpairs,4,
 'ラジウムとポロニウムの発見は1898年のキュリー夫妻の仕事。Henri Becquerelは1896年ウランの自然放射を見いだしたので4が誤り。Galileoは望遠鏡を改良して天体観測へ用いた。Huygensの振子時計、Arkwrightの水力紡績、Eastmanの写真材料・乾板の工業化という他の対応は、出題の代表的業績の範囲で扱う。',
 '放射能現象と元素発見、発明と改良・普及の区別。',['env58_curie'],d='basic_5_0',negative=True,
 ambiguity='原典は「アントワーヌ・ベクレル」と記載し人名が曖昧。放射能発見者Henri Becquerelとの対応を区別。Eastmanの「フィルム乾板」も乾板とロールフィルムをまとめた表現であり、原典を厳密な発明年表に一般化しない。',
 reasons=['望遠鏡の発明者そのものとする記述ではなく観測への利用。','振子を時間標準にする時計。','産業革命の水力紡績機。','放射能の発見とラジウム発見を取り違える。','乾板と柔軟な写真フィルムの開発・商業化という原典の代表表現。'])
env('H24-REG-BASIC-5-1','リサイクル制度の対象と責任主体。','recyclelaw',
 ['基本法は再生利用最優先','容器三品目の全費用を販売者','家電小売の引取・製造者への引渡し','全建設工事の発注者が分別再資源化','再利用なら有害物輸出規制なし'],3,
 '3が家電リサイクル法の小売業者の役割に対応。基本法はまず発生抑制。容器包装は三品目のみではなく、分別収集と再商品化の役割・費用も異なる。建設は規模等の対象条件があり全工事・発注者への実施義務という全称が違う。バーゼルは再利用目的の有害廃棄物でも規制を受け、条約成立の背景の輸送方向も逆。',
 '法の目的、対象条件、排出者・自治体・小売・製造者の役割。',['env_circular_law','env_appliance'],
 '出題時点の建設規模・バーゼル条約対象と例外は追加の法令履歴照合。現行FAQだけで全過去条文の確定とはしない。',d='basic_5_6')
env('H24-REG-BASIC-5-2','発熱量は指定表と単位質量で比較。','heating',
 ['A>B>C>D','A>B>D>C','B>C>D>A','C>A>B>D','C>A>D>B'],4,
 '指定された燃料種の質量当たり発熱量は天然ガスCが最大、原油A、輸入原料炭B、廃材Dの順なので4。天然ガスの表が体積単位なら密度でMJ/kgへ換算する。液体のMJ/Lを質量当たり値へ直接並べない。',
 '高位・低位発熱量、単位、燃料品種、密度換算。',['env58_heating'],d='basic_5_2',
 ambiguity='2005年度指定表の全四値を同じ定義で取得する作業は未完了。2023改訂資料の歴史表を補助参照し、後年値へ置換しない。')
env('H24-REG-BASIC-5-3','2010年の電源比とガス技術を分ける。','energy2010',
 ['30/再熱再生/タイトサンド','30/コンバインド/シェール','30/コンバインド/タイトサンド','20/再熱再生/シェール','20/コンバインド/シェール'],2,
 '2010年度の原子力比率は約30%。天然ガスのコンバインドサイクルはガスタービンと排熱による蒸気タービンを組み合わせる。米国で増産が注目された非在来ガスはシェールガス。三語の組合せ2。',
 '歴史的電源構成、複合サイクル、非在来型天然ガス。',d='basic_5_2',
 ambiguity='一般電気事業用という分母の2010年度原表と2005以降の米国生産統計は追加取得。現行の全発電量比率と混同しない。')
env('H24-REG-BASIC-5-5','産業革命の改良・工場化と担い手。','industrial',
 ['既存技術の改良の積重ね','機械化で大工場へ','娯楽自動機構から転用もある','大学研究者主導の産学協同例が多い','労働と児童労働が社会問題'],4,
 '産業革命期の代表的機械は職人・発明家・事業者の改良と事業化で広まり、当時の欧州大学研究者が開発を主導した例が多いという4は不適切。新規性だけでなく既存機構の組合せ、工場制度、生産と社会への影響も見る。Wattと大学との接点のような個別事例は、全体を大学主導とする証明ではない。',
 '発明、改良、普及、研究組織と生産制度。',['env58_steam'],d='basic_5_0',negative=True,
 ambiguity='からくりからの転用という肢3の個別史料は追加照合。一般論を特定発明の確定年表に拡大しない。')
env('H25-REG-BASIC-5-1','2012年石油統計の対象範囲を固定。','oil2012',
 ['93/マラッカ/クウェート/21','93/ホルムズ/サウジ/42','83/マラッカ/サウジ/42','83/ホルムズ/クウェート/42','83/ホルムズ/サウジ/21'],5,
 '2012年の指定統計では中東依存度約83%、主要経路ホルムズ海峡、最大輸入先サウジアラビア、原油と石油製品の総輸入額比約21%で5。数量の依存度と金額比は別であり、石炭・LNGを含む鉱物性燃料全体の比と原油・製品だけの比も違う。',
 '暦年と年度、数量と金額、統計品目、輸送経路。',['env58_oil'],d='basic_5_2',
 ambiguity='2012暦年の財務省四項目原表を全て取得していない。取得白書は2013年度83.6%とサウジ首位を支持する補助で、指定年の確定証跡とは区別する。')
env('H25-REG-BASIC-5-2','暖房と自動車のCO2排出量を比較。','co2',
 ['1:3','2:3','1:1','3:2','3:1'],2,
 '暖房は.5kW×3h×50=75kWh、排出31.5kg。自動車は200/10=20L、排出46.4kg。比31.5/46.4≈.679で2:3に最も近い。WをkWへ直してから時間を掛ける。',
 'エネルギー=電力×時間、燃料使用量、排出係数。',d='basic_5_2',
 conditions={'電力':'500W、3h/日×50日、.42kg-CO2/kWh。','車':'10km/L、200km、2.32kg-CO2/L。'})
env('H25-REG-BASIC-5-3','気候緩和と適応、LCAの境界。','lca',
 ['環境基準は維持が望ましい','CDMは京都の認証削減','CFPは全過程CO2換算','適応は排出削減で原因抑制','LCAは資源から廃棄まで評価'],4,
 '排出削減や吸収を通じて原因を減らすのが緩和。影響に対して被害を減らす対策が適応なので4が取り違え。CFPは温室効果ガスのCO2換算に着目し、LCAはより広い環境影響の評価。環境基準は環境の望ましい状態で、個別工場の排出許容値と同じではない。',
 '緩和・適応、機能単位とシステム境界、環境基準。',['env58_pmstandard'],negative=True,
 ambiguity='CDMとCFPの出題当時規則全文は未取得。定義の独立判断と条文・規格の確定は分ける。')
env('H25-REG-BASIC-5-4','下水処理の段階と環境対策。','treatment',
 ['管理型の遮水・浸出水処理','活性汚泥は一次処理','緑化の表面温度と空調低減','土壌対策に掘削除去が多い','完全燃焼と排ガス急冷'],2,
 '活性汚泥による生物処理は一般に二次処理。一次は沈殿等の物理処理であり、2が不適切。管理型処分場は浸出水等による汚染を防ぐ。緑化は遮蔽・蒸発散、ダイオキシン対策は燃焼と再合成防止の工程を分けて説明する。',
 '一次・二次・高度処理、物理と生物反応、汚染経路。',d='basic_5_4',negative=True,
 ambiguity='当時土壌対策の掘削除去割合と施設の詳細法定仕様は追加照合。緑化の効果は気象・水・建物条件に依存。')
for q,a,order in [('H25-REG-BASIC-5-5',2,'ア=社会理解、イ=科学技術間だけ、ウ=双方向、エ=媒体へ技術使用'),('H28-REG-BASIC-5-5',5,'ア=科学技術間だけ、イ=科学者に制作委任、ウ=社会理解、エ=双方向')]:
 env(q,'科学と社会をつなぐ双方向の対話。','communication',
 ['ア イ','ア ウ','イ ウ','イ エ','ウ エ'],a,
 '社会・国民の期待や考えを専門家自身が理解することと、専門家・非専門家間の双方向性が適切。基礎科学と応用技術の内部連携だけをこの領域全体の定義にはできず、媒体制作へ技術を使うことや科学者へ任せることも、社会と対話するという目的の代替ではない。原典の列順で組合せを選ぶ。',
 '専門家と社会、理解と対話、情報発信と相互学習。',['env58_communication'],d='basic_5_0',conditions={'四文の順序':order,'問':'適切な二文。'})
env('H25-REG-BASIC-5-6','発表・発明を古い順へ並べる。','historyorder',
 ['エア イオウ','アイエウオ','エアイウオ','アエオイウ','アイエオウ'],1,
 'ハレーの周期彗星の予測・同定が18世紀初頭、Wattの蒸気機関改良が18世紀後半、Darwin–Wallaceの自然選択発表が1858、一般相対論が1915、Fukuiのフロンティア理論が1952。エ→ア→イ→オ→ウで1。発見と理論発表、特許と実用化のどの段階をいうかも確認する。',
 '科学史の世紀区分、業績の段階、順序制約。',['env58_steam'],d='basic_5_0',
 ambiguity='全五業績の初出一次史料は未取得。特にハレー彗星の「発見」は周期性の同定を指す出題表現として留保。')
env('H26-REG-BASIC-5-1','粒径範囲と大気汚染の生成経路。','air',
 ['PM2.5は2.5μm付近だけ','SO2は燃料中S由来','NO2は燃焼と光化学前駆物質','光化学オキシダントはNOxとVOCの光反応','COは不完全燃焼でメタン寿命にも影響'],1,
 'PM2.5は概ね粒径2.5μm以下の微小粒子で、2.5付近だけに限定する1が誤り。規格上は2.5μmを50%分離する装置で採取するという測定定義もある。SO2は硫黄、NOxとVOCは二次生成、COは不完全燃焼とヘモグロビンの結合。COによるOH消費はメタン除去に影響する。',
 '大きさの範囲と測定、一次・二次汚染物質、生成と除去。',['env58_pmstandard','env58_pm25'],negative=True,d='basic_5_4',
 ambiguity='COによるメタン寿命の化学過程と各健康影響は追加一次資料照合。肺沈着と粒径の関係を2.5μm一値へ固定しない。')
env('H26-REG-BASIC-5-2','環境会計と評価・報告・監査を区別。','accounting',
 ['LCAは設備更新時のみ','環境報告書は設備の自治体届出','グリーン購入は生物資源優先のみ','環境監査は税務処理のみ','環境会計は費用効果を金額物量で'],5,
 '環境会計はコストと効果を認識して、貨幣単位又は物量単位で定量化・伝達する仕組みで5。LCAは設備の更新周期だけでなく製品等の全過程。環境報告は社会への情報開示、グリーン購入は必要性と環境負荷、環境監査は環境管理の点検であり、税務監査だけではない。',
 '対象、評価目的、会計単位、環境管理手段。',['env58_accounting'])
env('H26-REG-BASIC-5-3','2012開始のFITの原則と拒否事由。','fit',
 ['五種類の再エネ','大臣が年度価格設定','電力量に応じ賦課','地域負担差を調整','接続は一切拒否不可'],5,
 '正当な理由がある場合まで接続拒否を一切できないとする5は誤り。2012開始の対象は太陽光・風力・水力・地熱・バイオマスで、調達価格の設定、使用量に応じた賦課、費用調整という仕組みを区別する。例外を削って無条件義務にしない。',
 '固定価格、買取と接続、賦課金、例外。',['env58_fit2013'],negative=True,d='basic_5_6',
 ambiguity='2013METI資料の検索本文で正当拒否事由を確認したがPDF全文取得は失敗。出題時価格決定と対象水力条件の詳細、法令履歴は追加照合。')
env('H26-REG-BASIC-5-4','資源量と太陽光面積の桁を比較。','resource',
 ['石炭埋蔵エネルギーが石油超','石油確認埋蔵量は危機時より増','海水Uは1億t超','100km²太陽光が日本需要超','全球の光合成固定が人類需要超'],4,
 '100km²=10^8m²。例えば1kW/m²を昼間平均12h/日、効率を非現実的に100%としても年約438TWhで、当時の日本の年間電力需要約1000TWhに届かない。現実には夜間・天候・入射角・変換損失でさらに小さいので4。資源の存在量と経済的に採れる確認埋蔵量も同じではなく、後者は探鉱・価格・技術で増え得る。',
 '面積換算、電力とエネルギー、存在量と可採埋蔵量。',negative=True,d='basic_5_2',
 ambiguity='概算の日射・需要は桁比較であり厳密な上限証明ではない。石炭石油の指定時点埋蔵量、海水U総量、全球純生産と人類エネルギーの各原表は追加照合。初回記録の昼夜連続1kW仮定を解説では日照条件を示す概算へ改めた。')
env('H26-REG-BASIC-5-5','専門職責任は職務規定だけでは尽くせない。','ethics',
 ['職業で規範が異なる場合','力量外を引受けない','明文規定なしなら責任なし','行動規範は変化','専門知識は高い基準'],3,
 '規定に明示がないことを責任免除の根拠とする3が不適切。専門職は力量の範囲、安全・公益、説明と結果への責任を考える。依頼業務が力量を超える場合、能力ある者との協働や適切な引継ぎを含め、無能力のまま責任を引き受けることを避ける。',
 '力量、公益、説明責任、法と倫理の範囲。',['ipej_ethics2011'],d='basic_5_0',negative=True)
env('H26-REG-BASIC-5-6','観測・動力・検出・高分子の技術史。','historyorder',
 ['イアウオエ','イウアオエ','イアウエオ','ウアイオエ','ウイアエオ'],4,
 'Galileoの望遠鏡観測が1609年頃、Newcomen機関1712、Wattの改良特許1769、Wilson霧箱は20世紀初頭、Carothersのナイロンは1930年代。ウ→ア→イ→オ→エの4。ナイロンの合成・生産選定と1939の商業化を同一年にせず、霧箱より後という比較に必要な範囲で扱う。',
 '改良と新機構、検出技術、合成と商業化。',['env58_steam','env58_nylon'],d='basic_5_0',
 ambiguity='Galileo・Wilsonの初出史料は追加照合。ACSの1935生産選定と1939商業化を分ける。')
env('H27-REG-BASIC-5-1','廃棄物用語の略称と対象。','wasteterm',
 ['RDFはごみ固形化燃料','E-wasteはほぼ全て再資源化できるエコ廃物','バイオマスは化石除く生物資源','産廃は事業由来の法定20種類','硫酸ピッチは強酸性油泥'],2,
 'E-wasteはelectrical/electronic waste、廃電気電子機器。環境に良い又はほぼ全量再資源化可能という定義ではなく2が誤り。RDFは可燃廃物の加工燃料、バイオマスは化石資源を除く。産業廃棄物は事業活動由来なら全てという分類でなく法定種類と業種条件を確認する。',
 '略称、法定分類、処理特性と有害性。',negative=True,
 ambiguity='当時のRDF添加法・産廃業種条件・硫酸ピッチのガス生成に関する技術資料を追加照合。全RDFが同一添加処方という一般化をしない。')
env('H27-REG-BASIC-5-2','温対法の排出抑制と吸収作用。','warminglaw',
 ['森林吸収の保全に言及なし','対象七種の温室効果ガス','一定規模事業所別の算定報告','知事が推進員委嘱とセンター指定','少なくとも三年ごと計画検討'],1,
 '目的は排出抑制だけでなく吸収作用の保全・強化も含む。言及しないという1が誤り。対象ガス、算定報告の主体・規模、地方推進体制、計画見直しは別の制度事項なので、吸収と排出の二側面を軸に確認する。',
 '目的規定、吸収と排出、政令対象、計画。',d='basic_5_6',negative=True,
 ambiguity='2015施行時の全五条項を履歴条文で一括確認する作業は未完了。現行の2050目標を当時条文へ追加しない。')
env('H27-REG-BASIC-5-3','利用人数と時間を含めた一人当たり排出。','co2',
 ['a>b>c','a>c>b','b>a>c','c>a>b','c>b>a'],5,
 'aは100/10×2.32/3=7.73kg/人。bは500/200=2.5h、8000×2.5×.47/1000=9.4kg/人。cは.5×4×50×.47/4=11.75kg/人。c>b>aの5。総量の大小ではなく人数で割った量を比べる。',
 '排出係数、乗車人数、走行時間、総量と原単位。',d='basic_5_2',
 conditions={'a':'10km/L、100km、3人、2.32kg/L。','b':'8000kW、200km/h、500km、1000人、.47kg/kWh。','c':'500W、4h/日、50日、4人、.47kg/kWh。'})
env('H27-REG-BASIC-5-4','2011年一人当たり一次エネルギー。','energycapita',
 ['独日/米加/韓露','韓露/独日/米加','韓露/米加/独日','米加/独日/韓露','米加/韓露/独日'],5,
 '原典の2011年指標では米加が7toe以上、韓露約5toe、独日約4toeで5。1toe≈42GJを使い、国全体の総量と人口当たりを混同しない。世界1.9、中国2.0という同じ年・同じ指標で比較する。',
 '一次エネルギー、石油換算、人口当たり、年次比較。',d='basic_5_2',
 ambiguity='IEAの指定2011年国別原表は未取得。現行データページを当時値の照合証跡にはせず、Astraの追加確認対象に残す。')
env('H27-REG-BASIC-5-5','知的財産の範囲は特許発明より広い。','ip',
 ['特許は発明保護利用と産業発達','発明は自然法則利用の高度技術思想','知財は自然法則利用のものだけ','基本法は創造保護活用の基本事項','国に施策策定実施責務'],3,
 '特許法の発明は自然法則を利用した高度な技術的思想。知的財産基本法の知財は著作物・商標・商号・営業秘密なども含むので、自然法則利用へ限定する3が不適切。法律名とその定義の範囲を別々に確認する。',
 '発明、知的財産、産業財産権、基本法の責務。',['ip_patent_statute','ip_broad_scope'],d='basic_5_6',negative=True)
env('H28-REG-BASIC-5-1','産業廃棄物フローを物質収支で検算。','balance',
 ['直接再利用83で約40%','再利用207で55%・処分の16倍','処理後124で直接の1.5倍','減量159で42%','直接処分60で16%'],5,
 '単位百万t。中間処理290は再利用124、処理後処分7、減量159へ分かれる。総処分13から直接処分は13−7=6で、60ではないので5。総排出も83+290+6=379、最終の207+159+13=379で一致。83/207≈.40、207/379≈.55、207/13≈16、124/83≈1.5、159/379≈.42。',
 '分岐の収支、直接と処理後、百分率と比率。',negative=True,
 conditions={'排出':'379百万t。','中間処理':'290。','直接再生':'83。','処理後再生':'124。','処理後最終処分':'7。','全再生':'207。','全最終処分':'13。'})
env('H28-REG-BASIC-5-2','生物多様性条約と外来種防除。','biodiversity',
 ['組換え生物の議定書','1992署名開放・1993発効','保全・持続利用・利益配分','外来種に重大影響の例','日本は動物愛護で駆除禁止'],5,
 '外来種による生態系被害の防止には防除制度があり、一律に駆除を禁止する5が誤り。CBDの三目的は保全、持続可能な利用、遺伝資源の利益の公正衡平配分。組換え生物の扱いはCartagena議定書であり、遺伝資源の利益配分のNagoya議定書と混同しない。',
 '条約目的、署名と発効、外来種と防除。',negative=True,
 ambiguity='1992・1993と議定書、当時の外来生物法の防除条項の一次本文を追加照合。動物愛護上の配慮が不要という意味にはしない。')
env('H28-REG-BASIC-5-3','複合発電の高温側から低温側への順。','generation',
 ['一次使切・二次充電','EDLC急速・長サイクル','先に蒸気タービン次に廃熱ガスタービン','燃料電池は水電解の逆','揚水は位置エネルギーに貯蔵'],3,
 'コンバインドは燃焼ガスでガスタービンを回し、その高温排熱から蒸気を作って蒸気タービンへ進む。逆順の3が不適切。二次電池は再充電、EDLCは界面で蓄える。揚水は発電を消費側から切り離して電気を水の位置エネルギーへ変換する貯蔵で、発電時だけの効率を往復効率としない。',
 '温度段階、電気化学、静電蓄積、エネルギー変換。',negative=True,d='basic_5_2')
env('H28-REG-BASIC-5-4','2015年策定の2030電源見通しを読む。','energymix2015',
 ['石油25–27%','再エネ22–24%','原子力20–22%','自給率約25%と準国産','省エネで最終消費低下'],1,
 '2015の見通しの2030構成は、25–27%がLNGで石油は約3%。従って1が不適切。再エネ22–24%、原子力20–22%と、需給の省エネ・自給率目標は当時見通しの範囲。2030を対象とする後年改訂計画の比率をこの問題へ遡及しない。',
 '策定年と目標年、電源構成と自給率、見通し。',['env58_mix2015'],negative=True,d='basic_5_2',
 ambiguity='2015公開関連資料の検索と白書骨子を参照。策定7月の最終PDFの全図表照合は未了で後工程に残す。')
env('H28-REG-BASIC-5-6','電気・化学・電子の代表的業績の順序。','historyorder',
 ['アイウエオ','アイウオエ','ウイアオエ','ウアイオエ','ウイアエオ'],4,
 '雷の電気的性質のFranklinが18世紀、Mendeleevの周期律1869、Curie夫妻の新元素1898、De Forestの三極管1906頃、トランジスタ1947。ウ→ア→イ→オ→エの4。電子管から半導体素子への世紀をまたぐ発展と、発見・発明・商用普及の段階を分ける。',
 '周期律、放射性元素、電子管と半導体、年代順。',['env58_curie'],d='basic_5_0',
 ambiguity='雷の実験・三極管・トランジスタ各原報と特許の一次史料は追加照合。三人の貢献を同一作業に単純化しない。')

assert len(Q)==32 and set(R)=={e['question_id'] for e in Q}
for e in Q:
 e['learning_points']=e['required_knowledge']+' 指定年度・対象範囲・単位・否定を先に固定し、他年度の番号や現行値を転用しない。'
 e['law']='true' if e['concept_id'].split('_',1)[1] in ['recyclelaw','fit','warminglaw','ip','biodiversity','wasteorder'] else 'false'
 e['calculation']='true' if e['concept_id'].split('_',1)[1] in ['lng','co2','balance','resource'] else 'false'
 e['evaluation'].update(calculation_load='2' if e['calculation']=='true' else '0',difficulty_reason='原典時点の定義・統計範囲・制度主体・因果と単位を照合する。')
out=P/'config/authored_batches/S7_058_environment_history.json';assert not out.exists()
out.write_text(json.dumps({'batch_id':'S7_058_environment_history','reference_date':'2026-10-14','questions':Q},ensure_ascii=False,indent=2))
print('Prepared',len(Q),'partial',sum(bool(e['ambiguity']) for e in Q))
