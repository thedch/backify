#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset

datetime=$(date "+%B_%d_%Y_%T")
echo "-----> Backfiy at $datetime"
python3 main.py
git add --all
git commit -m "Updated playlists at ${datetime}"
git push
