"""Safe stage entry points; never advertise an unimplemented final pipeline."""
import argparse,subprocess,sys
from common import ROOT

def main():
 p=argparse.ArgumentParser();p.add_argument('--phase',choices=['initial','reviewed','draft','final'],default='reviewed');p.add_argument('--apply',action='store_true');a=p.parse_args()
 if a.phase=='final':raise SystemExit('Final review/quality/citation/compile sign-off is not implemented.')
 if a.phase=='initial' and (ROOT/'handoff/ASTRA_REVIEW_1.md').exists():raise SystemExit('Use --phase reviewed; original checkpoint is immutable.')
 def run(script,*args):subprocess.run([sys.executable,'-B',str(ROOT/'scripts'/script),*args],cwd=ROOT,check=True)
 if a.phase in ('initial','reviewed'):
  run('build_question_db.py',*(['--apply'] if a.apply else []));run('classify_questions.py',*(['--apply'] if a.apply else []))
  if not a.apply:return
  run('validate_answers.py');run('audit_completeness.py');run('prepare_checkpoint1.py')
 else:
  run('audit_completeness.py');run('generate_statistics.py');run('find_similar_questions.py');run('generate_year_index.py');run('generate_topic_index.py');run('build_textbook.py');run('audit_tex_labels.py')
 print('Completed stage',a.phase,'final sign-off unavailable')
if __name__=='__main__':main()
