# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,numbers,choices,negation='選択方向は一致。',figures='両原典の全5肢を実画像確認。設問固有図なし。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=numbers,negation_differences=negation,choice_differences=choices,figure_differences=figures,temporal_differences='法制度・時点依存の条件なし。',evidence='S7_015原典20頁の21問を画像確認。数値・式・否定・5肢・配置・表・次数を比較。関係承認は解釈疑義の解消とは異なる。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H23-REG-APPLIED-03','H25-REG-APPLIED-05','near_repeat','後退音源のドップラー効果','波長=(c+u)/f、観測c/λ','両年440 Hz、4 m/s、音速340 m/s、静止観測者。','430/435/440/445/450 Hzの配列が一致、2。前者の運動音源名等の表現差を残す。')
add('H23-REG-APPLIED-07','H26-REG-APPLIED-07','near_repeat','凸レンズの実虚・向き・移動','符号付き像距離とdb/da<0を使う','数値指定なし。焦点の内外と物体移動。','ア/イ/ウ/エ/オの5候補行が一致、2。文章表現の差を残す。',figures='両年の5×5空欄候補表を全セル照合。')
add('H25-REG-APPLIED-02','H29-REG-APPLIED-04','near_repeat','波長と位相速度','kλ=2π、d位相=0でv=ω/k','A,ω,k>0の同じ波y=A sin(ωt−kx)。','候補3と5が交換され、正答3→5。1/2/4は同じ組合せ。')
add('H29-REG-APPLIED-04','R07-REG-APPLIED-05','same_method','進行波の位相係数と速度','時間空間の2π反復と位相一定の微分','ω,k指定対T,λ指定。ω=2π/T、k=2π/λで対応。','前者はλとvを選び5、後者はvとωを選び4。候補の物理量が異なる。')
add('R01-REG-APPLIED-05','R05-REG-APPLIED-05','parameter_variant','2音源の干渉','sqrt(L²+a²)−Lを計算し、半波長へ対応','間隔2.0→2.4 m、正面距離3.3→4.0 m、音速はともに340 m/s。','280/310/370/430/490対160/210/260/320/400 Hz、正答2→3。次の次数はいずれも候補外。',figures='両配置図の中央・片方正面・間隔・聴取線の距離を比較。3.3 mを3 mへ丸めない。')
add('H24-REG-APPLIED-03','R02-REG-APPLIED-07','same_concept','電磁波のスペクトル','E=hc/λで順序を反転','数値指定なし。同じ赤外・可視・紫外・γの4領域。','5候補の領域配列は同じだが比較量が異なるため正答1→4。',negation='波長の長い順対光子エネルギーの大きい順。順序方向を無条件に流用しない。')
add('H28-REG-APPLIED-05','R06-REG-APPLIED-05','same_concept','焦点内の虚像','1/f=1/a+1/bの符号を読む','第一f15,a6,二枚間隔20,最終b60 cm対f15,a10 cm単レンズ。','第二焦点距離20 cmの3対手前30 cm正立虚像の5。求める量と二段計算の有無が異なる。',figures='H28二枚配置図あり、R06設問固有図なし。')
add('H24-REG-APPLIED-02','R04-REG-APPLIED-05','same_concept','縦横波と波速','変位方向の定義と等方弾性体の復元力を分ける','数値指定なし。H24は媒質・温度・速さ、R04は合成・衝撃波・変調も扱う。','共通肢の固体縦波>横波は適切。誤りはH24海水速度比較4、R04縦横の命名2。')
(ROOT/'config/authored_batches/S7_015_reviewed_relations.json').write_text(json.dumps({'relations':rows},ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'relations')
