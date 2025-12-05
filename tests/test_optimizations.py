"""
Test suite for optimization techniques
"""
import pytest
from src.optimizations import apply_optimizations
from src.config import OPTIONS

@pytest.fixture
def clean_options():
    # Reset all options to default before each test
    for var in OPTIONS.values():
        var.set(True)
    return OPTIONS

def test_remove_comments(clean_options):
    input_text = "print('hello')  # this is a comment\nx = 1"
    result = apply_optimizations(clean_options, input_text)
    assert "#" not in result

def test_remove_docstrings(clean_options):
    input_text = '"""This is docstring"""\ndef hello():\n    pass'
    result = apply_optimizations(clean_options, input_text)
    assert "docstring" not in result

def test_single_line_mode(clean_options):
    clean_options["single_line_mode"].set(True)
    input_text = "line1\nline2\nline3"
    result = apply_optimizations(clean_options, input_text)
    assert "⏎" in result
    assert "\n" not in result

def test_unicode_shortcuts(clean_options):
    input_text = "x in mylist and y not in banned"
    result = apply_optimizations(clean_options, input_text)
    assert "∈" in result and "∉" in result

def test_shorten_keywords(clean_options):
    clean_options["shorten_keywords"].set(True)
    input_text = "def hello(): return 42"
    result = apply_optimizations(clean_options, input_text)
    assert result.strip().startswith("d hello()")

def test_boolean_replacement(clean_options):
    clean_options["replace_booleans"].set(True)
    input_text = "x = True if False else None"
    result = apply_optimizations(clean_options, input_text)
    assert "1" in result and "0" in result and "~" in result