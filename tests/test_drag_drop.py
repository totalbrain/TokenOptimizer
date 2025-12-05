# tests/test_drag_drop.py
import pytest
from src.app import AITokenCrusher
import tkinter as tk

def test_drag_drop_enabled_when_tkdnd_available(monkeypatch):
    monkeypatch.setattr("src.app.TKDND_AVAILABLE", True)
    root = tk.Tk()
    root.withdraw()
    app = AITokenCrusher(root)
    assert app.input_text.tk.call("info", "commands", app.input_text._w + ".drop") != ""
    root.destroy()

def test_drag_drop_disabled_when_tkdnd_missing(monkeypatch):
    monkeypatch.setattr("src.app.TKDND_AVAILABLE", False)
    root = tk.Tk()
    root.withdraw()
    app = AITokenCrusher(root)
    # Should not crash, just skip
    assert app.input_text is not None
    root.destroy()