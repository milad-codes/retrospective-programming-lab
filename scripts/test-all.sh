#!/usr/bin/env bash
# Runs every exercise's tests. Python 3.10+ and Node 22.18+ (which runs TypeScript directly); no installs needed.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s python -t python
(cd typescript && node --test)
