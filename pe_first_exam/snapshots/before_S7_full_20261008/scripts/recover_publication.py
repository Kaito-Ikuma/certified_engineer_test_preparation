"""Explicitly roll back an interrupted publication, preserving its journal."""
import argparse,json,shutil
from common import ROOT,json_bytes
p=argparse.ArgumentParser();p.add_argument('--rollback',action='store_true');a=p.parse_args()
lock=ROOT/'data/publication.lock'
if not lock.exists():raise SystemExit('No interrupted publication')
name=lock.read_text().strip()
if not name:raise SystemExit('Empty lock: publication stopped before journal binding; inspect snapshots before recovery')
txn=ROOT/name;j=json.loads((txn/'journal.json').read_text())
if not a.rollback:raise SystemExit(json.dumps(j,indent=2))
if j['status']!='staging':
 for key in j['paths']:
  if j['existed'][key]:shutil.copy2(txn/'before'/key,ROOT/key)
  else:(ROOT/key).unlink(missing_ok=True)
j['status']='recovered_rollback';(txn/'journal.json').write_bytes(json_bytes(j));lock.unlink()
