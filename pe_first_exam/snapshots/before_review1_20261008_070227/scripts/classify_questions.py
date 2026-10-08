"""Evidence-based tentative classification. Overrides are versioned and reproducible."""
import json
import re
import unicodedata
from common import ROOT, read_csv, write_csv

# key, major category, middle category, chapter stem, evidence pattern.
APPLIED = [
('geo_exploration','地質','物理探査','geology/10_geophysical_exploration',r'探査|検層|VSP|ダウンホール|ウェンナー|シュランベル|測線|比抵抗法'),
('geo_resources','地質','資源・鉱床','geology/09_resources_deposits',r'鉱床|石炭|マンガン団塊|地熱資源|鉱業'),
('geo_engineering','地質','応用地質・地盤','geology/08_engineering_geology',r'液状化|地盤|せん断試験|一面せん断|土の|骨材|N値|標準貫入|透水試験|圧密|ダム'),
('geo_groundwater','地質','地下水','geology/07_hydrogeology',r'地下水|帯水層|ダルシー|水理伝導|間隙率|間際率'),
('geo_stratigraphy','地質','層序・古生物','geology/04_stratigraphy_paleontology',r'層序|不整合|不軽合|化石|三葉虫|サンゴ|示準|示相'),
('geo_structure','地質','構造地質','geology/05_structural_geology',r'断層|褶曲|しゅう曲|走向|傾斜|節理|プルアパート'),
('geo_sediment','地質','堆積学','geology/03_sedimentology',r'堆積|推積|砕屑|粒度|タービダイト|リップル|斜交'),
('geo_mineral','地質','鉱物学','geology/01_mineralogy',r'鉱物|偏光顕微鏡|偏光頭微鏡|石英|長石|方解石'),
('geo_petrology','地質','岩石学','geology/02_petrology',r'岩石|火成岩|変成岩|花崗岩|花商岩|玄武岩|風化|変質作用'),
('earth_isotope','地球物理及び地球化学','同位体地球化学','geophysics_geochemistry/09_isotope_geochemistry',r'同位体|年代測定|年代決定|年代を測定|宇宙線|放射性炭素|半減期.*(?:地球|地質)'),
('earth_volcano','地球物理及び地球化学','火山・マグマ','geophysics_geochemistry/05_volcanology',r'火山|マグマ|噴火'),
('earth_interior','地球物理及び地球化学','地球内部・プレート','geophysics_geochemistry/02_earth_interior',r'地球の内部|地球内部|マントル|地殻|プレート|リソスフェア|地球の構造|大陸移動'),
('earth_seismic','地球物理及び地球化学','地震学','geophysics_geochemistry/01_seismology',r'地震|震源|P波|S波|マグニチュード'),
('earth_gravity','地球物理及び地球化学','重力・測地','geophysics_geochemistry/03_gravity_geodesy',r'地球.*重力|重力異常|ブーゲー|フリーエア|測地|ジオイド|GNSS|測位衛星'),
('earth_magnet','地球物理及び地球化学','地磁気','geophysics_geochemistry/04_geomagnetism',r'地磁気|地球.*磁場|地球.*磁気|古地磁気|偏角'),
('earth_weather','地球物理及び地球化学','気象・大気','geophysics_geochemistry/06_meteorology_atmosphere',r'大気|気象|水蒸気|水循環|気候|台風|地球.*温暖|オゾン|雲|降水'),
('earth_ocean','地球物理及び地球化学','海洋','geophysics_geochemistry/07_ocean',r'海洋|海水|潮汐|海流|エルニーニョ'),
('earth_chem','地球物理及び地球化学','地球化学','geophysics_geochemistry/08_geochemistry',r'陸水|地球.*炭素|地球.*水|貯留形態|水質|地球化学|地球.*化学組成|地球上|地殻.*元素'),
('physics_units','物理及び化学','単位・計測','physics_chemistry/11_other',r'単位系|SI|ST単位|国際単位|組立単位|単位の換算'),
('physics_wave','物理及び化学','振動・波動','physics_chemistry/02_oscillation_wave',r'正弦波|振動|単振動|音速|音に|音波|音叉|音又|ドップラー|共鳴|汽笛'),
('physics_optics','物理及び化学','光学','physics_chemistry/05_optics',r'レンズ|凸レンズ|光の|紫外線.*可視|ガンマ線.*赤外線|屈折|干渉'),
('physics_modern','物理及び化学','現代物理・原子核','physics_chemistry/06_modern_physics',r'原子核|半減期|放射線|放射能|電子.*加速|X線.*波長|光電|プランク|ブロイ'),
('physics_thermo','物理及び化学','熱力学','physics_chemistry/03_thermodynamics',r'熱力学|カルノー|ピストン|比熱|熱量|断熱|内部エネルギー|理想気体|気体.*圧力|熱機関|熱伝導率'),
('physics_electro','物理及び化学','電磁気・物性','physics_chemistry/04_electromagnetism',r'コンデンサ|電界|電場|電荷|電位|磁性|磁気|ソレノイド|抵抗|誘電|コイル|熱電|インダク'),
('physics_mechanics','物理及び化学','力学','physics_chemistry/01_mechanics',r'摩擦|斜面|物体|弾性体|浮力|ピトー|ベルヌーイ|流体|加速度|運動量|速度|落下|静止衛星|ねじり|せん断応力'),
('chem_analysis','物理及び化学','分析化学','physics_chemistry/10_analytical_chemistry',r'分析|滴定|スペクトル|クロマト|吸光|NMR|ICP|蛍光X'),
('chem_atomic','物理及び化学','原子・分子・結晶','physics_chemistry/07_atomic_molecular',r'結晶構造|結晶|格子|電子軌道|水素結合|分子軌道|共有結合|原子.*基底状態'),
('chem_organic','物理及び化学','有機・高分子化学','physics_chemistry/12_organic_polymer',r'高分子|ナイロン|樹脂|掛脂|構脂|ポリ|ステアリン酸|界面活性剤|有機|芳香族|オクタン|石油|炭化水素|炭素.*水素.*酸素|ベンゼン|異性体'),
('chem_inorganic','物理及び化学','無機化学','physics_chemistry/09_inorganic_chemistry',r'希ガス|アルカリ金属|アルミニウム|元素|充素|素の|周期表|ランタノイド|レアメタル|気体の性質|ゼオライト|金属'),
('chem_physical','物理及び化学','物理化学','physics_chemistry/08_physical_chemistry',r'化学|平衡|電池|電極|触媒|反応|pH|溶液|溶解|凝固|疑固|沸点|蒸気圧|燃焼|熱化学|酸と塩基|還元|還示|吸着|真空ポンプ'),
]
BASIC_MAJOR=['設計・計画','情報・論理','解析','材料・化学・バイオ','環境・エネルギー・技術']
BASIC_STEMS=['01_design_planning','02_information_logic','03_analysis','04_material_chemistry_biology','05_environment_energy_technology']
BASIC_RULES={
1:[('信頼性設計',r'信頼|借頼|言頼|故障|直列|並列'),('品質・統計設計',r'標準偏差|検査|正規分布|品質|公差'),('プロジェクト・最適化',r'プロジェクト|工程|作業リスト|PERT|待ち行列|ATM|製造.*販売'),('安全・強度設計',r'安全率|安全係数|強度|許容|荷重|製造物責任'),('設計原理・管理',r'設計|PDCA|ISO|デザイン')],
2:[('論理・離散数学',r'論理|真理値|集合|命題|グラフ'),('計算機アーキテクチャ',r'キャッシュ|CPU|命令|メモリ|記憶|ビット|2進|進数|浮動'),('ネットワーク',r'ネットワーク|IP|ノード|伝送|パケット|通信'),('情報セキュリティ',r'セキュリティ|パスワード|暗号|認証'),('データ・AI',r'データベース|AI|学習|情報量|エントロピー|マルコフ'),('アルゴリズム・計算量',r'プログラム|アルゴリズム|自然数|計算量|フロー|うるう|繰り返')],
3:[('微積分・数値解析',r'積分|導関数|微分|数値|近似|関数'),('線形代数・ベクトル',r'ベクトル|行列|固有|内積|外積'),('連続体・構造力学',r'はり|梁|応力|棒|断面|座屈|ひずみ|歪|荷重|トラス'),('計算力学',r'有限要素|境界|熱伝導|解析'),('物理モデル・回路',r'回路|抵抗|電流|振動|運動')],
4:[('生物・バイオ',r'DNA|RNA|遺伝|タンパク|アミノ酸|生体|クローン|細胞|酵素'),('材料・金属',r'金属|材料|結晶|鉄|アルミ|強度|半導体|腐食|高分子'),('原子・無機化学',r'原子|元素|電子|イオン|周期|分子|結合'),('物理化学・反応',r'反応|熱|溶液|化学|電池|pH|触媒')],
5:[('科学技術史・社会',r'歴史|業績|人物|科学史|技術史|コミュニケーション|イノベーション|科学技術'),('環境・持続可能性',r'環境|温暖|廃棄|生物多様|循環|COP|持続|SDG'),('エネルギー',r'エネルギー|天然ガス|発電|石油|電力|原子力|電池'),('品質・統計・計測',r'品質|正規分布|統計|単位|測定')]
}
BASIC_RULES[1] += [('最適化・経済性',r'売上|利益|定価|資材|生産|費用|利得'),('力学設計',r'歯車|弾性|応力|ひずみ'),('品質・統計設計',r'検定|統計|ポアソン|到着|サービス率')]
BASIC_RULES[1] += [('意思決定・最適化',r'最適化|デシジョン|損失'),('設計の応用数学',r'微分|一変数|非負|相関係数'),('製図',r'製図|角法')]
BASIC_RULES[2] += [('数値表現・誤差',r'演算|浮動小数|精度|ランプ'),('言語・データ構造',r'構文|数値列|文字列|木|式で表現'),('論理・離散数学',r'道路網|議案|必要.*条件'),('データ・確率モデル',r'天気|確率|圧縮|符号|ISBN|モジュラス|情報理論'),('ネットワーク',r'TCP|LAN|ふくそう'),('情報セキュリティ',r'攻撃|マルウェア'),('アルゴリズム・計算量',r'アッカーマン|加工|順に')]
BASIC_RULES[2] += [('状態遷移・形式モデル',r'状態遷移|状態.*停止')]
BASIC_RULES[3] += [('運動・エネルギー',r'モータ|トルク|慣性|角速度|エネルギー'),('確率・統計',r'確率|統計')]
BASIC_RULES[3] += [('ベクトル解析・幾何',r'div|rot|座標|重心')]
BASIC_RULES[4] += [('化学・物質',r'反応|コロイド|酸|物質|放射線')]
BASIC_RULES[5] += [('環境・公害',r'汚染|大気|公害'),('科学技術史・社会',r'革命|年代|科学と技術|労働|倫理|責任|新技術')]
BASIC_RULES[5] += [('知的財産・制度',r'知的財産|特許法')]
APT=[
('技術士法・義務責務','01_engineer_act',r'技術士法|技術士.*義務|技術士.*責務|資質向上|名称表示|信用失墜|秘密保持'),
('研究・情報倫理','06_research_information_ethics',r'研究|捏造|盗用|改ざん|改ざん|データ.*偽|情報セキュリティ|個人情報|情報通信|ネット|ICT|不正行為'),
('環境・持続可能性','05_environment_sustainability',r'環境|持続可能|SDG|循環型|廃棄|温暖|気候|リサイクル'),
('安全・リスク','04_safety_risk',r'安全|リスク|労働|ハラスメント|災害|危機|健康|化学物質|製造物責任|品質'),
('コンプライアンス・説明責任','03_compliance_accountability',r'法律|保護法|知的財産|産業財産|特許|説明責任|公益通報|コンプライアンス|消費者|不当|倫理.*法'),
('技術者倫理・意思決定','02_engineering_ethics',r'倫理|責任|利益|公衆|ジレンマ|意思決定|組織|専門職|技術者|エンジニア'),
]

