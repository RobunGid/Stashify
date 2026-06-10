DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env

APP_FILE = docker_compose/app.yaml
DB_FILE = docker_compose/storages.yaml

APP_CONTAINER = main-app
DB_CONTAINER = stashify-database
DB_UI_CONTAINER = stashify-database-ui

.PHONE: all
all:
	${DC} -f ${APP_FILE} -f ${DB_FILE} ${ENV} up --build -d

.PHONE: all-down
all-down:
	${DC} -f ${APP_FILE} -f ${DB_FILE} ${ENV} down

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down	

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash	

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: db
db: 
	${DC} -f ${DB_FILE} ${ENV} up --build -d

.PHONY: db-shell
db-shell:
	${EXEC} ${DB_CONTAINER} bash	

.PHONY: db-logs
db-logs:
	${LOGS} ${DATABASE_CONTAINER} -f

.PHONY: db-down
db-down:
	${DC} -f ${DB_FILE} down	

.PHONY: app-test
app-test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: db-ui-logs
db-ui-logs:
	${LOGS} ${DATABASE_UI_CONTAINER} -f