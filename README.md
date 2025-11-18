# Notification Service

Микросервис для отправки уведомлений пользователям через несколько каналов: **Email**, **SMS**, **Telegram**.  
Поддерживает fallback — если один канал недоступен, сообщение будет отправлено через следующий.

Проект реализован на **Django + Django REST Framework**, очереди — через **Celery + Redis**, и упакован в **Docker Compose**.  
Кэширование шаблонов выполнено через **cacheops**.

---

## Основные возможности

- Отправка уведомлений по нескольким каналам
- Хранение шаблонов уведомлений с контекстом
- Логирование попыток отправки
- Асинхронная обработка через Celery
- REST API с Browsable Interface
- Docker Compose: PostgreSQL, Redis, Django, Celery worker
- Автоматическая загрузка фикстур при запуске
- Админ-панель для управления пользователями, шаблонами и каналами

---

## Запуск проекта через Docker Compose

### 1) Склонировать репозиторий

```bash
git clone https://github.com/MalkovGN/notifications-service.git
cd notifications-service
```

### 2) Добавить в корень проекта .env
```bash
DJANGO_SECRET_KEY=secret-key-for-my-app
DJANGO_DEBUG=0

POSTGRES_DB=notifications
POSTGRES_USER=notifications
POSTGRES_PASSWORD=notifications
DB_HOST=db
DB_PORT=5432

DATABASE_URL=postgres://notifications:notifications@db:5432/notifications

REDIS_URL=redis://redis:6379/0
```

### 3) Собрать и запустить контейнеры

```bash
docker compose up --build
```

### 4) После первого запуска доступны:

- Superuser `admin` (демо пароль для входа в админку admin123)
- Пользователь `test_user`
- Шаблоны уведомлений
- Каналы отправки

---

## 🧪 Демо-данные (fixtures)

Автоматически загружаются:

```
notifications/fixtures/initial_data.json
```

---

## REST API

### Создать уведомление

```
POST /api/notifications/
```

Тело:

```json
{
  "user_id": 2,
  "template_code": "example_tg_template",
  "context": {"example": true}
}
```

После отправки уведомления в логах контейнера Celery будут строки вида:
- [TELEGRAM] SEND TO === @test_user === BODY === Привет!
- [SMS] SEND TO === +79000000000 === BODY === Привет!
- [EMAIL] SEND TO === test_user@example.com === BODY === Привет!

### Получить уведомление

```
GET /api/notifications/<id>/
```

Ответ:
```json
{
    "id": 1,
    "user": 2,
    "template": 1,
    "context": {
        "example": true
    },
    "status": "sent",
    "created_at": "2025-11-18T13:27:29.487999Z",
    "attempts": [
        {
            "channel": "telegram",
            "status": "success",
            "error_message": "",
            "created_at": "2025-11-18T13:27:29.524727Z"
        }
    ]
}
```