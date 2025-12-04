<!--
Guidance for AI coding agents working on TokenOptimizer
Keep this short, concrete, and code-focused. Update when `main.py` changes.
-->
# Copilot / Agent Instructions — TokenOptimizer (concise)
Summary
- Small, single-process Tkinter desktop app. Primary logic lives in `main.py` (`AITokenCrusher`) and an identical copy in `src/app.py`.
- Purpose: deterministic, offline token minimization for text/code via string + regex transforms (keep substitutions literal).
Where to look (high-value files)
- `main.py` — canonical UI + optimization logic. Edit here for behavior changes.
- `src/app.py` — duplicate of `main.py` (check both when refactoring).
- `README.md` — user-facing description and release link.
- `assets/` — screenshots and static images used in README.
Big-picture architecture (quick)
- UI and logic are co-located in `AITokenCrusher`:
  - `self.options` (dict of `tk.BooleanVar`) drives which transforms run.
  - `apply_optimizations(self, text)` contains the pipeline of regex/string transforms.
  - `optimize()` reads input, calls `apply_optimizations`, updates output and stats.
- The UI auto-creates checkboxes by iterating `self.options` — adding an option is three small steps (see below).
Project-specific conventions (do these exactly)
- Option lifecycle: add a `tk.BooleanVar` key in `self.options` (snake_case), implement the transform in `apply_optimizations`, and the checkbox appears automatically.
- Keep UI references in `self.ui_elements` (avoid top-level globals).
- Theme configuration lives in `self.themes` and is applied with `toggle_theme()` / `apply_theme()`; prefer updating theme maps over hardcoding colors.
Critical transforms and literals to preserve
- `single_line_mode` replaces newlines with the literal character `⏎` (not a word). Do not normalize or escape it.
- Exact mappings (examples taken from `apply_optimizations`):
  - Keywords: `def ` → `d `, `return ` → `r `, `import ` → `i `, `lambda ` → `λ `
  - Booleans: `True` → `1`, `False` → `0`, `None` → `~`
  - Operators: `==` → `≡`, `!=` → `≠`, ` and ` → `∧`, ` or ` → `∨`
  - Print: `print(` → `p(`
- Regex-based removals (comments, docstrings, type hints) are implemented with `re.sub` — preserve the intent and the approximate patterns when editing.
Developer workflows / commands
- Run app locally (PowerShell):
  ```pwsh
  python .\main.py
  ```
- Build a one-file Windows executable (only if requested):
  ```pwsh
  pyinstaller --onefile --windowed main.py
  ```
Testing and verification
- There are no automated tests. When changing transforms: add a small, importable helper function and unit tests under `tests/`.
- Manual verification: run the GUI, paste input, toggle the relevant option(s), press *CRUSH TOKENS →*, and confirm output and the saved `%` metric.
Small-change checklist for agents (use before committing)
1. Add or rename an option: update `self.options` (tk.BooleanVar), add logic in `apply_optimizations`, keep key stable.
2. Avoid changing existing substitution characters (⏎, ≡, ≠, ∧, ∨, λ, ~) unless maintainer OK.
3. For UI changes, reuse `self.ui_elements` and the checkbox auto-creation loop.
4. When refactoring, update both `main.py` and `src/app.py` (one is a copy).
Files to reference in PRs
- `main.py`, `src/app.py`, `README.md`, and `assets/`.
If unclear
- Ask the maintainer whether a transform may change semantics. Default: preserve existing mappings and prefer small, testable helpers.
— End
