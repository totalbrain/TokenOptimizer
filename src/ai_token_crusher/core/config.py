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

PROFILES = {
    "safe": {**OPTIONS_DEFAULT, "single_line_mode": False, "use_short_operators": False, "unicode_shortcuts": False, "replace_booleans": False},
    "aggressive": OPTIONS_DEFAULT.copy(),
    "ECH": {k: True for k in OPTIONS_DEFAULT.keys()},
}
