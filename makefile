# Default shell
SHELL=/bin/bash

# Define the command for activating the virtual environment
ACTIVATE_VENV=source venv/bin/activate

# Load environment variables from the .env file
load-env:
	@echo "Loading environment variables..."
	@python -c "from dotenv import load_dotenv; load_dotenv(verbose=True)"

# Set up the virtual environment and install dependencies
install-dependencies: load-env
	@echo "Setting up the project environment..."
	@if [ ! -d "venv" ]; then python3 -m venv venv; fi
	$(ACTIVATE_VENV) && venv/bin/python -m pip install -r requirements.txt
	@echo "Project setup complete."

# Command to activate the virtual environment
activate:
	@echo "To activate the project's virtual environment, run 'source venv/bin/activate'"

# Run tests with pytest and Testdox format
run-tests: load-env
	@echo "Running tests..."
	$(ACTIVATE_VENV) && export PYTHONPATH=$$(pwd) && pytest --testdox tests/

# Run black for code formatting
run-black:
	$(ACTIVATE_VENV) && black --line-length 79 ./src/* ./tests/*

# Run all setup tasks
all: install-dependencies run-tests

# Run checks and formatting
run-checks: run-black run-tests

# This .PHONY line tells Make which targets are not files
.PHONY: install-dependencies run-tests run-black all run-checks load-env activate
