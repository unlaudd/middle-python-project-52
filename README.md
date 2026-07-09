# Task Manager

[![Actions Status](https://github.com/unlaudd/middle-python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/unlaudd/middle-python-project-52/actions)

## Описание

Task Manager — веб-приложение для управления задачами, аналог Redmine. Позволяет создавать задачи, назначать исполнителей и изменять их статусы. Для работы с системой требуется регистрация и аутентификация.

## Демо

**[Посмотреть на Render](https://middle-python-project-52-0k2i.onrender.com)**

## Возможности

- Регистрация и аутентификация пользователей
- Управление задачами со статусами и метками
- Назначение исполнителей на задачи
- Фильтрация и поиск
- Отслеживание ошибок через Rollbar

## Технологии

- Python 3.10+
- Django
- PostgreSQL
- Gunicorn
- WhiteNoise
- Render (PaaS)

## Локальная разработка

### Требования

- Python 3.10 или выше
- Менеджер пакетов uv

### Установка

```bash
# Клонируем репозиторий
git clone https://github.com/unlaudd/middle-python-project-52.git
cd middle-python-project-52

# Устанавливаем зависимости
uv sync

# Применяем миграции
uv run python manage.py migrate

# Запускаем сервер разработки
uv run python manage.py runserver
```

Приложение будет доступно по адресу `http://127.0.0.1:8000`

## Деплой
Проект развернут на платформе [Render](https://render.com/) в рамках бесплатного тарифа.

## Команды сборки и запуска
```bash
# Сборка
make build

# Запуск (продакшен)
make render-start

# Запуск (разработка)
make start
```

## Переменные окружения
Создайте файл `.env` в корневой директории:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

Для продакшен-деплоя установите эти переменные в панели управления Render:
 * `SECRET_KEY` - секретный ключ Django
 * `DEBUG` - False для продакшена
 * `DATABASE_URL` - строка подключения к PostgreSQL (предоставляется Render)