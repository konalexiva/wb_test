COMPOSE := docker-compose
WEB_CONTAINER_NAME := web

.DEFAULT_GOAL = help

build: ## build docker-compose
	$(COMPOSE) build

up: ## up docker-compose
	$(COMPOSE) up -d --build

stop: ## stop docker-compose
	$(COMPOSE) stop

shell: ## run python shell in web container
	$(COMPOSE) exec $(WEB_CONTAINER_NAME) python manage.py shell

show_logs: ## run logs of web container
	$(COMPOSE) exec $(WEB_CONTAINER_NAME) logs -f

makemigrations: ## make migrations
	$(COMPOSE) exec $(WEB_CONTAINER_NAME) python manage.py makemigrations

migrate: ## migrate
	$(COMPOSE) exec $(WEB_CONTAINER_NAME) python manage.py migrate

import_parsed_posts: ## import parsed data
	$(COMPOSE) exec $(WEB_CONTAINER_NAME) python manage.py import_parsed_posts

run_web_bash: ## run web container bash
	$(COMPOSE) exec $(WEB_CONTAINER_NAME) bash

parse_posts: ## run parser
	$(COMPOSE) exec $(WEB_CONTAINER_NAME) sh /code/run_mdf_parser.sh

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-23s\033[0m %s\n", $$1, $$2}'

