# coding: utf-8
import sys,json,re,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('net_dijkstra','Massachusetts Institute of Technology','6.006 Recitation 13: Dijkstra','https://live.ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ec187276db0faaa047d655979a44de7f_MIT6_006S20_r13.pdf','6頁資料の非負重み・最短距離・緩和の公開本文を確認。H26車高のmax-minは原典図で独立に経路と閾値分断を検算する。'),
('net_cosine','Christopher D. Manning and Prabhakar Raghavan and Hinrich Schuetze','Introduction to Information Retrieval: Dot Products','https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html','内積/ユークリッド長積、単位ベクトルへの正規化の公開節本文を確認。原典18セルは画像照合。'),
('net_nist2017','NIST','SP 800-63B (June 2017, updates March 2020)','https://pages.nist.gov/800-63-3/sp800-63b.html','5.1.1.2の恣意的周期変更非推奨、5.2.3生体の確率・提示攻撃、5.2.8再送耐性・nonceと固定秘密を確認。2020更新を含む版なので2017原文の改訂履歴も区別。2025-08-01に改版済み。'),
('net_nist2025','NIST','SP 800-63B-4: Authenticator and Verifier Requirements','https://pages.nist.gov/800-63-4/sp800-63b/authenticators/','3.1.1の周期変更禁止・侵害時変更、ローカルactivation secretとリモートpassword、試行制限を公開本文確認。2025版の長さ要件を過年度の値へ転用しない。'),
('net_wep','NIST','Mobile Threat Catalogue: LPN-2','https://pages.nist.gov/mobile-threat-catalogue/lan-pan-threats/LPN-2.html','WEP等弱暗号の傍受と無許可信頼なしAP自動接続回避の本文確認。現在資料のWPA2記載を唯一現行推奨と断定しない。'),
('net_pki','IETF','RFC 5280: Internet X.509 Public Key Infrastructure','https://www.rfc-editor.org/rfc/rfc5280.html','6章の名前と公開鍵のbinding・証明書検証の公開本文を確認。全RFC通読ではない。'),
('net_signature','NIST','FIPS 186-5: Digital Signature Standard','https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf','物理4〜6頁で秘密鍵生成/公開鍵検証、秘密鍵保護・システム全体安全非保証を確認。2023版は役割の一般原理補足、2015・2021へ規格全要件を遡及しない。'),
('net_ipa_account','情報処理推進機構','不正ログイン対策特集ページ','https://www.ipa.go.jp/security/anshin/measures/account_security.html','強い長い独自パスワードと多要素設定の公開本文確認。現在の更新内容を出題時の数値条件へ混ぜない。'),
('net_ssl2015','IETF','RFC 7568: SSLv3 Is Not Secure','https://www.rfc-editor.org/rfc/rfc7568.html','2015年6月の3章MUST NOTによるSSLv3使用禁止を確認。SSL/TLSという原典総称の問題を記録。'),
('net_target2020','情報処理推進機構','情報セキュリティ白書2020','https://www.ipa.go.jp/archive/publish/wp-security/qv6pgp0000000v98-att/000087025.pdf','公式PDF取得後テキストの正規オンラインストレージURL悪用・対策箇所のみ確認。Webはサイズ制限で全文取得できずローカル該当頁を読む。全冊通読ではない。'),
('net_target2023','情報処理推進機構','情報セキュリティ白書2023','https://www.ipa.go.jp/publish/wp-security/t6hhco00000014r1-att/2023_All.pdf','公式PDFローカル該当頁の外部ウイルス検査/サンドボックスへのアップロードと漏洩、共有・ログ等を確認。検索公開抜粋とローカル本文を区別、全冊通読ではない。'),
('net_telework','情報処理推進機構','テレワークを行う際のセキュリティ上の注意事項','https://www.ipa.go.jp/security/anshin/measures/telework.html','2020公開・2026更新の2章、画面・音声漏洩、パッチ・フィッシング・業務規程の本文を確認。オフィスとのリスク比の定量証拠としては使わない。'),
('net_meeting2020','情報処理推進機構','Web会議サービスを使用する際のセキュリティ上の注意事項','https://www.ipa.go.jp/archive/security/security-alert/2020/ssf7ph000000a4g3-att/000083955.pdf','物理2〜4頁3.3、4.1：安全な配付と参加認証、待機室、事前登録等を確認。'),
('net_tcp2009','IETF','RFC 5681: TCP Congestion Control','https://datatracker.ietf.org/doc/html/rfc5681','3.1のMSS依存IW、ACKのmin(N,SMSS)、加算増加、FlightSize/2と2SMSS下限、損失窓1SMSSを確認。RFC Editorは429、IETF本文を使用。'),
('net_ecn2001','IETF','RFC 3168: The Addition of ECN to IP','https://www.rfc-editor.org/rfc/rfc3168.html','冒頭と5章のIP CE、TCP ECE/CWR、明示的輻輳通知を確認。全RFC通読ではない。'),
('net_iw2013','IETF','RFC 6928: Increasing TCP Initial Window','https://www.rfc-editor.org/rfc/rfc6928.html','1〜2章でoptional IW10、実験的状態、min(10MSS,max(2MSS,14600))を確認。全実装の必須設定としない。'),
('net_hash','NIST','CSRC Glossary: Hash Function','https://csrc.nist.gov/glossary/term/hash_function','任意長→固定長、耐原像・第二原像・衝突耐性の公開定義を確認。パラメータ族の説明は理論的補足として区別。'),
('net_pq2024','NIST','First Three Finalized Post-Quantum Standards (2024)','https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards','2024-08-13 FIPS203/204/205、格子・ハッシュ系の標準化を確認。記事は2025更新、2024発表部分を区別。'),
('net_pq2022','NIST','IR 8413: Third Round Status Report','https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8413.pdf','物理61〜62頁Rainbowの実用攻撃・安全水準と選考不採用の公開本文。多変数族全体破綻という主張はしない。'),
('net_zkp2021','NIST','IR 8301: Blockchain Networks, Token Design and Management','https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=931698','物理42頁のprivate transaction・コミットメント・range proofs、次頁説明を確認。全84頁通読ではない。等式だけで全権限保証しない。')]
p=ROOT/'references.bib';s=p.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,title,url,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+title+'},\n url={'+url+'},\n urldate={2026-10-11}\n}\n'
p.write_text(s)
p=ROOT/'extracted/reference_checks/S7_024/source_notes.json'
local={}
for f in ['ipa_whitepaper2020.pdf','ipa_whitepaper2023.pdf']:
 q=p.parent/f;local[f]=hashlib.sha256(q.read_bytes()).hexdigest()
