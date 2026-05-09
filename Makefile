.PHONY: setup run clean help

PYTHON = python3
VENV = venv

help:
	@echo "MAES Simulation Management Commands:"
	@echo "  make setup   - Install dependencies in the venv"
	@echo "  make run     - Execute the MAES simulation"
	@echo "  make clean   - Remove cache and telemetry artifacts"

setup:
	$(VENV)/bin/pip install -e .

run:
	$(VENV)/bin/python3 test_run.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf artifacts/telemetry/*
