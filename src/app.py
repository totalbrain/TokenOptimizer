# main.py - AI Token Crusher v1.0
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser
import re

class AITokenCrusher:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Token Crusher - Cut up to 75% tokens")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#0d1117")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", foreground="#58a6ff", font=("Segoe UI", 18, "bold"), background="#0d1117")
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

        self.create_ui()

    def create_ui(self):
        main = tk.Frame(self.root, bg="#0d1117")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(main, text="AI Token Crusher", style="Title.TLabel").pack(pady=(0, 5))
        ttk.Label(main, text="Cut up to 75% of tokens for Grok • GPT • Claude • Llama", 
                 foreground="#8b949e", font=("Segoe UI", 11), background="#0d1117").pack(pady=(0, 20))

        top = tk.Frame(main, bg="#0d1117")
        top.pack(fill="both", expand=True)

        input_frame = tk.LabelFrame(top, text=" Input Text / Code ", fg="#f0f6fc", bg="#161b22", font=("Segoe UI", 10, "bold"))
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.input_text = scrolledtext.ScrolledText(input_frame, font=("Consolas", 10), bg="#0d1117", fg="#c9d1d9")
        self.input_text.pack(fill="both", expand=True, padx=10, pady=10)

        btns = tk.Frame(input_frame, bg="#161b22")
        btns.pack(pady=5)
        ttk.Button(btns, text="Load File", command=self.load_file).pack(side="left", padx=5)
        ttk.Button(btns, text="Copy Output", command=self.copy_output).pack(side="left", padx=5)

        options_frame = tk.LabelFrame(top, text=" Optimization Techniques ", fg="#f0f6fc", bg="#161b22", font=("Segoe UI", 10, "bold"))
        options_frame.pack(side="right", fill="y", padx=(10, 0))
        canvas = tk.Canvas(options_frame, bg="#161b22", highlightthickness=0)
        scrollbar = ttk.Scrollbar(options_frame, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#161b22")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        for key, var in self.options.items():
            name = key.replace("_", " ").title().replace("Shorten", "Short").replace("Remove", "Strip")
            tk.Checkbutton(scroll_frame, text=name, variable=var, bg="#161b22", fg="#c9d1d9", selectcolor="#21262d").pack(anchor="w", pady=2, padx=15)

        ttk.Button(main, text="CRUSH TOKENS →", command=self.optimize).pack(pady=20)

        output_frame = tk.LabelFrame(main, text=" Crushed Output (AI-Safe) ", fg="#f0f6fc", bg="#161b22", font=("Segoe UI", 10, "bold"))
        output_frame.pack(fill="both", expand=True, pady=(10, 0))
        self.output_text = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), bg="#0d1117", fg="#79c0ff")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Button(output_frame, text="Save Output", command=self.save_output).pack(pady=5)

        self.stats = ttk.Label(main, text="Ready to crush tokens...", foreground="#79c0ff", font=("Consolas", 11, "bold"), background="#161b22")
        self.stats.pack(pady=10)

        footer = tk.Frame(main, bg="#0d1117")
        footer.pack(pady=15)
        links = [("GitHub", "https://github.com/totalbrain/TokenOptimizer"), ("Roadmap", "https://github.com/users/totalbrain/projects/1")]
        for text, url in links:
            link = tk.Label(footer, text=text, fg="#58a6ff", bg="#0d1117", cursor="hand2", font=("Segoe UI", 9, "underline"))
            link.pack(side="left", padx=20)
            link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))

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
    root = tk.Tk()
    app = AITokenCrusher(root)
    root.mainloop()