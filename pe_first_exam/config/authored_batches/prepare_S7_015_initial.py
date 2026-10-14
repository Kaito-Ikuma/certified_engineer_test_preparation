# coding: utf-8
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sel=json.loads((ROOT/'extracted/logs/S7_015_wave_optics_selection.json').read_text())
answers=['2','2','4','1','2','3','2','2','1','3','5','2','2','5','5','4','3','2','3','5','4']
notes=[
'後退音源。440×340/(340+4)=434.884 Hz、435の2。',
'焦点外は反対向き実像、内は同じ向き虚像。物体が近付くと実像は遠くへ。表2。',
'海水の音速は空気より大きく、逆の4が誤り。',
'波長は赤外・可視・紫外・γの順、1。',
'電子線回折は電子の波動性であり、光の粒子性と最も関係が薄い2。',
'λ=2π/k、v=ω/kで3。',
'後退音源のf=434.884 Hzで2。',
'焦点外実像反転、内虚像正立、物体が近付くと実像遠ざかるため表2。',
'主極大間隔Lλ/dを増すならdを狭くする1。複スリットの暗線を全て数える場合のN依存は留意。',
'第一像b1=-10 cm、第二物体距離30 cm、像60 cmなのでf2=20 cmの3。',
'λ=2π/k、v=ω/kで5。',
'初期D0=(340+20)×3/2=540 m、戻った時点D1=540-60=480 mの2。',
'原画像の正面距離3.3 m、スピーカ間隔2 m。Δ=sqrt(3.3²+2²)-3.3。最初の極小f=340/(2Δ)≈304 Hz、310の2。次の次数は候補外。',
'光ファイバはコアの屈折率がクラッドより高く、逆の5。',
'格子d=650 nm/sin30°=1300 nm、1 mmの本数≈769で770の5。',
'光子E=hc/λなので高エネルギーからγ・紫外・可視・赤外、4。',
'反射明環は2t=(n+1/2)λ、t=x²/(2R)なのでx²/R=(n+1/2)λの3。ただしm番目を1から数えるならm-1/2となり該当肢なし。m=0始まりの条件は原文にない。',
'振動方向が伝播方向と平行なら縦波。横波とする2が誤り。',
'Δ=sqrt(4²+2.4²)-4、f=340/(2Δ)≈256 Hzで260の3。次の次数は候補外。',
'1/15=1/10+1/b、b=-30 cm、倍率3の正立虚像、物体側30 cmの5。',
'位相一定からv=λ/T、時間位相係数ω=2π/T、4。']
assert len(sel)==len(answers)==len(notes)==21
rows=[dict(question_id=s['question_id'],independent_answer=a,reason=n,source_images_viewed=s['pages'],official_answer_consulted=False) for s,a,n in zip(sel,answers,notes)]
dest=ROOT/'config/authored_batches/S7_015_independent_answers.json'
assert not dest.exists()
dest.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('独立解答21問保存。f=',340/(2*(math.sqrt(3.3**2+2**2)-3.3)),340/(2*(math.sqrt(4**2+2.4**2)-4)))
