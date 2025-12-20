


# create-cli-issue.ps1 - Creates CLI + GUI dual mode feature request (100% working)

$Repo = "totalbrain/TokenOptimizer"

Write-Host "Creating CLI + GUI Dual Mode Feature Request..." -ForegroundColor Cyan

gh issue create --repo $Repo --title "[Feature] Dual Mode: CLI + GUI with full optimization control via flags" --label "enhancement" --label "good first issue" --label "cli" --body @"
---
name: Feature Request
labels: enhancement, good first issue, cli
---

### Describe the feature

Add full dual-mode support (CLI + GUI):

```bash
python main.py                    # GUI (default)
python main.py --gui              # Force GUI
python main.py --terminal --file input.py
python main.py --cli --dir ./project/ --single-line --shorten-keywords
```

All current optimization options must be controllable via CLI flags.

### Why is this useful?

- Automation & scripting
- Batch processing
- CI/CD integration
- VS Code tasks / Git hooks
- Headless servers & Docker
- Much faster for power users

### CLI Flags to support

| Flag                        | Description                              |
|----------------------------|-------------------------------------------|
| --terminal / --cli         | Run in terminal mode                      |
| --gui                      | Force GUI mode                            |
| --file PATH                | Input file                                |
| --dir PATH                 | Process all files in directory            |
| --output PATH              | Output file (default: stdout)             |
| --remove-comments          | Enable comment removal                    |
| --remove-docstrings        | Enable docstring removal                  |
| --shorten-keywords         | def → d, return → r, etc.                 |
| --replace-booleans         | True→1, False→0, None→~                   |
| 
| --use-short-operators      | ==→≡, !=→≠, and→∧, or→∨                  |
| --single-line              | Replace newlines with ⏎                   |
| --unicode-shortcuts        | in→∈, not in→∉                            |
| --config FILE              | Load settings from JSON/YAML              |

### Example usage

```bash
python main.py --terminal --file prompt.py --single-line --shorten-keywords > crushed.py
find . -name "*.py" -exec python main.py --cli --file {} \;
```

### Priority
- [x] Must-have
"@

Write-Host "Feature Request created successfully!" -ForegroundColor Green
Write-Host "View all issues: https://github.com/$Repo/issues" -ForegroundColor Yellow