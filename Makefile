.PHONY: lint test run up down migrate

lint:
    @echo "Running linters..."
    @black --check app || (echo "Run 'black app' to fix formatting"; exit 1)
    @isort --check-only app
    @flake8 app

test:
    @echo "Running tests..."
    @pytest app/tests -v --cov=app --cov-report=term-missing

run:
    @docker-compose up -d --build

stop:
    @docker-compose down

clean:
    @find . -type d -name "__pycache__" -exec rm -r {} +
    @docker-compose down -v

clean-imports:
    autoflake --remove-all-unused-imports --in-place app/*.py app/tests/*.py

up:
    @echo "Starting containers..."
    @docker-compose up -d

down:
    @echo "Stopping containers..."
    @docker-compose down

migrate:
    @echo "Applying database migrations..."
    @docker-compose exec api python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

typecheck:
    @echo "Running typecheck..."
    @mypy app
