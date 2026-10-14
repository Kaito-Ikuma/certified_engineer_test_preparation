"""Independent coordinate-based comparison of ordinary official answer cells."""
import re,subprocess,xml.etree.ElementTree as ET
from collections import defaultdict
from common import ROOT,read_csv,norm,csv_bytes,json_bytes,publish_bundle

def main():
    groups=defaultdict(list)
    for r in read_csv('data/answers_official.csv'):groups[(r['source_file'],r['source_page'])].append(r)
    results=[];fail=[]
    for (source,page),rows in groups.items():
        raw=subprocess.run(['pdftotext','-f',page,'-l',page,'-bbox',str(ROOT/source),'-'],capture_output=True,text=True,check=True).stdout
        root=ET.fromstring(raw);words=[]
        for e in root.iter():
            if e.tag.endswith('word'):words.append({'text':norm(e.text or ''),'x':float(e.attrib['xMin']),'right':float(e.attrib['xMax']),'y':float(e.attrib['yMin'])})
        matched=[]
        for r in rows:
            # Separate reader: match a full number token, then nearest right cell
            # at the same y coordinate, without using the stored source_line.
            token=re.sub(r'\s+','',norm(r['official_number']))
            hits=[w for w in words if re.sub(r'\s+','',w['text'])==token]
            cells=[]
            for h in hits:
                after=sorted([w for w in words if abs(w['y']-h['y'])<2 and w['x']>h['right']],key=lambda w:w['x'])
                if after and re.fullmatch('[1-5]',after[0]['text']):cells.append((h,after[0]))
            if len(cells)==1:
                h,c=cells[0];matched.append((h['x'],h['y'],r,c['text']))
        # First and last ordinary entry in each physical column, all 48 tables.
        columns=defaultdict(list)
        for h,y,r,v in matched:columns[round(h/100)].append((y,r,v))
        chosen={}
        for col,values in columns.items():
            values.sort(key=lambda x:x[0])
            for y,r,v in values[:2]+values[-2:]:chosen[r['question_id']]=(r,v,col,y)
        if len(columns)<(1 if rows[0]['subject']=='APT' else 2):fail.append(source+':'+page+': missing column coverage')
        for q,(r,v,col,y) in chosen.items():
            ok=v==r['official_answer']
            if not ok:fail.append(q+': coordinate mismatch')
            results.append({'question_id':q,'source_file':source,'source_page':page,'source_sha256':r['source_sha256'],'column_bucket':col,'y_pdf_top_origin':y,'coordinate_answer':v,'stored_answer':r['official_answer'],'result':'match' if ok else 'mismatch','method':'bbox_nearest_right_same_row'})
    publish_bundle({'data/answer_coordinate_checks.csv':csv_bytes(results),'extracted/logs/answer_coordinate_checks.json':json_bytes({'pages':len(groups),'ordinary_cells_checked':len(results),'errors':fail,'scope':'Independent coordinate parsing, not visual or solution verification'})})
    print('Coordinate checks',len(results),'tables',len(groups),'errors',len(fail))
    if fail:raise SystemExit('\n'.join(fail))
if __name__=='__main__':main()
