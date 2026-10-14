# coding: utf-8
import json,sys,shutil,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
 ('ip_copyright_statute','e-Gov法令検索','著作権法：取得条文','https://laws.e-gov.go.jp/law/345AC0000000048','2条、13条、17〜20条、23条、30条の4、32条、47条の6、48条を確認。過去の43条と現在の翻訳規定の条番号を混同しない。'),
 ('ip_patent_statute','e-Gov法令検索','特許法：取得条文','https://laws.e-gov.go.jp/law/334AC0000000121','1条、2条、29条、30条、32条を確認。発明該当性・産業上利用可能性・新規性・公序良俗を分ける。'),
 ('ip_unfair_statute','e-Gov法令検索','不正競争防止法：営業秘密の定義','https://laws.e-gov.go.jp/law/405AC0000000047','本則2条6項で三要件を確認。資料名や会社内の作成という事情のみでは成立しない。'),
 ('ip_industrial_four','特許庁','産業財産権について','https://www.jpo.go.jp/system/patent/gaiyo/seidogaiyo/chizai01.html','前段でWeb本文を確認した特許・実用新案・意匠・商標の4種類。再取得は403。'),
 ('ip_broad_scope','特許庁','知的財産権について','https://www.jpo.go.jp/system/patent/gaiyo/seidogaiyo/chizai02.html','官公庁の検索索引本文で広い定義、商号、営業秘密を確認。ページの再取得は403であり全文取得とはしない。'),
 ('ip_secret_handbook2017','経済産業省','秘密情報の保護ハンドブック（2017年版）','https://www.meti.go.jp/policy/economy/chizai/chiteki/pdf/1706tradesec.pdf','検索索引の該当箇所で三要件、未利用情報の有用性、反社会的情報の除外を確認。全PDFを取得・閲読したとはしない。'),
 ('ip_secret_commentary2018','経済産業省','不正競争防止法逐条解説：定義規定（2018年）','https://www.meti.go.jp/policy/economy/chizai/chiteki/pdf/20181129chikujyokaisetsur.pdf','検索索引の有用性の節で失敗実験情報と反社会的行為の区別を確認。全文取得なし。'),
 ('ip_novelty_grace2018','特許庁','発明の新規性喪失の例外期間の延長','https://www.jpo.go.jp/system/laws/rule/guideline/patent/hatumei_reigai_encho.html','検索索引で2018年6月9日施行、6か月から1年、出願と公開日の経過措置を確認。公開済みであること自体を積極要件にしない。'),
 ('ip_flexible2019','文化庁','柔軟な権利制限規定に関する説明資料（2019年10月24日）','https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/h30_hokaisei/pdf/r1406693_17.pdf','83物理頁中13〜21頁の本文を確認。6事例、享受目的併存、必要限度、不当利益侵害、3DCGの表現承継、検索結果表示の境界。'),
]
p=ROOT/'references.bib';s=p.read_text()
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:
  s+='\n@online{'+k+',\n  author = {{'+a+'}},\n  title = {'+t+'},\n  url = {'+u+'},\n  urldate = {2026-10-12},\n  note = {'+n+'}\n}\n'
p.write_text(s)
concepts=[
 ('ip_scope_industrial','産業財産権4種類と広義知的財産の境界','産業財産権'),
 ('ip_scope_broad','知的財産の広い範囲と保護形態','知的財産権'),
 ('ip_copyright_basics','著作権の保護対象と無方式主義','著作権|著作者人格権'),
 ('ip_citation_conditions','引用・官公資料転載・翻訳の条件','引用|官公資料'),
 ('ip_trade_secret','営業秘密の三要件と有用性','営業秘密|非公知'),
 ('ip_patent_requirements','発明の定義と特許の要件','特許の要件|新規性'),
 ('ip_nonenjoyment','非享受目的の利用と権利制限の境界','30条の4|リバース'),
]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={c['id'] for c in d['concepts']}
if not all(k in ids for k,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_031_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['APT'],disciplines=['apt_4']))
 d['version']='1.24-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_031';folder.mkdir(exist_ok=True)
files=[]
for name in ['copyright.xml','patent.xml','unfair.xml','flexible2019.pdf','flexible2019.txt']:
 src=Path('/tmp/S7_031_'+name);target=folder/src.name;shutil.copyfile(src,target)
 files.append(dict(file=str(target.relative_to(ROOT)),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],local_files=files,limitations=['2013・2014年の著作権法版全文は取得していない。既存九州大学2015年資料URLは404。該当二問は当時条文の版照合を未完として保持する。','2018年のサイバー攻撃漏洩の急増を示す当時の定量系列は未確認。','経済産業省PDF取得は403。官公庁の索引に見える該当段落と取得済み法令条文を分ける。','API取得条文は現行理解の補助であり、過去版全文の代用ではない。']),ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
