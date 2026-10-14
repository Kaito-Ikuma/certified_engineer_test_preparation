# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,choices,neg,num='定量入力なし。',time='試験年度を定義基準日として固定。2019-05-20前後を区別。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=num,negation_differences=neg,choice_differences=choices,figure_differences='両原典は数式・記述候補で固有図なし。全5肢の指数・順序を照合。',temporal_differences=time,evidence='S7_023の原典18画像・19全肢確認、公式前初回保存後に比較。公式一致と原典の記述疑義を区別。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H23-REG-APPLIED-06','H27-REG-APPLIED-04','same_concept','SI組立単位の指数','量方程式から基本単位因子を導く','N2・Ω5は共通。H23のBq/TをH27はC/Paへ、Wは正しい4から長さ指数1の不適切4へ変更。正答T3対W4。','誤っている対最も不適切。',time='両問の導入は当時もcdを欠く6単位列挙。現行改定と無関係な疑義。')
add('H25-REG-APPLIED-04','H27-REG-APPLIED-04','same_method','仕事の長さ指数を電圧・仕事率へ移す','J=NmからP=J/s、V=J/Cを導く','不適切はV5対W4、長さ指数1を2へ戻す。同じ位置のN2/Pa3は適切。Hz1→C1、J4→W4、V5→Ω5へ集合変更。','誤っている対最も不適切。')
add('H23-REG-APPLIED-06','R05-REG-APPLIED-13','same_concept','SI電気抵抗と単位','Ω=J/(Q I)、Q=ItでAの指数-2','ΩはH23正しい5、R05はA^-1の誤り5。H23の誤りT3に対しR05はΩ5。R05は非SIのSt正しい4を加える。','誤っている対最も不適切。')
add('H28-REG-APPLIED-06','H29-REG-APPLIED-05','same_concept','旧Kの三重点基準','定義年と三重点・凝固点を分ける','H28はKの凝固点4が誤り、kg原器/mol12Cは適切。H29はK三重点1・.01C2は適切、V=N/C4が誤り。正答番号同じでも誤りの概念は違う。','ともに最も不適切。',time='2016/2017の両問は旧K定義。現行k固定と区別。')
add('H29-REG-APPLIED-05','R01-RET-APPLIED-01','near_repeat','温度・電荷・角とSI定義改定','提示単位等の妥当性を時点付きで確認','三重点.01C2・C=As3・無次元rad5は配置維持。H29のK三重点1を再試験はkg原器1へ、誤V=N/C4を正しい光速m4へ変更。誤り4→1。','ともに最も不適切。',time='2017旧K対2019改定明記。再試験三重点は近似/厳密さを区別し部分校正。')
add('R02-REG-APPLIED-09','R07-REG-APPLIED-09','parameter_variant','kgのhとGの取り違え','現行SI定義定数と基本単位を対応させる','m1位置同じ、A3→2、誤kgG2→3、mol5→4、R02正K4をR07正cd5へ置換。正答2→3。他肢を同一集合とはしない。','ともに最も不適切。',time='2020/2025はいずれも2019改定後。')
add('R03-REG-APPLIED-09','R07-REG-APPLIED-09','same_concept','光度と質量の定義定数','黒体の歴史と単色放射を分ける','R03の誤黒体cd1をR07は正単色cd5へ、正hのkg3を誤Gのkg3へ変更。秒はR03のみ、AはR07のみ。正答1対3。','ともに最も不適切。')
add('H26-REG-APPLIED-09','H28-REG-APPLIED-09','parameter_variant','半減期と元核種の残存比','N/N0=2^(-t/T)へ同単位の比を代入','H26候補1/6,1/8,1/9,1/16,1/18、H28は.20,.15,.07,.05,.03へ全候補変更、正答2→3。','最も適切な数値対最も近い値。','T30年/t90年の整数3半減期対T8日/t30日の3.75半減期。','数学模型は同じ、暦年と日の比を混ぜない。')
add('H28-REG-APPLIED-09','R04-REG-APPLIED-09','parameter_variant','非整数半減期の指数残存比','2^(-30/T)を整数へ丸めず計算','.20候補1は共通。.15/.07/.05/.03から.10/.05/.03/.01へ変更。約.0743選択3対約.0992選択2。','ともに最も近い値。','経過30日は共通、半減期8日→9日。','核種名を両問とも指定しない。T値だけの模型比較。')
assert len(rows)==9
(ROOT/'config/authored_batches/S7_023_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('prepared',len(rows))
