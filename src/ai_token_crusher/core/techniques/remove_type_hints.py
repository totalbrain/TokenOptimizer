# src/core/techniques/remove_type_hints.py
import re


def remove_type_hints(text: str) -> str:
    text = re.sub(r':\s*[^=\n\->]+', '', text)
    text = re.sub(r'->\s*[^:\n]+', '', text)
    return text
