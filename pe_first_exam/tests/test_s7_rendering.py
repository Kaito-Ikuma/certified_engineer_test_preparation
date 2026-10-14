"""Regression checks for the actual authoring/rendering failures seen in S7."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import ROOT
from tex_common import math_prose

class S7Rendering(unittest.TestCase):
 def test_mathematical_prose_is_not_rendered_as_source_code(self):
  text=r'切捨ては \(\lfloor16x\rfloor/16\)。'
  self.assertIn(r'\(\lfloor16x\rfloor/16\)',math_prose(text))
  self.assertEqual(r'\(x_{\xi}y_{\eta}\quad x_{\eta}y_{\xi}\)',math_prose(r'\(x_{\xi}y_{\eta}\quad x_{\eta}y_{\xi}\)'))
  self.assertEqual(r'\(\mathcal E=-\partial\Phi/\partial t, E=\sigma/\varepsilon_0, \hat r\)',math_prose(r'\(\mathcal E=-\partial\Phi/\partial t, E=\sigma/\varepsilon_0, \hat r\)'))
  self.assertEqual(r"\(A^{\ast}=T,\ 5'\to3'\)",math_prose(r"\(A^{\ast}=T,\ 5'\to3'\)"))
  self.assertEqual(r'\(101+X\equiv0\pmod{10}\)',math_prose(r'\(101+X\equiv0\pmod{10}\)'))
  self.assertEqual(r'\(\mathrm{CaCO_3}\rightleftharpoons\mathrm{Ca^{2+}}+\mathrm{CO_3^{2-}}\)',math_prose(r'\(\mathrm{CaCO_3}\rightleftharpoons\mathrm{Ca^{2+}}+\mathrm{CO_3^{2-}}\)'))
  self.assertEqual(r'\(\lambda\propto1/m\)',math_prose(r'\(\lambda\propto1/m\)'))
  self.assertEqual(r'\(C^\prime=-9/(1+x)^2+1,\ C^{\prime\prime}>0\)',math_prose(r'\(C^\prime=-9/(1+x)^2+1,\ C^{\prime\prime}>0\)'))
  self.assertEqual(r'\(R\sim U[18,23],\ S\sim U[10,20]\)',math_prose(r'\(R\sim U[18,23],\ S\sim U[10,20]\)'))
  self.assertEqual(r'\({3\choose2}r^2(1-r)+r^3\)',math_prose(r'\({3\choose2}r^2(1-r)+r^3\)'))
  self.assertEqual(r'\(\bar X=(X_1+\cdots+X_n)/n\)',math_prose(r'\(\bar X=(X_1+\cdots+X_n)/n\)'))
  with self.assertRaises(ValueError):math_prose(r'\(\input{outside}\)')

 def test_missing_digit_glyphs_use_text_scripts(self):
  rendered=math_prose('2⁻¹²⁶と(0.101)₂、aᵢ')
  self.assertNotIn('⁷',math_prose('10⁷'))
  self.assertIn(r'\textsuperscript{-126}',rendered)
  self.assertIn(r'\textsubscript{2}',rendered)
  self.assertIn(r'\textsubscript{i}',rendered)
  self.assertIn(r"f\ensuremath{'''}",math_prose('f‴'))

 def test_real_generated_theory_reference_has_no_carriage_return(self):
  p=ROOT/'generated/questions/aptitude/01_engineer_act.tex'
  content=p.read_bytes()
  self.assertNotIn(b'\r',content)
  self.assertIn(rb'\ref*{theory:engineer_act:competency}',content)

 def test_combination_options_have_their_statement_context(self):
  text=(ROOT/'generated/questions/aptitude/06_research_information_ethics.tex').read_text()
  self.assertIn('確認した条件・記述（独自要約）',text)
  self.assertIn('水曜日に許可された有償兼業',text)
  self.assertIn('個人の資金と労力で研究・公表するなら',text)
  self.assertIn('共著者は自分に関係した部分だけへ責任',text)

if __name__=='__main__':unittest.main()
