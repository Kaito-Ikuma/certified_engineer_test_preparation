# coding: utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,choices,negation='双方は最も不適切な記述を選ぶ。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences='数値計算の変更なし。専門語と代表モデルの条件を比較。',negation_differences=negation,choice_differences=choices,figure_differences='双方とも設問固有の図なし。全5肢と本文を原典画像で比較。',temporal_differences='地質モデルの比較である。各年度の記載を保持し、教材補足の条件を原文へ混入しない。',evidence='S7_029の15原典画像で18問を照合。初回解答は公式前に保存。肢順・否定・起源の限定と一般化の差を比較。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H23-REG-APPLIED-25','H29-REG-APPLIED-25','near_repeat','河川端成分と河口システム','蛇行/網状の典型を比較し、逆級化の非一意性を区別する。','5肢の対応と正5は同じ。H23は誤り、H29は最不適。勾配の語の細差を原典で保持。','H23は誤っているもの、H29は最も不適切。典型と全称の範囲は双方に疑義として残す。')
add('H29-REG-APPLIED-25','R05-REG-APPLIED-30','variant','蛇行/網状とデルタ・エスチュアリー','流路型の典型と海退/沈水の定義を比べる。','H29順[端成分,デルタ,内湾,逆級化,蛇行]正5、R05順[端成分,逆級化,蛇行,デルタ,内湾]正3。番号を移植しない。')
add('H30-REG-APPLIED-25','R04-REG-APPLIED-28','near_repeat','流れと堆積構造の対応','ヘリンボーンの潮流反転と蛇行主相を分ける。','H30正2、R04正1で入替え。H30は混濁流の起源を海底地すべりに限る語とBouma、R04は乱流支持の定義に変更。')
add('R04-REG-APPLIED-28','R07-REG-APPLIED-27','near_repeat','斜交・流痕・タービダイト','床形の移動、波浪、密度流を生成機構から対応させる。','R04[蛇行,HCS,移動,流痕,乱流]正1、R07[流痕,移動,蛇行,タービダイト,HCS]正3。R07は一般に級化という性状を記載。')
add('R01-REG-APPLIED-28','R06-REG-APPLIED-30','variant','未固結段階の火炎構造','沈積による初生とその後の荷重/流動変形を分ける。','同じ5名称がR01[流痕,火炎,リップル,葉理,級化]正2、R06[葉理,級化,火炎,リップル,流痕]正3。','双方は二次的構造に該当するものを選ぶ肯定問題。')
add('R02-REG-APPLIED-29','R01-REG-APPLIED-28','same_concept','未固結構造と形成時の上下','形の成因を分類し、荷重・脱水の向きを考える。','R02は羽毛/皿/荷重/流痕/生痕で最不適1。R01は火炎の二次分類正2。羽毛を火炎と取り違えない。','R02は上下判定で最不適、R01は二次構造の該当を選ぶ。')
add('H28-REG-APPLIED-34','R02-REG-APPLIED-31','same_concept','火山灰による層序対比','同定、適用域、初生性を分けて検討する。','H28は花粉淡水限定が正3で他に最確火山灰表現。R02は局地/水域/外観/時代の不当除外を避け、テフラ定義の4。','H28は最不適、R02は最適を選ぶ。')
add('H23-REG-APPLIED-25','R06-REG-APPLIED-31','same_concept','堆積相と環境帯の移動','河川/河口の相を記載し、相の組合せ・累重の用語へ接続する。','H23は蛇行/網状の典型混同正5、R06は組合せをシーケンスと呼ぶ混同正4。選択肢の命題は異なる。','H23は誤り、R06は最不適。')
p=ROOT/'config/authored_batches/S7_029_reviewed_relations.json';assert not p.exists()
p.write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n');print('Prepared',len(rows),'relations')
