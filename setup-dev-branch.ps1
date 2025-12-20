# setup-dev-branch.ps1 - AI Token Crusher Dev Branch Setup

$Token = "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"
$Owner = "totalbrain"
$Repo = "TokenOptimizer"

$Headers = @{
    Authorization = "Bearer $Token"
    Accept = "application/vnd.github+json"
}

Write-Host "Creating dev branch setup..." -ForegroundColor Cyan

# 1. Create dev branch from main
git checkout main
git pull origin main
git checkout -b dev
git push origin dev

# 2. Set dev as default branch
Invoke-RestMethod -Method Patch -Uri "https://api.github.com/repos/$Owner/$Repo" -Headers $Headers -Body (@{
    default_branch = "dev"
} | ConvertTo-Json)

# 3. Protect main branch (require PR, 1 approval)
$protect = @{
    required_pull_request_reviews = @{
        required_approving_review_count = 1
    }
    enforce_admins = $true
}
Invoke-RestMethod -Method Put -Uri "https://api.github.com/repos/$Owner/$Repo/branches/main/protection" -Headers $Headers -Body ($protect | ConvertTo-Json -Depth 10)

# 4. Update README with workflow
$readme_content = @"
## Workflow
- Fork the repo
- Create feature/issue-# branch from dev
- Work on the issue
- PR to dev
- After tests/approve, merge to dev
- For release: PR dev to main
"@
$readme_base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($readme_content))
$existing_readme = Invoke-RestMethod "https://api.github.com/repos/$Owner/$Repo/contents/README.md" -Headers $Headers
Invoke-RestMethod -Method Put -Uri "https://api.github.com/repos/$Owner/$Repo/contents/README.md" -Headers $Headers -Body (@{
    message = "Update README with workflow"
    content = $readme_base64
    sha = $existing_readme.sha
} | ConvertTo-Json)

# 5. Create GitHub Actions for tests on dev
mkdir .github/workflows -ErrorAction SilentlyContinue
$actions_yaml = @"
name: Test Dev Branch
on:
  push:
    branches: [dev]
  pull_request:
    branches: [dev]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install deps
        run: pip install pytest tiktoken
      - name: Run tests
        run: pytest tests/ -v
"@
$actions_yaml | Out-File -FilePath ".github/workflows/test-dev.yml" -Encoding utf8

# 6. Commit and push
git add .
git commit -m "setup: dev branch workflow, protected main, actions tests"
git push origin dev

Write-Host "All done! Dev branch is ready." -ForegroundColor Green
Write-Host "Contributors now PR to dev, merge after tests, then PR dev to main for release." -ForegroundColor Green