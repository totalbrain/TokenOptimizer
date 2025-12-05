"""
Test suite for optimization techniques
Works with current config.py (OPTIONS_DEFAULT as dict)
"""
import tkinter as tk
import pytest
from src.optimizations import apply_optimizations
from src.config import OPTIONS_DEFAULT


@pytest.fixture
def opts():
    """Convert OPTIONS_DEFAULT dict to actual BooleanVar objects (like app does)"""
    options = {}
    for key, default in OPTIONS_DEFAULT.items():
        var = tk.BooleanVar()
        var.set(default)  # Set to default value
        options[key] = var
    return options


def test_remove_comments(opts):
    text = "print('hello')  # this comment will be gone"
    result = apply_optimizations(opts, text)
    assert "#" not in result


def test_remove_docstrings(opts):
    text = '"""This is a docstring"""\ndef x():\n    pass'
    result = apply_optimizations(opts, text)
    assert "docstring" not in result


def test_single_line_mode(opts):
    opts["single_line_mode"].set(True)
    opts["remove_blank_lines"].set(True)
    text = "line1\nline2\nline3"
    result = apply_optimizations(opts, text)
    assert "⏎" in result
    assert "\n" not in result.rstrip("\n")  
    assert result.endswith("\n")


def test_unicode_shortcuts(opts):
    text = "x in items and y not in banned"
    result = apply_optimizations(opts, text)
    assert "∈" in result
    assert "∉" in result


def test_shorten_keywords(opts):
    opts["shorten_keywords"].set(True)
    text = "def hello():\n    return 42"
    result = apply_optimizations(opts, text)
    assert result.strip().startswith("d hello()")
    assert "r 42" in result


def test_boolean_replacement(opts):
    opts["replace_booleans"].set(True)
    text = "True and False or None"
    result = apply_optimizations(opts, text)
    assert result == "1 and 0 or ~"
