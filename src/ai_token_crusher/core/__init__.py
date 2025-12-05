from .engine import OptimizationEngine
from .config import OPTIONS_DEFAULT, PROFILES
from .models import OptimizationResult

# تکنیک‌ها رو بعداً اضافه می‌کنیم
def create_engine() -> OptimizationEngine:
    # به جای import * از import صریح استفاده کن
    from .techniques.remove_comments import remove_comments
    from .techniques.remove_docstrings import remove_docstrings
    from .techniques.remove_blank_lines import remove_blank_lines
    from .techniques.remove_extra_spaces import remove_extra_spaces
    from .techniques.single_line_mode import single_line_mode
    from .techniques.shorten_keywords import shorten_keywords
    from .techniques.replace_booleans import replace_booleans
    from .techniques.use_short_operators import use_short_operators
    from .techniques.remove_type_hints import remove_type_hints
    from .techniques.minify_structures import minify_structures
    from .techniques.unicode_shortcuts import unicode_shortcuts
    from .techniques.shorten_print import shorten_print
    from .techniques.remove_asserts import remove_asserts
    from .techniques.remove_pass import remove_pass
    engine = OptimizationEngine()
    engine.register("remove_comments", remove_comments)
    engine.register("remove_docstrings", remove_docstrings)
    engine.register("remove_blank_lines", remove_blank_lines)
    engine.register("remove_extra_spaces", remove_extra_spaces)
    engine.register("single_line_mode", single_line_mode)
    engine.register("shorten_keywords", shorten_keywords)
    engine.register("replace_booleans", replace_booleans)
    engine.register("use_short_operators", use_short_operators)
    engine.register("remove_type_hints", remove_type_hints)
    engine.register("minify_structures", minify_structures)
    engine.register("unicode_shortcuts", unicode_shortcuts)
    engine.register("shorten_print", shorten_print)
    engine.register("remove_asserts", remove_asserts)
    engine.register("remove_pass", remove_pass)
    return engine
