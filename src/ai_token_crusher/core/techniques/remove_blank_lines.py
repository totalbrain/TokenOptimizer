# src/core/techniques/remove_blank_lines.py
def remove_blank_lines(text: str) -> str:
    text = "\n".join(line for line in text.splitlines() if line.strip())
    return text
