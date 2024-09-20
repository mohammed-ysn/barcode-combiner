.PHONY: lint format check

# Lint target
lint: format check

format:
	ruff format .

check:
	ruff check --fix .
