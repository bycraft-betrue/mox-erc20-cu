# Run the formatters
format:
    uv run ruff check --select I --fix
    uv run mamushi ./contracts