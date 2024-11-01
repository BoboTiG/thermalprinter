#!/bin/bash
set -eu
python -m ruff format src
python -m ruff check --fix --unsafe-fixes src
python -m mypy src
