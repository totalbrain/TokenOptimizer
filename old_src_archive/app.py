# src/app.py - Main application class (fully modular, no early Tk errors)
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
import os

# Drag-and-drop support (optional)
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    TKDND_AVAILABLE = True
except ImportError:
    DND_FILES = None
    TkinterDnD = tk.Tk
    TKDND_AVAILABLE = False

from .config import OPTIONS_DEFAULT, THEMES, LINKS
from .ui import create_ui
from .optimizations import apply_optimizations


class AITokenCrusher:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Token Crusher - Cut up to 75% tokens")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 700)

        # --- CRITICAL FIX: Create BooleanVars AFTER root exists ---
        self.options = {}
        for key, default in OPTIONS_DEFAULT.items():
            self.options[key] = tk.BooleanVar(value=default)

        self.is_dark_theme = True
        self.ui_elements = {}
        self.checkbuttons = []
        self.link_labels = []

        # Initial theme setup
        self.root.configure(bg=THEMES["dark"]["bg"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Title.TLabel",
            foreground="#58a6ff",
            font=("Segoe UI", 18, "bold"),
            background=THEMES["dark"]["bg"]
        )

        # Build UI
        create_ui(self)

        # Enable drag & drop if available
        self.enable_drag_and_drop()

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def apply_theme(self):
        theme = THEMES["dark" if self.is_dark_theme else "light"]

        # Update root
        self.root.configure(bg=theme["bg"])

        # Update ttk style
        style = ttk.Style()
        style.configure("Title.TLabel", foreground=theme["accent"], background=theme["bg"])

        # Update theme button
        self.theme_button.config(
            text="☀️" if self.is_dark_theme else "🌙",
            bg=theme["bg"],
            fg=theme["accent"]
        )

        # Update stored UI elements
        for elem, widget in self.ui_elements.items():
            if hasattr(widget, "configure"):
                if "bg" in widget.config():
                    widget.configure(bg=theme.get("bg", theme["frame_bg"]))
                if "fg" in widget.config():
                    widget.configure(fg=theme.get("text_bright", theme["text"]))

        # Special widgets
        self.input_text.configure(bg=theme["input_bg"], fg=theme["input_fg"])
        self.output_text.configure(fg=theme["output_fg"])
        self.stats.configure(foreground=theme["accent_secondary"], background=theme["frame_bg"])

        # Checkbuttons
        for cb in self.checkbuttons:
            cb.configure(bg=theme["frame_bg"], fg=theme["text"], selectcolor=theme["select_bg"])

        # Links
        for link in self.link_labels:
            link.configure(bg=theme["bg"], fg=theme["accent"])

    def enable_drag_and_drop(self):
        if not TKDND_AVAILABLE or DND_FILES is None:
            return
        try:
            self.input_text.drop_target_register(DND_FILES)
            self.input_text.dnd_bind("<<Drop>>", self.on_drop_files)
        except Exception:
            pass  # Silently skip if DnD setup fails

    def on_drop_files(self, event):
        file_paths = self.root.splitlist(event.data)
        allowed = {".py", ".txt", ".md", ".json"}
        for path in file_paths:
            if os.path.splitext(path)[1].lower() in allowed:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
                    return
                except Exception as e:
                    messagebox.showerror("Read Error", f"Failed to open file:\n{e}")
        messagebox.showwarning("Invalid File", "Only .py, .txt, .md, .json files are supported.")

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, f.read())

    def copy_output(self):
        output = self.output_text.get(1.0, tk.END).strip()
        if output:
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            messagebox.showinfo("Copied!", "Crushed text copied to clipboard!")

    def save_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.output_text.get(1.0, tk.END))
            messagebox.showinfo("Saved", "Output saved successfully!")

    def optimize(self):
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please paste or load some text first.")
            return

        optimized = apply_optimizations(self.options, text)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, optimized)

        before = len(text)
        after = len(optimized)
        saved = 100 * (before - after) / before if before else 0

        self.stats.config(
            text=f"Before: {before:,} → After: {after:,} chars | Saved: {saved:.1f}%"
        )


# Entry point when running directly (python -m src.app)
if __name__ == "__main__":
    root = TkinterDnD.Tk() if TKDND_AVAILABLE else tk.Tk()
    app = AITokenCrusher(root)
    root.mainloop()