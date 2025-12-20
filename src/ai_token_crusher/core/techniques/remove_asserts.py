# src/ai_token_crusher/core/techniques/remove_asserts.py
import re

def remove_asserts(text: str) -> str:
    # Remove assert statements (safe in production)
    text = re.sub(r'^assert .*$\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r',\s*assert .*', '', text)  # در صورت inline
    return text