# coding: utf-8
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT,now
refs=[
('bio_composition','Alberts et al. / NCBI Bookshelf','Molecular Biology of the Cell, 4th edition: The Chemical Components of a Cell','https://www.ncbi.nlm.nih.gov/books/NBK26883/','公開検索抽出で水70・4小分子群・典型的組成を確認。直接ページはcaptchaで全文読了ではない。'),
('bio_cell_mass','Feijo Delgado et al.','Intracellular Water Exchange for Measuring the Dry Mass, Water Mass and Changes in Chemical Composition of Living Cells','https://pmc.ncbi.nlm.nih.gov/articles/PMC3699654/','2013研究論文の表2：細菌・酵母・哺乳類細胞、分母別の水・乾燥重量組成。検索抽出で確認。'),
('bio_membrane','Alberts et al. / NCBI Bookshelf','Molecular Biology of the Cell, 4th edition: The Lipid Bilayer','https://www.ncbi.nlm.nih.gov/books/NBK26871/','公式公開検索本文でcis・短鎖・相転移と温度適応を確認。'),
('bu_dna_melting','Boston University','Lecture 26: Nucleic Acids Introduction (2024)','https://www.bu.edu/aldolase/biochemistry/html_docs/26_NucleicAcids_Intro_24.pdf','講義PDF検索抽出で7頁DNA変性の紫外増色と260 nm・融解曲線。直接取得エラー、全文読了ではない。'),
('mit_amino','MIT OpenCourseWare','Structures of Amino Acids and Protein Synthesis (7.012, 2004)','https://ocw.mit.edu/courses/7-012-introduction-to-biology-fall-2004/93d90acfb2556162708a7401c8c7b7d8_protq.pdf','標準20種の側鎖構造とペプチド結合の独自講義資料を検索抽出で照合。'),
('mit_protein','MIT OpenCourseWare','31. Biochemistry: Protein Structure (3.091SC, 2010)','https://ocw.mit.edu/courses/3-091sc-introduction-to-solid-state-chemistry-fall-2010/pages/organic-materials/31-protein-structure/','講義本文の一次構造、等電点、酸塩基、ペプチド・S-S、疎水効果を確認。'),
('nhgri_dna','National Human Genome Research Institute','Deoxyribonucleic Acid (DNA) Fact Sheet','https://www.genome.gov/about-genomics/fact-sheets/Deoxyribonucleic-Acid-Fact-Sheet','塩基対、逆平行、転写と翻訳を公式公開本文で照合。'),
('nhgri_codon','National Human Genome Research Institute','Codon','https://www.genome.gov/genetics-glossary/Codon','64・61・3とコドンの機能を本文確認。'),
('nhgri_frameshift','National Human Genome Research Institute','Frameshift Mutation','https://www.genome.gov/genetics-glossary/Frameshift-Mutation','3の倍数でない挿入欠失と読み枠を本文確認。翻訳領域の成立条件を独自に明示。'),
('nhgri_sickle','National Library of Medicine','HBB gene: MedlinePlus Genetics','https://medlineplus.gov/genetics/gene/hbb/','HbSのGlu6Valと遺伝子変異を公式検索本文で確認。治療情報は教材へ持ち込まない。'),
('nhgri_cdna','National Human Genome Research Institute','cDNA (copy DNA)','https://www.genome.gov/genetics-glossary/copy-DNA-cDNA','mRNA由来と逆転写を本文確認。cDNAはUTRも含み得るので、ページのcoding-onlyという簡略化は採用しない。誤った推定URL404の後に実URL確認。'),
('nhgri_epigenomics','National Human Genome Research Institute','Epigenomics Fact Sheet','https://www.genome.gov/about-genomics/fact-sheets/Epigenomics-Fact-Sheet','配列変異と異なるメチル化、発現状態と細胞分裂での継承を本文確認。'),
('nhgri_cloning','National Human Genome Research Institute','Cloning Fact Sheet','https://www.genome.gov/about-genomics/fact-sheets/Cloning-Fact-Sheet','除核卵と体細胞核、核由来と表現型の差を本文確認。他の時点依存の人クローン記述は不使用。'),
('plant_regeneration','Bao et al.','Genome scale transcriptome analysis of shoot organogenesis in Populus (2009)','https://pubmed.ncbi.nlm.nih.gov/19919717/','一次研究の検索本文でホルモン処理、カルスとシュート再生を確認。直接取得captcha、全文読了でない。'),
('neb_pcr','New England Biolabs','PCR Troubleshooting Guide','https://www.neb.com/en/tools-and-resources/troubleshooting-guides/pcr-troubleshooting-guide','非特異産物欄の低温対策、プライマー条件、長い鋳型を公式製造者文書で確認。'),
('neb_ecori','New England Biolabs','EcoRI-HF','https://www.neb.com/en/products/r3101-ecori-hf','公式製造者ページ取得。認識図は画像で、GAATTC文字検索一致なし。平均間隔は独立等確率モデルから自分で導出し固定長を否定。'),
('fda_insulin','U.S. Food and Drug Administration','100 Years of Insulin','https://www.fda.gov/about-fda/fda-history-exhibits/100-years-insulin','1978開発と1982承認を公式歴史本文確認。'),
('nih_amino','National Library of Medicine','Amino acids: MedlinePlus Medical Encyclopedia','https://medlineplus.gov/ency/article/002222.htm','通常の必須9、非必須Pro、条件付き必須を本文確認。哺乳類全種を同じとする保証ではない。'),
('iubmb_lipase','IUBMB Enzyme Nomenclature','EC 3.1.1.3: triacylglycerol lipase','https://iubmb.qmul.ac.uk/enzyme/EC3/1/1/3.html','公式酵素分類の反応式と受容名を本文確認。'),
('iubmb_amylase','IUBMB Enzyme Nomenclature','EC 3.2.1.1: alpha-amylase','https://iubmb.qmul.ac.uk/enzyme/EC3/2/1/1.html','公式酵素分類のα1→4結合に対する加水分解を本文確認。'),
('hyper_amylase','Grzybowska et al.','Cloning, Expression, and Purification of Hyperthermophile alpha-Amylase from Pyrococcus woesei','https://pmc.ncbi.nlm.nih.gov/articles/PMC4700765/','2015一次研究の100℃至適の記述を公開検索本文で確認。20℃以下も100℃以上もないという肢はこの一例だけで否定。')
]
f=ROOT/'references.bib';s=f.read_text();keys=set(re.findall(r'@\w+\{([^,]+),',s))
for k,a,t,u,n in refs:
 if k not in keys:s+='\n@online{'+k+',\n  author={{'+a+'}},\n  title={'+t+'},\n  url={'+u+'},\n  urldate={2026-10-10}\n}\n'
