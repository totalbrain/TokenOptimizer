# main.py - AI Token Crusher v1.0
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser
import re
import os

# Drag-and-drop relies on native tkdnd bindings, so we import tkinterdnd2 optionally to avoid crashes when unavailable.
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    TKDND_AVAILABLE = True
except ImportError:
    DND_FILES = None
    TkinterDnD = tk.Tk  # fallback so type is available
    TKDND_AVAILABLE = False

class AITokenCrusher:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Token Crusher - Cut up to 75% tokens")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 700)

        # Theme management
        self.is_dark_theme = True
        self.themes = {
            "dark": {
                "bg": "#0d1117",
                "frame_bg": "#161b22",
                "text": "#c9d1d9",
                "text_secondary": "#8b949e",
                "text_bright": "#f0f6fc",
                "accent": "#58a6ff",
                "accent_secondary": "#79c0ff",
                "select_bg": "#21262d",
                "input_bg": "#0d1117",
                "input_fg": "#c9d1d9",
                "output_fg": "#79c0ff",
            },
            "light": {
                "bg": "#ffffff",
                "frame_bg": "#f6f8fa",
                "text": "#24292f",
                "text_secondary": "#57606a",
                "text_bright": "#1f2328",
                "accent": "#0969da",
                "accent_secondary": "#0550ae",
                "select_bg": "#ddf4ff",
                "input_bg": "#ffffff",
                "input_fg": "#24292f",
                "output_fg": "#0550ae",
            }
        }

        self.root.configure(bg=self.themes["dark"]["bg"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", foreground=self.themes["dark"]["accent"], font=("Segoe UI", 18, "bold"), background=self.themes["dark"]["bg"])
        style.configure("TButton", padding=10, font=("Segoe UI", 9, "bold"))

        self.options = {
            "remove_comments": tk.BooleanVar(value=True),
            "remove_docstrings": tk.BooleanVar(value=True),
            "remove_blank_lines": tk.BooleanVar(value=True),
            "remove_extra_spaces": tk.BooleanVar(value=True),
            "single_line_mode": tk.BooleanVar(value=True),
            "shorten_keywords": tk.BooleanVar(value=True),
            "replace_booleans": tk.BooleanVar(value=True),
            "use_short_operators": tk.BooleanVar(value=True),
            "remove_type_hints": tk.BooleanVar(value=True),
            "minify_structures": tk.BooleanVar(value=True),
            "unicode_shortcuts": tk.BooleanVar(value=True),
            "shorten_print": tk.BooleanVar(value=True),
            "remove_asserts": tk.BooleanVar(value=True),
            "remove_pass": tk.BooleanVar(value=True),
        }

        # Store references to UI elements
        self.ui_elements = {}
        self.checkbuttons = []

        self.create_ui()

        # Enable drag & drop if tkdnd is available
        self.enable_drag_and_drop()

    def create_ui(self):
        theme = self.themes["dark" if self.is_dark_theme else "light"]

        main = tk.Frame(self.root, bg=theme["bg"])
        main.pack(fill="both", expand=True, padx=20, pady=20)
        self.ui_elements["main"] = main

        # Header section (title and theme toggle button)
        header = tk.Frame(main, bg=theme["bg"])
        header.pack(fill="x", pady=(0, 5))
        self.ui_elements["header"] = header

        # Theme toggle button (placed on the right)
        theme_icon = "☀️" if self.is_dark_theme else "🌙"
        self.theme_button = tk.Button(
            header, text=theme_icon, command=self.toggle_theme,
            bg=theme["bg"], fg=theme["accent"], font=("Segoe UI", 16),
            relief="flat", cursor="hand2", bd=0, padx=10, pady=5
        )
        self.theme_button.pack(side="right")

        # Title (centered)
        self.ui_elements["title"] = ttk.Label(header, text="AI Token Crusher", style="Title.TLabel")
        self.ui_elements["title"].place(relx=0.5, rely=0.5, anchor="center")

        self.ui_elements["subtitle"] = tk.Label(
            main, text="Cut up to 75% of tokens for Grok • GPT • Claude • Llama",
            foreground=theme["text_secondary"], font=("Segoe UI", 11), background=theme["bg"]
        )
        self.ui_elements["subtitle"].pack(pady=(0, 20))

        top = tk.Frame(main, bg=theme["bg"])
        top.pack(fill="both", expand=True)
        self.ui_elements["top"] = top

        input_frame = tk.LabelFrame(top, text=" Input Text / Code ", fg=theme["text_bright"], bg=theme["frame_bg"], font=("Segoe UI", 10, "bold"))
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.ui_elements["input_frame"] = input_frame

        self.input_text = scrolledtext.ScrolledText(input_frame, font=("Consolas", 10), bg=theme["input_bg"], fg=theme["input_fg"])
        self.input_text.pack(fill="both", expand=True, padx=10, pady=10)

        btns = tk.Frame(input_frame, bg=theme["frame_bg"])
        btns.pack(pady=5)
        self.ui_elements["btns"] = btns
        ttk.Button(btns, text="Load File", command=self.load_file).pack(side="left", padx=5)
        ttk.Button(btns, text="Copy Output", command=self.copy_output).pack(side="left", padx=5)

        options_frame = tk.LabelFrame(top, text=" Optimization Techniques ", fg=theme["text_bright"], bg=theme["frame_bg"], font=("Segoe UI", 10, "bold"))
        options_frame.pack(side="right", fill="y", padx=(10, 0))
        self.ui_elements["options_frame"] = options_frame

        canvas = tk.Canvas(options_frame, bg=theme["frame_bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(options_frame, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=theme["frame_bg"])
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        self.ui_elements["canvas"] = canvas
        self.ui_elements["scroll_frame"] = scroll_frame

        self.checkbuttons = []
        for key, var in self.options.items():
            name = key.replace("_", " ").title().replace("Shorten", "Short").replace("Remove", "Strip")
            cb = tk.Checkbutton(
                scroll_frame, text=name, variable=var, bg=theme["frame_bg"],
                fg=theme["text"], selectcolor=theme["select_bg"]
            )
            cb.pack(anchor="w", pady=2, padx=15)
            self.checkbuttons.append(cb)

        ttk.Button(main, text="CRUSH TOKENS →", command=self.optimize).pack(pady=20)

        output_frame = tk.LabelFrame(main, text=" Crushed Output (AI-Safe) ", fg=theme["text_bright"], bg=theme["frame_bg"], font=("Segoe UI", 10, "bold"))
        output_frame.pack(fill="both", expand=True, pady=(10, 0))
        self.ui_elements["output_frame"] = output_frame

        self.output_text = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), bg=theme["input_bg"], fg=theme["output_fg"])
        self.output_text.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Button(output_frame, text="Save Output", command=self.save_output).pack(pady=5)

        self.stats = ttk.Label(
            main, text="Ready to crush tokens...", foreground=theme["accent_secondary"],
            font=("Consolas", 11, "bold"), background=theme["frame_bg"]
        )
        self.stats.pack(pady=10)

        footer = tk.Frame(main, bg=theme["bg"])
        footer.pack(pady=15)
        self.ui_elements["footer"] = footer

        self.link_labels = []
        links = [("GitHub", "https://github.com/totalbrain/TokenOptimizer"), ("Roadmap", "https://github.com/users/totalbrain/projects/1")]
        for text, url in links:
            link = tk.Label(
                footer, text=text, fg=theme["accent"], bg=theme["bg"],
                cursor="hand2", font=("Segoe UI", 9, "underline")
            )
            link.pack(side="left", padx=20)
            link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
            self.link_labels.append(link)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes["dark" if self.is_dark_theme else "light"]

        # Root window
        self.root.configure(bg=theme["bg"])

        # Update styles
        style = ttk.Style()
        style.configure("Title.TLabel", foreground=theme["accent"], background=theme["bg"])

        # Theme toggle button
        theme_icon = "☀️" if self.is_dark_theme else "🌙"
        self.theme_button.config(text=theme_icon, bg=theme["bg"], fg=theme["accent"])

        # Header and title frame
        if "header" in self.ui_elements:
            self.ui_elements["header"].configure(bg=theme["bg"])

        # Main frame
        if "main" in self.ui_elements:
            self.ui_elements["main"].configure(bg=theme["bg"])

        # Subtitle
        if "subtitle" in self.ui_elements:
            self.ui_elements["subtitle"].configure(bg=theme["bg"], fg=theme["text_secondary"])

        # Top frame
        if "top" in self.ui_elements:
            self.ui_elements["top"].configure(bg=theme["bg"])

        # Input frame
        if "input_frame" in self.ui_elements:
            self.ui_elements["input_frame"].configure(bg=theme["frame_bg"], fg=theme["text_bright"])

        # Input text
        self.input_text.configure(bg=theme["input_bg"], fg=theme["input_fg"])

        # Button frame
        if "btns" in self.ui_elements:
            self.ui_elements["btns"].configure(bg=theme["frame_bg"])

        # Options frame
        if "options_frame" in self.ui_elements:
            self.ui_elements["options_frame"].configure(bg=theme["frame_bg"], fg=theme["text_bright"])

        # Canvas and scroll frame
        if "canvas" in self.ui_elements:
            self.ui_elements["canvas"].configure(bg=theme["frame_bg"])
        if "scroll_frame" in self.ui_elements:
            self.ui_elements["scroll_frame"].configure(bg=theme["frame_bg"])

        # Check buttons
        for cb in self.checkbuttons:
            cb.configure(bg=theme["frame_bg"], fg=theme["text"], selectcolor=theme["select_bg"])

        # Output frame
        if "output_frame" in self.ui_elements:
            self.ui_elements["output_frame"].configure(bg=theme["frame_bg"], fg=theme["text_bright"])

        # Output text
        self.output_text.configure(bg=theme["input_bg"], fg=theme["output_fg"])

        # Statistics label
        self.stats.configure(foreground=theme["accent_secondary"], background=theme["frame_bg"])

        # Footer
        if "footer" in self.ui_elements:
            self.ui_elements["footer"].configure(bg=theme["bg"])

        # Link labels
        for link in self.link_labels:
            link.configure(bg=theme["bg"], fg=theme["accent"])

    def enable_drag_and_drop(self):
        """Enable drag & drop for files into the input text area (if supported)."""
        if not TKDND_AVAILABLE or DND_FILES is None:
            return
        try:
            self.input_text.drop_target_register(DND_FILES)
            self.input_text.dnd_bind("<<Drop>>", self.on_drop_files)
        except Exception:
            # If tkdnd is not correctly configured on the system, just skip DnD
            pass

    def on_drop_files(self, event):
        """Handle files dropped into the input text area."""
        # event.data is a Tcl list of file paths, may contain braces around paths with spaces
        file_paths = self.root.splitlist(event.data)
        allowed_exts = {".py", ".txt", ".md"}

        for path in file_paths:
            ext = os.path.splitext(path)[1].lower()
            if ext not in allowed_exts:
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, content)
                return
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file:\n{path}\n\n{e}")

        # If we reach here, either no valid file was found or extensions were unsupported
        messagebox.showwarning("Unsupported", "You can only drop .py, .txt, or .md files here.")

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
            messagebox.showwarning("Empty", "Paste or load text first!")
            return

        optimized = self.apply_optimizations(text)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, optimized)

        before = len(text)
        after = len(optimized)
        saved = 100 * (before - after) / before if before else 0
        self.stats.config(text=f"Before: {before:,} → After: {after:,} chars | Saved: {saved:.1f}%")

    def apply_optimizations(self, text):
        import re
        if self.options["remove_comments"].get():
            text = re.sub(r'#.*', '', text)
            text = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', '', text)
        if self.options["remove_docstrings"].get():
            text = re.sub(r'^[\r\n\s]*("""|\'\'\').*?\1', '', text, count=1, flags=re.DOTALL)
        if self.options["remove_blank_lines"].get():
            text = "\n".join(line for line in text.splitlines() if line.strip())
        if self.options["remove_extra_spaces"].get():
            text = re.sub(r'[ \t]+', ' ', text)
        if self.options["single_line_mode"].get():
            text = text.replace("\n", "⏎")
        if self.options["shorten_keywords"].get():
            rep = {"def ": "d ", "return ": "r ", "import ": "i ", "from ": "f ", "as ": "a ", "if ": "if", "class ": "c ", "lambda ": "λ "}
            for k, v in rep.items(): text = text.replace(k, v)
        if self.options["replace_booleans"].get():
            text = text.replace("True", "1").replace("False", "0").replace("None", "~")
        if self.options["use_short_operators"].get():
            text = text.replace("==", "≡").replace("!=", "≠").replace(" and ", "∧").replace(" or ", "∨")
        if self.options["remove_type_hints"].get():
            text = re.sub(r':\s*[^=\n\->]+', '', text)
            text = re.sub(r'->\s*[^:\n]+', '', text)
        if self.options["minify_structures"].get():
            text = re.sub(r',\s+', ',', text)
            text = re.sub(r':\s+', ':', text)
        if self.options["unicode_shortcuts"].get():
            text = text.replace(" in ", "∈").replace(" not in ", "∉")
        if self.options["shorten_print"].get():
            text = re.sub(r'print\s*\(', 'p(', text)
        return text.strip() + "\n"

if __name__ == "__main__":
    # Use TkinterDnD's Tk if available, otherwise fall back to standard Tk
    if TKDND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = AITokenCrusher(root)
    root.mainloop()