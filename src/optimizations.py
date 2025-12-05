# src/optimizations.py
import re

def apply_optimizations(options, text):
    if options["remove_comments"].get():
        text = re.sub(r'#.*', '', text)
        text = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', '', text)
    if options["remove_docstrings"].get():
        text = re.sub(r'^[\r\n\s]*("""|\'\'\').*?\1', '', text, count=1, flags=re.DOTALL)
    if options["remove_blank_lines"].get():
        text = "\n".join(line for line in text.splitlines() if line.strip())
    if options["remove_extra_spaces"].get():
        text = re.sub(r'[ \t]+', ' ', text)
    if options["single_line_mode"].get():
        text = text.replace("\n", "⏎")
    if options["shorten_keywords"].get():
        rep = {"def ": "d ", "return ": "r ", "import ": "i ", "from ": "f ", "as ": "a ", "if ": "if", "class ": "c ", "lambda ": "λ "}
        for k, v in rep.items():
            text = text.replace(k, v)
    if options["replace_booleans"].get():
        text = text.replace("True", "1").replace("False", "0").replace("None", "~")
    if options["use_short_operators"].get():
        text = text.replace("==", "≡").replace("!=", "≠").replace(" and ", "∧").replace(" or ", "∨")
    if options["remove_type_hints"].get():
        text = re.sub(r':\s*[^=\n\->]+', '', text)
        text = re.sub(r'->\s*[^:\n]+', '', text)
    if options["minify_structures"].get():
        text = re.sub(r',\s+', ',', text)
        text = re.sub(r':\s+', ':', text)
    if options["unicode_shortcuts"].get():
        text = text.replace(" in ", "∈").replace(" not in ", "∉")
    if options["shorten_print"].get():
        text = re.sub(r'print\s*\(', 'p(', text)
    return text.strip() + "\n"