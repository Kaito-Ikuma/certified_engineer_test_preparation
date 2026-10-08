"""Independent heading candidates; reconcile only after observed numbering."""
import argparse,hashlib,json,re
from collections import defaultdict
from common import ROOT,YEARS,SUBJECTS,read_csv,csv_bytes,json_bytes,publish_bundle,norm,qid,year_label,digest

FIELDS='question_id year era_year exam_session subject question_number source_file source_page major_category middle_category minor_category topic subtopic question_type requires_calculation requires_figure requires_law difficulty priority official_answer answer_verified question_summary core_concept required_knowledge solution_summary wrong_choice_summary related_question_ids tex_label tex_file status needs_manual_verification notes astra_review_required source_year_directory source_page_end printed_question_number heading_text heading_line_index heading_bbox boundary_verified question_text_file extraction_method ocr_min_confidence summary_verified answer_kind answer_source_file answer_source_page classification_method classification_confidence classification_verified'.split()

def candidates(subject,line):
    raw=line['text'].strip(); text=norm(raw).replace('一','-')
    if not raw or raw[0] in '①②③④⑤⑥⑦⑧⑨（(' or line['x']>.30: return []
    if subject=='BASIC':
        match=re.match(r'^.{1,4}?\s*-?\s*([1-5])\s*-\s*(\d+)',text)
        if not match: return []
        g,digits=match.groups()
        # A heading may join to numeric prose: I-3-2 + 2次 => I-3-22次.
        return [(f'{g}-{digits[0]}',match.group(0))] if digits[0] in '1234567' else []
    match=re.match(r'^([^\d]{1,4}|[1Il]{1,4})\s*-\s*(\d+)',text)
    if not match:return []
    digits=match.group(2)
    possibilities=[]
    for length in (2,1):
        if len(digits)>=length and 1<=int(digits[:length])<= (15 if subject=='APT' else 35):
            possibilities.append((str(int(digits[:length])), match.group(0)))
    return possibilities

EXTRA='official_group source_sha256 raw_text_sha256 end_line_index end_bbox printed_number_observed printed_number_expected extraction_revision summary_status discipline_id chapter_id concept_id classification_evidence classification_candidates taxonomy_version topic_verified corrected_content_sha256 correction_status'.split()
SOURCE_FIELDS='year era_year exam_session subject question_number source_file source_page source_page_end source_year_directory heading_line_index heading_bbox heading_text end_line_index end_bbox printed_question_number printed_number_observed printed_number_expected question_text_file source_sha256 raw_text_sha256 extraction_method extraction_revision ocr_min_confidence official_answer answer_verified answer_kind answer_source_file answer_source_page'.split()

