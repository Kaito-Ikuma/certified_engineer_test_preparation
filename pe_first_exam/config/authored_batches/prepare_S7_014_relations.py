# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,choices,negation='選択方向は一致'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences='数値計算の条件なし。形成過程・鉱物名・対象範囲を比較。',negation_differences=negation,choice_differences=choices,figure_differences='両原典とも設問固有図なし。全5肢・否定・名称を実画像比較。',temporal_differences='法制度・時点依存の指定なし。地質の典型分類と例外を区別。',evidence='S7_014原典14頁を表示して全17問の肢と条件を比較。校正JSONへ追跡可能。関係の承認は解釈疑義の解消を意味しない。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H25-REG-APPLIED-19','H27-REG-APPLIED-29','near_repeat','特殊土の起源','5土を母材・運搬・有機物へ対応','5説明と順序が同じ。泥炭5適切。表記差を含むため原文完全同一とは認定しない。')
add('H27-REG-APPLIED-29','R01-RET-APPLIED-28','near_repeat','特殊土の起源','泥炭を選び他4の起源誤りを判断','黄土3→1、しらす2→2、泥炭5→3、まさ土1→4、火山灰4→5。適切5→3。')
add('H30-REG-APPLIED-30','R02-REG-APPLIED-25','near_repeat','火成岩の鉱物組合せ','主要鉱物と有色分類を別判断','花崗岩有色2→1、はんれい岩5→2、花崗岩無色1→3、玄武岩3→4、安山岩4→5。公式5→2。白雲母の疑義も同じ内容であり保持。')
add('R01-RET-APPLIED-31','R05-REG-APPLIED-26','near_repeat','付加体の構成岩','海洋プレートの履歴へ5岩種を対応','玄武岩1→1、花崗岩4→2、石灰岩5→3、チャート3→4、泥岩2→5。最も関係のない花崗岩4→2。')
add('R03-REG-APPLIED-24','R06-REG-APPLIED-26','near_repeat','火砕岩の分類・支持構造','粒径と支持と溶結を別判断','最初3説明は一致。降下/流れの支持構造4→5、アグルチネート5→4。スコリアの色は黒/暗色→黒/暗褐色で軽微表記差。公式4→5。')
add('R05-REG-APPLIED-24','R07-REG-APPLIED-23','near_repeat','変成作用と対の変成帯','沈み込みの冷たい側と火成熱源側を対応','最初3説明はほぼ同じ。大理石4→5、逆の変成帯5→4。広域変成の文言に帯状高温圧/帯状に生じた温度圧力の表現差。公式5→4。')
add('R05-REG-APPLIED-24','R06-REG-APPLIED-27','same_concept','変成作用・接触/広域・高温低圧/低温高圧','温度圧力の成因と例示/全称を区別','5説明の形式が異なる。弧海溝配置5から領家/三波川の型4へ。R06の大理石の断定分類に追加疑義があるので同一再出題とは認定しない。')
add('R01-REG-APPLIED-24','R03-REG-APPLIED-23','same_concept','変成作用と鉱物組織','化学組成・温度圧力と組織を分ける','前者は組成依存を無視する3、後者は片麻岩の縞を否定する3。番号は同じだが誤りの概念は異なる。')
(ROOT/'config/authored_batches/S7_014_reviewed_relations.json').write_text(json.dumps({'relations':rows},ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'source-compared relations')
