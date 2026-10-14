# coding: utf-8
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('info_markov','MIT OpenCourseWare','Stochastic Processes I, Lecture 5 (2013)','https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/f5784e4facf3de690210d17c97358eba_MIT18_S096F13_lecnote5.pdf','PDF物理3〜5頁の遷移・累乗・定常と全要素正の収束を照合。資料は列ベクトル、本教材は行ベクトルを定義して使う。試験行列の固有値計算は独立導出。'),
('info_errors','MIT OpenCourseWare','Information and Entropy, Chapter 4: Errors (2008)','https://ocw.mit.edu/courses/6-050j-information-and-entropy-spring-2008/71667aa5e13663096278c6617fca34e5_MIT6_050JS08_chapter4.pdf','PDF物理4頁の偶数パリティ・奇数反転検出・偶数不能・位置不能を照合。教材の剰余式と具体候補計算は独立に作成。'),
('info_cache','MIT OpenCourseWare','Memory Hierarchy and Caches Worksheet (2017)','https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/b71446c5273c385dfcc4e50f00a26b6a_caches_answers.pdf','PDF冒頭のAMAT=HitTime+MissRatio*MissPenaltyと局所性を確認。試験の排他的総時間モデルとの定義差を併記する。数値解答は自分で期待値から計算。'),
('info_isbn','International ISBN Agency','ISBN Users Manual (2012), Appendix 1','https://www.isbn-international.org/sites/default/files/ISBN%20Manual%202012%20-corr.pdf','PDF物理27頁の1/3交互重みとmod10を本文抽出で照合。13桁が2007年以降の方式であり、H26問題指定の旧10桁式と区別。割当保証と算術条件を分ける。'),
('info_deflate','P. Deutsch / RFC Editor','RFC 1951: DEFLATE Compressed Data Format Specification version 1.3','https://www.rfc-editor.org/rfc/rfc1951','本文のLZ77/Huffman、反復列参照、動的木と全入力を圧縮不能という計数議論を確認。原文の転載なし。'),
('info_universal','Yury Polyanskiy and Yihong Wu / MIT','Information Theory, Chapter 9: Universal Compression (2016)','https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/18b243d5e475579b7434260214ad9a25_MIT6_441S16_chapter_9.pdf','PDF冒頭の分布非指定の構成・情報源クラスへ同時漸近最適という意味を確認。高度な全証明読了ではない。'),
('info_separation','Yury Polyanskiy and Yihong Wu / MIT','Information Theory, Chapter 20: Source-Channel Separation (2016)','https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/dfddd4345fee8dd49420be583be2b952_MIT6_441S16_chapter_20.pdf','点対点・定常無記憶・長ブロックの情報源/通信路分離を照合。有限遅延と多元系へ無条件拡張しない。'),
('info_lossless','Yury Polyanskiy and Yihong Wu / MIT','Information Theory, Chapter 6: Variable-length Lossless Compression (2016)','https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/67d8e68cd8fda55366e3f9f0a9465c17_MIT6_441S16_chapter_6.pdf','PDF物理11〜12頁のKraft/一意復号/平均符号長のエントロピー下限を確認。個別列の長さの絶対下限と誤読しない。'),
('info_jpeg','Joint Photographic Experts Group','JPEG 1','https://jpeg.org/jpeg/','公式本文で静止画規格のDCT損失圧縮に加え可逆方式も含むことを照合。代表用途と全規格の性質を分ける。'),
('info_mpeg','MPEG','WG 4: MPEG Video Coding','https://www.mpeg.org/structure/video-coding/','公式ページ/公開検索本文で動画圧縮の規格策定を確認。新規格の最新性能値は教材に使用しない。')]
f=ROOT/'references.bib';s=f.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-11}\n}\n'
f.write_text(s)
d=ROOT/'extracted/reference_checks/S7_019';d.mkdir(exist_ok=True,parents=True)
(d/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],limitations=['理論資料は該当節の確認であり全ページ読了とはしない。','ISBN-10は試験原典で明示された式から独立計算。ISBN-13資料で旧方式を代用しない。','キャッシュ主記憶時間の総時間/追加時間の定義差と候補の最近値を明記。']),ensure_ascii=False,indent=2)+'\n')
new=[('markov_transition','有限マルコフ連鎖の遷移と定常分布','天気.*確率|マルコフ',['basic_2_1']),('source_compression','可逆性・圧縮限界・普遍性と情報源通信路分離','圧縮|情報理論',['basic_2_1']),('data_transfer','データ容量・圧縮率・通信速度の単位換算','伝送時間|回線利用率|格納.*ページ',['basic_2_1','basic_2_3'])]
f=ROOT/'config/concepts.json';d=json.loads(f.read_text());ids={x['id'] for x in d['concepts']}
if not all(x[0] in ids for x in new):
 snap=ROOT/'snapshots/config_before_S7_019_concept.json';assert not snap.exists();snap.write_bytes(f.read_bytes())
 for k,label,pat,disc in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pat,subjects=['BASIC'],disciplines=disc))
 old=d['version'];d['version']='1.12-S7-concept-additions';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 f=ROOT/'config/concept_change_log_S7.json';rows=json.loads(f.read_text());rows.append(dict(time=now(),batch='S7_019_information',previous_version=old,version=d['version'],added=[x[0] for x in new],reason='15原典の中心概念を3追加。既存符号・キャッシュ・文法概念を再利用。131概念の前版保存。'));f.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
