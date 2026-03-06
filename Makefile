.PHONY: dev api web test lint eval deploy-staging deploy-prod clean

# Start all services locally (< 60 seconds target)
dev:
	docker-compose up -d postgres neo4j redis minio meilisearch ollama
	@echo "Waiting for services to be healthy..."
	@sleep 10
	@echo "Services ready. Run 'make api' and 'make web' in separate terminals."

# Start FastAPI backend with hot reload
api:
	cd apps/api && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start Next.js frontend with hot reload
web:
	cd apps/web && npm run dev

# Run all tests
test:
	cd apps/api && pytest --cov=. --cov-report=term-missing
	cd apps/web && npm test

# Run linters
lint:
	cd apps/api && ruff check . && ruff format --check .
	cd apps/web && npm run lint

# Format code
format:
	cd apps/api && ruff format .
	cd apps/web && npm run format

# Evaluate prompts against golden dataset
eval:
	cd eval && python run_eval.py

# Database migrations
migrate:
	cd apps/api && alembic upgrade head

# Generate new migration
migration:
	cd apps/api && alembic revision --autogenerate -m "$(msg)"

# Deploy to staging (auto on merge to main)
deploy-staging:
	kubectl apply -f infra/k3s/staging/

# Deploy to production (manual approval required)
deploy-prod:
	kubectl apply -f infra/k3s/prod/

# Pull Llama 3.1 8B model for local inference
pull-llama:
	docker exec -it qantam-ai-ollama-1 ollama pull llama3.1:8b

# Clean up all containers and volumes
clean:
	docker-compose down -v
	rm -rf apps/api/__pycache__ apps/api/.pytest_cache
	rm -rf apps/web/.next apps/web/node_modules

# Show logs for all services
logs:
	docker-compose logs -f

# Show logs for specific service
logs-%:
	docker-compose logs -f $*
