# src/core/techniques/use_short_operators.py
import re


def use_short_operators(text: str) -> str:
    text = text.replace("==", "≡").replace("!=", "≠")
    text = text.replace(" and ", "∧").replace(" or ", "∨")
    text = re.sub(r'\band\b', '∧', text)
    text = re.sub(r'\bor\b', '∨', text)
    return text
