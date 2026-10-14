# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,ch,neg,num='計算数値なし。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=num,negation_differences=neg,choice_differences=ch,figure_differences='設問固有図なし。組合せ/語句表は各原典の行列順と全セルを別々に照合。',temporal_differences='各出題年度の制度と原典語を保持。原典誤植・公式採点措置と現在の補足を区別。',evidence='S7_020原典18画像で幹・記述・候補・否定を照合。初回独立解答と一次資料の後続確認を分離。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H24-REG-APT-05','R04-REG-APT-10','same_concept','循環資源の一般優先順位','定義と順位の入替を検出','H24は5順位列の比較で3。R04は4記述のOOXXを5候補から選び4。再生利用の定義も問う。','最も適切な順位対正誤の適切組合せ。')
add('R04-REG-APT-10','R07-REG-APT-10','same_method','再使用・再生利用と一般優先','形態を定義し真偽を集約','前者ウの再使用を再生利用と誤称、エの2/3位入替。後者イウが双方入替、オ順位入替で正しいアエ2。候補表4対数候補3。','正誤組合せ対適切数。','4記述対5記述。候補数値4/3/2/1/0。')
add('R01-RET-APT-11','R06-REG-APT-05','same_method','オフセットとニュートラル','全部/一部・取組/状態という二軸を比較','前者ウエの2定義が逆でXOXX1。後者アエが逆でXOOX5、他の2項目は地球限界/トップランナーへ置換。誤植や強い一般化の疑義を同一に扱わない。','双方最適な正誤組合せ。')
add('H30-REG-APT-13','R01-RET-APT-11','same_concept','オフセットと残余排出','削減後の埋め合わせを判定','H30アの取組説明は適切。再試ウエは取組/状態の入替。H30の持続性/ゼロ/濃縮と再試のGHG/低炭素の項目は異なる。候補5対1。','双方正誤組合せ。')
add('R01-REG-APT-15','R04-REG-APT-14','same_concept','SDGsの普遍・包摂・統合・参画','対象の限定と3側面の統合を比較','双方7記述だが、REGアは途上国だけ、R04アは先進国だけ。REGの期限/数/評価はR04のMDGs/人権/協働へ置換。正しい数4→候補5対XOOOOOX→候補3。','正しい数対正誤組合せ。','目標17、期限2030はREGに明示。')
add('R01-RET-APT-14','R06-REG-APT-06','same_concept','SDGsの三側面と普遍・統合','空欄の文脈を先に固定','再試は4語組の選択で候補3に感梁症の誤植、公式ALL。R06は4空欄に入らない語で平和2。一部の語が共通でも同文の反復としない。','空欄の適切組合せ対どの空欄にも入らない語。','再試は17/169目標数を空欄に含む。R06は語句だけ。')
add('R06-REG-APT-02','R06-REG-APT-06','same_method','SDGsの指定文脈と全体の区別','4空欄を埋め残る1語を選ぶ','前者は段落20の能力強化/雇用/leadership/意思決定でケア5が余る。後者は経済/統合/普遍/安全で平和2が余る。両余剰語もSDGs全体には関連する。','双方どの空欄にも入らない語。')
(ROOT/'config/authored_batches/S7_020_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'reviewed comparisons')
