# coding:utf-8
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from common import ROOT
initial={r['question_id']:r for r in json.loads((ROOT/'config/authored_batches/S7_038_independent_answers.json').read_text())['records']}
sel={r['question_id']:r for r in json.loads((ROOT/'extracted/logs/S7_038_employment_selection.json').read_text())['records']}
out=[]
def add(q,stem,cid,labels,knowledge,statements,solution,choices,learning,cites,ambiguity='',law=True):
 r=initial[q];s=sel[q];image='extracted/pages/'+s['source_file'].split('/')[1]+'/aptitude/page_%03d.png'%int(s['source_page'])
 out.append(dict(question_id=q,source_sha256=r['source_sha256'],stem=stem,summary=stem,conditions={'原典確認':'記述の主体・否定・全称・年度・5候補の記号対応を原典画像で確認。','適用時点':q.split('-')[0]+'年度の制度又は指針に沿う。現在の2026-10-12時点の説明は共通理論で別記する。','各記述の判断':statements,'前提':knowledge},choices={str(i):dict(value=v,verdict=t,reason=why) for i,(v,t,why) in enumerate(choices,1)},figures='図なし。組合せ表又は個数の5候補を画像で照合。',ambiguity=ambiguity,evidence=[image],core_concept=stem,required_knowledge=knowledge,solution=solution,answer_reason=solution,independent_answer=r['answer_initial'],independent_solution_note='公式前の初回解答を別ファイルに保存し保持。'+r['reason']+(' 初回の対象業務誤認を一次資料により訂正し、extracted/logs/S7_038_independent_followup.jsonに記録。' if q=='H25-REG-APT-04' else ''),learning_points=learning,theory_references=labels,discipline_id='apt_4',concept_id=cid,cross_concepts=[],classification_reason='環境持続可能性又は安全リスクという暫定分類を原典で見直した。中心は雇用上の権利と事業主の責務、制度の成立要件でありコンプライアンスへ配置する。'+learning,calculation='false',figure='false',law='true' if law else 'false',evaluation=dict(knowledge_novelty='2',reasoning_steps='2',calculation_load='0',figure_reading='0',difficulty='3' if law else '2',difficulty_reason='物理専攻には雇用制度と例外の知識が新規である。主体・全称・時点を切り分け、各記述の真偽から組合せ又は個数へ戻す。'),citations=cites,foundationality='high',transferability='high'))
def combos(rows,correct):
 letters='アイウエオカキ';out=[]
 for row in rows:
  diff=[letters[i] for i,(a,b) in enumerate(zip(row,correct)) if a!=b]
  out.append(('・'.join('○' if a=='O' else '×' for a in row),'適切' if not diff else '不適切','各記述の判断と全て一致する。' if not diff else '記述'+ '・'.join(diff)+'の真偽が逆であり、正しい組合せではない。'))
 return out
def count_choices(values,count,wrong=False):
 return [(str(v),'適切' if v==count else '不適切',('不適切' if wrong else '適切')+'な記述を個別に数えると'+str(count)+'個であり、'+('一致する。' if v==count else 'この個数とは一致しない。')) for v in values]
sexc=['employment_sexual_current','employment_sexual2018'];powerc=['employment_power2012','employment_power_current']
add('H24-REG-APT-03','セクハラの二類型・行為者範囲・派遣労働者の保護を判定する。','workplace_sexual_harassment',['theory:employment:sexual','theory:employment:scope'],
 '均等法の対価型と環境型。派遣元だけでなく派遣先にも防止措置が必要である。行為者は雇用組織内の者に限定されない。',
 {'ア':'○：拒絶による解雇等は対価型。','イ':'○：性的言動で能力発揮が妨げられる例は環境型。','ウ':'○：取引先・顧客・患者・教員学生等も行為者となり得る。','エ':'×：派遣労働者を一律に除外できない。'},
 'ア・イは二つの被害の形、ウは行為者の範囲であり適切である。エの派遣除外が誤りなので○○○×、2である。派遣先で起こる性的言動の防止を、雇用契約が派遣元にあることだけで放棄しない。',combos(['OOOO','OOOX','OOXO','OXOO','XOOO'],'OOOX'),
 '性的言動の被害を処遇上の不利益と環境悪化へ分け、保護対象と加害者範囲を別々に確認する。',sexc+['employment_sexual2006'])
