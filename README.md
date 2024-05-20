# clean_domain

## Prerequisites
Install following requirements to use this setup.
* pyenv
* poetry
* make

### Pyenv
Pyenv is used to create and manage different virtual python environments.
In order to use it first create and activate an environment.

Create new virtual env and activate it (see [here](https://realpython.com/intro-to-pyenv/)):

`pyenv virtualenv 3.10.13 clean_domain`

`pyenv activate clean_domain`

### Poetry
Poetry is used to configure virtualenvs. It is utilized to add and manage dependencies
for development and production.
Follow [instructions](https://python-poetry.org/docs/#installing-with-the-official-installer) on how to install poetry.

Used poetry version: `POETRY_VERSION=1.8.2`

Install with: `curl -sSL https://install.python-poetry.org | POETRY_VERSION=X.X.X python3 -`

Add dependencies with `poetry add "numpy@*"`. Do not pin down specific version in order to allow updates.
Add development dependencies with `poetry add "pytest@*" -D` to allow excluding them when building a docker image.

## Static checks
### Typing
`poetry run mypy .` or `make static-check`

### Formatter
`poetry run ruff format .` Add `--check` for dry run.


### Testing
For integration tests with _Postgresql_ make sure a postgres instance is running: `make postgres-start`.
User, password, port etc. must be given in `.env` on project level.
