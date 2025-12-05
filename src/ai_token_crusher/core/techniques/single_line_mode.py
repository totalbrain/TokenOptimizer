# src/core/techniques/single_line_mode.py
def single_line_mode(text: str) -> str:
    text = text.replace("\n", "⏎")
    return text
