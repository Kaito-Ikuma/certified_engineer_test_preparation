# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,ch,neg,num='計算入力なし。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=num,negation_differences=neg,choice_differences=ch,figure_differences='両原典に設問固有図なし。全5肢の文字・化学記号・数値を別々に照合。',temporal_differences='原典当時の説明と現在の補足を区別。代表水貯留・河川平均は推定集計の時点を示し、今日の精密値へ置換しない。',evidence='S7_021原典19画像で幹・全5肢・方向・数値を照合。初回独立解答保存後に公式と一次資料比較。疑義のある肢も原語を保持。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H23-REG-APPLIED-19','H28-REG-APPLIED-27','near_repeat','炭素循環・初期CO2・温室・嫌気生成・海洋貯留','5記述を科学的過程へ対応','H23肢3の風化・生物均衡をH28肢4へ移動、メタン肢4を3へ。残りは同じ文言群。公式3→4。均衡範囲疑義は両問で残す。','正しいもの対最も適切。共に適切肢を選ぶ。')
add('H26-REG-APPLIED-27','R03-REG-APPLIED-21','near_repeat','CO2赤外・風化促進・貯留とメタン代謝','過程・反応方向・量関係を独立判定','同じ5概念を再配列。H26肢4の濃度減少の原因という文言はR03肢2で減少プロセスへの関与へ変更。公式4→2。','双方最も適切。')
add('H23-REG-APPLIED-19','H26-REG-APPLIED-27','same_concept','速い生物循環と遅い岩石炭素循環','貯留量と過程を区別','初期CO2の低/高、光合成・分解・呼吸の均衡文対風化と光合成の関与、メタンの酸化条件対光合成の取り違え。誤り機構と疑義が異なる。','正しいもの対最も適切。','海洋との比が1/2対同程度という誤答条件。')
add('H24-REG-APPLIED-33','H29-REG-APPLIED-20','same_method','世界河川の海塩支配の否定と採水変化','イオン源・Fe酸化・硫化物・CO2脱気を比較','海塩支配肢5を肢1へ、鉄沈殿肢1を肢5へ。鉱山・珪酸が中間で共通。pHは室内放置との比較対攪拌との比較で条件が変わるため同一問題としない。公式5→1。','双方最も不適切。')
add('H25-REG-APPLIED-31','R01-REG-APPLIED-20','same_concept','石灰岩と陸水・同位体','溶存種と分別履歴の対応','Ca増加と原本炭酸カルシウム型が共通し名称疑義を保持。H25同位体の反比例が誤り4、R01緯度効果は適切でFeMnの大小が誤り1。','双方最も不適切。')
add('H26-REG-APPLIED-25','R01-RET-APPLIED-18','same_method','全球水量の概数・分母と貯留','河川と大気のストック比較','後半の河川/湖肢の順を入替、湖沼に淡水という限定を追加。河川が大気より多い誤り5→4。陸水70%分母疑義も共通する。','双方最も不適切。','総14億km3・海97%・陸水雪氷70%の概数は一致。湖は全湖対淡水湖の対象差。')
add('H23-REG-APPLIED-22','H26-REG-APPLIED-25','same_concept','水の貯留と流量の違い','候補集合内のストック大小を比較','H23は5貯留から地下水最大4。H26は概数・割合・湖地下大小・河大気大小を判定し5。不適切選択へ方向が変わる。','最大量対最も不適切。')
add('H27-REG-APPLIED-27','R01-REG-APPLIED-20','same_concept','河川ケイ酸と酸化還元','地質供給・溶存形態・電子受容体を判定','両問にケイ酸と還元地下水があるがH27は珪藻/逆風化の条件疑義で公式5・初回4|5、R01はFeMn大小が誤り1。H27の未解決をR01の一致で解消しない。','双方最も不適切。')
add('R04-REG-APPLIED-20','R06-REG-APPLIED-22','same_concept','鉱物水反応・風化・二次鉱物','反応条件と平衡/速度を分ける','R04は活量理論対象の誤り1、R06はCO2脱気の方向逆2。方解石・粘土の接続はあるが個別解法と誤り対象は異なる。R04の固相全溶解条件疑義も保持。','双方最も不適切。')
(ROOT/'config/authored_batches/S7_021_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'reviewed comparisons')
