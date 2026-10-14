# coding: utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,numeric,choices,fig,temporal='所与確率のモデルであり法令時点の同一視をしない。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=numeric,negation_differences='双方は最も適切な値・順位又は組合せを選ぶ。否定の方向を逆転しない。',choice_differences=choices,figure_differences=fig,temporal_differences=temporal,evidence='S7_028の25原典画像と全22問の候補を比較。独立性、非零根、代表安全率と法令時点の疑義を各部分校正に保持。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H25-REG-BASIC-1-1','H27-REG-BASIC-1-4','near_repeat','製造物責任法の目的・欠陥',
 '製造物・欠陥・被害者・安全性を第1条と第2条から対応させる。','数値計算なし。空欄語は同じ。',
 '全5組の配列も同じで正答3。問題番号と年度を保持する。','双方4列の組合せ表で、全値を照合。',
 '2013年と2015年の原典引用、2018年解説を比較。現行までの全改正履歴未照合を保持。')
add('H27-REG-BASIC-1-4','H30-REG-BASIC-1-6','near_repeat','通常有すべき安全性としての欠陥',
 '目的の被害者保護と法的な安全性を、故障や機能不足から区別する。','数値なし。',
 'H27の正答3がH30で4。H30は故障/信頼性等の誤候補へ変更し単なる順序変更ではない。','両者の4列表を実見。',
 '2015年と2018年の原典、2018年逐条解説。全改正履歴未照合を保持。')
add('H26-REG-BASIC-1-5','R01-RET-BASIC-1-6','near_repeat','予防・事後と保全時期の基準',
 '故障前後と時間又は状態で時期を決める軸を分ける。','数値なし。第三空欄はH26状態監視、再試験時間計画。',
 'H26の正1が予防事後状態監視定期経時、再試験の正5が予防事後時間計画定期経時。他4列も違う。','5列の語表を比較。',
 '2014年と2019再試験。2013年公的保全資料の用語を参考にし、JIS全版一致の確認とはしない。')
add('H28-REG-BASIC-1-1','H30-REG-BASIC-1-1','same_method','未知単体信頼度を持つ系の同等条件',
 '独立模型で両系を縮約し、信頼度範囲で根を選び全体系の値を求める。',
 'H28 .81(2x-x²)=.95x²、R.8048747。H30 .9025(2x-x²)=x³、R.9014573。H30はx>0明記、H28は明記せず零根も存在。',
 'H28正4 .805、H30正3 .901。H30の5 .966は単体xの近似値。','H28の中央Bは.95、H30は三個全てx。共通両端の値も.9→.95。')
add('H24-REG-BASIC-1-1','H26-REG-BASIC-1-4','same_method','直並列系を内側から縮約',
 '並列の失敗補集合と直列の成功積を用いる。','H24 .9/.8/.5/.7からR.8474、H26四個.9からR.8019、三直列単体x.9290521。',
 'H24は全体系Rの候補.25/.60/.73/.85/.91正4、H26は未知単体x .87/.90/.93/.96/.99正3。','H24最外並列、H26両端直列と中央並列。問われる量も異なる。')
add('H27-REG-BASIC-1-1','R03-REG-BASIC-1-2','same_concept','成功経路による信頼度順位',
 'どの機能が全て必要か、どれか一つで足りるかを事象へ写す。','H27 .9単独/.81直列/.99並列。R03 .9/.8/.7の接続で.916/.926/.956/.776/.846。',
 'H27三系B<A<C正5、R03五系C>B>A>E>D正2。','H27単独と二要素、R03異なる三要素の五接続。独立は双方明記。')
add('R02-REG-BASIC-1-6','R05-REG-BASIC-1-4','same_concept','成功要素数と冗長系の要求',
 '許す故障数から成功事象を定義し、独立な個数の確率を評価する。',
 'R02並列n個.7と外.95でR≥.94の最小n4。R05三個.7の2/3多数決R.784。',
 'R02個数2/3/4/5/不可能正3、R05信頼度区間正4。','R02任意一個成功と外の一要素、R05任意二個成功。全並列と多数決を同一視しない。')
add('H23-REG-BASIC-1-5','H29-REG-BASIC-1-2','same_concept','用途によって異なる安全係数',
 '代表1.5/6/100の定義と対象を限って比較する。','H23四対象に主索使用時4を追加。H29は最初の三対象の順序だけ。',
 'H23四値組合せ正4、H29三対象のウ>イ>ア正5。','四列表と大小順序を区別。',
 '2011年と2017年。航空機2011規則・食品安全2008説明・クレーン規則を参照。主索2011当時版と薬品全称の疑義はH23に保持。')
p=ROOT/'config/authored_batches/S7_028_reviewed_relations.json';assert not p.exists()
p.write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n');print('Prepared',len(rows),'relations')
