# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,choices,neg='双方最も不適切。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method='形成機構・幾何・物質・活動時期を分けて全肢を定義と比較する。',numerical_differences='新たな数値計算なし。原典の年代/割合/距離の有無は肢差に保持。',negation_differences=neg,choice_differences=choices,figure_differences='双方設問図なし、全5肢を原典画像で確認。配列の方位を推測しない。',temporal_differences='各年の原典を保持。地質学の共通概念でも史料条件・可能性の時点条件の追加や削除を区別。',evidence='S7_025原典15画像の全肢確認、公式前初回20候補保存後に比較。独立解答の一致と各肢の一般妥当性は別。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H25-REG-APPLIED-20','R07-REG-APPLIED-30','near_repeat','断層の直接記録とダイアピール上昇','H25鏡肌1→R07鏡肌4、条線3→2、プルアパート4→1、ダイアピール5→5。H25破砕岩2はR07カタクレーサイト3へ具体化。共通候補だけで全肢同一とはしない。公式5→5。','双方最も関係が薄い。')
add('H25-REG-APPLIED-21','R05-REG-APPLIED-29','near_repeat','褶曲用語と貫入岩体','H25キンク1→R05キンク5、背斜2→3、ヒンジ3→4、プランジ4→2、ラコリス5→1。候補集合は一致するが配列と正答5→1が変わる。','双方最も関係が薄い。')
add('H25-REG-APPLIED-21','R02-REG-APPLIED-27','same_concept','褶曲の幾何と貫入','共通はキンク1→5、ヒンジ3→2。背斜はアンチフォーム、プランジはカルミネーション、ラコリスはシルへ変更。年代情報を使う背斜と形態アンチフォーム、線の傾きと軸の高まりは同義でない。正5→4。','双方最も関係が薄い。')
add('H26-REG-APPLIED-35','R06-REG-APPLIED-28','near_repeat','震源断層と地表の変位','H26分類1→R06分類1、震源誤定義2→5、活断層3→4、鏡肌条線4→3、断層岩5→2。全文の意味と第四紀更新世以降/近い将来の表現は対応する。正2→5。')
add('R01-REG-APPLIED-31','R05-REG-APPLIED-27','near_repeat','断層岩の機構と基質割合','R01ガウジ1→R05ガウジ5、誤固結度2→4、溶融3→2、フィッシュ4→3、雁行5→1。雁行の対象はR01断層岩→R05塑性剪断帯という差、可塑性等の表記差を保持。正2→4。配列/方位疑義を共有。')
add('H30-REG-APPLIED-26','R07-REG-APPLIED-29','near_repeat','地塁地溝と地震断層','H30誤地塁5→R07誤地塁4、分類3→1、撓曲4→2は単斜を追加、活断層1→3は第四紀→最近の地質時代。H30地震断層2の史料条件はR07地表地震断層5に無い。正5→4。初回一致でも史料条件の差は消さない。')
add('R01-RET-APPLIED-30','R03-REG-APPLIED-27','same_concept','雁行・共役と条線の情報','再試験の共役と雁行の誤同一視2はR03の異時期群を共役と誤認し得る正2へ。条線4→R03軸方向1、R03再活動の新旧3/条件依存断層岩4/ミ型5を追加。再試験は正断層1/トランスフォーム3/ガウジ5で集合が異なる。正2→5。')
add('H30-REG-APPLIED-26','R04-REG-APPLIED-29','same_concept','地塁地溝・相対上下と断層幾何','H30落ち込む地塊を地塁とする誤5に対しR04高い地塊は地塁・低い地塊は地溝の正4。R04誤リストリック5はH30に無く、ナップ・底剥離・花束も追加。H30史料条件2はR04に無い。正5→5でも誤記の対象は異なる。')
assert len(rows)==8
(ROOT/'config/authored_batches/S7_025_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'relations')
