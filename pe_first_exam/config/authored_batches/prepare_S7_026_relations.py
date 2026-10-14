# coding: utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,choices,neg,fig='設問図なし。組合せ表は列順を原典で確認。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,
 shared_method='各命題の範囲・否定・対策順位を定義と一次資料に比較し、個数又は表へ変換する。',
 numerical_differences='新しい数値計算なし。経験比1:29:300の普遍化や規格年・法律施行年の同一視をしない。',
 negation_differences=neg,choice_differences=choices,figure_differences=fig,
 temporal_differences='各原典の年・規格版・法令の時点を保持。2006努力義務と2016対象化学物質義務は同一範囲でない。現在の解説を当時の原文へ置換しない。',
 evidence='S7_026原典23画像で全22問の条件/全候補を比較。公式前初回を保存し、その後全22一致。各肢の疑義は別に保持。',
 approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H23-REG-APT-05','H29-REG-APT-12','same_concept','許容基準の社会条件と安全の階層',
 'H23不変4→H29不変3。H23国別文化1/2・新機械3→H29安全定義1・残留記録2・人間の誤り5。H23階層5→H29階層4。国別一般化とアセスメントだけで低減の疑義は異なる。',
 '双方不適切1肢、正4→3。')
add('H24-REG-APT-10','H26-REG-APT-10','near_repeat','残留の説明と対応・努力義務',
 'H24ア設計超過外力はH26前文へ。H24イ対応→H26ア、H24ウ努力とエ助言はH26ウ/エ。H26イには被害説明不要という新たな誤り。○○○○→○×○○、正1→4。',
 '双方正誤4列の適切な組合せ。受容すべきの一般化疑義を保持。')
add('R01-RET-APT-12','R04-REG-APT-06','same_concept','反復・階層・ALARP水準',
 '再試験ア安全/イ使用者誤使用/ウ残留/エ順位なし/オALARP。R04は反復1、略語2、水準3、著しい不均衡4、順位なし5。順位なしが共通の誤りだが使用者同定とALARP領域の詳しさが違う。',
 '再試験は不適切個数1個→候補2、R04は不適切肢5。番号が異なる回答形式。')
add('H30-REG-APT-11','R06-REG-APT-13','same_concept','職場調査指針と低減順位',
 'H30誤順位3は設計工学保護具管理。R06エは高順位措置/著しい不均衡/重大危害暫定という正命題。H30化学義務2・時期5に対しR06対象除外イ・疲労ウを問う。対象と法源の疑義を消さない。',
 'H30最も不適切3、R06正誤4列全部○の候補5。')
add('R03-REG-APT-12','R06-REG-APT-07','near_repeat','事故比・報告保護・4S・SDS',
 'R03イ状態行動→R06ア、ウ比→イ（同じ人間/数千を追加、軽傷原因除去保証を削除）、エ報告→ウ、オ4Sしつけ→エ4S洗浄。R03カは使用者RA義務→R06オ譲渡情報定義へ変更。R03ア法目的/キ健診はR06で削除。',
 'R03適切個数5→3、R06○○○×○→4。Heinrich比の因果保証と集計条件の疑義は同じでない。')
add('R03-REG-APT-10','R05-REG-APT-14','same_concept','設計の優先と予算超過をALARPにしない',
 'R03イの僅かな予算超過による設計省略→R05肢3の当初事業予算。R03ア軽量設計/ウ言語/エ危害結果/オ誤使用/カ保守と、R05反復1/全称ALARP2/設計最重要4/表示性5は別。言語疑義とあらゆるの範囲を分ける。',
 'R03誤り個数3→候補3、R05不適切肢3。番号一致でも理由集合は違う。')
add('R04-REG-APT-06','R07-REG-APT-14','same_concept','ALARP領域の条件付き許容',
 'R04ALARP水準3/費用効果4はR07正候補2の条件。R07無条件1/補償費3/下の水準4/別事業5を比較。R04誤5は階層なしでありR07にない。R07前文の安全と下位水準の等置疑義を保持。',
 'R04不適切5、R07中間水準で最適条件2。',
 'R04図なし、R07独自3領域のキャロット図を原典画像確認。幅を数値尺度としない。')
add('R02-REG-APT-07','R05-REG-APT-08','same_concept','アセスメントと評価後の活動',
 'R02は対策後の見積り評価・残留許容・妥当文書の4空欄。R05は組織リスク特定分析評価対応の4空欄。用語の同定/特定、反復と外周監視の位置を区別し同じ選択肢とはしない。',
 '双方最適組合せ、R02正4→R05正2。',
 'R02安全Guide51の反復フロー2頁、R05ISO31000組織プロセスの囲み1頁。原図転載なし。')
assert len(rows)==8
p=ROOT/'config/authored_batches/S7_026_reviewed_relations.json';assert not p.exists()
p.write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(rows),'relations')
