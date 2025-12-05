# src/core/techniques/minify_structures.py
import re


def minify_structures(text: str) -> str:
    text = re.sub(r',\s+', ',', text)
    text = re.sub(r':\s+', ':', text)
    return text
