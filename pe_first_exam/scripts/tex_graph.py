"""Follow local literal TeX inputs from the actual compilation entry point."""
import re
from common import ROOT

def input_graph(entry='main.tex'):
    files={};errors=[];active=set()
    def visit(name):
        path=ROOT/name
        if path.suffix!='.tex':path=path.with_suffix('.tex')
        if not path.resolve().is_relative_to(ROOT.resolve()):
            errors.append('TeX input outside project: '+name);return
        key=str(path.relative_to(ROOT))
        if key in active:errors.append('cyclic TeX input: '+key);return
        if key in files:return
        if not path.exists():errors.append('missing TeX input: '+key);return
        text=path.read_text();text=re.sub(r'(?<!\\)%[^\n]*','',text)
        files[key]=text;active.add(key)
        for child in re.findall(r'\\(?:input|include)\{([^}]+)\}',text):visit(child)
        active.remove(key)
    visit(entry)
    return files,errors
