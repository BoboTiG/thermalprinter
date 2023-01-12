#!/bin/bash
set -eu
python -m isort thermalprinter tests
python -m black thermalprinter tests
python -m flake8 thermalprinter tests
python -m pylint thermalprinter
python -m mypy thermalprinter
