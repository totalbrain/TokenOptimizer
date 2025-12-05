# src/core/techniques/shorten_print.py
import re


def shorten_print(text: str) -> str:
    text = re.sub(r'print\s*\(', 'p(', text)
    return text
