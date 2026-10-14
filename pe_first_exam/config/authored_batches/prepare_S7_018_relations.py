# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,num,ch,neg='双方とも最も不適切。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=num,negation_differences=neg,choice_differences=ch,figure_differences='双方に設問固有図なし。全5肢を別年度の原典画像で確認。',temporal_differences='出題年度差を保持。観測概数はその問題の指定精度として扱い現在値で上書きしない。',evidence='S7_018の19原典画像で23問を照合。数値・条件・肢対応を比較。部分校正の疑義を関係承認で解消しない。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H26-REG-APPLIED-26','R06-REG-APPLIED-20','same_concept','地球放射収支と太陽定数','反射率・帯域・季節原因・緯度収支・上端定義を比較','31%と約365日は共通。','前者1→後者3、2→5、3→1、4→4、5→2。正答1対3。','双方最も適切。')
add('H26-REG-APPLIED-26','R01-REG-APPLIED-22','same_concept','短波の帯域と全球反射率','何が適切な概数かを各肢独立判断','31%が15%へ、ガンマ/X線約半分が可視約半分へ変更。','前者1は真→後者4偽、前者2偽→後者3真。残り3→1、4→5、5→2は誤りを維持。単純な肢順変更ではない。','双方最も適切。')
add('H28-REG-APPLIED-26','H30-REG-APPLIED-22','same_method','円の受光断面と球面平均','P=S0πR²、km→m換算','双方R6370km・S0=1368W/m²。','前者候補1.74,3.49,6.97×10^17、1.39,2.79×10^18。後者は8.71×10^16を先頭へ追加し最大を削る。正答1→2。H28は反射吸収無視、H30は上端。','双方最も近い値。')
add('H28-REG-APPLIED-26','R01-RET-APPLIED-20','same_concept','受光総量・平均放射束・アルベド','S0πR²からS0/4と反射率へ段階を区別','前者1368・6370km総量、後者342W/m²平均・反射107。','前者総量Wの5値、後者放射束W/m²の68/107/137/171/205。答1対2。平均を再び4で割らない。','前者最も近い、後者最も適切。')
add('H29-REG-APPLIED-19','R01-REG-APPLIED-21','same_concept','氷床の貯留と輸送、水蒸気の潜熱・滞留','貯留/流量と全球水収支を比較','数値指定なし、短い大気滞留と長い氷床交換を比較。','前者1→後者2、2→1、3→3、4→5、5→4。正答4対5。')
add('H30-REG-APPLIED-20','R05-REG-APPLIED-18','same_concept','大気組成の量順と微量成分循環','N2>O2>Ar>CO2を確認して源・季節・地史を判断','数値混合比なし。','前者1→後者3、2→4、3→5、4→1、5→2。正答4対1。')
add('R01-RET-APPLIED-21','R04-REG-APPLIED-22','same_concept','鉛直構造と環境気温減率','3K/kmの一般化を代表6.5と区別','対流圏3/4、減率3、オゾン9割は共通。','前者1→後者5、2→1、3→4、4→3、5→2。正答2対1。')
add('R01-REG-APPLIED-19','R07-REG-APPLIED-21','same_concept','大気鉛直構造・混合・オゾン・密度の概数','温度層序と組成を分け誤肢と概数疑義を区別','10km密度1/4共通。80kmが数10kmへ、成層圏90%の補集合10%追加。','前者CO2加熱4が偽、後者極域界面高2が偽。前者8:2組成肢は消え、後者対流圏オゾン10%が入る。原典密度の疑義は双方保持。')
add('H27-REG-APPLIED-24','R02-REG-APPLIED-21','same_concept','大循環・海陸風・層序・地衡風','緯度帯・日夜・転向力・等圧線を独立比較','中間圏80km極大が成層圏50km極大へ、後者170/1000km上層条件追加。','前者4昼海→陸が真、後者4夜海→陸が偽。前者1/2/3/5の誤った条件を後者では修正。単純に同じ正答4とは扱わない。','前者最も適切、後者最も不適切。')
add('H27-REG-APPLIED-26','R05-REG-APPLIED-20','same_concept','降水の酸塩基平衡とpH対数','pH差と濃度、CO2平衡・中和の地域条件を区別','前者pH3.3/30μmolという誤肢、後者海洋極域pH8以上という誤肢。共通5/6・5.6・中和7。','前者1→後者3、3→2、5→4。前者日本pH5未満が後者酸性雨被害へ置換。正答2対1。')
(ROOT/'config/authored_batches/S7_018_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'reviewed comparisons')
