# coding: utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,read_csv
by={r['question_id']:r for r in read_csv('data/questions.csv')};rows=[]
def add(a,b,kind,concept,method,choices,neg='双方の問題方向・各肢否定を比較。',num='定量入力なし。',fig='両問の全5肢を画像確認、固有図なし。',time='年度ごとの対象条件・出題意図を保持。'):
 rows.append(dict(left_question_id=a,right_question_id=b,relation_type=kind,shared_concept=concept,shared_method=method,numerical_differences=num,negation_differences=neg,choice_differences=choices,figure_differences=fig,temporal_differences=time,evidence='S7_024原典18画像の全肢・図表、公式前独立初回16問保存後に条件差を比較。初回と公式の一致は本文疑義の解消とは区別。',approval_status='verified',source_hash_left=by[a]['source_sha256'],source_hash_right=by[b]['source_sha256'],rubric_version='1.0-review1'))
add('H23-REG-BASIC-2-2','H26-REG-BASIC-2-6','same_concept','重み付きグラフの経路制約','目的量を先に定め、実現経路と限界を示す。加算最短法とmax-minは別手法。','数値候補1,5,6,8,10対3,4,5,6,7。両答は値5だが候補2対3、最小遅延対最大車高。','最小値対最大値。','6頂点9辺の遅延対12頂点17辺の車高制限。','H23無向通信網A〜F対H26位置呼称で補助する道路A〜B。辺・接続を同一視しない。')
add('H27-REG-BASIC-2-5','R03-REG-BASIC-2-1','near_repeat','公開鍵・CA・署名と無線','鍵の向き、CAと公開鍵主体の対応を照合。','H27誤公開鍵のみ1→R03正しい暗号化復号1。CA公開鍵の正2→秘密鍵の誤2。スマートフォン3は双方誤り、署名4は誤公開鍵暗号化→逆鍵生成検証、WEP完全安全5→現在推奨5。正2→1。','双方最も適切。',time='2015/2021双方でWEPの絶対安全は成立しない。現在推奨という時点表現はR03のみ。')
add('H23-REG-BASIC-2-5','R05-REG-BASIC-2-1','same_concept','パスワードと暗号だけでない認証条件','方式名・文字長・段階数を保証条件と分ける。','WEPの正当化はH23肢1、R05肢5、双方不適切。H23の伝送公開鍵2が意図正答、R05は周期変更不要1が正答。共有端末、平文保存、辞書列はH23のみ、PIN・生体・段階要素はR05のみ。','双方最も適切。',time='2011の伝送対2023の更新方針。2017・2025NIST版と原典の時点を区別。')
add('H29-REG-BASIC-2-1','H30-REG-BASIC-2-1','same_concept','漏洩した認証情報の扱い','侵害可能な差出人・資格情報と複数地点の対策を比較。','H29の知人添付1が不適切、H30のパスワード再利用4が不適切。周期変更4対同番号の再利用4は別記述。H29パッチ・AV・USBとH30FW・TLS・IoT・APは候補集合も異なる。','双方最も不適切。',time='2017定期変更指針と2018原典SSL/TLS総称の疑義を別々に保持。')
add('R02-REG-BASIC-2-3','R07-REG-BASIC-2-4','near_repeat','標的型攻撃の多層防御・窓口・実行制限','サービス名や検査の目的だけでファイル・取扱いの安全を決めない。','R02正しい多層2→R07正1、窓口3→2、実行制限4→3。R02訓練5はR07に無く手口共有4を追加。R02誤正規ストレージ/ゲートウェイ1はR07誤外部サンドボックス投入5へ。正1→5。','双方最も不適切。',time='2020正規ストレージ悪用は白書2020、2025外部解析漏洩は白書2023の該当箇所で裏付け。')
add('R04-REG-BASIC-2-1','R07-REG-BASIC-2-4','same_concept','技術対策と組織報告・情報開示','異なる攻撃経路と連絡遅延を分ける。','R04の連絡先不明による拡大5とR07窓口周知2は対応する対策。R04誤URL安全送付のみ1対R07誤解析先投入5で保証の不足は別。VPN・場所・リスク比較と共有/実行制限も候補差。','双方最も不適切。',time='テレワーク一般の相対リスクはR04で条件未確定、R07にはその主張なし。')
add('R01-RET-BASIC-2-1','R07-REG-BASIC-2-4','same_concept','検知・除去と復旧・機密の扱い','防御の目的と副作用を比較。','R01RETのウイルス後完全修復困難5が適切、R07の外部解析積極投入5が不適切。同じウイルス検査関連でも結果の既発生損傷対投入情報漏洩。R01短い秘密・AV不要・企業名信用・全ポートとR07多層/窓口/制限/共有は別。','最も適切対最も不適切。')
add('H29-REG-BASIC-2-1','R01-RET-BASIC-2-1','same_concept','送信者の信用と端末防御','表示名・アドレスと添付の安全性を分離。','H29知人添付を直ちに開く1は不適切、R01企業名だから信用3も不適切。AV導入のH29正2はR01性能のため不要の誤2へ否定が逆。H29パッチ/周期変更/USBはR01短い秘密/全ポート/完全修復困難へ変更。正1対5。','最も不適切対最も適切。')
add('R03-REG-BASIC-2-1','R06-REG-BASIC-2-6','same_concept','電子署名と検証鍵','生成者の秘密鍵と検証者の真正公開鍵の役割を固定。','R03の公開鍵生成・秘密鍵検証4は誤り、R06本人生成・誰でも検証3は鍵保護前提で妥当。R03正暗号化1対R06誤MFA/再送4で問いの核心は異なる。R06はハッシュ・PQC・ZKを追加。','最も適切対最も不適切。',time='2021鍵の基本役割対2024の候補暗号時点・秘匿証明の条件疑義。')
assert len(rows)==9
(ROOT/'config/authored_batches/S7_024_reviewed_relations.json').write_text(json.dumps(dict(relations=rows),ensure_ascii=False,indent=2)+'\n')
print('prepared',len(rows))
