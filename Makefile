.PHONY: setup run clean help

PYTHON = python3
VENV = maes-simulation/venv
SIM_DIR = maes-simulation

help:
	@echo "SEDS Framework Management Commands:"
	@echo "  make setup   - Install dependencies in the venv"
	@echo "  make run     - Execute the SEDS simulation protocol"
	@echo "  make clean   - Remove cache and telemetry artifacts"

setup:
	$(VENV)/bin/pip install -e .

run:
	cd $(SIM_DIR) && ../$(VENV)/bin/python3 test_run.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(SIM_DIR)/artifacts/telemetry/*
