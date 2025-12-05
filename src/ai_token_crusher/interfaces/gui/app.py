# src/ai_token_crusher/interfaces/gui/app.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser
from pathlib import Path

# --- Drag & Drop ---
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except ImportError:
    TkinterDnD = tk
    DND_AVAILABLE = False

from ...core import create_engine, OPTIONS_DEFAULT
from .ui import create_ui
from .theme import THEMES


class TokenCrusherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Token Crusher v1.2 – Cut up to 75% tokens")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 700)

        self.engine = create_engine()
        self.options = {k: tk.BooleanVar(value=v) for k, v in OPTIONS_DEFAULT.items()}
        self.is_dark_theme = True
        self.ui_elements = {}
        self.checkbuttons = []
        self.link_labels = []

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))

        create_ui(self)
        self.apply_theme()

        if DND_AVAILABLE:
            self.enable_drag_drop()

    def apply_theme(self):
        theme = THEMES["dark" if self.is_dark_theme else "light"]
        self.root.configure(bg=theme["bg"])

        for widget in self.ui_elements.values():
            if hasattr(widget, "configure"):
                if "bg" in widget.config():
                    widget.configure(bg=theme.get("bg", theme["frame_bg"]))
                if "fg" in widget.config():
                    widget.configure(fg=theme.get("text_bright", theme["text"]))

        self.input_text.configure(bg=theme["input_bg"], fg=theme["input_fg"])
        self.output_text.configure(fg=theme["output_fg"])
        self.stats.configure(foreground=theme["accent_secondary"], background=theme["frame_bg"])
        self.theme_button.config(
            text="☀" if self.is_dark_theme else "🌙",
            bg=theme["bg"], fg=theme["accent"]
        )

        for cb in self.checkbuttons:
            cb.configure(bg=theme["frame_bg"], fg=theme["text"], selectcolor=theme["select_bg"])
        for link in self.link_labels:
            link.configure(fg=theme["accent"], bg=theme["bg"])

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def enable_drag_drop(self):
        """Enable drag-and-drop – works 100% on Windows with tkinterdnd2"""
        if not DND_AVAILABLE:
            return
        try:
            # Critical: bind to the internal Text widget of ScrolledText
            text_widget = self.input_text._text

            text_widget.drop_target_register(DND_FILES)
            text_widget.dnd_bind('<<Drop>>', self.on_drop)

            # Also bind to the ScrolledText itself (just in case)
            self.input_text.drop_target_register(DND_FILES)
            self.input_text.dnd_bind('<<Drop>>', self.on_drop)

        except Exception as e:
            print(f"[DND] Disabled: {e}")

    def on_drop(self, event):
        """Handle dropped files – fully Windows-compatible"""
        data = event.data.strip()

        # Windows wraps paths in {} when multiple files are dropped
        if data.startswith('{') and data.endswith('}'):
            data = data[1:-1]

        import shlex
        try:
            files = shlex.split(data)
        except:
            files = [f.strip('{}') for f in data.split()]

        for file_path in files:
            file_path = file_path.strip('"\'')
            path = Path(file_path)
            if path.exists():
                if path.suffix.lower() in {
                    ".py", ".txt", ".md", ".json", ".yml", ".yaml",
                    ".log", ".csv", ".js", ".ts", ".html", ".css",
                    ".jsx", ".tsx", ".sql"
                }:
                    try:
                        self.input_text.delete(1.0, tk.END)
                        self.input_text.insert(tk.END, path.read_text(encoding="utf-8"))
                        self.stats.config(text=f"Loaded: {path.name}")
                        return
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not open file:\n{e}")
                        return

        messagebox.showwarning("Invalid file", "Please drop a supported text file.")

    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.py *.txt *.md *.json *.yml *.yaml *.js *.ts *.html *.css"), ("All Files", "*.*")]
        )
        if path:
            self.load_text_from_file(path)

    def load_text_from_file(self, path):
        try:
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(tk.END, Path(path).read_text(encoding="utf-8"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def copy_output(self):
        text = self.output_text.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied!", "Crushed text copied to clipboard!")

    def save_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt"), ("All Files", "*.*")])
        if path:
            try:
                Path(path).write_text(self.output_text.get(1.0, tk.END), encoding="utf-8")
                messagebox.showinfo("Saved", "Output saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{e}")

    def optimize(self):
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please paste or load some text first.")
            return

        options = {k: v.get() for k, v in self.options.items()}
        result = self.engine.apply(text, options)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result.optimized_text)

        self.stats.config(
            text=f"Before: {len(text):,} → After: {len(result.optimized_text):,} chars | Saved: {result.total_saved_percent:.1f}%"
        )


def run_gui():
    root = TkinterDnD.Tk() if DND_AVAILABLE else tk.Tk()
    app = TokenCrusherGUI(root)
    root.mainloop()