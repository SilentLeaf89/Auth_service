build:
	docker-compose build

prod:
	docker-compose -f docker-compose.yml up -d

dev:
	docker-compose -f docker-compose.yml -f docker-compose.override.dev.yml up -d

test:
	docker-compose -f docker-compose.yml -f docker-compose.override.dev.yml -f docker-compose.override.tests.yml up -d --force-recreate

redis-cli:
	docker-compose exec redis redis-cli

fastapi-console:
	docker-compose exec fastapi python

logs:
	docker-compose logs --follow

stop:
	docker-compose down

remove:
	docker-compose down --remove-orphans --rmi local

create-super:
	docker-compose exec fastapi python -m cli --login $(LOGIN) --password $(PASSWORD) --firstname $(FIRSTNAME) --lastname $(LASTNAME)
