#!/bin/bash
set -e

# Настройка PYTHONPATH
export PYTHONPATH=/app

# Запуск приложения
uvicorn main:app --host 0.0.0.0 --port 8080 &

sleep 4
# Выполнение миграций базы данных (если необходимо)
alembic upgrade head

# Ожидание завершения uvicorn
wait