APP_NAME ?= app
SERVICE ?=  # run all by default
IS_RUNNING = `docker-compose ps --filter 'status=running'  --services | grep $(APP_NAME)`

run:
	docker-compose up --build $(SERVICE)

test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build \
		--abort-on-container-exit --exit-code-from $(APP_NAME)

clean:
	docker-compose rm --stop --force $(SERVICE)

shell:
	@if [ -n "$(IS_RUNNING)" ]; then \
		docker-compose exec $(APP_NAME) /opt/runtime/entrypoint.sh bash; \
	else \
		docker-compose run --rm $(APP_NAME) /opt/runtime/entrypoint.sh bash; \
	fi;

command:
	@if [ -n "$(IS_RUNNING)" ]; then \
		docker-compose exec -e ARGS=$(ARGS) -e COMMAND=$(COMMAND) $(APP_NAME) /opt/runtime/entrypoint.sh make command; \
	else \
		docker-compose run --rm -e ARGS=$(ARGS) -e COMMAND=$(COMMAND) $(APP_NAME) /opt/runtime/entrypoint.sh make command; \
	fi;
