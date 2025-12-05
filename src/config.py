# src/config.py - Only pure data, no Tkinter variables
import tkinter as tk  # فقط برای type hint و استفاده در جاهای دیگه

# Default option states (will be converted to BooleanVar in app.py)
OPTIONS_DEFAULT = {
    "remove_comments": True,
    "remove_docstrings": True,
    "remove_blank_lines": True,
    "remove_extra_spaces": True,
    "single_line_mode": True,
    "shorten_keywords": True,
    "replace_booleans": True,
    "use_short_operators": True,
    "remove_type_hints": True,
    "minify_structures": True,
    "unicode_shortcuts": True,
    "shorten_print": True,
    "remove_asserts": True,
    "remove_pass": True,
}

# Pure theme data (no Tkinter objects)
THEMES = {
    "dark": {
        "bg": "#0d1117",
        "frame_bg": "#161b22",
        "text": "#c9d1d9",
        "text_secondary": "#8b949e",
        "text_bright": "#f0f6fc",
        "accent": "#58a6ff",
        "accent_secondary": "#79c0ff",
        "select_bg": "#21262d",
        "input_bg": "#0d1117",
        "input_fg": "#c9d1d9",
        "output_fg": "#79c0ff",
    },
    "light": {
        "bg": "#ffffff",
        "frame_bg": "#f6f8fa",
        "text": "#24292f",
        "text_secondary": "#57606a",
        "text_bright": "#1f2328",
        "accent": "#0969da",
        "accent_secondary": "#0550ae",
        "select_bg": "#ddf4ff",
        "input_bg": "#ffffff",
        "input_fg": "#24292f",
        "output_fg": "#0550ae",
    }
}

# Footer links
LINKS = [
    ("GitHub", "https://github.com/totalbrain/TokenOptimizer"),
    ("Roadmap", "https://github.com/users/totalbrain/projects/1")
]