Required commands

docker run --name hw8 -p 5432:5432 -e POSTGRES_PASSWORD=admin -d postgres

docker exec -it hw8 psql -U postgres -c "CREATE DATABASE hw8;"

alembic init alembic

alembic revision -m "Movie model" --autogenerate

alembic upgrade head

fastapi dev main.py
