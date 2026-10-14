"""Deterministic LaTeX escaping and references for generated views."""
def esc(s):
    table={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    table.update({'′':r"\ensuremath{'}",'″':r"\ensuremath{''}",'‴':r"\ensuremath{'''}"})
    return ''.join(table.get(c,c) for c in str(s))
def qref(r):return r'\hyperref['+r['tex_label']+']{'+esc(r['question_number'])+'}'

def math_prose(s):
    """Escape prose, retaining only explicit math and a restricted macro vocabulary."""
    import re
    allowed=set('frac sqrt sin cos tan log ln exp pi omega alpha beta gamma delta epsilon varepsilon eta theta kappa mu nu xi rho sigma tau lambda phi Delta Gamma Omega Theta Phi hat mathcal mathrm mathbf text left right quad cdot times approx simeq le ge gg ll neq pm infty sum int partial vec dot ddot operatorname circ max min ell rm lfloor rfloor overline oplus cap cup setminus land lor neg Rightarrow Leftrightarrow gcd forall exists subseteq ast to equiv pmod rightleftharpoons'.split())
    allowed.update({'propto','prime','sim','choose','bar','cdots'})
    pieces=re.split(r'(\\\(.*?\\\)|\\\[.*?\\\])',str(s),flags=re.S);out=[]
    for p in pieces:
        if p.startswith(('\\(','\\[')):
            unknown=set(re.findall(r'\\([A-Za-z]+)',p))-allowed
            if unknown:raise ValueError('Unsupported math macros: '+str(unknown))
            out.append(p)
        else:
            parts=re.split(r'([⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+|[₀₁₂₃₄₅₆₇₈₉₋₊ᵢ]+)',p)
            trans=str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺','0123456789-+')
            subtrans=str.maketrans('₀₁₂₃₄₅₆₇₈₉₋₊ᵢ','0123456789-+i')
            out.append(''.join(r'\textsuperscript{'+v.translate(trans)+'}' if re.fullmatch(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+',v) else r'\textsubscript{'+v.translate(subtrans)+'}' if re.fullmatch(r'[₀₁₂₃₄₅₆₇₈₉₋₊ᵢ]+',v) else re.sub(r'(?<=[0-9A-Za-z)])=(?=[0-9A-Za-z(])',lambda m:r'=\allowbreak{}',esc(v)) for v in parts))
    return ''.join(out)
