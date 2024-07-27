env:
	pip install poetry
	pip install pre-commit
	poetry install
	pre-commit install
	poetry shell

requirements:
	rm -rf .venv
	rm -f poetry.lock
	poetry install --without testing,linting
	poetry shell
	pip freeze > requirements.txt
	rm -rf .venv
	rm -f poetry.lock

