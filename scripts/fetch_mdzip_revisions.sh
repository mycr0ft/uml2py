#!/usr/bin/env bash
# Fetch mdzip revision pairs for check_mdzip_diff.py (third-party model
# snapshots; NOT committed).  Uses /tmp/mdzip_history.json from the scour
# step or re-derives pairs from scripts/mdzip_corpus_tools.py scour data.
set -euo pipefail
DEST="${MDZIP_REVISIONS:-/mnt/TBFox/mdzip_corpus/_revisions}"
echo "Revision pairs are fetched via the GitHub API per-commit."
echo "See scripts/mdzip_corpus_tools.py scour output + /tmp/fetch_pairs.py"
echo "pattern: for each mdzip path with >=2 commits, download old/new blobs."
mkdir -p "$DEST"
ls -la "$DEST" 2>/dev/null || true