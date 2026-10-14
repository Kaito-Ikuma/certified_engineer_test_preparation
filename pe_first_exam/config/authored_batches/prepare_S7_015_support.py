# coding: utf-8
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('os_doppler','University Physics Volume 1, 17.7 The Doppler Effect','https://openstax.org/books/university-physics-volume-1/pages/17-7-the-doppler-effect','音源と観測者の速度を媒質に対して測り、波長と通過速度を区別する。'),
('os_sound','University Physics Volume 1, 17.2 Speed of Sound','https://openstax.org/books/university-physics-volume-1/pages/17-2-speed-of-sound','復元力と密度、気体の温度依存、通常の流体音波と固体波を確認。'),
('os_superposition','University Physics Volume 1, 16.5 Interference of Waves','https://openstax.org/books/university-physics-volume-1/pages/16-5-interference-of-waves','線形波の重ね合わせと相対位相の役割。'),
('os_lens','University Physics Volume 3, 2.4 Thin Lenses','https://openstax.org/books/university-physics-volume-3/pages/2-4-thin-lenses','実像・虚像と符号、レンズ方程式、倍率、複数レンズ。'),
('os_thinfilm','University Physics Volume 3, 3.4 Interference in Thin Films','https://openstax.org/books/university-physics-volume-3/pages/3-4-interference-in-thin-films','反射時のπ位相差と2ntの伝播位相を別々に足す。明環の次数の開始値は問題原典と別に確認。'),
('os_double','University Physics Volume 3, 4.3 Double-Slit Diffraction','https://openstax.org/books/university-physics-volume-3/pages/4-3-double-slit-diffraction','複数スリットの干渉と単スリット包絡の区別。'),
('os_grating','University Physics Volume 3, 4.4 Diffraction Gratings','https://openstax.org/books/university-physics-volume-3/pages/4-4-diffraction-gratings','主極大位置d sinθ=mλ。本数Nは主極大間隔ではなく幅・副極大と関係。'),
('os_fiber','University Physics Volume 3, 1.4 Total Internal Reflection','https://openstax.org/books/university-physics-volume-3/pages/1-4-total-internal-reflection','高屈折率側から低屈折率側への全反射と光ファイバ。'),
('os_spectrum','University Physics Volume 2, 16.5 The Electromagnetic Spectrum','https://openstax.org/books/university-physics-volume-2/pages/16-5-the-electromagnetic-spectrum','電磁波領域の波長・周波数の順序。'),
('os_photoelectric','University Physics Volume 3, 6.2 Photoelectric Effect','https://openstax.org/books/university-physics-volume-3/pages/6-2-photoelectric-effect','光子エネルギーと仕事関数、閾値。'),
('os_matter','University Physics Volume 3, 6.5 De Broglie\u2019s Matter Waves','https://openstax.org/books/university-physics-volume-3/pages/6-5-de-broglies-matter-waves','電子線回折は物質波の証拠で、光子の粒子性とは対象が異なる。'),
('mit_optics2014','Optics, Spring 2014: Lecture Notes','https://ocw.mit.edu/courses/2-71-optics-spring-2014/pages/lecture-notes/','幾何光学、波動光学、干渉の講義構成を参照。講義PDF全頁読了ではない。')]
f=ROOT/'references.bib';s=f.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n  author={{'+('Massachusetts Institute of Technology' if k.startswith('mit_') else 'OpenStax, Rice University')+'}},\n  title={'+t+'},\n  url={'+u+'},\n  urldate={2026-10-10}\n}\n'
f.write_text(s)
dest=ROOT/'extracted/reference_checks/S7_015';dest.mkdir(parents=True,exist_ok=True)
(dest/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,t,u,n in refs],limitations=['ウェブ本文と検索抜粋を照合。講義PDFの全頁目視を意味しない。','複スリット暗線の括弧と明環次数の開始値は原典の疑義として保持。']),ensure_ascii=False,indent=2)+'\n')
new=[('wave_kinematics','進行波の位相・波長・角振動数','正弦波|位相速度',['physics_wave']),('acoustic_propagation','音波・弾性波・媒質の復元力','音速|縦波|横波|衝撃波',['physics_wave']),('acoustic_doppler','音源運動・ドップラー・反射音','ドップラー|音源|反射音',['physics_wave']),('acoustic_interference','音の経路差・位相差・干渉','スピーカ|経路差',['physics_wave']),('thin_lens','薄レンズの実像・虚像と符号','凸レンズ|焦点距離',['physics_optics']),('optical_diffraction','光の干渉・回折格子','スリット|回折格子',['physics_optics']),('thinfilm_interference','薄膜反射位相・ニュートンリング','ニュートンリング|明環',['physics_optics']),('photon_matter_wave','光子の量子性・電子の物質波','光電効果|電子線回折',['physics_modern']),('em_spectrum','電磁波領域・光子エネルギー','赤外線|紫外線|可視光線|ガンマ線',['physics_optics','physics_em'])]
f=ROOT/'config/concepts.json';d=json.loads(f.read_text());ids={x['id'] for x in d['concepts']}
if not all(x[0] in ids for x in new):
 snap=ROOT/'snapshots/config_before_S7_015_concept.json';assert not snap.exists();snap.write_bytes(f.read_bytes())
 for k,label,pat,disc in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pat,subjects=['APPLIED'],disciplines=disc))
 old=d['version'];d['version']='1.8-S7-concept-additions';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 log=ROOT/'config/concept_change_log_S7.json';rows=json.loads(log.read_text());rows.append(dict(time=now(),batch='S7_015_wave_optics',previous_version=old,version=d['version'],added=[x[0] for x in new],reason='既存分野を保持し、位相・媒質・運動・経路差・像・回折・薄膜・光子・スペクトルを区別。9概念追加、99概念の前版保存。'));log.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('References 12, concepts',len(d['concepts']))
