# coding: utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,numbers,choices,figures,temporal='統計の定義を共通理論で扱い、個別の仮定と各年度の語句は保持する。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=numbers,negation_differences='双方は最も適切な組合せ又は範囲を選ぶ。',choice_differences=choices,figure_differences=figures,temporal_differences=temporal,evidence='S7_030の14原典画像で16問を照合。初回16解答を公式前に保存し、全候補と表の列を比較した。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H26-REG-BASIC-1-3','H28-REG-BASIC-1-2','near_repeat','計数値抜取と二つの危険','個数・危険の負担者・ロット間切換えを対応させる。','計算数値なし。H26は合否閾値も空欄、H28は合格判定個数を本文に指定。','H26は5項目/正1、H28は4項目/正4。候補の平均値、判定値、危険と多回の混同を比較。','双方に組合せ表。5列から4列となる差を確認。','JIS切換え全文未取得の範囲と手順固定の疑義は双方で保持する。')
add('R03-REG-BASIC-1-3','R07-REG-BASIC-1-2','near_repeat','PDCAの段階','Plan/Doが正、C/Aの名称の置換が誤りと読む。','計算数値なし。','R03はChange/Adjustで正2、R07はChoose/Achieveで正4。誤りの命題の語を保持。','双方の4項目の正誤組合せ表を確認。')
add('H27-REG-BASIC-1-6','R03-REG-BASIC-1-3','same_concept','PDCAの順序と目的','四段階の名前・実施・確認・改善を対応。','計算数値なし。','H27は順序の正5、R03は説明文の正誤正2。','H27は英語4列、R03は正誤4列。','H27はISO9001:2008を明記、R03は一般PDCA。規格の未取得本文を一般問題へ転用しない。')
add('H23-REG-BASIC-5-4','R06-REG-BASIC-1-6','same_method','独立正規の線形結合','平均は係数付き和、分散は係数二乗付き和。','H23は80/120g,4/3g,各4個。R06は平均と分散を記号で指定。','H23は平均と総質量の正3、R06は接続長さとすき間の正3。同番号でも同じ問題とはしない。','双方の組合せ表。H23は数値、R06は添字と平方を含む数式。')
add('H27-REG-BASIC-1-5','R04-REG-BASIC-1-3','same_method','正規和差の上側確率','符号を持つ平均と正の分散を合成し閾値を標準化。','H27は1800+1700mm,偏差0.4/0.3,閾値3501.5。R04は300-200N,偏差30/40,閾値200。','H27はz3/.13%正1、R04はz2/2.28%正3。同じ5確率範囲。','双方の同じ上側確率表を確認。')
add('R02-REG-BASIC-1-2','R06-REG-BASIC-1-6','same_method','独立正規変数の差','差の平均と分散和から分布を得る。','R02は4つの応力強度比、R06は寸法の記号。','R02は故障確率順序の正4、R06は和差分布の正3。応力強度の符号とすき間の符号を比較。','R02はケース比と候補列、R06は数式2列を確認。')
add('H24-REG-BASIC-5-4','R03-REG-BASIC-1-3','same_concept','プロセスの標準化とPDCA','検査とプロセス改善を区別し、循環の各段階を定める。','計算数値なし。','H24は検査/源流/標準/プロセス正2、R03は段階説明の正誤正2。番号一致を反復の証拠としない。','H24は日本語4項目、R03は正誤4項目。')
add('H25-REG-BASIC-1-6','R05-REG-BASIC-1-6','same_concept','回帰モデルと相関','応答との関連を扱う道具の目的と、適合・因果を区別する。','H25は計算なしの道具定義、R05はrの範囲とR²の関係を検討。','H25は4用語の正3、R05は相関命題正2。用途の名称と数学的性質の違い。','H25は組合せ表、R05は5命題の一覧。')
p=ROOT/'config/authored_batches/S7_030_reviewed_relations.json';assert not p.exists()
p.write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'relations')
