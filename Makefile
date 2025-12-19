.PHONY: start stop restart catalog-service build run clean test

start:
	docker compose up -d

stop:
	docker compose down --volumes

restart: stop start

migrate:
	flyway -configFiles=flyway.developer.conf migrate

catalog-service:
	npx json-server --watch src/main/resources/json-server/db.json --port 3000

build:
	./mvnw clean package -DskipTests

run:
	SPRING_PROFILES_ACTIVE=prod ./mvnw spring-boot:run

run-dev:
	SPRING_PROFILES_ACTIVE=dev ./mvnw spring-boot:run

clean:
	./mvnw clean

test:
	flyway -configFiles=flyway.test.conf migrate
	./mvnw test

install:
	./mvnw clean install