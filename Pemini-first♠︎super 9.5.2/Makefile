.PHONY: help install dev test docker docker-up docker-down k8s-deploy clean

help:
	@echo "Pemini Girl 9.5.2 - Commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make dev         - Run development server"
	@echo "  make test        - Run tests"
	@echo "  make docker-up   - Start with Docker Compose"
	@echo "  make docker-down - Stop Docker Compose"
	@echo "  make k8s-deploy  - Deploy to Kubernetes"
	@echo "  make clean       - Clean build artifacts"

install:
	pip install -r requirements.txt

dev:
	python main.py --web

test:
	pytest tests/ -v

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down -v

k8s-deploy:
	kubectl apply -f k8s-deployment.yaml

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
