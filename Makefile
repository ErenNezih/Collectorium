# Collectorium - Development Makefile
# Quick commands for common tasks

.PHONY: help install test lint format clean run migrate

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install all dependencies
	pip install -e ".[dev,test,lint]"
	pre-commit install

test:  ## Run tests with pytest
	pytest -v --cov=. --cov-report=html

test-fast:  ## Run tests without coverage
	pytest -v -x

lint:  ## Run linting checks
	ruff check .
	black --check .
	isort --check-only .

format:  ## Auto-format code
	black .
	isort .
	ruff check --fix .

clean:  ## Clean up generated files
	find . -type d -name  "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf dist/
	rm -rf build/

run:  ## Run development server
	python manage.py runserver

migrate:  ## Run database migrations
	python manage.py makemigrations
	python manage.py migrate

shell:  ## Open Django shell
	python manage.py shell

collectstatic:  ## Collect static files
	python manage.py collectstatic --noinput

createsuperuser:  ## Create a superuser
	python manage.py createsuperuser

loaddata:  ## Load fixture data
	python manage.py loaddata fixtures/categories.json

check:  ## Run Django system check
	python manage.py check

pre-commit:  ## Run pre-commit hooks
	pre-commit run --all-files

