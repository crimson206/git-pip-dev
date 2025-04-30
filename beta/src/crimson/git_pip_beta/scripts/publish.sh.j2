#!/bin/bash
set -e

INDEX="{{ index }}"
VERSION="{{ version }}"
TAG="gh-pip-${INDEX}-v${VERSION}"

# Ensure tag is added locally
git tag "$TAG"
git push origin "$TAG"

# Create GitHub release with all dist files
gh release create "$TAG" dist/* \
  --title "$TAG" \
  --generate-notes

echo "Release $TAG created and files uploaded."
