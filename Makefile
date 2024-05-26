include .env

# CODE CHECKS
static-check:
	@echo "" && echo "Check and fix code (pylint, isort)!"
	@poetry run ruff check --fix
	@echo "" && echo "Format code!"
	@poetry run ruff format
	@echo "" && echo "Check annotations (mypy)!"
	@poetry run mypy .
	@echo ""

# POSTGRESQL
postgres-start:
	docker run -d --rm --name ${POSTGRES_CONTAINER_NAME} \
	-e POSTGRES_USER=${POSTGRES_USER} \
	-e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
	-e POSTGRES_DB=${POSTGRES_DB} \
	-p 5432:${POSTGRES_PORT} postgres:12.18

postgres-stop:
	docker stop clean_domain


# ALEMBIC MIGRATION
name?=blog
upgrade-revision:
	poetry run alembic -n $(name) upgrade head

current-revision:
	poetry run alembic -n $(name) current

autogenerate-revision:
	poetry run alembic -n $(name) revision --autogenerate -m "$(message)"
