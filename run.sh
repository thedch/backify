#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset

python3 main.py
git add --all
datetime=$(date "+%B_%d_%Y_%T")
git commit -m "Updated playlists at ${datetime}"
git push