f.write_text(s)
dest=ROOT/'extracted/reference_checks/S7_017';dest.mkdir(parents=True,exist_ok=True)
(dest/'source_notes.json').write_text(json.dumps(dict(checked_at=now(),sources=[dict(key=k,title=t,url=u,checked_claim=n) for k,a,t,u,n in refs],limitations=['H26B4-6の組成比の普遍性を未確定として保持。代表例と全生物を区別。','検索抽出と直接本文の範囲を区別しcaptcha/取得エラーを読了にしない。']),ensure_ascii=False,indent=2)+'\n')
new=[('cell_composition','細胞組成の分母と代表値','細胞.*組成'),('membrane_fluidity','膜脂質の充填と流動性','生体膜|飽和脂肪酸'),('amino_acids','アミノ酸の共通骨格・側鎖・立体配置と必須性','アミノ酸'),('protein_structure','タンパク質の配列・折畳み・電荷','タンパク質.*構造|等電点'),('dna_structure','DNAの相補性・主鎖・複製方向','相補鎖|二重らせん'),('dna_denaturation','DNAの融解・再会合と紫外吸収','DNA.*変性'),('genetic_code','遺伝暗号の縮重と読み枠','コドン'),('molecular_biology_techniques','PCR・制限酵素・電気泳動・DNAライブラリ','PCR|組換えDNA|組換え技術'),('cloning','植物の再分化と体細胞核移植','クローン'),('genetic_mutation','塩基変化の種類と遺伝子発現への効果','突然変異'),('enzyme_catalysis','酵素の基質特異性・障壁・温度条件','酵素|アミラーゼ|リパーゼ')]
f=ROOT/'config/concepts.json';d=json.loads(f.read_text());ids={x['id'] for x in d['concepts']}
if not all(x[0] in ids for x in new):
 snap=ROOT/'snapshots/config_before_S7_017_concept.json';assert not snap.exists();snap.write_bytes(f.read_bytes())
 for k,label,pat in new:
  if k not in ids:d['concepts'].append(dict(id=k,label=label,pattern=pat,subjects=['BASIC'],disciplines=['basic_4_0']))
 old=d['version'];d['version']='1.10-S7-concept-additions';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 log=ROOT/'config/concept_change_log_S7.json';rows=json.loads(log.read_text());rows.append(dict(time=now(),batch='S7_017_biology',previous_version=old,version=d['version'],added=[x[0] for x in new],reason='生命科学28原典に現れる11概念を既存basic_4_0内で整理。113概念の前版保存。'));log.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('References',len(refs),'concepts',len(d['concepts']))
