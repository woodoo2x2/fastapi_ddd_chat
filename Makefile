DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = main-app
STORAGE_FILE = docker_compose/storages.yaml

.PHONY : app
app:
	$(DC) -f $(APP_FILE) $(ENV) up --build -d

.PHONY : storages
storages:
	$(DC) -f $(STORAGE_FILE) $(ENV) up --build -d

.PHONY : all
all:
	$(DC) -f $(APP_FILE) -f $(STORAGE_FILE) $(ENV) up --build -d


.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) down

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGE_FILE) down

.PHONY: app-shell
app-shell:
	$(EXEC) $(APP_CONTAINER) bash

.PHONY : app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f

.PHONY : app-tests
app-tests:
	$(EXEC) $(APP_CONTAINER) pytest