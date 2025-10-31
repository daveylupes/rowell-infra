# Rowell Infra Makefile
# Alchemy for Africa: Stellar + Hedera APIs & Analytics

.PHONY: help install dev build test clean docker-up docker-down docker-logs

# Default target
help:
	@echo "Rowell Infra - Alchemy for Africa"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install     - Install all dependencies"
	@echo "  dev         - Start development environment"
	@echo "  build       - Build all components"
	@echo "  test        - Run all tests"
	@echo "  clean       - Clean build artifacts"
	@echo "  docker-up   - Start Docker services"
	@echo "  docker-down - Stop Docker services"
	@echo "  docker-logs - Show Docker logs"
	@echo "  setup       - Complete setup for development"
	@echo ""
	@echo "Python virtual environment helpers:"
	@echo "  api-install      - Install API dependencies in venv"
	@echo "  sdk-python-install - Install Python SDK dependencies in venv"
	@echo "  api-shell        - Open Python shell with API venv"
	@echo "  sdk-python-shell - Open Python shell with SDK venv"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	cd api && python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	cd sdk/js && npm install
	cd sdk/python && python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -e .
	cd sdk/flutter && flutter pub get
	cd cli && npm install
	@echo "Dependencies installed!"

# Development setup
dev: docker-up
	@echo "Starting development environment..."
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "Prometheus: http://localhost:9090"

# Build all components
build:
	@echo "Building all components..."
	cd api && . venv/bin/activate && python3 -m py_compile main.py
	cd sdk/js && npm run build
	cd sdk/python && . venv/bin/activate && python3 setup.py build
	cd sdk/flutter && flutter build
	cd cli && npm run build
	@echo "Build complete!"

# Run tests
test:
	@echo "Running tests..."
	cd api && . venv/bin/activate && python3 -m pytest tests/ -v
	cd sdk/js && npm test
	cd sdk/python && . venv/bin/activate && python3 -m pytest tests/ -v
	cd cli && npm test
	@echo "Tests complete!"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "venv" -exec rm -rf {} +
	@echo "Clean complete!"

# Docker commands
docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 10
	@echo "Services started!"

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down
	@echo "Services stopped!"

docker-logs:
	docker-compose logs -f

# Complete setup
setup: install docker-up
	@echo "Setting up database..."
	cd api && . venv/bin/activate && python3 -c "from api.core.database import init_db; import asyncio; asyncio.run(init_db())"
	@echo "Setup complete!"
	@echo ""
	@echo "🚀 Rowell Infra is ready!"
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"
	@echo "Grafana: http://localhost:3000 (admin/admin)"

# Development helpers
api-logs:
	docker-compose logs -f api

db-shell:
	docker-compose exec postgres psql -U rowell -d rowell_infra

redis-shell:
	docker-compose exec redis redis-cli

# Python virtual environment helpers
api-shell:
	cd api && . venv/bin/activate && python3

sdk-python-shell:
	cd sdk/python && . venv/bin/activate && python3

api-install:
	cd api && python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

sdk-python-install:
	cd sdk/python && python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -e .

# Production deployment
deploy-prod:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Production deployment complete!"

# Security scan
security-scan:
	@echo "Running security scan..."
	cd api && . venv/bin/activate && safety check
	cd sdk/js && npm audit
	cd sdk/python && . venv/bin/activate && safety check
	@echo "Security scan complete!"

# Format code
format:
	@echo "Formatting code..."
	cd api && . venv/bin/activate && black . && isort .
	cd sdk/js && npm run format
	cd sdk/python && . venv/bin/activate && black . && isort .
	@echo "Code formatted!"

# Lint code
lint:
	@echo "Linting code..."
	cd api && . venv/bin/activate && flake8 . && mypy .
	cd sdk/js && npm run lint
	cd sdk/python && . venv/bin/activate && flake8 . && mypy .
	@echo "Linting complete!"

# Generate documentation
docs:
	@echo "Generating documentation..."
	cd api && mkdocs serve
	@echo "Documentation available at http://localhost:8001"

# Backup database
backup-db:
	@echo "Backing up database..."
	docker-compose exec postgres pg_dump -U rowell rowell_infra > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backup complete!"

# Restore database
restore-db:
	@echo "Restoring database..."
	@read -p "Enter backup file name: " file; \
	docker-compose exec -T postgres psql -U rowell -d rowell_infra < $$file
	@echo "Database restore complete!"
