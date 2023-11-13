build: ## Build the base image
	docker compose build

up: ## Up container
	docker compose up

up-d: ## Up container
	docker compose up -d

up-build: ## Build the base image
	docker compose up --build

makemigrations: ## Run django makemigrations command
	docker compose run web python manage.py makemigrations

migrate: ## Run django migrate command
	docker compose run web python manage.py migrate

shell: ## Run django shell_plus command
	docker compose run web python manage.py shell

load-fixtures:
	docker compose run web python manage.py loaddata /app/fixtures/departments.json

test: ## Run django shell_plus command ARGS=--fixtres -v for scenary details
	docker compose run web pytest $(ARGS)

# docker exec ed2c09e98e46 python manage.py loaddata /app/fixtures/task_status.json
docker-exec: ## Run django shell_plus command make docker-exec CONTAINER_ID=244ff84b4b81 ARGS=pytestmkw
	docker exec -it $(CONTAINER_ID) $(ARGS)

#make docker-attach CONTAINER_ID=8be173a0b68a
docker-attach: ## docker attach
	docker attach --detach-keys ctrl-d $(CONTAINER_ID)
