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
from .ui import create_modern_ui
from .theme import THEMES


class TokenCrusherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Token Crusher v1.2")
        self.root.geometry("1520x940")
        self.root.minsize(1200, 760)
        self.root.configure(bg="#0d1117")
        self.root.state('zoomed') if tk.TkVersion >= 8.6 else None  # Fullscreen on Windows

        self.engine = create_engine()
        self.options = {k: tk.BooleanVar(value=v) for k, v in OPTIONS_DEFAULT.items()}
        self.is_dark_theme = True
        self.ui_elements = {}

        # Modern style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 28, "bold"), foreground="#58a6ff")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 12), foreground="#8b949e")
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10)
        style.map("TButton", background=[("active", "#1f6feb")])

        create_modern_ui(self)
        self.apply_theme()

        if DND_AVAILABLE:
            self.enable_drag_drop()

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def apply_theme(self):
        theme = THEMES["dark" if self.is_dark_theme else "light"]
        self.root.configure(bg=theme["bg"])

        for widget in self.ui_elements.values():
            if hasattr(widget, "configure"):
                cfg = widget.config()
                if "bg" in cfg:
                    widget.configure(bg=theme.get("bg", theme["frame_bg"]))
                if "fg" in cfg:
                    widget.configure(fg=theme.get("text_bright", theme["text"]))

        # رنگ‌های معتبر برای tkinter
        self.input_text.configure(
            bg=theme["input_bg"], 
            fg=theme["input_fg"],
            insertbackground=theme["text"],           # مکان‌نما
            selectbackground="#1f6feb"                # انتخاب متن (رنگ ثابت و معتبر)
        )
        self.output_text.configure(
            fg=theme["output_fg"], 
            bg=theme["input_bg"],
            insertbackground=theme["output_fg"],
            selectbackground="#1f6feb"
        )
        self.stats.configure(
            foreground=theme["accent"], 
            background=theme["frame_bg"],
            font=("Consolas", 13, "bold")
        )
        self.theme_button.config(
            text="Light Mode" if self.is_dark_theme else "Dark Mode",
            bg=theme["frame_bg"], fg=theme["accent"], font=("Segoe UI", 12, "bold"),
            relief="flat", bd=0, highlightthickness=0
        )

        for cb in getattr(self, "checkbuttons", []):
            cb.configure(bg=theme["frame_bg"], fg=theme["text"], selectcolor=theme["select_bg"])
        for link in getattr(self, "link_labels", []):
            link.configure(fg=theme["accent"], bg=theme["bg"])


    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def enable_drag_drop(self):
        if not DND_AVAILABLE:
            return
        try:
            text_widget = self.input_text._text
            text_widget.drop_target_register(DND_FILES)
            text_widget.dnd_bind('<<Drop>>', self.on_drop)
            self.input_text.drop_target_register(DND_FILES)
            self.input_text.dnd_bind('<<Drop>>', self.on_drop)
        except Exception as e:
            print(f"[DND] Failed: {e}")

    def on_drop(self, event):
        data = event.data.strip()
        if data.startswith('{') and data.endswith('}'):
            data = data[1:-1]
        import shlex
        try:
            files = shlex.split(data)
        except:
            files = [f.strip('{}') for f in data.split()]

        for fp in files:
            fp = fp.strip('"\'')
            path = Path(fp)
            if path.exists():
                if path.suffix.lower() in {".py", ".js", ".ts", ".html", ".css", ".json", ".md", ".txt", ".log", ".yaml", ".yml", ".sql"}:
                    try:
                        content = path.read_text(encoding="utf-8", errors="ignore")
                        self.input_text.delete(1.0, tk.END)
                        self.input_text.insert(tk.END, content)
                        self.stats.config(text=f"Dropped • {path.name} • {len(content):,} chars")
                        return
                    except Exception as e:
                        messagebox.showerror("Error", f"Cannot read file:\n{e}")
                        return

    def load_file(self):
        path = filedialog.askopenfilename(
            title="Open source file",
            filetypes=[("All Supported", "*.py *.js *.ts *.jsx *.tsx *.html *.css *.json *.md *.yaml *.yml *.txt *.log *.sql"), ("All Files", "*.*")]
        )
        if path:
            self.load_text_from_file(path)

    def load_text_from_file(self, path):
        try:
            content = Path(path).read_text(encoding="utf-8", errors="ignore")
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(tk.END, content)
            self.stats.config(text=f"Loaded • {Path(path).name} • {len(content):,} chars")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load:\n{e}")

    def copy_output(self):
        text = self.output_text.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied", "Crushed output copied!")

    def save_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".py", title="Save crushed code")
        if path:
            try:
                Path(path).write_text(self.output_text.get(1.0, tk.END), encoding="utf-8")
                messagebox.showinfo("Saved", f"Saved to {Path(path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed:\n{e}")

    def optimize(self):
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("No Input", "Drop a file or paste code first.")
            return

        options = {k: v.get() for k, v in self.options.items()}
        result = self.engine.apply(text, options)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result.optimized_text)

        saved = result.total_saved_percent
        before = len(text)
        after = len(result.optimized_text)
        time_ms = result.total_time_ms

        self.stats.config(
            text=f"Success • Saved {saved:.1f}% • {before:,} → {after:,} chars • {time_ms:.1f}ms"
        )


def run_gui():
    root = TkinterDnD.Tk() if DND_AVAILABLE else tk.Tk()
    app = TokenCrusherGUI(root)
    root.mainloop()