add('H25-REG-APT-03','パワハラの優位性・指導の範囲・六類型を判定する。','workplace_power_harassment',['theory:employment:power','theory:employment:scope'],
 '平成24年WG報告の定義と脚注。顧客等の人格侵害も問題となるが、同じ職場内のパワハラ定義と顧客等からの行為を区別する。',
 {'ア':'○：上下関係以外もあり、顧客等による人格侵害の事実も報告の脚注にある。','イ':'×：専門知識や協力への依存も優位性となる。','ウ':'○：業務上適正な指示への主観的不満だけではパワハラとならない。','エ':'○：身体・精神・隔離・過大・過小・私生活侵害の六類型が挙げられる。'},
 '職位だけが優位性ではない。必要な知識を特定の同僚だけが持つ状況でも相手への依存が生じるため、専門知識を除外するイは×である。ア・ウ・エは○なので○×○○、4である。アの顧客等の例を、当時の職場内定義そのものの拡大と読み替えない。',combos(['OOOO','OOOX','OOXO','OXOO','XOOO'],'OXOO'),
 '肩書でなく抵抗・拒絶の難しさを生む関係に着目し、業務の必要性と態様の相当性を調べる。',powerc)
add('H25-REG-APT-04','労働三法・36協定・産業医・裁量労働の対象業務を区別する。','labor_discretionary_scope',['theory:employment:law','theory:employment:discretion'],
 '平成25年度の専門業務型は19業務。技術士の資格保有を一律に対象業務とする規定はない。個人が研究開発等の対象業務へ従事する場合とは別である。',
 {'ア':'○：労働基準法・労働組合法・労働関係調整法を労働三法と呼ぶ。','イ':'○：36条の時間外・休日労働協定は締結だけでなく届出を要する。','ウ':'○：一定規模の事業場に産業医の選任義務がある。','エ':'×：当時の19業務の列挙に技術士業務はない。'},
 'ア・イ・ウは適切である。エの裁量労働制の説明の前半は制度に対応するが、技術士も19業務に含むという最後の文が誤りである。○○○×、公式5となる。初回は技術士業務を対象と誤認して3と答えたが、当時に近い東京労働局平成26年3月資料の全19業務と説明頁を確認して訂正した。資格名の類似から対象業務を補わない。',combos(['XOOO','OXOO','OOOO','OOXO','OOOX'],'OOOX'),
 '資格を持つ人と法律が列挙する業務を区別し、複合文では最後の一節まで確認する。',['employment_discretion2014','employment_discretion_current','employment_industrial_physician','employment_labor_three','employment_overtime'],ambiguity='公式前の初回3は誤認であり保存する。一次資料で5へ訂正済み初稿。保存した旧資料はH26.3版であり、H25時点との告示版差の最終確認をAstra対象として残す。')
add('H26-REG-APT-05','主観的不満と業務の適正範囲を分けてパワハラを判定する。','workplace_power_harassment',['theory:employment:power'],
 '平成24年WG報告の職場内優位性・適正範囲・苦痛又は環境悪化の条件。通常の指導でも方法が適正範囲を超えれば別の判断となる。',
 {'判断基準':'肩書だけでなく関係、指導内容と態様を確認する。'},
 '業務の適正な範囲内であると明示された指導を、個人が不満に感じただけでパワハラとする4は定義に反する。他の肢は優位性の広がり又は典型的な行為類型に対応する。',
 [('上下以外の人間関係でも優位性がある','適切','部下から上司や同僚間でも抵抗しにくい関係があり得る。'),('暴力・人格否定はパワハラ','適切','身体的・精神的な攻撃に対応する。個別事実に即して判断する。'),('隔離・無視は原則パワハラ','適切','合理性のない排除は人間関係からの切り離しの典型である。'),('適正範囲の指導でも不満があればパワハラ','不適切','適正な指導を主観的不満だけで定義へ含めるのは誤りである。'),('過大・過小要求や個の侵害は該当することがある','適切','これらは報告の類型であり、あり得るという限定とも合う。')],
 '不満を無視することと、法的な該当性を客観条件で調べることを混同しない。',powerc)
