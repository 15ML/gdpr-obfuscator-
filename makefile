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
	python3 -m venv venv
	$(ACTIVATE_VENV) && pip install -r requirements.txt
	@echo "Project setup complete."

# Command to activate the virtual environment
activate:
	@echo "To activate the project's virtual environment, run 'source venv/bin/activate'"

# Set PYTHONPATH
export-pythonpath:
	export PYTHONPATH=$$(pwd)
	@echo "PYTHONPATH set to current directory."

# Run tests with pytest and testdox format
run-tests: load-env
	@echo "Running tests..."
	$(ACTIVATE_VENV) && pytest --testdox tests/

# Run all setup tasks
all: install-dependencies export-pythonpath run-tests

# This .PHONY line tells Make which targets are not files
.PHONY: install-dependencies export-pythonpath run-tests all load-env activate
