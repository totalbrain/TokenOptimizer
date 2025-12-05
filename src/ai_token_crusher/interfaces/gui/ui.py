# src/ai_token_crusher/interfaces/gui/ui.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser
from .theme import THEMES, LINKS


def create_modern_ui(app):
    theme = THEMES["dark" if app.is_dark_theme else "light"]

    # Header
    header = tk.Frame(app.root, bg=theme["bg"], height=90)
    header.pack(fill="x", padx=30, pady=(20, 0))
    header.pack_propagate(False)

    tk.Label(header, text="AI Token Crusher", font=("Segoe UI", 32, "bold"), fg=theme["accent"], bg=theme["bg"]).pack(side="left", pady=10)
    
    app.theme_button = tk.Button(
        header, text="Light Mode", command=app.toggle_theme,
        bg=theme["frame_bg"], fg=theme["accent"], font=("Segoe UI", 12, "bold"),
        relief="flat", bd=0, padx=20, pady=10, cursor="hand2"
    )
    app.theme_button.pack(side="right", pady=10)

    tk.Label(header, text="Crush up to 75% of tokens instantly • Grok • GPT • Claude • Llama", 
             font=("Segoe UI", 11), fg=theme["text_secondary"], bg=theme["bg"]).pack(side="left", padx=20)

    # Main Content Area
    content_frame = tk.Frame(app.root, bg=theme["bg"])
    content_frame.pack(fill="both", expand=True, padx=30, pady=20)

    # Input + Options Side by Side (با grid — بدون PanedWindow!)
    input_options_frame = tk.Frame(content_frame, bg=theme["bg"])
    input_options_frame.pack(fill="both", expand=True)

    # Input Panel (چپ)
    input_frame = tk.LabelFrame(input_options_frame, text=" Input • Drop file or paste code ", 
                                font=("Segoe UI", 11, "bold"), fg=theme["text_bright"], bg=theme["frame_bg"], bd=2, relief="groove")
    input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    app.input_text = scrolledtext.ScrolledText(input_frame, font=("Consolas", 11), bg=theme["input_bg"], fg=theme["input_fg"], undo=True)
    app.input_text.pack(fill="both", expand=True, padx=12, pady=12)

    btn_frame = tk.Frame(input_frame, bg=theme["frame_bg"])
    btn_frame.pack(pady=8)
    ttk.Button(btn_frame, text="Load File", command=app.load_file).pack(side="left", padx=8)
    ttk.Button(btn_frame, text="Clear Input", command=lambda: app.input_text.delete(1.0, tk.END)).pack(side="left", padx=8)

    # Options Panel (راست)
    options_frame = tk.LabelFrame(input_options_frame, text=" Optimization Techniques ", 
                                  font=("Segoe UI", 11, "bold"), fg=theme["text_bright"], bg=theme["frame_bg"], bd=2, relief="groove")
    options_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    canvas = tk.Canvas(options_frame, bg=theme["frame_bg"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(options_frame, orient="vertical", command=canvas.yview)
    scrollable = tk.Frame(canvas, bg=theme["frame_bg"])
    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=12, pady=12)
    scrollbar.pack(side="right", fill="y")

    app.checkbuttons = []
    for key, var in app.options.items():
        name = key.replace("_", " ").title().replace("Shorten", "Short").replace("Remove", "Strip")
        cb = tk.Checkbutton(scrollable, text=name, variable=var, bg=theme["frame_bg"], fg=theme["text"], 
                            selectcolor=theme["select_bg"], font=("Segoe UI", 10))
        cb.pack(anchor="w", pady=4, padx=20)
        app.checkbuttons.append(cb)

    # تنظیم وزن برای تقسیم مساوی
    input_options_frame.grid_columnconfigure(0, weight=1)
    input_options_frame.grid_columnconfigure(1, weight=1)
    input_options_frame.grid_rowconfigure(0, weight=1)

    # Bottom Section: Crush Button + Output
    bottom = tk.Frame(content_frame, bg=theme["bg"])
    bottom.pack(fill="both", expand=True, pady=(20, 0))

    ttk.Button(bottom, text="CRUSH TOKENS", command=app.optimize).pack(pady=15)

    output_frame = tk.LabelFrame(bottom, text=" Crushed Output • AI-Safe & Readable ", 
                                 font=("Segoe UI", 11, "bold"), fg=theme["text_bright"], bg=theme["frame_bg"], bd=2, relief="groove")
    output_frame.pack(fill="both", expand=True)

    app.output_text = scrolledtext.ScrolledText(output_frame, font=("Consolas", 11), bg=theme["input_bg"], fg=theme["output_fg"])
    app.output_text.pack(fill="both", expand=True, padx=12, pady=12)

    btn_out = tk.Frame(output_frame, bg=theme["frame_bg"])
    btn_out.pack(pady=8)
    ttk.Button(btn_out, text="Copy Output", command=app.copy_output).pack(side="left", padx=8)
    ttk.Button(btn_out, text="Save As...", command=app.save_output).pack(side="left", padx=8)

    # Stats
    app.stats = tk.Label(bottom, text="Ready to crush tokens...", font=("Consolas", 13, "bold"),
                          fg=theme["accent"], bg=theme["bg"])
    app.stats.pack(pady=10)

    # Footer
    footer = tk.Frame(app.root, bg=theme["bg"])
    footer.pack(pady=15)
    app.link_labels = []
    for text, url in LINKS:
        link = tk.Label(footer, text=text, fg=theme["accent"], bg=theme["bg"], cursor="hand2", 
                        font=("Segoe UI", 10, "underline"))
        link.pack(side="left", padx=25)
        link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
        app.link_labels.append(link)

    app.ui_elements.update({
        "header": header, "content_frame": content_frame, "footer": footer
    })