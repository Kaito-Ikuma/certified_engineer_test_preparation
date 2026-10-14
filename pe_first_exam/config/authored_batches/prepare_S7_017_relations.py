# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')}; rows=[]
def add(a,b,kind,concept,method,numbers,choices,negation='双方とも最も適切。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=numbers,negation_differences=negation,choice_differences=choices,figure_differences='設問固有図なし。候補表のある問題は全5行を各原典で実画像照合。',temporal_differences='出題年度差を保持。法制度・統計版の置換なし。分子機構は各問題の所与条件で比較。',evidence='S7_017原典22頁28問、初回独立判断を保存。内容・数値・肢順・分母・方向を比較。部分校正の疑義をこの関係承認で解消しない。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H23-REG-BASIC-4-5','H26-REG-BASIC-4-5','same_concept','膜脂質の鎖長・不飽和と温度適応','結合→充填→融点→昇温補償の方向を6空欄に対応','両方20→30℃、飽和炭素12以上。','6空欄と全5行の対応が同じで3。ただし原典の別年度資料を個別に確認しハッシュを残す。')
add('H25-REG-BASIC-4-5','H29-REG-BASIC-4-5','same_concept','アミノ酸の共通骨格と側鎖・配置','20・カルボキシ・疎水・Lを独立に判定','両方標準20対候補30。','正答1と候補1〜3は同じ。4・5が交換、側鎖という明示も追加。正答番号だけで同一問と認定しない。')
add('H24-REG-BASIC-4-5','H28-REG-BASIC-4-6','same_concept','DNA変性で解ける鎖間と残る主鎖','水素会合と主鎖共有結合・GC・冷却を区別','特定の数値温度なし。','H24は水素/紫外/C/アニーリング、H28は水素/ヌクレオチド/ホスホジエステル/Cの4空欄。問いの一部が違い双方3。')
add('H28-REG-BASIC-4-6','R01-REG-BASIC-4-5','same_concept','DNA鎖間と主鎖の結合','水素/ヌクレオチド/ホスホジエステル/Cを表へ対応','数量条件なし。','前者アミノ酸を含む表の3、後者グルコースを含む表の4。正しい概念が同じでも誤答語と行順が異なる。')
add('H27-REG-BASIC-4-6','R04-REG-BASIC-4-6','same_method','DNAの相補写像と割合保存','一方の鎖の残りを100から引き相補写像を使う','前者C20T35→同鎖A+G45、後者G25A15→相補G+A60。','前者1/2は単独未決定、4/5和が逆。後者G+C90は非負条件から不可能。正答3対5。')
add('H28-REG-BASIC-4-5','R01-RET-BASIC-4-5','same_concept','遺伝暗号の縮重','64入力を20アミノ酸と3停止の多対一対応へ整理','両方4^3=64と標準20。','前者の順1,2,3,4,5が後者では3,5,4,2,1に対応。正答1対3。修飾体・転写・消失・第一塩基の全誤答も照合。')
add('H29-REG-BASIC-4-6','R01-RET-BASIC-4-6','same_concept','ゲノムと発現RNA、DNA操作の条件','発現由来、電荷、理想増幅と確率平均を分ける','後者PCR30回で30倍という誤答が追加、両者6塩基認識で4^6固定長という誤答。','前者耐熱PCR1が正しく全ゲノム→肝臓cDNA5が誤り。後者同組織ゲノム存在/発現cDNA不存在3が正しく耐熱肢を30倍誤答へ変更。共通の歴史・電気泳動・EcoRIの肢順も交換。')
add('H30-REG-BASIC-4-6','R06-REG-BASIC-4-6','same_concept','タンパク質配列と共有結合分類','核酸指定、L、ペプチド/S-S共有、疎水分布を比較','両者標準20、その他数値なし。','前者3の一次構造を後者4のアミノ酸配列に言い換える。前者5→後者1、2→2、1→3、4→5。後者非共有列挙に疎水相互作用も追加。')
add('R02-REG-BASIC-4-6','R05-REG-BASIC-4-6','same_concept','PCRの温度サイクル・伸長・プライマー','変性の対象、特異性、長さ/時間、耐熱性を比較','時間・温度の実数指定なし。','前者4耐熱性高いは正しいが後者4低いは誤り。前者1主鎖共有切断は誤りだが後者5水素会合は正しい。その他前者2→後者1、3→2、5→3。正答4対5。')
add('H26-REG-BASIC-4-6','H30-REG-BASIC-4-5','same_concept','細胞組成の分母と代表値','原子個数と湿重量・有機物重量を分ける','前者主要4はPを含む99、後者Nを含む99。水約70は共通。','前者最も不適切1は元素P/N。後者最も不適切5は核酸最大。前者2全て同様は部分校正の疑義、後者3よく似ておりという比較的緩い表現。','双方とも最も不適切、原典の断定範囲が異なる。')
add('H30-REG-BASIC-4-5','R07-REG-BASIC-4-6','same_concept','細胞の水・小分子・高分子の割合','分母と対象細胞を明示して比較','主要4元素の原子数99対人体90以上。水約70・H60以上は共通。','核酸最大の誤答は動物細胞の有機成分5対細菌の巨大分子4。水は1→5、4群は4→3。原子数2/3は後者人体1/2へ対象変更。','双方とも最も不適切。')
(ROOT/'config/authored_batches/S7_017_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'reviewed comparisons')
