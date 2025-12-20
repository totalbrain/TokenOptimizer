# create_issue.py - Create new GitHub Issue for AI Token Crusher
import requests
import sys

TOKEN = "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"
OWNER = "totalbrain"
REPO = "TokenOptimizer"
PROJECT_ID = "1"  # Global ID or number for the project

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Issue details
title = "Refactor: Separate Core Logic from UI for CLI/GUI Independence"
body = """
**Description**
Separate the core optimization logic from the UI to make the app modular. The core should handle input/output independently (e.g., console, file, event viewer) without relying on Tkinter. This is like logging systems that output to multiple sinks.

**Why this is useful?**
- Enables CLI mode (--terminal) without GUI dependencies
- Makes output flexible (console, file, notification, etc.)
- Improves maintainability and testability
- Allows future extensions (web API, integration with other tools)
- Reduces main.py length by modularizing

**Implementation Ideas**
- Create src/core.py for all optimizations (apply_optimizations)
- Use abstract I/O handlers (e.g., ConsoleOutput, FileOutput)
- Main entry: Check args --gui / --terminal and load appropriate mode
- Example structure:
  - src/core.py: Pure functions for token crushing
  - src/ui.py: GUI logic (Tkinter)
  - src/cli.py: Console logic (argparse)
  - main.py: Parse args and route to UI or CLI

**Additional context**
- Inspired by logging modules (console, file handlers)
- Relates to issue #X (CLI version)
- Test with pytest: Core independent of UI

**Priority**
- [x] Must-have
"""

labels = ["enhancement", "priority:high", "refactor"]

# Create Issue
issue_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
data = {
    "title": title,
    "body": body,
    "labels": labels
}
response = requests.post(issue_url, headers=HEADERS, json=data)
if response.status_code == 201:
    issue = response.json()
    issue_number = issue["number"]
    print(f"Issue #{issue_number} created successfully!")
else:
    print(f"Error creating issue: {response.text}")
    sys.exit(1)

# Add Issue to Project Board
gql_body = {
    "query": f'mutation {{ addProjectV2ItemById(input: {{projectId: "{PROJECT_ID}" contentId: "{issue["id"]}"}}) {{ item {{ id }} }} }}'
}
gql_response = requests.post("https://api.github.com/graphql", headers=HEADERS, json=gql_body)
if gql_response.status_code == 200:
    print("Issue added to Project Board!")
else:
    print(f"Error adding to board: {gql_response.text}")
