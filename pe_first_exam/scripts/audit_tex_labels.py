"""Every question exactly one generated label; check actual source references."""
import re,json
from collections import Counter
from common import ROOT,read_csv,publish_bundle,json_bytes
from tex_graph import input_graph

def main():
    labels=[];refs=[]
    files,errors=input_graph()
    for t in files.values():
        labels.extend(re.findall(r'\\label\{([^}]+)\}',t));refs.extend(re.findall(r'\\(?:ref|pageref)\{([^}]+)\}|\\hyperref\[([^]]+)\]',t))
    count=Counter(labels);qs=read_csv('data/questions.csv');expected={r['tex_label'] for r in qs}
    errors+=['missing/duplicate question label '+k for k in expected if count[k]!=1];errors+=['extra question label '+k for k in count if k.startswith('q:') and k not in expected];errors+=['duplicate label '+k for k,n in count.items() if n>1];errors+=['unresolved reference '+(a or b) for a,b in refs if (a or b) not in count]
    publish_bundle({'extracted/logs/tex_label_audit.json':json_bytes({'question_labels':len(expected),'errors':errors,'scope':'source labels/references only, not final content/compile sign-off'})})
    print('Question labels',len(expected),'errors',len(errors))
    if errors:raise SystemExit('\n'.join(errors[:20]))
if __name__=='__main__':main()
