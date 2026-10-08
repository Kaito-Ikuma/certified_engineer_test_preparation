"""Generate classification candidates; explicit apply preserves curated columns."""
import argparse
import json
import re
import unicodedata
from common import ROOT,read_csv,csv_bytes,json_bytes,publish_bundle,digest

CLASS_FIELDS='major_category middle_category minor_category topic subtopic core_concept tex_file classification_method classification_confidence classification_verified discipline_id chapter_id concept_id classification_evidence classification_candidates taxonomy_version topic_verified'.split()

def prompt_text(raw):
    # Only a line-leading option marker starts the choices. Inline ①〜⑤ is prose.
    lines=[]
    for line in raw.splitlines():
        if re.match(r'^\s*[①②③④⑤](?!\s*[〜～~ー-]\s*[①②③④⑤])',line):break
        lines.append(line)
    return unicodedata.normalize('NFKC','\n'.join(lines))

def classify(row, rules, taxonomy, concepts, overrides):
    raw=(ROOT/row['question_text_file']).read_text();text=unicodedata.normalize('NFKC',raw);prompt=prompt_text(raw)
    subject=row['subject'];matches=[];forced=None;method='keyword_rules_initial';scope_used='prompt'
    if subject=='BASIC':
        g=int(row['question_number'].split('-')[0]);major=rules['basic_major'][g-1];file='chapters/basic/'+rules['basic_stems'][g-1]+'.tex'
        pool=[(title,pat) for title,pat in rules['basic_rules'][str(g)]]
        for scope in (prompt,text):
            matches=[(title,re.search(pat,scope).group()) for title,pat in pool if re.search(pat,scope)]
            if matches:
                middle,evidence=matches[0];scope_used='prompt' if scope==prompt else 'choices';break
        else:middle=major+'（横断・詳細要確認）';evidence='公式群のみ';scope_used='unknown'
    elif subject=='APT':
        matches=[(title,re.search(pat,prompt).group(),stem) for title,stem,pat in rules['apt'] if re.search(pat,prompt)]
        if matches:major,evidence,stem=matches[0];middle=major;file='chapters/aptitude/'+stem+'.tex'
        else:major=middle='技術者倫理・意思決定';file='chapters/aptitude/02_engineering_ethics.tex';evidence='未確定';scope_used='unknown'
    else:
        applied={x[0]:x for x in rules['applied']}
        if '同位体' in prompt and re.search(r'SMOW|VSMOW|同位体.*標準|水素.*酸素|酸素.*水素|天然の水|δ',text):
            forced=('earth_isotope','同位体の自然試料文脈')
        if not forced:
            for key,pat in rules['title_rules']:
                m=re.search(pat,prompt)
                if m:forced=(key,m.group());break
        for scope in (prompt,text):
            matches=[(key,re.search(pat,scope).group(),re.search(pat,scope).start()) for key,ma,mi,st,pat in rules['applied'] if re.search(pat,scope)]
            if forced or matches:
                if forced:key,evidence=forced
                else:key,evidence,_=min(matches,key=lambda x:x[2])
                _,major,middle,stem,_=applied[key];file='chapters/applied_science/'+stem+'.tex'
                scope_used='prompt' if scope==prompt else 'choices';break
        else:raise ValueError('No candidate classification: '+row['question_id'])
    override=overrides.get(row['question_id'])
    if override:major,middle,file,evidence=override['major'],override['middle'],override['file'],override['evidence'];method='manual_content_review'
    cat=next((t for t in taxonomy if (t['subject'],t['major'],t['middle'],t['file'])==(subject,major,middle,file)),None)
    if not cat:raise ValueError('Unregistered category: '+row['question_id']+'/'+middle)
    # Retain competing cues as evidence; medium is not content verification.
    alternatives=sorted(set(x[0] for x in matches));tags=[]
    tag_scope=prompt if prompt.strip() else text
    for c in concepts:
        if subject in c['subjects'] and (not c['disciplines'] or cat['id'] in c['disciplines']):
            m=re.search(c['pattern'],tag_scope)
            if m:tags.append((c,m.group()))
    # Broad concept with no unique evidence stays unknown, never fabricated.
    primary=tags[0][0] if tags else None
    result=dict(row)
    result.update(major_category=major,middle_category=middle,minor_category=primary['label'] if primary else '未確定',
        topic=primary['label'] if primary else '未確定',subtopic='',core_concept=middle,tex_file=file,
        classification_method=method,classification_confidence='low' if scope_used!='prompt' else 'medium',
        classification_verified='false',discipline_id=cat['id'],chapter_id=file.removeprefix('chapters/').removesuffix('.tex'),
        concept_id=primary['id'] if primary else '',classification_evidence=evidence,
        classification_candidates=json.dumps(alternatives,ensure_ascii=False),taxonomy_version='1.0-review1',topic_verified='false')
    if row.get('summary_verified')!='true' and row.get('summary_status') in ('','placeholder',None):
        result['question_summary']=middle+'を扱う索引用仮要約。';result['summary_status']='placeholder'
    if row.get('correction_status')!='verified' and row.get('summary_verified')!='true':
        if '組合せ' in prompt or '組み合わせ' in prompt:kind='組合せ選択'
        elif re.search('不適切|誤って|誤り',prompt):kind='誤り選択'
        elif re.search('最も近い|求め|計算|値として|大きさは',prompt):kind='数値・計算選択'
        else:kind='正しい記述・用語選択'
        result.update(question_type=kind,requires_calculation='true' if kind=='数値・計算選択' else 'unknown',
            requires_figure='true' if re.search('図|グラフ|真理値表|下表',prompt) else 'unknown',
            requires_law='true' if re.search('法第|法律|法令|責任法|保護法|技術士法|基本法',text) else 'unknown')
    return result,tags

