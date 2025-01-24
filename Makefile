# Variables
DOCKER_COMPOSE = docker-compose
CONTAINER_NAME_BACKEND = save_backend_1
CONTAINER_NAME_FRONTEND = save_frontend_1
DB_PATH = backend/db.sqlite3

# Default target
.PHONY: all build up down logs clean

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

# Créer la base de données et appliquer les migrations
migrate:
	@if [ ! -f $(DB_PATH) ]; then \
		echo "La base de données n'existe pas, création de la base..."; \
		docker-compose run --rm backend python manage.py migrate; \
	else \
		echo "La base de données existe déjà, pas besoin de la créer."; \
	fi

# Démarrer le projet avec la création de la base et les migrations
start: up migrate

# Arrêter et nettoyer le projet
stop: down clean