add('H27-REG-APT-11','拒絶の意思表示・適正指導・行為者範囲・専門知識の優位性を判定する。','workplace_harassment_judgment',['theory:employment:power','theory:employment:sexual'],
 '性的不利益又は環境悪化と、パワハラの業務上の相当性をそれぞれの枠組みで確認する。明示的に嫌だと言わなかったことは同意の保証ではない。',
 {'ア':'×：意思表示の有無だけに限定しない。','イ':'○：適正範囲の指導は主観的不満だけでパワハラとならない。','ウ':'○：取引先・顧客・患者・教員学生等もセクハラの行為者となり得る。','エ':'×：専門知識も優位性の背景となる。'},
 'アは被害者が拒絶を明示できるとは限らないこと、エは専門知識による依存を除外できないことから×である。イ・ウは○なので×○○×、5である。',combos(['XXOX','OOOX','XOOO','OXXO','XOOX'],'XOOX'),
 'セクハラとパワハラの判断条件を切り分け、相手の沈黙を同意として扱わない。',powerc+sexc)
def harassment_count(q,new=False):
 st=({'ア':'○：外部の顧客等も行為者となり得る。','イ':'×：意思表示の有無だけで決めない。','ウ':'○：人前の人格否定は精神的攻撃となり得る。','エ':'○：客観的に適正な指導はパワハラではない。','オ':'×：妊婦への適切な負担軽減の相談は直ちにハラスメントではない。','カ':'○：性的指向・性自認に関する言動はハラスメントとなり得る。','キ':'×：専門知識による優位性も含む。'} if new else {'ア':'×：明示拒絶だけに限定しない。','イ':'○：人前の人格否定は精神的攻撃となり得る。','ウ':'○：適正指導への不満だけではパワハラではない。','エ':'○：顧客等も行為者となり得る。','オ':'○：妊婦本人に相談する負担調整は直ちにハラスメントではない。','カ':'×：専門知識による優位性を含む。','キ':'○：性的指向・性自認を理由とする言動はハラスメントとなり得る。'})
 n=4 if new else 5
 add(q,'複数のハラスメント判断を主体・目的・態様ごとに判定して適切数を数える。','workplace_harassment_judgment',['theory:employment:power','theory:employment:maternity','theory:employment:scope'],
 '一般のハラスメントという語と、各法のパワハラ・セクハラ・妊娠等ハラスメントの定義を分ける。本人への配慮の相談を、一方的な不利益変更と混同しない。',st,
 ('ア・ウ・エ・カが○、イ・オ・キが×。適切4個で4である。' if new else 'イ・ウ・エ・オ・キが○、ア・カが×。適切5個で5である。')+'行為者範囲は広いが、全ての法定類型に同じ範囲と条件が適用されるわけではない。人格否定と専門知識への依存、妊婦に相談する調整と不利益な排除を区別する。',count_choices([1,2,3,4,5],n),
 '七つの記述の真偽を先に固定し、最後に正しい記述だけを数える。',powerc+sexc+['employment_sexual2018'],ambiguity='原典はハラスメントを広い語で記述する。客観的な適正指導の除外はパワハラの枠組みであり、全ての性的言動等に無条件で適用するものではない。周囲の就業環境への影響も個別条件を要する。')
