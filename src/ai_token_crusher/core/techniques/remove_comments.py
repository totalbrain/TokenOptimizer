# src/ai_token_crusher/core/techniques/remove_comments.py
import re

def remove_comments(text: str) -> str:
    # Remove single-line comments
    text = re.sub(r'#.*', '', text)
    
    # Remove triple-quoted strings (multi-line comments / docstrings in code)
    text = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', '', text,	flags=re.DOTALL)
    
    return text