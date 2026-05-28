# Память — Интернет-магазин ритуальных услуг

Django-проект интернет-магазина ритуальных услуг с панелью администратора, каталогом товаров, новостями, корзиной и заказами.

## Требования

- Python 3.8+
- pip

## Установка и запуск проекта

### 1. Создание виртуальной среды

```bash
python -m venv venv
```

### 2. Активация виртуальной среды

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

> **Примечание:** Если файл `requirements.txt` отсутствует, установите необходимые пакеты вручную:
> ```bash
> pip install django==5.2 djangorestframework django-jazzmin pillow
> ```

### 4. Применение миграций

```bash
python manage.py migrate
```

### 5. Загрузка начальных данных (фикстур)

```bash
python manage.py loaddata fixtures/initial_data.json
```

### 6. Сбор статических файлов (опционально, для production)

```bash
python manage.py collectstatic --noinput
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

После запуска сервер будет доступен по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Админ-панель

Для доступа к админ-панели перейдите по адресу: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

**Учётные данные из фикстур:**
- Логин: `admin`
- Пароль: установите свой при первой авторизации или используйте пароль из фикстур

## Структура проекта

```
.
├── config/              # Настройки проекта Django
│   ├── settings.py      # Основные настройки
│   ├── urls.py          # Корневой URLconf
│   └── wsgi.py          # WSGI конфигурация
├── apps/                # Приложения проекта
│   ├── core/            # Основное приложение (контекстные процессоры, контактная информация)
│   ├── goods/           # Каталог товаров и категорий
│   ├── news/            # Новости
│   ├── cart/            # Корзина покупок
│   ├── orders/          # Заказы
│   └── users/           # Пользователи
├── templates/           # HTML шаблоны
├── static/              # Статические файлы (CSS, JS, изображения)
├── fixtures/            # Начальные данные для загрузки
├── scripts/             # Скрипты (создание пользователей и др.)
├── manage.py            # Утилита управления Django
└── db.sqlite3           # База данных SQLite
```

## Дополнительные команды

### Создание суперпользователя

```bash
python manage.py createsuperuser
```

### Запуск тестов

```bash
python manage.py test
```

### Проверка кода на ошибки

```bash
python manage.py check
```

## Технологии

- **Backend:** Django 5.2, Django REST Framework
- **Database:** SQLite (по умолчанию)
- **Admin UI:** Django Jazzmin (кастомизированная тема)
- **Frontend:** HTML, CSS, JavaScript

## Лицензия

© ООО «Память»
