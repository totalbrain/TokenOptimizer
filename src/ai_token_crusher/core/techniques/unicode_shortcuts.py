# src/core/techniques/unicode_shortcuts.py
import re


def unicode_shortcuts(text: str) -> str:
    text = re.sub(r'\bnot\s+in\b', '∉', text)
    text = re.sub(r'\bin\b', '∈', text)
    text = text.replace(" not in ", "∉").replace(" in ", "∈")
    return text
