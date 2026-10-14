"""Isolated integration tests: no source or production CSV mutation."""
import copy,csv,hashlib,json,pathlib,shutil,subprocess,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]

def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

class Review1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='pe_review1_tests_');cls.p=pathlib.Path(cls.tmp.name)
        for folder in ('scripts','data','config','handoff'):shutil.copytree(ROOT/folder,cls.p/folder,ignore=shutil.ignore_patterns('ocr_pdf','__pycache__'))
        (cls.p/'sources').symlink_to(ROOT/'sources',target_is_directory=True)
        shutil.copytree(ROOT/'extracted/text',cls.p/'extracted/text')
        (cls.p/'extracted/questions').symlink_to(ROOT/'extracted/questions',target_is_directory=True)
        (cls.p/'extracted/pages').symlink_to(ROOT/'extracted/pages',target_is_directory=True)
        if (ROOT/'extracted/questions_raw').exists():(cls.p/'extracted/questions_raw').symlink_to(ROOT/'extracted/questions_raw',target_is_directory=True)
        shutil.copytree(ROOT/'extracted/corrected',cls.p/'extracted/corrected')
        (cls.p/'extracted/logs').mkdir();cls.base=read(cls.p/'data/questions.csv');cls.cls=read(cls.p/'data/classifications.csv');cls.checks=read(cls.p/'data/verification_records.csv')
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def setUp(self):
        write(self.p/'data/questions.csv',self.base);write(self.p/'data/classifications.csv',self.cls);write(self.p/'data/verification_records.csv',self.checks)
    def run_script(self,name,*args):return subprocess.run([sys.executable,'-B',str(self.p/'scripts'/name),*args],capture_output=True,text=True)
    def inline(self,code):return subprocess.run([sys.executable,'-B','-c',code],cwd=self.p,capture_output=True,text=True)
    def test_authored_columns_survive_both_entrypoints(self):
        rows=copy.deepcopy(self.base);r=rows[0];r['solution_summary']='Sentinel authored solution';r['required_knowledge']='Sentinel knowledge';r['question_summary']='Sentinel authored summary'
        # Curated summary is preserved by making a minimal valid correction fixture.
        cp=self.p/'corrected_test.json';cp.write_text(json.dumps({'source_sha256':r['source_sha256']}));ch=hashlib.sha256(cp.read_bytes()).hexdigest()
        r.update(corrected_content_file='corrected_test.json',corrected_content_sha256=ch,summary_verified='true',summary_status='verified',classification_verified='true')
        fields=list(r)
        for x in rows:
            for k in fields:x.setdefault(k,'')
        write(self.p/'data/questions.csv',rows)
        checks=copy.deepcopy(self.checks)
        import importlib.util
        spec=importlib.util.spec_from_file_location('fixture_common',ROOT/'scripts/common.py');common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)
        for kind in ('summary','classification'):checks.append({'question_id':r['question_id'],'kind':kind,'source_sha256':r['source_sha256'],'content_sha256':ch,'reviewer':'Test fixture only','reviewed_at':'2026-10-08T00:00:00+09:00','status':'verified','evidence':'synthetic isolated test','notes':'','payload_sha256':common.verification_payload_hash(r,kind),'payload_bound_at':'2026-10-08T00:00:00+09:00'})
        write(self.p/'data/verification_records.csv',checks)
        for script in ('build_question_db.py','classify_questions.py'):
            result=self.run_script(script,'--apply');self.assertEqual(result.returncode,0,result.stderr)
        result=read(self.p/'data/questions.csv')[0]
        for k in ('solution_summary','required_knowledge','question_summary','classification_verified','summary_verified'):self.assertEqual(result[k],r[k])
    def test_idempotent_rebuild(self):
        for s in ('build_question_db.py','classify_questions.py'):
            self.assertEqual(self.run_script(s,'--apply').returncode,0)
        before=(self.p/'data/questions.csv').read_bytes()
        for s in ('build_question_db.py','classify_questions.py'):self.assertEqual(self.run_script(s,'--apply').returncode,0)
        self.assertEqual(before,(self.p/'data/questions.csv').read_bytes())
    def test_authored_revision_rejects_stale_hash_preserves_history_and_draft(self):
        batch=json.loads((self.p/'config/authored_batches/S7_007_thermodynamics.json').read_text())
        e=next(x for x in batch['questions'] if x['question_id']=='H29-REG-APPLIED-06')
        old=next(x for x in self.base if x['question_id']==e['question_id'])
        old_path=self.p/old['corrected_content_file'];old_bytes=old_path.read_bytes()
        e.update(stem='Isolated revision fixture',summary='Isolated revision fixture',revision_of_content_sha256='0'*64,revision_of_batch=old['authoring_batch'],revision_reason='Synthetic fixture only: exercise explicit revision guard',independent_solution_note='Initial attempt retained; revised against a separate primary source after answer comparison. Test fixture only.')
        batch.update(batch_id='test_explicit_revision',questions=[e])
        path=self.p/'config/authored_batches/test_revision.json';path.write_text(json.dumps(batch))
        before=(self.p/'data/questions.csv').read_bytes()
        result=self.run_script('publish_authored_batch.py','config/authored_batches/test_revision.json')
        self.assertNotEqual(result.returncode,0);self.assertIn('hash-bound revision',result.stderr)
        self.assertEqual(before,(self.p/'data/questions.csv').read_bytes())
        e['revision_of_content_sha256']=old['corrected_content_sha256'];path.write_text(json.dumps(batch))
        result=self.run_script('publish_authored_batch.py','config/authored_batches/test_revision.json')
        self.assertEqual(result.returncode,0,result.stderr)
        new=next(x for x in read(self.p/'data/questions.csv') if x['question_id']==e['question_id'])
        self.assertNotEqual(new['corrected_content_sha256'],old['corrected_content_sha256'])
        self.assertEqual(old_bytes,old_path.read_bytes())
        self.assertEqual(new['solution_review_status'],'draft_pending_astra')
        records=read(self.p/'data/verification_records.csv')
        self.assertTrue(any(x['question_id']==e['question_id'] and x['kind']=='independent_solution' and x['content_sha256']==new['corrected_content_sha256'] and x['notes']==e['independent_solution_note'] for x in records))
        self.assertTrue(any(x['question_id']==e['question_id'] and x['content_sha256']==old['corrected_content_sha256'] and x['status']=='superseded' for x in records))
        updated=(self.p/'data/questions.csv').read_bytes()
        self.assertEqual(self.run_script('publish_authored_batch.py','config/authored_batches/test_revision.json').returncode,0)
        self.assertEqual(updated,(self.p/'data/questions.csv').read_bytes())
    def test_no_ocr_switch_preserves_cached_text(self):
        text=self.p/'extracted/text/H24/basic.txt';before=text.read_bytes()
        result=self.inline("import sys;sys.path.insert(0,'scripts');import extract_pdf_text as e;e.extract(e.ROOT/'sources/H24/basic.pdf',False)")
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(before,text.read_bytes())
    def test_changed_source_invalidates_reviews_keeps_solution(self):
        rows=copy.deepcopy(self.base);rows[0]['source_sha256']='0'*64;rows[0]['solution_summary']='Keep authored content';write(self.p/'data/questions.csv',rows)
        result=self.run_script('build_question_db.py','--apply');self.assertEqual(result.returncode,0,result.stderr)
        r=read(self.p/'data/questions.csv')[0];self.assertEqual(r['solution_summary'],'Keep authored content');self.assertEqual(r['needs_manual_verification'],'true')
        self.assertTrue(read(self.p/'data/source_change_conflicts.csv'))
    def test_final_rejects_flags_and_labels_only(self):
        result=self.run_script('audit_completeness.py','--final');self.assertNotEqual(result.returncode,0);self.assertIn('not implemented',result.stderr+result.stdout)
    def test_schema_negative_cases(self):
        applied=next(c['id'] for c in json.loads((self.p/'config/concepts.json').read_text())['concepts'] if c['subjects']==['APPLIED'])
        for field,value in [('source_page','0'),('source_page','9999'),('heading_line_index','-1'),('heading_bbox','{"x":2,"y":0,"width":1,"height":1}'),('end_bbox','{}'),('official_group','9'),('answer_kind','all_awarded'),('discipline_id','nonexistent'),('concept_id',applied),('related_question_ids',self.base[0]['question_id']),('related_question_ids','nonexistent'),('status','explained_verified')]:
            rows=copy.deepcopy(self.base);rows[0][field]=value;write(self.p/'data/questions.csv',rows)
            self.assertNotEqual(self.run_script('validate_schema.py').returncode,0,(field,value))
    def test_mismatched_answer_rejected(self):
        rows=copy.deepcopy(self.base);rows[0]['official_answer']='1' if rows[0]['official_answer']!='1' else '2';write(self.p/'data/questions.csv',rows)
        self.assertNotEqual(self.run_script('validate_answers.py').returncode,0)
    def test_duplicate_classification_rejected(self):
        write(self.p/'data/classifications.csv',self.cls+[self.cls[0]])
        self.assertNotEqual(self.run_script('audit_completeness.py').returncode,0)
    def test_heading_deletion_not_fabricated(self):
        path=self.p/'extracted/text/H24/basic.json';before=path.read_bytes();j=json.loads(before)
        r=next(x for x in self.base if x['question_id']=='H24-REG-BASIC-3-2');j['pages'][int(r['source_page'])-1]['lines'][int(r['heading_line_index'])]['text']='Heading removed in isolated fixture';path.write_text(json.dumps(j))
        try:self.assertNotEqual(self.run_script('build_question_db.py','--apply').returncode,0)
        finally:path.write_bytes(before)
    def test_transaction_validation_failure_keeps_old_file(self):
        f=self.p/'data/questions.csv';before=f.read_bytes()
        r=self.inline("import sys;sys.path.insert(0,'scripts');from common import publish_bundle;\ndef fail(paths):raise ValueError('synthetic validation failure')\npublish_bundle({'data/questions.csv':b'corrupt'},fail)")
        self.assertNotEqual(r.returncode,0);self.assertEqual(before,f.read_bytes());self.assertFalse((self.p/'data/publication.lock').exists())
    def test_classification_known_cases(self):
        rows={r['question_id']:r for r in self.base}
        self.assertEqual(rows['H26-REG-BASIC-2-4']['middle_category'],'データ構造・形式言語')
        self.assertEqual(rows['H24-REG-BASIC-3-2']['middle_category'],'振動・運動')
        self.assertEqual(rows['H26-REG-APPLIED-16']['middle_category'],'分析化学')
        self.assertEqual(rows['R02-REG-APPLIED-08']['middle_category'],'材料物性')
        self.assertEqual(rows['R04-REG-APPLIED-30']['middle_category'],'構造地質')
        self.assertEqual(rows['H28-REG-APPLIED-10']['topic'],'同位体の基礎')
        r=self.inline("import sys;sys.path.insert(0,'scripts');from classify_questions import prompt_text;assert '分析' in prompt_text('III-16 以下の①〜⑤の陽イオンの分析を行った。\\n① Na+')")
        self.assertEqual(r.returncode,0,r.stderr)
    def test_candidate_and_full_pipeline_keep_authored_records(self):
        rows=copy.deepcopy(self.base);rows[0]['solution_summary']='Authored pipeline sentinel';write(self.p/'data/questions.csv',rows)
        before=(self.p/'data/questions.csv').read_bytes()
        result=self.run_script('build_all.py','--phase','reviewed')
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(before,(self.p/'data/questions.csv').read_bytes())
        result=self.run_script('build_all.py','--phase','reviewed','--apply')
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(read(self.p/'data/questions.csv')[0]['solution_summary'],'Authored pipeline sentinel')
    def test_cached_source_hash_mismatch_does_not_overwrite(self):
        path=self.p/'extracted/text/H24/basic.json';before=path.read_bytes();j=json.loads(before);j['source_sha256']='0'*64;path.write_text(json.dumps(j));changed=path.read_bytes()
        try:
            r=self.inline("import sys;sys.path.insert(0,'scripts');import extract_pdf_text as e;e.extract(e.ROOT/'sources/H24/basic.pdf',False)")
            self.assertNotEqual(r.returncode,0);self.assertEqual(path.read_bytes(),changed)
        finally:path.write_bytes(before)
    def test_partial_corrected_hash_must_match(self):
        rows=copy.deepcopy(self.base);r=next(x for x in rows if x['correction_status']=='partial');r['corrected_content_sha256']='0'*64;write(self.p/'data/questions.csv',rows)
        self.assertNotEqual(self.run_script('validate_schema.py').returncode,0)
    def test_changed_verified_summary_invalidates_evidence(self):
        rows=copy.deepcopy(self.base);r=next(x for x in rows if x['summary_verified']=='true');r['question_summary']='Changed after source review';write(self.p/'data/questions.csv',rows)
        self.assertNotEqual(self.run_script('validate_schema.py').returncode,0)
    def test_special_answer_evidence_is_versioned_and_set_based(self):
        code="import sys,copy;sys.path.insert(0,'scripts');from common import read_csv;from validate_answers import visual_verified,verify;ans=read_csv('data/answers_official.csv');q=read_csv('data/questions.csv');ev=read_csv('data/answer_verification_records.csv');r=next(r for r in ans if r['question_id']=='R02-REG-BASIC-5-5');assert visual_verified(r,ev);r['official_answer']='3|4';assert visual_verified(r,ev);verify(ans,q);r['source_sha256']='0'*64;assert not visual_verified(r,ev);assert all(not r['official_note'] for r in ans if r['question_id']=='H26-REG-BASIC-5-2')"
        result=self.inline(code);self.assertEqual(result.returncode,0,result.stderr)
    def test_relationship_self_reference_and_stale_source_rejected(self):
        path=self.p/'data/question_relations.csv';before=path.read_bytes()
        try:
            for field,value in [('right_question_id','H24-REG-BASIC-3-2'),('source_hash_left','0'*64)]:
                relations=read(ROOT/'data/question_relations.csv');relations[0][field]=value;write(path,relations)
                self.assertNotEqual(self.run_script('audit_completeness.py').returncode,0)
        finally:path.write_bytes(before)
    def test_relation_publisher_rejects_invalid_type_without_mutation(self):
        paths=['data/questions.csv','data/question_relations.csv']
        before={k:(self.p/k).read_bytes() for k in paths}
        relation=copy.deepcopy(read(self.p/'data/question_relations.csv')[0])
        relation['relation_type']='variant'
        (self.p/'bad_relation.json').write_text(json.dumps({'relations':[relation]}))
        result=self.run_script('publish_reviewed_relations.py','bad_relation.json')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Invalid relationship type',result.stderr)
        for k,b in before.items():self.assertEqual((self.p/k).read_bytes(),b)
    def test_transaction_mid_replacement_failure_rolls_back(self):
        paths=['data/questions.csv','data/classifications.csv'];before={k:(self.p/k).read_bytes() for k in paths}
        r=self.inline("import sys;sys.path.insert(0,'scripts');import common;real=common.os.replace;calls=0\ndef replace(a,b):\n global calls\n calls+=1\n if calls==2:raise OSError('synthetic replacement failure')\n return real(a,b)\ncommon.os.replace=replace\ncommon.publish_bundle({'data/questions.csv':b'changed','data/classifications.csv':b'changed'})")
        self.assertNotEqual(r.returncode,0)
        for k,b in before.items():self.assertEqual((self.p/k).read_bytes(),b)
    def test_actual_input_graph_duplicate_and_reference_rejection(self):
        labels='\n'.join('\\label{'+r['tex_label']+'}' for r in self.base)
        (self.p/'main.tex').write_text('\\input{test_labels.tex}')
        path=self.p/'test_labels.tex';path.write_text(labels)
        self.assertEqual(self.run_script('audit_tex_labels.py').returncode,0)
        path.write_text(labels+'\n\\label{'+self.base[0]['tex_label']+'}\n\\ref{missing_ref}')
        result=self.run_script('audit_tex_labels.py');self.assertNotEqual(result.returncode,0);self.assertIn('unresolved reference',result.stderr);self.assertIn('duplicate',result.stderr)
        (self.p/'main.tex').unlink();path.unlink()
if __name__=='__main__':unittest.main()
