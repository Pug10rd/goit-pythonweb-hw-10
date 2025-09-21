Required commands

docker run --name hw10 -p 5432:5432 -e POSTGRES_PASSWORD=admin -d postgres

docker exec -it hw10 psql -U postgres -c "CREATE DATABASE hw10;"

alembic init alembic

alembic revision -m "Movie model" --autogenerate

alembic upgrade head

fastapi dev main.py
