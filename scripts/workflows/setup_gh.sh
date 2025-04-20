#!/bin/bash
set -euo pipefail

echo "🛠 Installing GitHub CLI (gh)..."

# Install gh (if needed)
sudo apt update
sudo apt install -y gh

echo "✅ gh installed"

# Just check status; login is automatic in GitHub Actions with GH_TOKEN
echo "🔒 Checking GitHub CLI authentication..."

if ! gh auth status; then
  echo "❌ gh auth failed. Check GH_TOKEN or GitHub Actions secrets."
  exit 1
fi

echo "✅ gh authenticated successfully"
