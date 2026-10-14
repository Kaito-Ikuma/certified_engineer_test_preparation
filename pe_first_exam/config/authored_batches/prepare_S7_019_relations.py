# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,num,ch,neg,fig='双方に設問固有図なし。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=num,negation_differences=neg,choice_differences=ch,figure_differences=fig,temporal_differences='年度の違いを保持。ISBNは旧10桁と13桁の方式の時点差を区別し、現在方式へ原典を書き換えない。',evidence='S7_019の12原典画像で15問を読み、全5肢・数値・式・図・否定を個別比較。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H24-REG-BASIC-2-3','H28-REG-BASIC-2-1','same_method','3状態マルコフ連鎖','行列累乗と定常分布','自己1/2、他1/4、二日自己3/8、他5/16、極限1/3が共通。','H24の誤肢4雨→雨1/4をH28では肢1雨→雨3/8へ修正。H24肢3雨→曇5/16がH28肢4曇→晴3/16へ変更され誤りとなる。他1→2、2→3、5→5。正答番号は双方4だが問う内容は異なる。','誤っている対最も不適切。同方向。','自己3ループと他状態6矢印を両年度で確認。状態位置と全確率は一致。')
add('H28-REG-BASIC-2-5','R06-REG-BASIC-2-4','near_repeat','偶数パリティ','反転数の偶奇と位置情報','7ビット1010100、付加1、8ビット10101001が共通。','1/2/3は一致、4と5を交換。正答4→5。全候補を別画像で比較。','双方最も適切。')
add('R02-REG-BASIC-2-1','R05-REG-BASIC-2-4','near_repeat','可逆/非可逆と事前分布未知の圧縮','適応/辞書型を反例にする','数値指定なし。','前者1→後者4、2→3、3→5、4→1、5→2。後者の完全復号/復元の表現差は可逆の趣旨が同じ。正答4→1。','双方最も不適切。')
add('H28-REG-BASIC-2-4','R02-REG-BASIC-2-6','parameter_variant','キャッシュ平均アクセス時間','期待値で時間を平均し速度比は逆比','1/100ns・95%から50/450ns・90%へ。総時間/追加時間の両模型で最近候補は変わらない。','前者時間のみ0.05/0.95/5/5.95/95ns、後者時間45/60/90と速度2/5倍の組。正答4対5。','前者最近の値、後者適切な組。','前者文章と5値、後者ア/イの候補表の全セルを画像照合。')
add('R03-REG-BASIC-2-3','R07-REG-BASIC-2-5','same_method','圧縮後データ長と有効通信速度','t=D/(vη)を未知量へ解き単位を統一','5GB・1/2・200Mbps・70%から250MB・8/10・100Mbps・25秒へ。十進G/Mは共通。','前者時間286/143/100/18/13秒、後者利用率8/10/16/64/80%。正答2対4。求める量が異なる。','前者最近の値、後者適切な値。')
add('H26-REG-BASIC-2-3','R05-REG-BASIC-2-3','same_concept','ISBN重み付き検査数字','合同式の剰余条件','ISBN10は重み10〜1/法11、ISBN13は重み1/3交互/法10。元の桁列は異なる。','前者は五つの変更後番号から有効番号を選ぶ。後者は未知末尾Xを1/3/5/7/9から選ぶ。正答4対5。同じ方式として計算しない。','双方適切な候補。','前者ISBN数字と積の表、後者添字a13〜a1と合同式の全項を画像確認。')
(ROOT/'config/authored_batches/S7_019_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'reviewed comparisons')
