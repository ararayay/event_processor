# Event Processor

Event Processor — это микросервис, который принимает события от:

- **ADs Service** (клики)
- **Payment Service** (покупки)

и объединяет их в единый поток данных, отправляя в внешнюю систему **AdVantage**.

Документация Swagger доступна по адресу: http://127.0.0.1:8000/docs

## Запуск локально

```bash
# 1. Установить зависимости
pip install -r requirements.txt
# 2. Создать .env по аналогии с .env.example
# 3. Применить миграции
alembic upgrade head
# 4. Запустить сервер
uvicorn app.main:app --reload
# 5. Запустить воркер
python -m app.workers.advantage_sender
```

## Запуск через Docker

```bash
# 1. Создать .env по аналогии с .env.example
# 2. Запустить контейнеры
docker compose up --build -d
```

## Остановка

```bash
docker compose down
```

## Технический стек

- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- pytest

## Эндпоинты

| Method | Endpoint    | Description |
|---|-------------|---|
| POST | `/click/`   | Создание клика |
| POST | `/payment/` | Создание покупки |