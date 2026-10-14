# coding: utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,numeric,choices,fig,neg='双方は適切な空欄又は組合せを選ぶ。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=numeric,negation_differences=neg,choice_differences=choices,figure_differences=fig,temporal_differences='規格・法令時点の同一視を行う設問ではない。所与の強度・価格・費用と現在値を区別する。',evidence='S7_027の16原典画像で17問の全候補と図を比較、公式前初回17一致。前提不足の疑義は部分校正に保持。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H25-REG-BASIC-1-2','H28-REG-BASIC-1-3','near_repeat','薄い定規の引張/圧縮・座屈と安全率',
 '引張と圧縮の安定性を分け、許容応力を強度/安全率とする。','計算値なし。前提と空欄語が同じ。',
 '最初の3候補は同じ。H25の4と5がH28の5と4へ入れ替わる。正答5→4。','双方定規の変形を用いる。図の文脈を原典で確認。')
add('R01-REG-BASIC-1-4','R05-REG-BASIC-1-2','near_repeat','小径柱の曲げ座屈',
 '小さい径→小EI、臨界を超える軸圧縮→曲げ座屈、共振/ねじれを排除。','新たな寸法や数値を与えず同じ定性モデル。',
 'R01正5→R05正4。R01の誤候補は小以下ねじれ座屈、大以下ねじれ共振、小超ねじれ共振、大超曲げ共振。R05は大以下ねじれ共振、小超ねじれ座屈、大超曲げ共振、小以下曲げ共振。全候補同一とはしない。',
 '棒の固定端と軸圧縮・横曲がりの図を比較。')
add('H29-REG-BASIC-1-4','R05-REG-BASIC-1-3','near_repeat','引張測定と弾塑性・引張強さ',
 '伸びと規格化ひずみ、回復と残留、最大公称応力の定義を対応。','数値計算なし。H29応力は断面積の初期値未指定、R05は公称応力を明示。',
 'H29正5→R05正3。他4組の語は共通で配列が変わる。H29第4の破断強度はR05第5の引張強さへも変更。全候補の単なる並べ替えではない。',
 '組合せの列順を画像確認。公称の語の差を残す。')
add('R01-RET-BASIC-1-5','R04-REG-BASIC-1-4','same_method','安全率と総費用の凸最小化',
 'C=a/(1+bx)+cxを微分し、停留点・二階微分・定義域・候補を確認。','再試験a90/b4/c10、x≥1、最小1.25、27.5億。R04 a9/b1/c1、x>1、最小2、5億。',
 '再試験候補1,1.25,1.5,1.75,2の正2。R04候補2,2.5,3,3.5,4の正1。',
 '設問所与の費用式と不等号を照合。図の形状を同じ数値として流用しない。')
add('R04-REG-BASIC-1-5','R06-REG-BASIC-1-3','near_repeat','円梁の曲げ応力とたわみの寸法依存',
 '固定q,L,EでI∝d4、Z∝d3から応力逆3乗、たわみ逆4乗。','R04は矩形幅固定の高さ逆2乗も問う。R06は円だけ。固定荷重と自重の疑義を双方保持。',
 'R04空欄3/inverse/4/2正3。R06空欄3/inverse/4/inverse正1。空欄Dの対象も違う。',
 '双方両端単純支持等分布荷重の円梁を確認。R04矩形の荷重方向高さも照合。')
add('R03-REG-BASIC-1-5','R06-REG-BASIC-1-2','same_concept','限界状態の複数性',
 '使用・疲労・終局を分け、一つだけという主張を排除。','新しい数値計算なし。',
 'R03は座屈/許容応力/限界状態の正誤4列、限界はエ誤、全体誤正誤誤正5。R06は使用/疲労/終局の穴埋め、正2。',
 '組合せ表の列数と順を確認。',
 'R03は個々の正誤の組合せ、R06は3空欄の対応。正の番号の転用不可。')
add('H24-REG-BASIC-1-2','R02-REG-BASIC-1-3','same_concept','部分損傷の非線形と崩壊・座屈の区別',
 '弾性部材だけで全体崩壊を決めず、塑性再配分と機構、全体安定を分ける。','数値なし。H24は高不静定の余力、R02は5破損モデル。',
 'H24は4空欄正5、R02は5記述正誤正3。全体安全の全称と短柱の破断強度の疑義は別々に保持。',
 '全候補の原典列順を比較。',
 'H24は適切な語、R02は誤誤正正正の組合せ。')
add('H25-REG-BASIC-1-2','R03-REG-BASIC-1-5','same_concept','座屈と許容応力の安全率',
 '材料強度/nと弾性座屈のEI/(KL)2を分ける。','H25は数値なし定規、R03は長さ/降伏強度の比較で計算値なし。',
 'H25は引張圧縮座屈安全率正5、R03は長さ増加/同E/掛ける安全率/唯一限界の正誤正5。番号一致は問題同一を意味しない。',
 '定規図とR03の正誤4列表を区別。')
p=ROOT/'config/authored_batches/S7_027_reviewed_relations.json';assert not p.exists()
p.write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'relations')
