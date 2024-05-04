static-check:
	@echo "" && echo "Check and fix code (pylint, isort)!"
	@poetry run ruff check --fix
	@echo "" && echo "Format code!"
	@poetry run ruff format
	@echo "" && echo "Check annotations (mypy)!"
	@poetry run mypy .
	@echo ""