# Prefer explicit topic cues in the question stem over vocabulary in distractors.
TITLE_RULES=[
('geo_exploration',r'探査|検層|VSP|ダウンホール'),
('earth_chem',r'水.鉱物反応|自然界の水.*酸化|炭素循環|窒素循環|水質|陸水.*化学|地殻.*(?:存在度|存在量|存在比)|土壌.*化学'),
('earth_isotope',r'同位体地球化学|年代測定|年代を測定|年代を決定|水素及び酸素の同位体|自然界の水.*同位体'),
('geo_mineral',r'造岩鉱物|鉱物の.*(?:観察|同定)|構成する鉱物|含まれる鉱物|重鉱物'),
('geo_petrology',r'変成岩|岩石の風化|岩石.*分類|付加体|土壌の特徴|火山砕.*岩'),
('geo_engineering',r'地すべり|山崩れ|液状化|せん断試験|地盤沈下|含水比|土の状態|堆積岩で起こる問題|地中熱'),
('geo_resources',r'鉱床|地熱資源|マンガン団塊|天然資源'),
('earth_volcano',r'マグマ|火山|水山噴火|水山砕屑|溶岩.*噴出率'),
('earth_interior',r'地球の内部|地球内部|地殻|プレート境界|弧.海溝'),
('earth_ocean',r'海洋.*海水|海洋及び|海水の.*組成'),
('earth_ocean',r'津波に関する'),
('earth_chem',r'自然界の水.*電気伝導|地下水中の溶解'),
('earth_magnet',r'偏角|地磁気'),
('earth_weather',r'地球の熱収支|地球表面.*太陽|太陽放射エネルギー|水循環|降水のpH'),
('earth_interior',r'大陸と大洋底|日本列島|地球表面の高度'),
('geo_groundwater',r'帯水層|地下水'),
('geo_stratigraphy',r'テフロクロノロジー|テフラ|地層の上下'),
('physics_units',r'SI|単位系|単位の換算|国際単位'),
('physics_wave',r'正弦波|振動.*波動|振動数.*音|汽笛|音に関する|単振動|ばね.*周期'),
('physics_mechanics',r'力学に|静止衛星|初速度|最大せん断応力|金属材料の力学|一様な棒|摩擦|斜面'),
('physics_optics',r'凸レンズ|スリット'),
('physics_modern',r'ド.ブロイ|電子.*加速|連続X線|吸収線量|原子核'),
('physics_electro',r'電流素片|電磁気|磁性|金属の電気抵抗|電磁波'),
('physics_thermo',r'熱伝導|伝熱'),
('chem_analysis',r'分析方法|分析機器|分析手法|多元素同時分析|クロマト|成分分離|分子量測定|分離操作|分離に|光と分子'),
('chem_physical',r'電池|生成熱|燃焼熱|純物質の状態|物質の状態|化学反応|反応に関する|蒸気圧|蒸留|酸と塩基|カルシウムの化合物'),
('chem_atomic',r'原子.*基底状態|電子配置|同位体に関する|結晶|水素結合|電子の軌道|電子のエネルギー|化学結合'),
('chem_inorganic',r'ケイ素|水素化物|ハロゲン|ハロゲン|レアメタル|メタン|水に関する'),
('chem_organic',r'高分子|生体分子|界面活性剤|石油化学|オクタン|ニトロトルエン'),
('earth_chem',r'地球上.*水|地球の水|貯留形態'),
]

