docker-compose up --build

docker-compose run --rm app alembic revision --autogenerate -m "migration_name"

docker-compose run --rm app alembic upgrade head
