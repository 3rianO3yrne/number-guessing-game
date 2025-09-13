test:
	docker compose -f compose.test.yaml run --build --rm test_server

down:
	docker compose down --remove-orphans

up:
	docker compose up 

build:
	docker compose up --build

watch:
	docker compose up --watch

rebuild:
	docker compose build --no-cache
	

