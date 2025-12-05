# src/ai_token_crusher/interfaces/gui/ui.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser
from .theme import THEMES, LINKS

def create_ui(app):
    theme = THEMES["dark" if app.is_dark_theme else "light"]

    # Main container
    main = tk.Frame(app.root, bg=theme["bg"])
    main.pack(fill="both", expand=True, padx=20, pady=20)
    app.ui_elements["main"] = main

    # Header with theme toggle
    header = tk.Frame(main, bg=theme["bg"])
    header.pack(fill="x", pady=(0, 5))
    app.ui_elements["header"] = header

    # Theme toggle button
    theme_icon = "☀️" if app.is_dark_theme else "🌙"
    app.theme_button = tk.Button(
        header, text=theme_icon, command=app.toggle_theme,
        bg=theme["bg"], fg=theme["accent"], font=("Segoe UI", 16),
        relief="flat", cursor="hand2", bd=0
    )
    app.theme_button.pack(side="right")

    # Title
    ttk.Label(header, text="AI Token Crusher", style="Title.TLabel").place(relx=0.5, rely=0.5, anchor="center")

    # Subtitle
    app.ui_elements["subtitle"] = tk.Label(
        main, text="Cut up to 75% of tokens for Grok • GPT • Claude • Llama",
        fg=theme["text_secondary"], bg=theme["bg"], font=("Segoe UI", 11)
    )
    app.ui_elements["subtitle"].pack(pady=(0, 20))

    # Input + Options layout
    top = tk.Frame(main, bg=theme["bg"])
    top.pack(fill="both", expand=True)
    app.ui_elements["top"] = top

    # Input panel
    input_frame = tk.LabelFrame(top, text=" Input Text / Code ", fg=theme["text_bright"], bg=theme["frame_bg"], font=("Segoe UI", 10, "bold"))
    input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
    app.ui_elements["input_frame"] = input_frame

    app.input_text = scrolledtext.ScrolledText(input_frame, font=("Consolas", 10), bg=theme["input_bg"], fg=theme["input_fg"])
    app.input_text.pack(fill="both", expand=True, padx=10, pady=10)

    btns = tk.Frame(input_frame, bg=theme["frame_bg"])
    btns.pack(pady=5)
    ttk.Button(btns, text="Load File", command=app.load_file).pack(side="left", padx=5)
    ttk.Button(btns, text="Copy Output", command=app.copy_output).pack(side="left", padx=5)

    # Options panel
    options_frame = tk.LabelFrame(top, text=" Optimization Techniques ", fg=theme["text_bright"], bg=theme["frame_bg"], font=("Segoe UI", 10, "bold"))
    options_frame.pack(side="right", fill="y", padx=(10, 0))

    canvas = tk.Canvas(options_frame, bg=theme["frame_bg"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(options_frame, command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=theme["frame_bg"])
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    app.checkbuttons = []
    for key, var in app.options.items():
        name = key.replace("_", " ").title().replace("Shorten", "Short").replace("Remove", "Strip")
        cb = tk.Checkbutton(scroll_frame, text=name, variable=var, bg=theme["frame_bg"], fg=theme["text"], selectcolor=theme["select_bg"])
        cb.pack(anchor="w", pady=2, padx=15)
        app.checkbuttons.append(cb)

    # Crush button
    crush_btn = ttk.Button(main, text="CRUSH TOKENS →", command=app.optimize)
    crush_btn.pack(pady=20)
    app.ui_elements["crush_btn"] = crush_btn

    # Output panel
    output_frame = tk.LabelFrame(main, text=" Crushed Output (AI-Safe) ",
                                 fg=theme["text_bright"], bg=theme["frame_bg"], font=("Segoe UI", 10, "bold"))
    output_frame.pack(fill="both", expand=True, pady=(10, 0))
    app.output_text = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), bg=theme["input_bg"], fg=theme["output_fg"])
    app.output_text.pack(fill="both", expand=True, padx=10, pady=10)
    ttk.Button(output_frame, text="Save Output", command=app.save_output).pack(pady=5)

    # Stats
    app.stats = ttk.Label(main, text="Ready to crush tokens...", foreground=theme["accent_secondary"],
                          font=("Consolas", 11, "bold"), background=theme["frame_bg"])
    app.stats.pack(pady=10)

    # Footer links
    footer = tk.Frame(main, bg=theme["bg"])
    footer.pack(pady=15)
    app.link_labels = []
    for text, url in LINKS:
        link = tk.Label(footer, text=text, fg=theme["accent"], bg=theme["bg"], cursor="hand2", font=("Segoe UI", 9, "underline"))
        link.pack(side="left", padx=20)
        link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
        app.link_labels.append(link)

    app.ui_elements.update({
        "canvas": canvas, "scroll_frame": scroll_frame, "footer": footer,
        "options_frame": options_frame, "output_frame": output_frame
    })