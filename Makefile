PROJECT_NAME ?= auction
VERSION = $(shell python3.8 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= haraleks
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

all:
	@echo "make run         - Create & run development environment in terminal (realtime)"
	@echo "make migrate     - Create and Apply all migrations in django"
	@echo "make clean       - Clean docker volumes"
	@echo "make shell       - Start Django shell in terminal"
	@echo "make test        - Run tests"
	@echo "make stop        - Stops docker containers and delete them"
	@echo "make clean_images - Clean docker images"
	@exit 0


_clean_makefile:
	rm -fr *.egg-info dist

_down_docker:
	docker-compose down --remove-orphans

clean:
	docker volume prune

run:
	docker-compose -f docker-compose.yml up --build
	docker image prune -a -f

migrate:
	docker-compose exec web python manage.py makemigrations && \
	docker-compose exec web python manage.py migrate

shell:
	docker-compose exec web python manage.py shell

stop: _down_docker _clean_makefile

test: start_test_docker stop

start_test_docker:
	docker-compose -f docker-compose.yml run web python manage.py test

clean_images:
	docker image prune -a -f
