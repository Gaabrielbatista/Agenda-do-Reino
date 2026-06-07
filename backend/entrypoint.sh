#!/bin/sh

echo "Rodando migrações do Alembic..."
alembic upgrade head

echo "Rodando o seed do banco de dados..."
python -m app.seeds.seed_admin

echo "Iniciando Gunicorn..."
exec gunicorn -w 4 -b 0.0.0.0:5000 "app.app:create_app()"