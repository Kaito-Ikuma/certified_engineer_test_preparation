"""Non-destructive native extraction and source/config keyed OCR caching."""
import argparse,json,subprocess,tempfile
from concurrent.futures import ThreadPoolExecutor
from common import ROOT,digest,publish_bundle,json_bytes

SETTINGS={'engine':'macOS Vision','languages':['ja-JP','en-US'],'dpi':200,'recognition':'accurate','version':2}

def extract(path,ocr=False):
    relative=path.relative_to(ROOT/'sources').with_suffix('');textpath=ROOT/'extracted/text'/relative.with_suffix('.txt');meta_path=textpath.with_suffix('.json');sha=digest(path)
    cached=json.loads(meta_path.read_text()) if meta_path.exists() else None
    # Existing source/config-bound OCR is reusable even without --ocr.
    same=bool(cached and cached.get('source_sha256')==sha and cached.get('ocr_settings')==SETTINGS)
    if cached and not cached.get('source_sha256'):raise RuntimeError('Legacy cache requires explicit verified binding: '+str(meta_path))
    native=subprocess.run(['pdftotext','-layout',str(path),'-'],capture_output=True,text=True,check=True).stdout
    chunks=native.split('\f');pages=chunks[:-1] if chunks[-1]=='' else chunks
    results=[]
    cachekey=__import__('hashlib').sha256(json_bytes(SETTINGS)).hexdigest()[:12]
    images=ROOT/'extracted/pages/cache'/sha/cachekey
    for i,page in enumerate(pages,1):
        if page.strip():results.append({'page':i,'method':'pdftotext','text':page})
        elif same and i<=len(cached['pages']):results.append(cached['pages'][i-1])
        elif ocr:
            jp=images/f'page_{i:03d}.json'
            if not jp.exists():
                proc=subprocess.run([str(ROOT/'scripts/ocr_pdf'),str(path),str(images),str(i),str(i)],capture_output=True,text=True)
                if proc.returncode:raise RuntimeError(proc.stderr)
            result=json.loads(jp.read_text());result.update(method='ocr_unverified',text='\n'.join(x['text'] for x in result['lines']),source_sha256=sha,ocr_settings=SETTINGS);results.append(result)
        else:
            # New extraction is incomplete: report, never overwrite earlier useful data.
            raise RuntimeError('No matching OCR cache; rerun --ocr: '+str(path)+f' page {i}')
    meta={'source':str(path.relative_to(ROOT)),'source_sha256':sha,'ocr_settings':SETTINGS,'pages':results}
    combined='\f'.join(r['text'] for r in results)+'\f'
    publish_bundle({str(textpath.relative_to(ROOT)):combined,str(meta_path.relative_to(ROOT)):json_bytes(meta)})
    return [meta['source'],len(results),sum(r['method']=='ocr_unverified' for r in results)]

def bind_legacy():
    """One-time migration: historical OCR + unchanged official manifest provenance."""
    from common import read_csv
    manifest={r['path']:r for r in read_csv('data/source_files.csv')};files={};bindings=[]
    for mp in (ROOT/'extracted/text').rglob('*.json'):
        meta=json.loads(mp.read_text())
        if 'pages' not in meta or 'source' not in meta or meta.get('source_sha256'):continue
        source=meta['source'];row=manifest[source];sha=digest(ROOT/source)
        if sha!=row['sha256'] or len(meta['pages'])!=int(row['page_count']):raise ValueError('Cannot bind changed source: '+source)
        for page in meta['pages']:
            if page.get('method')=='ocr_unverified' and ('lines' not in page or page.get('render_dpi',200)!=200):raise ValueError('Invalid legacy OCR')
        meta.update(source_sha256=sha,ocr_settings=SETTINGS,legacy_binding_basis='unchanged CP1 PDF hash; retained historical OCR, not re-recognized')
        files[str(mp.relative_to(ROOT))]=json_bytes(meta);bindings.append({'source':source,'source_sha256':sha,'metadata':str(mp.relative_to(ROOT)),'basis':meta['legacy_binding_basis']})
    if files:
        files['extracted/logs/cache_bindings.json']=json_bytes(bindings);publish_bundle(files)
    print('Bound legacy extraction caches',len(bindings))

def main():
    p=argparse.ArgumentParser();p.add_argument('--ocr',action='store_true');p.add_argument('--answers-only',action='store_true');p.add_argument('--workers',type=int,default=2);p.add_argument('--bind-legacy',action='store_true');a=p.parse_args()
    if a.bind_legacy:bind_legacy();return
    targets=sorted(x for x in (ROOT/'sources').rglob('*.pdf') if (x.name in ['basic.pdf','aptitude.pdf','17_applied_science.pdf'] and not a.answers_only) or 'official_answers' in x.name)
    # Publication serializes shared files; native OCR work can be batched later.
    rows=[extract(x,a.ocr) for x in targets]
    publish_bundle({'extracted/logs/extraction_summary.json':json_bytes(rows)})
    print('Extracted',len(rows),'source/config bound PDFs')
if __name__=='__main__':main()
