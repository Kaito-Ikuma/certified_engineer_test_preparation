# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,ch,neg,num='定量入力なし。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=num,negation_differences=neg,choice_differences=ch,figure_differences='両原典に固有図なし。質量数・δ・標準旧名称・全5肢を各画像で照合。',temporal_differences='試料年代と試験年度を区別。旧SMOW/PDB/CDTと出題前1995年V尺度勧告を区別。現在の精密校準を旧原典条件へ追加しない。',evidence='S7_022の15原典画像と全5肢を確認し、公式前初回独立解答を保存。15一致でも標準物質とCl36経路の疑義を保持。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H23-REG-APPLIED-24','H26-REG-APPLIED-31','near_repeat','若い貝の炭素時計','試料・半減期範囲を一致させる','2万年前貝とKAr/RbSr/UPb/14C/FTの5法・順序が一致。両公式4。海生淡水生は両原典で未指定。','ともに最も適切。','両原典2万年前。')
add('H28-REG-APPLIED-32','R01-RET-APPLIED-35','near_repeat','白亜紀では14Cが短すぎる','数万年の時計と数千万〜億年の対象を比較','5法は同じで並び変更。14Cは1→5、KAr2→1、UPb3→2、RbSr4→3、FT5→4。','ともに最も不適切。','白亜紀対象は一致。具体年齢・鉱物は指定なし。')
add('R01-RET-APPLIED-35','R04-REG-APPLIED-25','near_repeat','白亜紀の時計選択','時間範囲と適用試料を点検','14C5→3、KAr1→2、UPb2→1、RbSr3→4、FT4→5。正答位置5→3。','ともに最も不適切。','具体数値入力なし、対象は白亜紀で一致。')
add('H23-REG-APPLIED-21','H30-REG-APPLIED-21','near_repeat','同位体標準の元素対応','H/O水、C/O炭酸塩、Sの尺度を対応させる','同じ5組合せを並替。C-CDT2→3、S-CDT4→1、H-SMOW1→5、O-SMOW3→2、O-PDB5→4。誤りを旧名称の省略とは別に説明。','誤っている対最も不適切。')
add('H24-REG-APPLIED-32','R02-REG-APPLIED-20','same_concept','自然水・炭素混合・氷床分別と標準','比の基準と気候分別を別々に判定','海水天水熱水、古い炭素、蒸発が共通。H24は全酸素SMOW限定が誤り3、氷期大は正しい。R02は氷期大小を逆転した肢3が誤り、標準肢はS-CDTへ変更。正答番号が同じでも同型解法だけとはしない。','ともに最も不適切。')
add('R02-REG-APPLIED-20','R06-REG-APPLIED-21','near_repeat','有孔虫δ18Oと氷期の大小','氷床16O隔離と低温炭酸塩分別を組み合わせる','5記述群は一致し、間氷期大3→1、蒸発1→3、海水5→4、CDT4→5、古いC2は位置維持。公式3→1。CDT名称疑義は両問で保持。','ともに最も不適切。')
add('H27-REG-APPLIED-25','R05-REG-APPLIED-21','same_concept','天水線・水素核種・自然水分別','天水線の軸、安定比と放射性時計を分ける','H27はδ17O対δ18Oを天水線とする誤り3。R05は天水線は正しく、2Hを半減期12.3年とする誤り1。R05は熱水酸素シフトが追加される。','ともに最も不適切。','H27は核実験1952年以降、R05は誤った2H半減期12.3年。')
add('H23-REG-APPLIED-24','H28-REG-APPLIED-32','same_method','試料年代と14C感度','半減期と検出限界を時間範囲へ適用','同じ5法の集合だが14Cは適切4対不適切1。貝の生物炭素と未指定白亜紀地質試料という対象差。','最も適切対最も不適切。','2万年対白亜紀の数千万〜億年。')
add('H27-REG-APPLIED-25','R07-REG-APPLIED-22','same_concept','自然水の同位体トレーサーと年代','生成入力・壊変・親娘保持と混合を分ける','H27は3H核実験履歴と水分別、誤りは天水線軸。R07は3H/3He・14C・10Be・36Cl・4Heの方法比較、公式誤り4はCl生成経路疑義。別の公式一致で疑義を解除しない。','ともに最も不適切。')
(ROOT/'config/authored_batches/S7_022_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'source comparisons')
