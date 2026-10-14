# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,concept,method,choices,negation,time):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type='same_concept',shared_concept=concept,shared_method=method,numerical_differences='計算の数値条件なし。候補の項目数・組合せはchoice_differencesに記録。',negation_differences=negation,choice_differences=choices,figure_differences='両原典を実画像確認。設問固有図なし。組合せ表又は項目数候補も全5肢照合。',temporal_differences=time,evidence='S7_016原典全13問の画像と初回独立判断を保存。主題・条件・否定・時点を比較。関係承認は一方の判決資料未確認を解消するものではない。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('R01-REG-APT-09','R05-REG-APT-02','秘密情報の接近制御と相互確認','各対策のアクセス・持出し・気付きへの効果を判定','6記述から不適切数0/1/2/3/4を選ぶ前者は1項目の2。後者は5対策から単独作業の3を選ぶ。分類・表示・配置の趣旨は共通、暗号/ID・紙削減対コピー制限で技術的項目が異なる。','不適切な項目数対最も不適切な対策。','令和元年と令和5年。現行2024版を両出題当時の法律義務へ流用しない。')
add('H25-REG-APT-06','R01-REG-APT-14','ISO26000の対象と社会的責任の原則','ガイダンス・対象・原則を不要な限定と区別','前者は4記述の正誤を5行から選び×○××の5。後者は7原則に関する5記述から政府意向を加えた4を選ぶ。設問条件は同一でなく同じ規格の別論点。','正誤組合せ対最も不適切。','ISO26000:2010が共通。後者はJIS Z26000:2012にも言及。現在の背景を出題時の記述へ上書きしない。')
add('H30-REG-APT-14','R05-REG-APT-09','事故機構・組織の改善と個別の刑事責任','物理的事象、調査による推定、被告人の判決を分離','5事故の集合は共通、H30は刑事判決で初回2|5対公式ALL、不起訴の不適格注記あり。R05は技術的事実でエレベーター破断落下4が誤り。H30の1/3/4判決は一次資料未確認。','実際の判決と異なるもの対事故の事実と異なるもの。','平成30年と令和5年で参照時点と判断軸が異なる。後年の経緯からH30当時の判決を補わない。')
(ROOT/'config/authored_batches/S7_016_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'source comparisons')