def normalize(text):return unicodedata.normalize('NFKC',text)
TOPIC_RULES=[
('地震・弾性波探査',r'地震探査|弾性波.*探査|屈折法|反射法'),('重力・磁気探査',r'重力探査|磁気探査'),
('電気・電磁探査',r'電気.*探査|電磁探査|比抵抗法'),('ボーリング・検層',r'ボーリング|検層|VSP|ダウンホール'),
('表面波・微動探査',r'表面波|微動'),('探査データ処理・逆解析',r'データ.*処理|数値解析|インバージョン|逆解析'),
('地中レーダ',r'地中レーダ'),('放射年代・同位体標準',r'年代|同位体.*標準|国際標準'),
('安定同位体・水循環',r'同位体'),('構造物の強度・安全率',r'安全率|安全係数|許容応力'),
('信頼性と故障',r'信頼|借頼|言頼|故障'),('待ち行列',r'ATM|待ち行列|ポアソン|到着率'),
('工程管理・PERT',r'PERT|プロジェクト|作業リスト|アロー'),('最適化・意思決定',r'最適化|線形計画|利益|利得|デシジョン'),
('品質管理・統計',r'検査|品質|標準偏差|検定|相関係数'),('暗号・認証・攻撃対策',r'セキュリティ|パスワード|暗号|攻撃'),
('IP・通信',r'IP|TCP|ネットワーク|通信'),('論理式・命題',r'論理|真理値|必要.*条件'),
('キャッシュ・CPU',r'キャッシュ|CPU|クロック'),('数値表現',r'進数|浮動|ビット|精度'),
('アルゴリズム・再帰',r'アルゴリズム|プログラム|アッカーマン'),('形式言語・木',r'構文|文字列|数値列|算術木'),
('ベクトル・微分演算',r'ベクトル|div|rot|勾配'),('微積分・求積',r'積分|導関数|微分'),('有限要素法',r'有限要素'),
('材料の応力・変形',r'応力|ひずみ|歪|荷重|断面|はり|弾性'),('生物・遺伝',r'DNA|RNA|遺伝|生体|クローン|タンパク'),
('環境法・循環・持続可能性',r'循環|環境|廃棄|温暖|SDG'),('科学技術史',r'科学史|技術史|業績|革命'),
('技術士の義務・責務',r'技術士法|信用失墜|資質向上|秘密保持'),('公益・説明責任',r'公衆|説明責任|公益'),
('知的財産',r'知的財産|特許|産業財産'),('安全・リスク評価',r'安全|リスク'),('研究・情報倫理',r'研究|捏造|盗用|個人情報'),
('ばね・振り子',r'ばね|振り子|ひも.*錘'),('摩擦・力のつり合い',r'摩擦|斜面'),('軌道・万有引力',r'初速度|静止衛星'),
('静電場・容量',r'コンデンサ|電界|静電|電荷'),('電磁誘導・磁性',r'コイル|ソレノイド|磁性|磁場|磁気'),
('回路・抵抗',r'抵抗|回路'),('波動・音',r'正弦波|音|振動'),('光学・レンズ',r'レンズ|光の|スリット|回折格子'),
('熱力学・熱機関',r'カルノー|ピストン|熱力学|比熱|熱伝導'),('単位系・換算',r'単位|SI'),
('原子核・放射線',r'原子核|半減期|放射線|吸収線量'),('化学平衡・反応',r'平衡|反応|触媒'),
('相平衡・溶液',r'蒸気圧|溶液|凝固|沸点|溶解'),('電気化学',r'電池|電極'),('結晶・分子構造',r'結晶|格子|電子配置|結合'),
('有機・高分子',r'高分子|ナイロン|樹脂|界面活性剤|ベンゼン|メタン'),('分析・分離',r'分析|蒸留|分離|スペクトル'),
('鉱物・岩石',r'鉱物|岩石|変成岩'),('堆積相・構造',r'堆積|推積'),('地質構造',r'断層|褶曲'),
('地球内部・プレート',r'地球.*内部|マントル|プレート|地殻'),('火山・マグマ',r'火山|水山|マグマ'),
('資源・鉱床',r'鉱床|地熱資源'),('地盤・斜面災害',r'液状化|地盤|地すべり|山崩れ|トンネル'),
('地下水・水理',r'地下水|帯水層|水理'),('大気・海洋・物質循環',r'大気|海洋|海水|水循環|炭素循環|陸水')]
def main():
    rows=read_csv('data/questions.csv'); output=[]; unresolved=[]
    overridepath=ROOT/'config/classification_overrides.json'
    overrides=json.loads(overridepath.read_text()) if overridepath.exists() else {}
    taxonomy=[]
    for key,major,middle,stem,pattern in APPLIED:
        taxonomy.append({'key':key,'subject':'APPLIED','major':major,'middle':middle,'file':'chapters/applied_science/'+stem+'.tex','pattern':pattern})
    for group,rules in BASIC_RULES.items():
        for n,(middle,pattern) in enumerate(rules):
            taxonomy.append({'key':f'basic_{group}_{n}','subject':'BASIC','major':BASIC_MAJOR[group-1],'middle':middle,'file':'chapters/basic/'+BASIC_STEMS[group-1]+'.tex','pattern':pattern})
    for n,(middle,stem,pattern) in enumerate(APT):
        taxonomy.append({'key':f'apt_{n}','subject':'APT','major':middle,'middle':middle,'file':'chapters/aptitude/'+stem+'.tex','pattern':pattern})
    (ROOT/'config/taxonomy.json').write_text(json.dumps(taxonomy,ensure_ascii=False,indent=2))
    for row in rows:
        rawtext=(ROOT/row['question_text_file']).read_text()
        text=normalize(rawtext)
        lines=rawtext.splitlines(); prompt=[]
        for line in lines:
            if re.search('[①②③④⑤]',line):break
            prompt.append(line)
        prompt=normalize('\n'.join(prompt))
        major=middle=stem=evidence=''; confidence='low'; method='keyword_rules_initial'
        if row['subject']=='BASIC':
            group=int(row['question_number'].split('-')[0]);major=BASIC_MAJOR[group-1]
            stem='chapters/basic/'+BASIC_STEMS[group-1]+'.tex'
            for scope in (prompt,text):
                for title,pattern in BASIC_RULES[group]:
                    match=re.search(pattern,scope)
                    if match:middle=title;evidence=match.group();confidence='medium' if scope==prompt else 'low';break
                if middle:break
            if not middle:middle=major+'（横断・詳細要確認）';evidence='公式問題群番号';method='official_group_only'
        elif row['subject']=='APT':
            for title,file,pattern in APT:
                match=re.search(pattern,prompt)
                if match:major=middle=title;stem='chapters/aptitude/'+file+'.tex';evidence=match.group();confidence='medium';break
            if not major:major=middle='技術者倫理・意思決定';stem='chapters/aptitude/02_engineering_ethics.tex';evidence='適性科目・要個別確認';method='subject_only_initial'
        else:
            forced=None
            isotope_context='同位体' in prompt and re.search(r'海水|SMOW|標準.*(?:試料|物質)|降水|酸素.*水素|水素.*酸素|天然の水|炭酸塩|δ|VSMOW',text)
            if isotope_context:
                forced=next(rule for rule in APPLIED if rule[0]=='earth_isotope')
                _,major,middle,file,_=forced;stem='chapters/applied_science/'+file+'.tex';evidence=isotope_context.group();confidence='medium'
            for key,pattern in TITLE_RULES:
                if forced:break
                match=re.search(pattern,prompt)
                if match:
                    forced=next(rule for rule in APPLIED if rule[0]==key)
                    _,major,middle,file,_=forced;stem='chapters/applied_science/'+file+'.tex';evidence=match.group();confidence='medium'
                    break
            for scope in (() if forced else (prompt,text)):
                matches=[]
                for key,title,category,file,pattern in APPLIED:
                    match=re.search(pattern,scope)
                    if match: matches.append((match.start(),title,category,file,match.group()))
                if matches:
                    _,major,middle,file,evidence=min(matches,key=lambda x:x[0])
                    stem='chapters/applied_science/'+file+'.tex';confidence='medium' if scope==prompt else 'low'
                if major:break
        override=overrides.get(row['question_id'])
        if override:
            major=override['major'];middle=override['middle'];stem=override['file'];evidence=override['evidence'];method='manual_content_review';confidence='medium'
        if not major:unresolved.append(row['question_id'])
        topic=middle+'（概念横断）'
        for title,pattern in TOPIC_RULES:
            if re.search(pattern,prompt):topic=title;break
        row.update(major_category=major,middle_category=middle,minor_category=topic,topic=topic,subtopic=evidence,
                   core_concept=middle,tex_file=stem,classification_method=method,
                   classification_confidence=confidence,classification_verified='false')
        if '組合せ' in prompt or '組み合わせ' in prompt:kind='組合せ選択'
        elif re.search('不適切|誤って|誤り',prompt):kind='誤り選択'
        elif re.search('最も近い|求め|計算|値として|大きさは',prompt):kind='数値・計算選択'
        else:kind='正しい記述・用語選択'
        row['question_type']=kind
        row['requires_calculation']='true' if kind=='数値・計算選択' else 'unknown'
        row['requires_figure']='true' if re.search(r'図|グラフ|真理値表|下表',prompt) else 'unknown'
        row['requires_law']='true' if re.search(r'法第|法律|法令|責任法|保護法|技術士法|基本法',text) else 'unknown'
        row['question_summary']=(middle+'を扱う'+kind+'問題。') if middle else ''
        output.append({'question_id':row['question_id'],'major_category':major,'middle_category':middle,
                       'minor_category':topic,'topic':topic,'tex_file':stem,'method':method,
                       'evidence':evidence,'confidence':confidence,'classification_verified':'false',
                       'review_required':'true'})
    write_csv('data/questions.csv',rows)
    write_csv('data/classifications.csv',output)
    (ROOT/'extracted/logs/unclassified.json').write_text(json.dumps(unresolved,ensure_ascii=False,indent=2))
    print('Tentative classifications:',len(rows),'unclassified:',len(unresolved))
    print('\n'.join(unresolved))

if __name__=='__main__':main()
