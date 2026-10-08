"""Deterministic LaTeX escaping and references for generated views."""
def esc(s):
    table={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(table.get(c,c) for c in str(s))
def qref(r):return r'\hyperref['+r['tex_label']+']{'+esc(r['question_number'])+'}'
