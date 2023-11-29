# All
all: up

# Start all services
up:
	docker-compose up -d --build

# Stop and remove all services
down:
	docker-compose down

# Refresh Project
re: down all

.PHONY: up down re