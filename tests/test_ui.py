# tests/test_ui.py
import tkinter as tk
import pytest
from src.app import AITokenCrusher


@pytest.fixture
def app():
    root = tk.Tk()
    root.geometry("1x1+-1000+-1000")  # خارج از صفحه، بدون withdraw
    app_instance = AITokenCrusher(root)
    yield app_instance
    root.destroy()


def test_main_ui_elements_exist(app):
    assert hasattr(app, "input_text")
    assert hasattr(app, "output_text")
    assert hasattr(app, "theme_button")
    assert hasattr(app, "stats")
    assert len(app.checkbuttons) == len(app.options)


def test_crush_button_exists_and_calls_optimize(app, monkeypatch):
    called = False
    def mock_optimize():
        nonlocal called
        called = True

    monkeypatch.setattr(app, "optimize", mock_optimize)

    crush_btn = app.ui_elements.get("crush_btn")
    assert crush_btn is not None, "CRUSH button not stored in ui_elements!"

    