p.write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_pdf_sha256=local,limitations=['現行推奨と出題時点を分離。','全冊・全RFC通読を称さない。','独立初回のH26道幅は車高へ校正し初回履歴は保持。']),ensure_ascii=False,indent=2)+'\n')
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
new=[('network_path','最短経路とボトルネック経路','最短|車高','basic_2_8'),('network_routing','動的経路制御の情報共有と次ホップ','ルーティング|RIP|OSPF','basic_2_3'),('tcp_congestion','TCPの窓・ACK・輻輳制御','TCP|ふくそう','basic_2_3'),('document_cosine','文書特徴ベクトルのコサイン類似度','文書.*距離|類似','basic_2_16'),('password_lifecycle','パスワード運用・端末・認証要素','パスワード|PIN','basic_2_7'),('public_key_identity','公開鍵暗号・署名・PKIの鍵の役割','公開鍵|認証局','basic_2_7'),('targeted_defense','標的型攻撃の多層防御・報告・復旧','標的型|テレワーク','basic_2_7'),('cryptographic_guarantees','暗号の安全性・再送防止・秘匿証明','ゼロ知識|リプレイ|ポスト量子','basic_2_7')]
if not all(k in ids for k,_,_,_ in new):
 snap=ROOT/'snapshots/config_before_S7_024_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,label,pat,disc in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pat,subjects=['BASIC'],disciplines=[disc]))
 d['version']='1.17-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
