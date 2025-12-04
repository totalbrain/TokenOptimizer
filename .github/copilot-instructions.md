<!--
Guidance for AI coding agents working on TokenOptimizer
Keep this short, concrete, and code-focused. Update when `main.py` changes.
-->

# Copilot / Agent Instructions — TokenOptimizer

Summary
- This repository is a small single-file Python desktop app: `main.py` implements a Tkinter GUI and the token-optimization logic in the `AITokenCrusher` class.
- Primary goal: conservative, offline token minimization for text/code using deterministic string and regex transforms.

Where to look
- Core app and logic: `main.py` (UI, options, `apply_optimizations`).
- Project description / releases: `README.md`.
- Static assets: `assets/` (images, screenshots).
- Contribution workflow: `feature_request.md` describes feature requests.

Big-picture architecture
- Single-process GUI: `AITokenCrusher` constructs the UI and stores state in `self.options` (a dict of `tk.BooleanVar`) and `self.ui_elements`.
- The optimization pipeline is implemented in `apply_optimizations(self, text)` and applied from `optimize()`.
- UI <-> logic boundary: do not embed heavy business logic in widget callbacks; extend or refactor `apply_optimizations` when adding new transforms.

Project-specific patterns & conventions
- Option keys are snake_case strings in `self.options` (e.g. `remove_comments`, `single_line_mode`). Follow this pattern when adding flags.
- Checkbuttons are created by iterating `self.options`; adding a new option requires:
  1) add a `tk.BooleanVar` entry to `self.options` in `__init__`,
  2) reference it in `apply_optimizations`, and
  3) let the existing loop auto-create the checkbox.
- UI state containers: use `self.ui_elements` to store references (avoid creating loose globals).
- Theme handling: themes live in `self.themes` and switching occurs via `toggle_theme()` + `apply_theme()` — prefer updating these maps rather than hardcoding colors.

Optimization details agents must preserve
- `apply_optimizations` mixes regex and string replacements. Important examples to preserve exactly:
  - Newline single-line mode uses the literal character `⏎` (replaces `\n`).
  - Boolean/text replacements: `True`→`1`, `False`→`0`, `None`→`~`.
  - Shortened keywords: `def `→`d `, `return `→`r `, `import `→`i `, `lambda `→`λ `.
  - Operator replacements: `==`→`≡`, `!=`→`≠`, ` and `→`∧`, ` or `→`∨`.
  - Short print: `print(` → `p(` (note the removed whitespace pattern).
- These substitutions are intentionally non-standard/unicode; preserve their literal characters and avoid accidentally normalizing or escaping them.

Run / build / debug
- Run locally: `python main.py` (uses system Python with Tkinter). On Windows PowerShell:
  ```pwsh
  python .\main.py
  ```
- Packaging (not present in repo): releases show a Windows `.exe`. If creating builds, use a one-file GUI build (example):
  ```pwsh
  pyinstaller --onefile --windowed main.py
  ```
  Only add packaging config if requested; keep runtime behaviour deterministic.

Testing and verification
- There are no automated tests. Changes that affect behavior require manual testing: launch the GUI, paste sample code, toggle options, and verify `apply_optimizations` output.
- When adding new transforms, include small unit-testable helper functions and a minimal manual verification harness that calls `apply_optimizations(text)`.

Safe editing guidance for agents
- Be conservative: prefer adding small helper functions over large refactors.
- Keep public names and option keys stable (changing keys requires UI and saved-state updates).
- When introducing new dependencies, document why and prefer pure-Python stdlib solutions (this repo intentionally targets offline usage).

Files to reference in PRs
- `main.py` — implementation and starting point for most changes.
- `README.md` — user-facing description, check for mismatch with behaviour.
- `assets/` — update assets if UI text or screenshots change.

If something is unclear
- Ask the maintainer which transforms are allowed to change semantics; otherwise assume existing substitutions must remain literal and reversible for humans.

— End —
