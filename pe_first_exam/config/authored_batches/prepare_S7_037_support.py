# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('mit_roy_fea1999','David Roylance','Finite Element Analysis','https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/812a432c72099369788f78fb344eb047_MIT3_11F99_fea.pdf','MIT講義資料。表紙の日付2001-02-28を確認。変位補間、ひずみと応力、剛性行列、高勾配の細分化の本文を確認。Q4・面積座標の具体的導出は本教材の独自計算である。'),
('nist_newton','National Institute of Standards and Technology','Digital Library of Mathematical Functions: 3.8 Nonlinear Equations','https://dlmf.nist.gov/3.8','Newton反復式3.8.4、単根近傍の二次収束、初期値への依存を確認。ステップ幅だけで停止する設問の実務上の不足を区別する。'),
('nist_differentiation','National Institute of Standards and Technology','Digital Library of Mathematical Functions: 3.4 Differentiation','https://dlmf.nist.gov/3.4','補間多項式の微分による差分と余項の節を確認。過去問の各差分のTaylor展開・次数判定は独自に計算する。'),
('nist_interpolation','National Institute of Standards and Technology','Digital Library of Mathematical Functions: 3.3 Interpolation','https://dlmf.nist.gov/3.3','相異なる節点に対する補間多項式の一意性、Lagrange基底と誤差項を確認。3点の係数は本教材で独自に導出する。'),
('openstax_thermal_conduction','OpenStax','University Physics Volume 2: 1.6 Mechanisms of Heat Transfer','https://openstax.org/books/university-physics-volume-2/pages/1-6-mechanisms-of-heat-transfer','定常平板の熱伝導式1.9とFourier式を確認。二層の並列・直列の有効値は熱流及び温度差の加算から独自に導出する。')]
p=ROOT/'references.bib';s=p.read_text();added=0
for k,a,t,u,n in refs:
 if '@online{'+k+',' not in s:
  s+='\n@online{'+k+',\n author={{'+a+'}},\n title={'+t+'},\n url={'+u+'},\n urldate={2026-10-12},\n note={'+n+'}\n}\n';added+=1
p.write_text(s)
concepts=[('fem_interpolation_continuity','要素補間・変位と応力の連続性','連続|不連続'),('layered_thermal_conductivity','二層材料の有効熱伝導率','熱伝導率'),('fem_mesh_convergence','有限要素のメッシュ収束','要素分割|安全側'),('triangle_area_coordinates','三角形の面積座標','面積座標|内心|重心'),('finite_difference_consistency','差分式の整合性','差分'),('polynomial_interpolation','多項式補間','補間'),('bilinear_shape_expansion','双一次形状関数の展開','形状関数'),('triangle_double_integral','三角領域の重積分','重積分'),('quadrature_weight_moments','求積の重みとモーメント条件','積分公式'),('newton_iteration_flow','Newton反復と停止判定','ニュートン|Newton'),('constant_strain_triangle','一定ひずみ三角形','ひずみ|歪み'),('floating_expression_stability','等価式と有限精度の安定性','桁落ち|情報落ち')]
p=ROOT/'config/concepts.json';d=json.loads(p.read_text());ids={x['id'] for x in d['concepts']}
if not all(k in ids for k,_,_ in concepts):
 snap=ROOT/'snapshots/config_before_S7_037_concept.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
 for k,t,pat in concepts:
  if k not in ids:d['concepts'].append(dict(id=k,label=t,pattern=pat,subjects=['BASIC'],disciplines=['basic_3_1','basic_3_2']))
 d['version']='1.30-S7-concept-additions';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
folder=ROOT/'extracted/reference_checks/S7_037';folder.mkdir(parents=True,exist_ok=True)
(folder/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,url=u,checked_claim=n) for k,a,t,u,n in refs]+[dict(key='goldberg1991',url='https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html',checked_claim='Cancellation節の入力の丸め誤差が近い差で増幅する説明を確認。差の演算そのものが常に誤差を新生するという断定はしない。'),dict(key='nist_quadrature',url='https://dlmf.nist.gov/3.5',checked_claim='台形則と滑らかな関数の余項を確認。重みのモーメント検算を独自に導出する。')],limitations=['原典画像21問を確認し公式前の独立解答を別ファイルに保存。','11問の条件不足や全称表現を部分校正として保持する。','本文の式は原典と一次資料を参照した独自導出であり、資料の図は転載しない。']),ensure_ascii=False,indent=2)+'\n')
print('Concepts',len(d['concepts']),'references added',added)
