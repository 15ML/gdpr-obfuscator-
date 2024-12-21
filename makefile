# Default shell
SHELL=/bin/bash

# Setup the virtual environment and install dependencies
setup:
    python3 -m venv venv
    source venv/bin/activate; \
    pip install -r requirements.txt

# Command to activate the virtual environment
activate:
    @echo "To activate the project's virtual environment, run 'source venv/bin/activate'"

# Set PYTHONPATH
export-path:
    export PYTHONPATH=$$(pwd)

# Run tests with pytest and testdox format
test:
    source venv/bin/activate; \
    pytest --testdox tests/

# Run all setup tasks
all: setup activate export-path test

# This .PHONY line tells Make which targets are not files
.PHONY: setup activate export-path test all
