# tests/test_optimizations.py
import tkinter as tk
import pytest
from src.optimizations import apply_optimizations
from src.config import OPTIONS_DEFAULT


@pytest.fixture
def opts():
    """همه گزینه‌ها خاموش — برای تست کاملاً ایزوله"""
    options = {}
    for key in OPTIONS_DEFAULT:
        var = tk.BooleanVar()
        var.set(False)
        options[key] = var
    return options


def test_remove_comments(opts):
    opts["remove_comments"].set(True)
    text = "print('hi')  # TODO: fix"
    result = apply_optimizations(opts, text)
    assert "#" not in result


def test_single_line_mode(opts):
    opts["single_line_mode"].set(True)
    text = "line1\nline2\nline3"
    result = apply_optimizations(opts, text)
    assert "⏎" in result          # این دقیقاً رفتار واقعی کده
    assert "\n" not in result[:-1] # فقط یک \n در انتها مجاز
    assert result.endswith("\n")
    assert result.count("⏎") == 2


def test_shorten_keywords(opts):
    opts["shorten_keywords"].set(True)
    text = """def greet():
    return "hello"
"""
    result = apply_optimizations(opts, text)
    assert "d greet():" in result
    assert "r \"hello\"" in result or "r 'hello'" in result


def test_unicode_shortcuts(opts):
    opts["unicode_shortcuts"].set(True)
    text = "x in items and y not in banned"
    result = apply_optimizations(opts, text)
    assert "∈" in result
    assert "∉" in result


def test_boolean_replacement(opts):
    opts["replace_booleans"].set(True)
    text = "True and False or None"
    result = apply_optimizations(opts, text).strip()
    assert result == "1 and 0 or ~"