def classification_view(rows):
    keys='question_id major_category middle_category minor_category topic tex_file discipline_id chapter_id concept_id classification_method classification_evidence classification_confidence classification_verified taxonomy_version'.split()
    return [{k:r.get(k,'') for k in keys} for r in rows]

def main():
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
    rules=json.loads((ROOT/'config/classification_rules.json').read_text());taxonomy=json.loads((ROOT/'config/taxonomy.json').read_text())['categories'];concepts=json.loads((ROOT/'config/concepts.json').read_text())['concepts'];over=json.loads((ROOT/'config/classification_overrides.json').read_text())
    old=read_csv('data/questions.csv');candidates=[];final=[];changes=[];topics=[]
    for row in old:
        candidate,tags=classify(row,rules,taxonomy,concepts,over);candidates.append(candidate)
        if row.get('classification_verified')=='true':
            merged=dict(candidate)
            for key in CLASS_FIELDS:merged[key]=row.get(key,'')
        else:merged=candidate
        final.append(merged)
        delta=[k for k in CLASS_FIELDS if row.get(k,'')!=merged.get(k,'')]
        if delta:changes.append({'question_id':row['question_id'],'fields':'|'.join(delta),'old_major':row['major_category'],'old_middle':row['middle_category'],'old_topic':row['topic'],'new_major':merged['major_category'],'new_middle':merged['middle_category'],'new_topic':merged['topic'],'evidence':merged['classification_evidence'],'source_file':row['source_file'],'source_page':row['source_page']})
        if row.get('classification_verified')=='true':continue
        for c,e in tags:topics.append({'question_id':row['question_id'],'concept_id':c['id'],'role':'primary' if c['id']==merged['concept_id'] else 'cross_reference','evidence':e,'status':'candidate','source_sha256':row.get('source_sha256','')})
    # Preserve all approved topic relations, including user-added cross-references.
    if (ROOT/'data/question_topics.csv').exists():
        topics.extend(r for r in read_csv('data/question_topics.csv') if r['status']=='verified' or next(x for x in old if x['question_id']==r['question_id']).get('classification_verified')=='true')
    dedup={(r['question_id'],r['concept_id']):r for r in topics};topics=list(dedup.values())
    files={'data/classification_candidates.csv':csv_bytes(candidates),'data/classification_changes.csv':csv_bytes(changes, 'question_id fields old_major old_middle old_topic new_major new_middle new_topic evidence source_file source_page'.split())}
    if a.apply:
        from validate_schema import validate_rows
        validate_rows(final)
        files.update({'data/questions.csv':csv_bytes(final),'data/classifications.csv':csv_bytes(classification_view(final)),
            'data/question_topics.csv':csv_bytes(topics,'question_id concept_id role evidence status source_sha256'.split())})
    publish_bundle(files);print('classification candidates',len(candidates),'changes',len(changes),'applied',a.apply)
if __name__=='__main__':main()
