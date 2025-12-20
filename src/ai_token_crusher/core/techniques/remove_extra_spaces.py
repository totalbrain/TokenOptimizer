# src/core/techniques/remove_extra_spaces.py
import re


def remove_extra_spaces(text: str) -> str:
    text = re.sub(r'[ \t]+', ' ', text)
    return text
