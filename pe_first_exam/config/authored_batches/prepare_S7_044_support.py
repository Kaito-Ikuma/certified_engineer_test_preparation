# coding:utf-8
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now,json_bytes,digest
refs=[('rfc4291_addresses','R. Hinden and S. Deering','RFC 4291: IP Version 6 Addressing Architecture','https://www.rfc-editor.org/rfc/rfc4291.html','2節の128bitと2.2節の8個16bit表記・IPv4表記を確認。予約を除いた実用割当数と全ビット列数を分ける。'),('princeton_bst','Robert Sedgewick and Kevin Wayne','Algorithms 4th edition: Binary Search Trees','https://algs4.cs.princeton.edu/32bst/','取得HTMLの定義・Search・Insert・Analysisを確認。挿入順に依存する木形と左右部分木の大小条件を確認。'),('mit_discrete2015','Eric Lehman and F. Thomson Leighton and Albert R. Meyer','Mathematics for Computer Science (2015)','https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/mit6_042js15_textbook.pdf','取得PDF印刷250--251頁の拡張互除法、529--530頁のBig O、584--585頁のn集合包除を確認。全882頁読了とはしない。問題の数値は独自計算。')]
p=ROOT/'references.bib';s=p.read_text()
for k,a,t,u,n in refs:
 assert '@online{'+k+',' not in s
 s+='\n@online{'+k+',\n author={'+a+'},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n+'}\n}\n'
p.write_text(s)
concepts=[('discrete_state_counts','ビット列・積の法則と写像数','ビット|写像',['basic_2_2','basic_2_4']),('set_inclusion_exclusion','包除原理・補集合と多重共通部分','集合',['basic_2_4']),('expression_tree_postorder','算術木・演算優先と後置記法','算術木|後置|ポーランド',['basic_2_0']),('binary_search_tree_order','二分探索木・挿入順の祖先制約','二分探索木',['basic_2_0']),('algorithm_scan_invariants','走査の不変条件・分岐と素数判定','アルゴリズム|素数',['basic_2_8']),('extended_euclid_matrix','拡張互除法の係数と行列積','互除法',['basic_2_8']),('asymptotic_growth_order','漸近上界と増大の階層','漸近|オーダ',['basic_2_8']),('ackermann_recursion','アッカーマン関数と入れ子再帰','アッカーマン',['basic_2_8'])]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']};snap=ROOT/'snapshots/config_before_S7_044_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
for k,t,pat,disc in concepts:
 assert k not in ids;d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['BASIC'],disciplines=disc))
d['version']='1.37-S7-concept-additions';p.write_bytes(json_bytes(d))
(ROOT/'extracted/reference_checks/S7_044/source_notes.json').write_bytes(json_bytes(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs],local_sources=[dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in (ROOT/'extracted/reference_checks/S7_044').glob('*') if p.suffix in ['.pdf','.html']],notes=['原典21問29頁画像を確認し、公式前初回21解答は全一致。','R03逆ポーランドのOCR減算を原典の除算へ校正。H30補集合の上線を確認。','Bézout方程式だけでは複数候補を満たすため、指定行列積の第二行を条件にする。'])))
print('concepts',len(d['concepts']),'refs',len(refs))
