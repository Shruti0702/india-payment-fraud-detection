#!/usr/bin/env bash
# Push PayGuard AI to GitHub. Run after: gh auth login
set -euo pipefail

REPO_NAME="${1:-india-payment-fraud-detection}"
VISIBILITY="${2:-public}"

cd "$(dirname "$0")/.."

if ! gh auth status &>/dev/null; then
  echo "Not logged in. Run: gh auth login"
  exit 1
fi

GITHUB_USER=$(gh api user -q .login)
REMOTE="git@github.com:${GITHUB_USER}/${REPO_NAME}.git"

if ! gh repo view "${GITHUB_USER}/${REPO_NAME}" &>/dev/null; then
  gh repo create "${REPO_NAME}" --${VISIBILITY} --source=. --remote=origin --description "AI fraud detection for Indian digital payments (UPI/IMPS/NEFT) — Django + scikit-learn"
else
  git remote add origin "${REMOTE}" 2>/dev/null || git remote set-url origin "${REMOTE}"
fi

git branch -M main
git push -u origin main

echo ""
echo "Repository: https://github.com/${GITHUB_USER}/${REPO_NAME}"
