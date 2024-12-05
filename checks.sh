#!/bin/bash
set -eu
python -m ruff format docs src
python -m ruff check --fix --unsafe-fixes docs src
python -m mypy src
