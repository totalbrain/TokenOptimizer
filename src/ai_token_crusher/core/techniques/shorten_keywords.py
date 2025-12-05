# src/core/techniques/shorten_keywords.py
def shorten_keywords(text: str) -> str:
    rep = {
            "def ": "d ", "return ": "r ", "import ": "i ", "from ": "f ", "as ": "a ",
            "if ": "if", "class ": "c ", "lambda ": "λ "
        }
    for k, v in rep.items():
        text = text.replace(k, v)
    return text
