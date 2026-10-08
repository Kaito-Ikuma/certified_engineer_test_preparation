"""Reproduce S0-S3 locally. Final pipeline is intentionally gated until review."""
import argparse
import subprocess
import sys
from common import ROOT, YEARS, SUBJECTS

def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['initial','final'],default='initial');a=p.parse_args()
    if a.phase=='final':raise SystemExit('最終工程は未実装です。Checkpoint 1のAstra査読とS4以降を先に実施してください。')
    if (ROOT/'handoff/ASTRA_REVIEW_1.md').exists():raise SystemExit('査読後のデータ保護のため初期再構築を停止。修正内容に応じて個別スクリプトを実行してください。')
    missing=[f'{y}/{s}' for y in YEARS for s in SUBJECTS if not (ROOT/'extracted/text'/y/(s+'.json')).exists()]
    if missing:raise SystemExit('先にextract_pdf_text.py --ocrを実行してください: '+', '.join(missing))
    for script in ['scan_sources.py','parse_official_answers.py','build_question_db.py','classify_questions.py','validate_answers.py','audit_completeness.py']:
        subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)
    print('S0-S3再構築完了。教材・統計・最終PDFは未生成。')
if __name__=='__main__':main()
