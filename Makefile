install: .check-venv .update-pip ## Install project
	pip install --editable .

test: .check-venv ## Run tests
	python -m pytest

lint: .clean tool ## Run linters
	python -m black .
	python -m ruff --fix .
	python -m mypy .

check:
	python -m pip install ".[dev]"
	rm -rf build/
	python -m black --check .
	python -m ruff .
	python -m mypy --check .

tool: .check-venv ## Install development tools
	python -m pip install  --editable ".[dev]"

help: ## Show this help message
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Delete the build directory
.clean:
	rm -rf build/

# Update pip
.update-pip: .check-venv
	python -m pip install --upgrade pip

# Check if in Python virtual environment
.check-venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Not in a Python virtual environment. Activate the virtual environment and try again."; \
		exit 1; \
	fi