harassment_count('H29-REG-APT-04');harassment_count('R04-REG-APT-05',True)
add('H29-REG-APT-05','労働時間・管理監督者・柔軟勤務・健康管理の範囲を判定する。','labor_worktime_management',['theory:employment:worktime','theory:employment:flex'],
 '指揮命令下の時間は労働時間である。管理監督者も深夜割増賃金と年次有給休暇が一律除外されるわけではない。平成29年度のフレックス清算期間上限は1か月。',
 {'ア':'×：使用者の指示で業務に必要な学習をする時間も労働時間。','イ':'×：管理監督者にも深夜割増と年休を適用。','ウ':'○：総時間内で始業終業を労働者が決めるのがフレックス。','エ':'○：長時間労働へのメンタルヘルス体制は重要。','オ':'○：働き方自体を見直す経営側の取組が必要。'},
 'ア・イは対象からの過大な除外なので×、ウ・エ・オは○である。××○○○、3となる。部長等の呼称だけで管理監督者性は決まらず、フレックスでも時間把握の責務は残る。',combos(['OOOXO','OXXOO','XXOOO','XXOOX','XO XOO'.replace(' ','')],'XXOOO'),
 '勤務場所や肩書ではなく指揮命令・実態・制度の適用範囲を確認する。',['employment_hours2017','employment_manager2008','employment_reform2018','employment_worklife2010'])
add('H30-REG-APT-12','仕事と生活の調和へ向けた十の業務改善策の目的を判定する。','worklife_process_improvement',['theory:employment:worklife'],
 '内閣府の十の実践に対応する組織的な業務改善を考える。効率化は労働時間を減らす目的であり、同じ時間へ仕事を詰め込むことだけではない。',
 dict(zip('アイウエオカキクケコ',['会議の目的と終点を明確にする。','不要資料を減らす。','探索時間を減らす。','属人化を減らす。','負荷と時間を把握する。','分担を整える。','相互支援の余地を増す。','予定を共有する。','集中と対話の時間を確保する。','改善策を共有する。'])),
 '十の記述はそれぞれ会議・資料・探索・属人化・時間把握・分担・応援・共有・集中・改善共有という業務改善に対応する。不適切0個、1である。アの必ず結論は会議の到達点を確認する趣旨であり、不十分な証拠で技術判断を強行する指示と読まない。',count_choices([0,1,2,3,4],0,True),
 '残業を個人の努力だけで減らすのではなく、仕事の流れと組織の負荷分担を見直す。',['employment_worklife2010'],ambiguity='会議で必ず結論を出すは啓発上の表現である。安全判断の証拠不足や追加検証が必要な場合まで、無理に結論を確定させる一般則ではない。',law=False)
add('R01-REG-APT-12','同性セクハラ・事業主の措置・産前産後休業の条件を判定する。','labor_maternity_protection',['theory:employment:sexual','theory:employment:maternity'],
 '産前休業は本人の請求、産後は原則8週間の就業禁止。産後6週間経過後の本人請求と医師の認定には例外がある。雇用形態で産休対象を限定しない。',
 {'ア':'○：同性間もセクハラに該当し得る。','イ':'×：防止措置は単なる努力目標ではない。','ウ':'×：有期の契約社員や派遣等も産休の対象。','エ':'×：個々の事情に応じた必要な措置を禁じる規定ではない。','オ':'×：産前休業は請求が条件であり両方必ずという命題は誤る。'},
 'アだけ○、イからオは×なので○××××、1である。産休と育児休業は根拠法と条件が異なる。事業主による措置義務は個別配慮を禁じる意味ではなく、本人の状況と法定保護を両立させる必要がある。',combos(['OXXXX','XOXXO','OXOOO','XXOXX','OOXOO'],'OXXXX'),
 '義務か努力か、産前か産後か、産休か育休かという制度の境界を読み分ける。',sexc+['employment_sexual2018','employment_maternity_current','employment_maternity2014'])
