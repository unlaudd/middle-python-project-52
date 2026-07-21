# Менеджер задач (Task Manager)
[![CI](https://github.com/твой-username/hexlet-code/actions/workflows/ci.yml/badge.svg)](https://github.com/твой-username/hexlet-code/actions/workflows/ci.yml)
[![Actions Status](https://github.com/unlaudd/middle-python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/unlaudd/middle-python-project-52/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=unlaudd_middle-python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=unlaudd_middle-python-project-52)

## Описание

Менеджер задач — это веб-приложение для управления задачами, аналог Redmine. Оно позволяет создавать задачи, назначать исполнителей, отслеживать статусы и категоризировать работу с помощью меток. Для работы с системой требуется регистрация и аутентификация.

## Демо

**[Посмотреть на Render](https://middle-python-project-52-0k2i.onrender.com)**

## Возможности

- **Управление пользователями:** регистрация, аутентификация и управление профилем. Пользователи могут редактировать или удалять только свои собственные аккаунты.
- **Управление задачами:** полный цикл CRUD-операций для задач, включая назначение исполнителей и отслеживание даты создания.
- **Статусы и метки:** настраиваемые статусы и метки для эффективной категоризации задач.
- **Расширенная фильтрация:** фильтрация задач по статусу, исполнителю, метке или просмотр опции «Только мои задачи».
- **Целостность данных:** защита от удаления сущностей, связанных с другими сущностями (например, нельзя удалить статус, метку или пользователя, если они привязаны к существующей задаче).
- **Отслеживание ошибок:** интеграция с Rollbar для мониторинга ошибок в продакшене в реальном времени.

## Технологический стек

- **Язык:** Python 3.12
- **Фреймворк:** Django
- **База данных:** PostgreSQL (продакшен), SQLite (локальная разработка)
- **Сервер:** Gunicorn
- **Статические файлы:** WhiteNoise
- **Менеджер пакетов:** `uv`
- **Хостинг:** Render (PaaS)
- **Мониторинг:** Rollbar

## Локальная разработка

### Требования

- Python 3.10 или выше
- Установленный менеджер пакетов `uv`

### Установка

```bash
# Клонируем репозиторий
git clone https://github.com/unlaudd/middle-python-project-52.git
cd middle-python-project-52

# Устанавливаем зависимости
make install

# Применяем миграции базы данных
make migrate

# (Опционально) Компилируем файлы переводов
make compilemessages

# Запускаем сервер разработки
make start
```

Приложение будет доступно по адресу `http://127.0.0.1:8000`.

### Переменные окружения

Создайте файл .env в корневой директории проекта:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ROLLBAR_ACCESS_TOKEN=your-rollbar-token-here
ROLLBAR_ENVIRONMENT=development
```

Для продакшен-деплоя установите следующие переменные окружения в панели управления Render:
* `SECRET_KEY`: надежный уникальный секретный ключ Django.
* `DEBUG`: False для продакшена.
* `DATABASE_URL`: строка подключения к PostgreSQL, предоставленная Render.
* `ROLLBAR_ACCESS_TOKEN`: токен доступа вашего проекта в Rollbar.
* `ROLLBAR_ENVIRONMENT`: production.

## Команды сборки и запуска
В проекте используется `Makefile` для удобного управления рабочими процессами. Введите make help, чтобы увидеть список всех доступных команд.

```
# Установка зависимостей
make install

# Запуск скрипта продакшен-сборки (миграции, сборка статики и т.д.)
make build

# Запуск приложения с Gunicorn (для продакшена/Render)
make render-start

# Запуск локального сервера разработки
make start

# Запуск набора тестов
make test
```

## Деплой

Проект развернут на платформе [Render](https://render.com) в рамках бесплатного тарифа. Процесс деплоя автоматизирован с помощью скрипта `build.sh`, который управляет установкой зависимостей, сборкой статических файлов, применением миграций базы данных и компиляцией сообщений переводов.