def observed_locations(subject,flattened,overrides,directory,stem):
    locations=[];audit=[];last=None
    for pos,(page,line_index,line) in enumerate(flattened):
        options=candidates(subject,line);key=f'{directory}/{stem}/{page}/{line_index}';manual=key in overrides
        if manual:options=[(overrides[key]['number'],line['text'])]
        if not options:continue
        values=[(tuple(int(x) for x in n.split('-')),n,h) for n,h in options]
        upcoming=[v for v in values if last is None or v[0]>last]
        # Ordered observed candidates only: official answer numbers are not used.
        selected=upcoming[0] if upcoming else None
        if last is None:
            first=(1,1) if subject=='BASIC' else (1,)
            selected=next((v for v in upcoming if v[0]==first),selected)
        if selected and last:
            next_number=(last[0],last[1]+1) if subject=='BASIC' else (last[0]+1,)
            close=next((v for v in upcoming if v[0]==next_number),None)
            if close:selected=close
            elif subject!='BASIC' and selected[0][0]-last[0]>2 and not manual:selected=None
        if selected:
            last=selected[0];locations.append((selected[1],pos,page,line_index,line,manual))
        audit.append({'source':f'sources/{directory}/{stem}.pdf','page':page,'line_index':line_index,'text':line['text'],'bbox':{k:line[k] for k in ['x','y','width','height']},'options':[n for n,h in options],'selected':selected[1] if selected else None,'reason':'manual_image_override' if manual else 'observed_monotonic' if selected else 'duplicate_or_nonmonotonic'})
    return locations,audit

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    answers={r['question_id']:r for r in read_csv('data/answers_official.csv')};sources={r['path']:r for r in read_csv('data/source_files.csv')}
    old={r['question_id']:r for r in read_csv('data/questions.csv')} if (ROOT/'data/questions.csv').exists() else {}
    overrides=json.loads((ROOT/'config/boundary_overrides.json').read_text());records=[];issues=[];all_audit=[];conflicts=[];files={}
    for directory in YEARS:
        for stem,subject in SUBJECTS.items():
            meta=json.loads((ROOT/'extracted/text'/directory/(stem+'.json')).read_text());flattened=[]
            for page in meta['pages']:
                for ix,line in enumerate(page.get('lines',[])):flattened.append((page['page'],ix,line))
            locations,audit=observed_locations(subject,flattened,overrides,directory,stem);all_audit.extend(audit)
            for i,(number,pos,page,line_index,line,manual) in enumerate(locations):
                question_id=qid(directory,subject,number)
                if question_id not in answers:issues.append({'question_id':question_id,'issue':'extra_observed_heading'});continue
                end=locations[i+1][1] if i+1<len(locations) else len(flattened);body=flattened[pos:end]
                content=[l['text'] for _,_,l in body if not re.search(r'(基礎|適性|応用理学).*[（(][HR]',l['text'])]
                raw='\n'.join(content);raw_hash=hashlib.sha256(raw.encode()).hexdigest();a=answers[question_id];prior=old.get(question_id,{})
                record={k:'' for k in FIELDS+EXTRA};record.update(prior)
                changed=bool(prior and ((prior.get('source_sha256') and prior['source_sha256']!=sources[meta['source']]['sha256']) or (prior.get('raw_text_sha256') and prior['raw_text_sha256']!=raw_hash)))
                # Immutable extraction path; retain original path when byte-identical.
                oldpath=ROOT/prior['question_text_file'] if prior.get('question_text_file') else None
                textpath=prior['question_text_file'] if oldpath and oldpath.exists() and oldpath.read_text()==raw else f'extracted/questions_raw/{question_id}/{raw_hash}.txt'
                if not (ROOT/textpath).exists():files[textpath]=raw
                endpoint=body[-1]
                record.update(official_group=number.split('-')[0] if subject=='BASIC' else '',question_id=question_id,year=directory.replace('_retest',''),era_year=year_label(directory),exam_session='RET' if directory.endswith('_retest') else 'REG',subject=subject,question_number=number,source_file=meta['source'],source_page=str(page),source_page_end=str(endpoint[0]),source_year_directory=directory,
                    official_answer=a['official_answer'],answer_verified=a['answer_verified'],answer_kind=a['answer_kind'],answer_source_file=a['source_file'],answer_source_page=a['source_page'],
                    printed_question_number=line['text'],printed_number_observed=number,printed_number_expected=a['official_number'],heading_text=line['text'],heading_line_index=str(line_index),heading_bbox=json.dumps({k:line[k] for k in ['x','y','width','height']}),
                    end_line_index=str(endpoint[1]),end_bbox=json.dumps({k:endpoint[2][k] for k in ['x','y','width','height']}),question_text_file=textpath,source_sha256=sources[meta['source']]['sha256'],raw_text_sha256=raw_hash,extraction_revision='independent_candidates_v1',extraction_method='ocr_unverified',ocr_min_confidence=str(min(l['confidence'] for _,_,l in body)))
                if not prior:
                    record.update(boundary_verified='true' if manual else 'false',classification_verified='false',summary_verified='false',summary_status='placeholder',tex_label='q:'+question_id.lower(),status='registered_initial',needs_manual_verification='true',astra_review_required='true',correction_status='pending',topic_verified='false')
                record['summary_status']=record.get('summary_status') or 'placeholder';record['correction_status']=record.get('correction_status') or 'pending'
                if changed:
                    conflicts.append({'question_id':question_id,'old_source_sha256':prior.get('source_sha256',''),'new_source_sha256':record['source_sha256'],'old_raw_sha256':prior.get('raw_text_sha256',''),'new_raw_sha256':raw_hash,'action':'preserve_authored_content_invalidate_reviews'})
                    record.update(needs_manual_verification='true',boundary_verified='false',summary_verified='false',classification_verified='false',topic_verified='false',summary_status='stale',correction_status='stale',status='registered_initial')
                records.append(record)
    ids=[r['question_id'] for r in records]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate independently observed heading')
    missing=set(answers)-set(ids)
    issues.extend({'question_id':q,'issue':'heading_not_found'} for q in sorted(missing))
    files.update({'data/db_candidates.csv':csv_bytes(records),'data/source_change_conflicts.csv':csv_bytes(conflicts,'question_id old_source_sha256 new_source_sha256 old_raw_sha256 new_raw_sha256 action'.split()),'extracted/logs/heading_candidates.json':json_bytes(all_audit),'extracted/logs/boundary_missing.json':json_bytes(issues)})
    if args.apply:
        if issues:raise ValueError('Independent heading reconciliation failed: '+str(issues[:20]))
        # Preserve every non-source field; new columns are introduced explicitly.
        files['data/questions.csv']=csv_bytes(records)
    publish_bundle(files);print('Observed',len(records),'issues',len(issues),'source conflicts',len(conflicts),'applied',args.apply)
if __name__=='__main__':main()
