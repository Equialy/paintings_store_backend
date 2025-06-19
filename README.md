# Paintings Store API

REST‑сервис для управления интернет‑магазином картин: пользователи, каталог, корзина и заказы через асинхронный FastAPI и PostgreSQL.

---

## Содержание

- [Функции](#функции)  
- [Технологии](#технологии)  
- [Структура проекта](#структура-проекта)  
- [Начало работы](#начало-работы)  
  - [Быстрый старт](#быстрый-старт)  
  - [Запуск приложения](#запуск-приложения)  
- [Аутентификация](#аутентификация)  
- [Эндпоинты API](#эндпоинты-api)  
  - [Публичный каталог](#публичный-каталог)  
  - [Корзина](#корзина)  
  - [Заказы (пользователь)](#заказы-пользователь)  
  - [Админ: Каталог](#админ-каталог)  
  - [Админ: Заказы](#админ-заказы)  
- [Структура слоёв](#структура-слоёв)  
- [Дополнительно](#дополнительно)  

---

## Функции

- **JWT‑авторизация** пользователей  
- **CRUD** для картин и категорий (публично и в админ‑панели)  
- **Корзина**: добавление, удаление, изменение количества  
- **Оформление заказа**: создание заказа, просмотр истории  
- **Админ‑панель**: управление каталогом, просмотр и смена статусов заказов  
- **Документированное API** Swagger/OpenAPI  
- **Docker + Alembic** для миграций и быстрого развёртывания  

---

## Технологии

- **Python3.13**  
- **FastAPI** (асинхронный)  
- **PostgreSQL**  
- **SQLAlchemy2.0** + **Alembic**  
- **Pydantic**  
- **JWT** (python-jose) + **bcrypt**  
- **Docker**, **docker-compose**  
- **Pytest** (юнит‑ и интеграционные тесты)  

---


---

## Начало работы

### Быстрый старт

1. **Клонировать репозиторий**  
   ```bash
   git clone https://github.com/your-org/paintings-store-backend.git
   cd paintings-store-backend
   
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
   
   cp .env.example .env
   заполните параметры DATABASE_URL, JWT_SECRET, и т.д.
   
   alembic upgrade head   Запустить миграции
   
   uvicorn src.presentation.main:app --reload --port 8000
   ```
   
# API Documentation




## Структура слоёв

* **Domain** — бизнес‑логика, Pydantic‑схемы, Protocol‑интерфейсы
* **Infrastructure** — SQLAlchemy‑модели и репозитории (реализация Protocol)
* **Presentation** — FastAPI‑роутеры и DI‑зависимости



## Структура проекта

```
src/
├── domain/
│   ├── accounts/          # схемы, интерфейсы, use‑cases, JWT и парольные сервисы
│   ├── pictures/          # схемы, интерфейсы, use‑cases для каталога
│   ├── cart/              # схемы, интерфейсы, use‑cases корзины
│   ├── orders/            # схемы, интерфейсы, use‑cases заказов
│   └── admin/             # схемы и интерфейсы CRUD‑админки (каталог, заказы)
├── infrastructure/
│   ├── database/
│   │   ├── migrations/    # Alembic
│   │   ├── models/        # SQLAlchemy‑модели
│   │   └── repositories/  # реализация Protocol‑репозиториев
│   ├── base.py            # DeclarativeBase и сессии
│   └── utils/             # хранилище файлов, др. утилиты
├── presentation/
│   ├── api/               # FastAPI‑роутеры (user, admin, cart, orders)
│   ├── dependencies/      # DI‑зависимости (репозитории, сервисы, auth)
│   ├── main.py            # точка входа приложения
│   └── middleware.py      # CORS, обработчики ошибок
├── settings.py            # Pydantic BaseSettings
└── tests/                 # тесты (юнит, интеграция)
```

## Аутентификация

* **POST** `/api/v1/auth/register` — регистрация (`username`, `email`, `password`)
* **POST** `/api/v1/auth/login` — вход, возвращает JWT (`access_token`, `token_type`, `is_superuser`)

Все защищённые эндпоинты требуют заголовок:

```
Authorization: Bearer <your_token>
```

## Эндпоинты API

### Публичный каталог

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/v1/pictures` | Список картин (с фильтром/поиском) |
| GET | `/api/v1/pictures/{id}` | Детали картины |

### Корзина

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/v1/cart/` | Просмотр текущей корзины |
| POST | `/api/v1/cart/` | Добавить в корзину (`picture_id`, `qty`) |
| PATCH | `/api/v1/cart/{item_id}` | Изменить количество в корзине |
| DELETE | `/api/v1/cart/{item_id}` | Удалить из корзины |

### Заказы (пользователь)

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/v1/orders/` | Оформить заказ (`address`, `phone`, `items`) |
| GET | `/api/v1/orders/` | Список своих заказов |
| GET | `/api/v1/orders/{id}` | Детали своего заказа |

### Админ: Каталог

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/admin/pictures/` | Добавить новую картину |
| GET | `/admin/pictures/` | Список всех картин |
| GET | `/admin/pictures/{id}` | Данные картины по ID |
| PUT | `/admin/pictures/{id}` | Обновить информацию и изображение |
| DELETE | `/admin/pictures/{id}` | Удалить картину |

### Админ: Заказы

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/admin/orders/` | Список всех заказов |
| GET | `/admin/orders/{id}` | Детали заказа |
| PATCH | `/admin/orders/{id}/status` | Изменить статус заказа |

