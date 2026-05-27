# TeamFinder

Веб-приложение для поиска команды на проект. **Вариант 2** — навыки пользователей и фильтрация.

## Запуск проекта (для ревьюера)

### 1. Запустите базу данных

```bash
docker compose up -d
```

PostgreSQL поднимется на порту `5436`. Данные хранятся в volume и не пропадают при рестарте.

> Если хотите использовать свой локальный PostgreSQL — создайте базу `team_finder` и пользователя `team_finder` с паролем `team_finder`, и поменяйте `POSTGRES_PORT` в `.env` на свой порт.

### 2. Установите зависимости

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Примените миграции и загрузите тестовые данные

```bash
python manage.py migrate
python manage.py create_test_data
```

### 4. Запустите сервер

```bash
python manage.py runserver
```

Открывайте: **http://localhost:8000**

---

## Тестовые аккаунты

| Email | Пароль | |
|---|---|---|
| admin@example.com | admin123 | суперпользователь |
| ivanov@example.com | test123 | |
| petrova@example.com | test123 | |
| sidorov@example.com | test123 | |
| kozlova@example.com | test123 | |

Панель администратора: http://localhost:8000/admin/

---

## Что реализовано (вариант 2)

- Регистрация и вход по email
- Создание/редактирование проектов, участие в проектах
- Редактирование профиля, смена пароля
- **Навыки пользователя** — добавление и удаление без перезагрузки страницы, автодополнение
- **Фильтрация участников по навыкам** — `/users/list/?skill=Python`
- Пагинация (12 элементов на странице)

---

## .env

Файл `.env` уже заполнен и лежит в корне проекта. При использовании Docker менять ничего не нужно.

```
TASK_VERSION=2
POSTGRES_PORT=5436
```
