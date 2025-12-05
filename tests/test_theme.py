"""
Test dark/light theme toggle functionality
"""
import tkinter as tk
import pytest
from src.app import AITokenCrusher
from src.config import THEMES


@pytest.fixture
def app():
    root = tk.Tk()
    root.withdraw()
    app_instance = AITokenCrusher(root)
    yield app_instance
    root.destroy()


def test_initial_theme_is_dark(app):
    assert app.is_dark_theme is True
    assert app.root.cget("bg") == THEMES["dark"]["bg"]


def test_toggle_to_light_mode(app):
    app.toggle_theme()
    assert app.is_dark_theme is False
    assert app.root.cget("bg") == THEMES["light"]["bg"]


def test_toggle_back_to_dark_mode(app):
    app.toggle_theme()  # light
    app.toggle_theme()  # back to dark
    assert app.is_dark_theme is True
    assert app.root.cget("bg") == THEMES["dark"]["bg"]


def test_theme_button_icon_changes(app):
    assert app.theme_button.cget("text") == "☀️"  # dark → show sun
    app.toggle_theme()
    assert app.theme_button.cget("text") == "🌙"  # light → show moon