add('R02-REG-APT-13','テレワークでも残る労働時間把握と中抜け・移動作業の扱いを判定する。','labor_telework_time',['theory:employment:telework'],
 '雇用型テレワークの平成30年指針。自由利用と指揮命令を区別する。時間単位年休には労使協定と本人の請求等の制度要件があり、使用者が勝手に年休扱いできるわけではない。',
 {'ア':'○：可能な勤務場所を明示することが望ましい。','イ':'×：自己管理でも使用者の把握責務は消えない。','ウ':'○：自由な中抜けは休憩や制度要件を満たす時間単位年休として扱える。','エ':'○：移動中でも指揮命令下で作業すれば労働時間。'},
 '場所の柔軟性は法令の適用除外を意味しない。労働時間の把握責務がないとするイだけ×なので○×○○、4である。自由な休止をしている時間と、移動しながら命令された作業を行う時間は異なる。令和2年版厚生労働白書の平成30年指針概要でも四点を確認した。',combos(['OOOO','OOOX','OOXO','OXOO','XOOO'],'OXOO'),
 '事業場の外という場所ではなく、時間の自由利用と指揮命令下の作業の有無から区別する。',['employment_telework2020','employment_telework_current'],ambiguity='ウの時間単位年休について、原典は労使協定・本人請求等の成立要件を省略する。自由な中抜けだけで年休へ一方的に振替えられるという意味にはしない。')
add('R06-REG-APT-10','セクハラの意思表示と行為者範囲、パワハラの指導・優位性を判定する。','workplace_harassment_judgment',['theory:employment:power','theory:employment:sexual'],
 '各行為をセクハラ又はパワハラの該当条件へ対応させる。人格否定は正当な業務上の指導という名称だけで許容されない。',
 {'ア':'×：明示拒絶のある場合だけに限定しない。','イ':'○：人格を否定する公然の叱責はパワハラとなり得る。','ウ':'○：患者家族・学校生徒等もセクハラの行為者となり得る。','エ':'○：適正範囲内の指導は不満だけでパワハラではない。','オ':'×：専門知識による優位性も含む。'},
 'ア・オは×、イ・ウ・エは○なので×○○○×、3である。拒絶が難しい関係、業務に必要な知識への依存、本人と周囲の環境を個別に評価する。',combos(['OXXXO','XOOXX','XOOOX','XXOOO','OXXOX'],'XOOOX'),
 '主語と行為の種類を固定して判断し、真偽の並びを原典の表へ戻す。',powerc+sexc)
add('R07-REG-APT-15','働き方改革の年休取得・残業上限・割増・フレックスを対応させる。','labor_reform_provisions',['theory:employment:reform','theory:employment:flex'],
 '令和7年度の制度。年5日取得の確保、法定上限、月60時間超の割増、フレックス清算上限3か月を区別する。年休の本人取得・計画付与分は指定日数へ算入する。',
 {'ア':'○：年10日以上付与される者の年5日取得を確保する仕組み。本人取得・計画付与との調整を要する。','イ':'×：使用者が指示で法定上限を緩和できない。','ウ':'×：月60時間超を10時間ごとに代休1日とする制度ではない。','エ':'○：清算期間上限が1か月から3か月に延長された。'},
 'ア・エは○、イ・ウは×なので○××○、2である。月60時間超は割増賃金率が5割以上となる仕組みであり、代替休暇を設ける場合も労使協定と換算の条件がある。休日勤務の代休と混同しない。',combos(['XXOO','OXXO','OOXX','XOOX','OOOO'],'OXXO'),
 '施策名と数値だけでなく、対象者・義務主体・上限・代替の成立条件を組み合わせる。',['employment_reform2018','employment_paidleave','employment_alternative2008'],ambiguity='アの使用者による時季指定は、本人請求や計画付与の取得済み日数を差し引く。原典の年5日指定という説明を、全員に追加で5日指定する意味へ拡張しない。')
assert len(out)==13
p=ROOT/'config/authored_batches/S7_038_employment.json';assert not p.exists();p.write_text(json.dumps(dict(batch_id='S7_038_employment',reference_date='2026-10-12',questions=out),ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(out),'partial',sum(bool(q['ambiguity']) for q in out))
