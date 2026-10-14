"""Explicit comparisons from the manually viewed source pairs, not score promotion."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(left,right,kind,concept,method,numbers,choices,figures='両方図なし',negation='選択方向は一致'):
 rows.append(dict(left_question_id=left,right_question_id=right,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=numbers,negation_differences=negation,choice_differences=choices,figure_differences=figures,temporal_differences='時点依存の法制度・観測値なし',evidence='両問題の原典ページ画像・条件・5肢を比較。校正JSONと各バッチのsource evidenceへ追跡可能。自動類似候補からの承認ではない。',approval_status='verified',source_hash_left=by[left]['source_sha256'],source_hash_right=by[right]['source_sha256'],rubric_version='1.0-review1'))
add('H29-REG-BASIC-2-2','R01-RET-BASIC-2-4','near_repeat','数値表現・指数バイアス','13を1.625×2^3に正規化し符号・指数・仮数を作る','入力13.0と形式1/8/23ビット、バイアス127は一致','符号・指数・仮数の候補の配列が異なり、正答位置4→5。誤答内の重複候補も原典通り保持')
add('H27-REG-BASIC-2-4','R01-RET-BASIC-2-3','near_repeat','情報容量と基数接頭語','2×10^12 Bを2^40 Bで割る','入力2 TBと問題独自の二進TB定義は一致','候補は1.8/2.0/2.1/2.2/2.3対1.6/1.8/2.0/2.2/2.4、正答位置1→2')
add('H30-REG-BASIC-2-3','R02-REG-BASIC-2-4','parameter_variant','固定幅補数','1の補数はビット反転、2の補数はさらに1加算','5ビット01011対6ビット100110','二補数/一補数の順は一致、値と誤答配列が異なり位置3→2')
add('H27-REG-BASIC-2-3','R06-REG-BASIC-2-1','parameter_variant','循環二進小数','2倍して整数部を取り剰余を反復','入力0.1対0.6、表示16桁は一致','生成する16桁と5候補が異なり位置3→1')
add('R02-REG-BASIC-2-5','R04-REG-BASIC-2-5','parameter_variant','二進整数の逐次評価','s←2s+a_iの上位桁からのHorner法','11010101対11001011','途中値の空欄が3個対4個、正答位置はともに5だが穴の位置・値が異なる','同じ更新構造。例示ビット列・途中値・空欄位置を両流れ図で照合')
add('H30-REG-APPLIED-32','R04-REG-APPLIED-35','near_repeat','重力・磁気探査の物理量','各語を重力・磁気・熱放射へ対応','数値条件なし','5語の集合は同じだが順序が異なる。プランク関数は位置3→4')
add('R04-REG-APPLIED-35','R06-REG-APPLIED-34','parameter_variant','重力・磁気探査と別の観測量','ジオイド/運動補正/磁化比/転移温度を対応','数値条件なし','共通4語の並びを変更。非該当語はプランク関数からAEへ、位置4→3',negation='不適切対最も関係が薄い。判断の相対的な方向は一致')
add('H27-REG-APPLIED-22','R07-REG-APPLIED-33','same_concept','重力補正と密度効果','基準場・平板引力・観測条件を分離','H27は無限層の深度独立、R07は密度差の符号','5記述は異なる。誤りは深度依存2対密度符号5。重力補正の同概念であり同一問題とはしない')
add('H30-REG-BASIC-2-4','R03-REG-BASIC-2-2','near_repeat','XNORの否定とXOR','対象の否定をド・モルガン則で変形してXORと確認','変数・対象式は一致、数値条件なし','正答の表記はORとAND否定の積対2つのORの積。候補5→2。他の候補も比較し、単なる番号対応ではない','対象式の二重上線・各項の否定範囲を画像照合')
add('H26-REG-BASIC-2-2','R05-REG-BASIC-2-2','parameter_variant','ユークリッド互除法','非零の余りで更新、零で終了しBを出力','入力はともに正の自然数、具体的数値なし','ア/イ/ウの候補配列が異なり、正答2→4','H26はアが横の終了、R05はアが下の更新分岐。アとイの位置を入れ替え、両図の矢印を比較')
add('H29-REG-BASIC-2-4','R03-REG-BASIC-2-4','near_repeat','うるう年規則と決定表','4条件列の動作を平年/うるう年/平年/うるう年と判定','4・100・400の条件は一致。独自に示した2019/2024/1900/2000は解説用の例','原典の候補2と3の動作表を交換。正答3→2、他の表も全セル比較','条件部の全行、不要欄、動作行のXと−を両年の画像で確認')
add('H25-REG-BASIC-2-4','R01-RET-BASIC-2-5','same_concept','部分集合の上下限','既知領域を分割して未知領域の最小・最大を求める','全100万、65万、55万は同じ数値だが、H25はLとIの各総数、再試験はI総数と共通部分。求める対象もLかつ非I対非Lと異なる','可能範囲はともに10〜45万だが候補4→1。条件が違うので近似再出題とは認定しない')
extra=ROOT/'config/authored_batches/S7_007_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_008_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_009_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_010_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_011_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_012_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_013_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_014_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_015_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_016_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_017_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_018_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_019_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_020_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_021_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_022_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_023_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_024_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
extra=ROOT/'config/authored_batches/S7_025_reviewed_relations.json'
if extra.exists():rows.extend(json.loads(extra.read_text())['relations'])
(ROOT/'config/authored_batches/S7_reviewed_relations.json').write_text(json.dumps({'relations':rows},ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'explicit source comparisons')
