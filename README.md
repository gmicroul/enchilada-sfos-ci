# OpenClaw Control UI

This repository contains a small PyQt5 application that lets you upload a local directory to a new or existing GitHub repository.

## Features
- Create a repository on GitHub (or reuse an existing one).
- Commit the contents of a chosen directory.
- Push the commit to GitHub.
- Simple, head‑less friendly – you can run it in a Docker container or on a machine without a display by setting `QT_QPA_PLATFORM=offscreen`.

## Configuration

The application expects a valid **GitHub personal access token** with the `repo` scope.  You can provide it either:

1. Via the GUI in the *GitHub Token* field.
2. As an environment variable `GITHUB_TOKEN`.

The GitHub user identity (name/email) is set to a placeholder if not otherwise configured; you may wish to set `git config --global user.name` / `user.email` on the host machine.

## Usage

```bash
# 1. If you have a display
python3 control_gui.py

# 2. Head‑less (e.g., in Docker)
QT_QPA_PLATFORM=offscreen python3 control_gui.py
```

## Security notes

- The token is never written to disk – it is only kept in memory while the GUI is running.
- All network traffic goes directly to GitHub; no proxy or intermediary is used.
- Git commit identity is configurable in the script (currently defaults to `you@example.com` / `Your Name`).

Feel free to fork or extend this project – all code is licensed under MIT.

---

### How to create a GitHub Personal Access Token
1. Go to **GitHub** → **Settings** → **Developer settings** → **Personal access tokens**.
2. Click **Generate new token**.
3. Give it a descriptive **Note** (e.g., "OpenClaw Control UI").
4. Select the **`repo`** scope (or at least **`repo:status`** and **`repo:push`** if you only need read/write).
5. Click **Generate token**.
6. **Copy** the token immediately – you won’t be able to see it again.
7. Use this token in the GUI field or set it as `GITHUB_TOKEN` in your shell:
   ```bash
   export GITHUB_TOKEN="YOUR_TOKEN"
   ```

### Set the default branch to `main`
If you prefer the repository to default to `main` instead of `master`, rename the branch locally and push it:

```bash
cd /home/user/.openclaw/workspace/qt5-github
# Rename local branch
git branch -m master main
# Push the new branch and set upstream
git push -u origin main
```

After pushing, you can update the repository settings on GitHub to make `main` the default branch if it isn’t already.
