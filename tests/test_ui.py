"""
Test that all main UI elements are created correctly
"""
import tkinter as tk
import pytest
from src.app import AITokenCrusher


@pytest.fixture
def app():
    root = tk.Tk()
    root.withdraw()
    app_instance = AITokenCrusher(root)
    yield app_instance
    root.destroy()


def test_main_ui_elements_exist(app):
    assert hasattr(app, "input_text")
    assert hasattr(app, "output_text")
    assert hasattr(app, "theme_button")
    assert hasattr(app, "stats")
    assert hasattr(app, "checkbuttons")
    assert len(app.checkbuttons) == len(app.options)


def test_crush_button_exists_and_calls_optimize(app, monkeypatch):
    called = False
    def mock_optimize():
        nonlocal called
        called = True

    monkeypatch.setattr(app, "optimize", mock_optimize)

    # Find CRUSH button
    crush_btn = None
    for widget in app.root.winfo_children():
        if hasattr(widget, "winfo_children"):
            for child in widget.winfo_children():
                if isinstance(child, tk.Button) and "CRUSH" in child.cget("text"):
                    crush_btn = child
                    break
            if crush_btn:
                break

    assert crush_btn is not None, "CRUSH TOKENS button not found!"
    crush_btn.invoke()
    assert called is True, "optimize() was not called!"