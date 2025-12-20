# src/core/techniques/replace_booleans.py
def replace_booleans(text: str) -> str:
    text = text.replace("True", "1").replace("False", "0").replace("None", "~")
    return text
