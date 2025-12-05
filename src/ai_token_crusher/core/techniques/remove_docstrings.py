# src/core/techniques/remove_docstrings.py
import re


def remove_docstrings(text: str) -> str:
    text = re.sub(r'^[\r\n\s]*("""|\'\'\').*?\1', '', text, count=1, flags=re.DOTALL)
    return text
