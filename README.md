# Random User API Service

## Описание

Веб-приложение для загрузки, хранения и отображения информации о пользователях с внешнего API [randomuser.me](https://randomuser.me/). Позволяет загружать пользователей, хранить их в базе данных, просматривать списком, по id и получать случайного пользователя.

## Стек технологий
- **FastAPI** — быстрый асинхронный фреймворк для создания REST API.
- **PostgreSQL** — надёжная реляционная база данных.
- **SQLAlchemy** — ORM для работы с БД.
- **Docker, docker-compose** — для стандартизации окружения и быстрого запуска.
- **pytest** — для тестирования.

### Почему выбран этот стек?
FastAPI обеспечивает высокую производительность и простоту разработки API. PostgreSQL отлично подходит для хранения больших объёмов структурированных данных. Docker и docker-compose позволяют быстро развернуть сервис в любом окружении. Все компоненты легко масштабируются и поддерживаются сообществом.

## Как запустить сервис

### 1. Клонируйте репозиторий
```bash
git clone <your_repo_url>
cd yadro_test_task
```

### 2. Скопируйте пример переменных окружения (если есть)
```bash
cp .env.example .env
```

### 3. Запустите сервис через Docker Compose
```bash
docker-compose up --build
```
- Приложение будет доступно на [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Миграции применяются автоматически
При запуске контейнера приложения автоматически выполняется команда alembic upgrade head.

### 5. Остановка сервиса
```bash
docker-compose down
```

## Как создать первую миграцию Alembic (в контейнере Docker)

Если вы запускаете проект впервые без версий миграций или изменили модели, создайте и примените миграцию:

```bash
docker-compose exec app alembic revision --autogenerate -m "initial"
docker-compose exec app alembic upgrade head
```

## Как запустить тесты

### 1. На локальной машине (если установлен Python 3.10+ и зависимости):
```bash
pytest
```

### 2. В контейнере Docker:
```bash
docker-compose exec app pytest
```

## Пример .env

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres
```

## Примечания
- Для корректной работы убедитесь, что папки `app/static` и `app/templates` существуют.
- Все тесты можно запускать одной командой `pytest`.
- Для ручного применения миграций используйте:
  ```bash
  docker-compose exec app alembic upgrade head
  ``` 