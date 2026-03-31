"""
Makefile for cp_mes Django project.
"""

.PHONY: help install dev run test clean migrate docker-up docker-down lint format

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make dev          - Install development dependencies"
	@echo "  make run          - Run development server"
	@echo "  make test         - Run tests with coverage"
	@echo "  make migrate      - Run database migrations"
	@echo "  make clean        - Clean up generated files"
	@echo "  make docker-up    - Start Docker containers (production)"
	@echo "  make docker-dev   - Start Docker containers (development)"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make lint         - Run code linting"
	@echo "  make format       - Format code with black and isort"

install:
	pip install -r requirements/production.txt

dev:
	pip install -r requirements/development.txt

run:
	python manage.py runserver 0.0.0.0:8000

test:
	pytest tests/ -v --cov=apps --cov-report=html --cov-report=term

migrate:
	python manage.py makemigrations
	python manage.py migrate

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-dev:
	docker-compose -f docker/docker-compose.dev.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down
	docker-compose -f docker/docker-compose.dev.yml down

lint:
	flake8 apps/ config/ tests/
	mypy apps/ config/

format:
	black apps/ config/ tests/
	isort apps/ config/ tests/

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

db-shell:
	python manage.py dbshell

collectstatic:
	python manage.py collectstatic --noinput
