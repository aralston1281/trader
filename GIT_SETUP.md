# GitHub Setup Guide

Quick guide to push this project to GitHub.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Name your repository (e.g., `options-bot`)
3. Choose **Private** (recommended) or Public
4. **Do NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Initialize Local Git Repository

Open a terminal in the `options_bot` directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit: Options Bot Framework v1.0"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/options-bot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify .gitignore

Make sure sensitive files are NOT committed:

```bash
# These should NOT be in git:
# - .env (your actual config with webhook URL)
# - data/
# - logs/
# - __pycache__/
# - *.pyc

# These SHOULD be in git:
# - .env.example (template without secrets)
# - All .py files
# - README.md
# - config/universe.csv
```

## Step 4: Set Repository Settings

### Make Repository Private (Recommended)

Your `.env` file contains your Discord webhook URL. While `.gitignore` prevents it from being committed, it's safer to keep the repo private.

1. Go to repository Settings
2. Scroll to "Danger Zone"
3. Click "Change visibility" → Private

### Add Repository Description

Add a description like:
```
Automated options trading ideas generator with Discord notifications
```

Add topics:
- `options-trading`
- `trading-bot`
- `python`
- `discord`
- `finance`
- `automated-trading`

## Step 5: Create a Personal .env File

On each machine where you clone/run this:

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/options-bot.git
cd options-bot

# Create your .env from the example
cp .env.example .env

# Edit with your settings
nano .env  # or use any text editor
```

## Common Git Workflows

### Updating Code

```bash
# Check status
git status

# Stage changes
git add .

# Commit with message
git commit -m "Add new feature: XYZ"

# Push to GitHub
git push
```

### Pulling Updates (on another machine)

```bash
git pull
```

### Branching for Experiments

```bash
# Create and switch to new branch
git checkout -b experimental-feature

# Make changes, commit them
git add .
git commit -m "Experimental change"

# Push branch to GitHub
git push -u origin experimental-feature

# Switch back to main
git checkout main

# Merge if successful
git merge experimental-feature
```

## Protect Sensitive Data

### If You Accidentally Commit .env

```bash
# Remove from git but keep local file
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from git"

# Push
git push
```

**Important**: If you pushed `.env` to GitHub, anyone who had access can still see it in the history. You should:

1. Delete and recreate your Discord webhook
2. Change any API keys
3. Consider using `git filter-branch` or BFG Repo-Cleaner to remove from history

### Use Git Secrets (Optional)

Install git-secrets to prevent committing sensitive data:

```bash
# Install (Mac)
brew install git-secrets

# Install (Linux)
git clone https://github.com/awslabs/git-secrets
cd git-secrets
sudo make install

# Set up
cd /path/to/options-bot
git secrets --install
git secrets --register-aws
git secrets --add 'DISCORD_WEBHOOK_URL.*'
git secrets --add '[A-Za-z0-9/+=]{40,}'  # Catch API keys
```

## GitHub Actions (Optional)

Create `.github/workflows/test.yml` for automatic testing:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest -m "not slow"  # Skip slow tests that call external APIs
```

## Collaboration

### Adding Collaborators

If working with others:

1. Go to repository Settings → Collaborators
2. Add team members
3. They can clone and contribute

### Pull Request Workflow

1. Collaborator forks repo or creates branch
2. Makes changes
3. Opens Pull Request
4. You review and merge

## Deployment Secrets

For deploying to cloud:

### Using GitHub Secrets

1. Go to Settings → Secrets and variables → Actions
2. Add secrets:
   - `DISCORD_WEBHOOK_URL`
   - Any API keys
3. Reference in GitHub Actions:
   ```yaml
   env:
     DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
   ```

### Using Environment Files

For Docker or VMs:

1. Keep `.env` files on the server only
2. Use environment-specific configs:
   - `.env.development`
   - `.env.production`
3. Load appropriate file based on environment

## Backup Strategy

### Regular Commits

Commit frequently:
```bash
git add .
git commit -m "Update: [description]"
git push
```

### Tags for Releases

Mark stable versions:
```bash
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"
git push origin v1.0.0
```

### Backup .env Separately

Since `.env` is not in git, back it up separately:
```bash
# Encrypt and store somewhere safe
gpg -c .env
# This creates .env.gpg which you can backup

# To decrypt later:
gpg .env.gpg
```

## Troubleshooting

### "Permission denied (publickey)"

Set up SSH keys or use HTTPS with personal access token:
```bash
# Use HTTPS instead
git remote set-url origin https://github.com/YOUR_USERNAME/options-bot.git
```

### "Large files warning"

Git doesn't handle large files well. If you have large data files:
```bash
# Add to .gitignore
echo "data/*.csv" >> .gitignore
```

Consider Git LFS for large files:
```bash
git lfs install
git lfs track "*.csv"
```

### "Merge conflicts"

```bash
# Pull latest
git pull

# Fix conflicts in files
# Look for <<<<<<< markers

# Stage resolved files
git add .

# Complete merge
git commit -m "Resolve merge conflicts"
```

## Resources

- Git documentation: https://git-scm.com/doc
- GitHub guides: https://guides.github.com/
- Git cheat sheet: https://education.github.com/git-cheat-sheet-education.pdf

## Quick Reference

```bash
# Common commands
git status              # Check status
git add .              # Stage all changes
git commit -m "msg"    # Commit changes
git push               # Push to GitHub
git pull               # Pull from GitHub
git log                # View commit history
git diff               # See changes
git branch             # List branches
git checkout -b name   # Create new branch
git merge name         # Merge branch
git clone URL          # Clone repository
```

