#!/bin/bash
set -euo pipefail

echo "🛠 Installing GitHub CLI (gh)..."

# Install gh CLI (Ubuntu/Debian)
sudo apt update
sudo apt install -y gh

echo "✅ gh installed"

# Login using GitHub token (from GitHub Actions secret)
# GH_TOKEN must be set as an environment variable
if [ -z "${GH_TOKEN:-}" ]; then
  echo "❌ GH_TOKEN is not set"
  exit 1
fi

echo "$GH_TOKEN" | gh auth login --with-token

# Verify authentication
gh auth status

echo "✅ gh authenticated successfully"
