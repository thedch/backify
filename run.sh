#!/bin/bash

python main.py
git add --all
datetime=$(date "+%B_%d_%Y_%T")
git commit -m "Updated playlists at $(datetime)"
git push
