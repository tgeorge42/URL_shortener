# Variables
DOCKER_COMPOSE = docker-compose
CONTAINER_NAME_BACKEND = save_backend_1
CONTAINER_NAME_FRONTEND = save_frontend_1
DB_PATH = backend/db/mydatabase.db

# Default target
.PHONY: all build up down logs clean test

all: build up

# Build docker images
build:
	$(DOCKER_COMPOSE) build

# Start docker containers
up:
	$(DOCKER_COMPOSE) up -d

# Stop docker containers
down:
	$(DOCKER_COMPOSE) down

# Display containers logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Clean docker volumes and containers
clean:
	$(DOCKER_COMPOSE) down --volumes --remove-orphans

# Create the db and migrate
migrate:
	@if [ ! -f $(DB_PATH) ]; then \
		echo "La base de données n'existe pas, création de la base..."; \
		docker-compose run --rm backend python manage.py migrate; \
	else \
		echo "La base de données existe déjà, pas besoin de la créer."; \
	fi

# Start the project
start: up migrate

# Stop the project
stop: down clean

# Launch the backend tests
test:
	docker-compose exec backend pytest app/tests/ --verbose
