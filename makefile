# Variables
VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
ACTIVATE := . $(VENV_DIR)/bin/activate

# Default target
.DEFAULT_GOAL := help

# Help target to list available commands
help:
	@echo "Available targets:"
	@echo "  make venv          - Create the virtual environment"
	@echo "  make activate      - Activate the virtual environment"

# Create virtual environment
venv:
	python3 -m venv $(VENV_DIR)

# Activate virtual environment
activate:
	@echo "Run 'source $(VENV_DIR)/bin/activate' to activate the virtual environment."
