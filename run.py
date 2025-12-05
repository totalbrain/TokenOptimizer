# run.py - Entry point for AI Token Crusher
import sys
import os

# Add src to path so imports work when running from root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Optional: Better error if tkdnd2 not installed
try:
    from tkinterdnd2 import TkinterDnD
    RootClass = TkinterDnD.Tk
except ImportError:
    from tkinter import Tk
    RootClass = Tk

from src.app import AITokenCrusher

if __name__ == "__main__":
    root = RootClass()
    app = AITokenCrusher(root)
    root.mainloop()