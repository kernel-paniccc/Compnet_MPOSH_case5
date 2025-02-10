# Система управления спортивным инвентарем ️

## [Демо деплой](https://ppo-case.ru/)
## [Видеоролик](https://vk.com/video327031277_456239035)

## Содержание <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/File%20Folder.webp" alt="File Folder" width="25" height="25" />
- [Описание](#описание)
- [Стек технологий](#стек-технологий)
- [Запуск и установка](#запуск-и-установка)

## Описание <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Books.webp" alt="Books" width="25" height="25" />
Система управления спортивным инвентарем предназначена для учета, управления и мониторинга спортивного оборудования. Она позволяет пользователям легко добавлять, редактировать и удалять инвентарь, а также отслеживать его состояние и доступность.

## Стек технологий <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Laptop.webp" alt="Laptop" width="25" height="25" />

### Backend
- **Python**: основной ЯП бекэнда 
- **Flask**: веб-фреймворк для создания RESTful API 
- **Flask-Login**: для управления аутентификацией пользователей 
- **Requests**: для выполнения HTTP-запросов 
- **Werkzeug**: библиотека для работы с паролями и хешированием 
- **Selenium**: для автоматизации парсинга
- **Pytest**: написание unit-тестов (модульное тестирование)

### Frontend
- **HTML**: разметка страниц 
- **CSS**: стилизация интерфейса 
- **jQuery**: упрощение манипуляций с DOM 
- **Bootstrap**: шаблоны для быстрой верстки 
- **JavaScript**: для управления анимациями и Flash сообщениями 

### Database
- **SQLite3**: легковесная реляционная база данных 
- **SQLAlchemy ORM**: для работы с базой данных через объектно-реляционное отображение 
- **Alembic**: инструмент для управления миграциями базы данных 

### Другие технологии 
- **Docker**: система контейнеризации 
- **Git**: система контроля версий 
- **Ngrok**: создание временных публичных URL для локального сервера 
- **Nginx**: веб-сервер для обслуживания статического контента и обратного проксирования 
- **Gunicorn**: WSGI HTTP-сервер для Python
- **Poetry**: управление зависимостями и пакетами Python
- **Bitrix**: автоматизация и управление закупками
- **Yandex ID**: интеграция OAuth 2.0 

## Запуск и установка <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Rocket.png" alt="Rocket" width="25" height="25" />

### Локальный запуск

Для локального запуска системы управления спортивным инвентарем выполните следующие шаги:

## Предварительные требования <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Symbols/Check%20Mark%20Button.webp" alt="Check Mark Button" width="25" height="25" />

Перед началом убедитесь, что у вас установлены следующие компоненты:

- **Python 3.10 или выше**: Скачайте и установите Python с [официального сайта](https://www.python.org/downloads/).
- **Poetry**: Установите Poetry для управления зависимостями. Инструкции можно найти на [официальном сайте Poetry](https://python-poetry.org/docs/#installation).

## Шаги по установке и запуску <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Open%20Book.webp" alt="Open Book" width="25" height="25" />


1. **Клонирование репозитория**\
   Откройте терминал и выполните следующую команду:
```bash
   git clone https://github.com/kernel-paniccc/Compnet_MPOSH_case5.git
   cd Compnet_MPOSH_case5
```

2. **Установка зависимостей**
```bash
    pip install poetry
    poetry install
```
или
```bash
    pip install -r requierements.txt
```
3. **Переменные окружения**\
Создайте файл .env и добавьте в него переменные:
```
NGROK_AUTHTOKEN='ngrok_token'
BITRIX=https:'bitrix_api_key'
KEY='app_sec_key'
```
Так же в приложение интегрирован OAuth 2.0 с использование Yandex ID:

```
YANDEX_CLIENT_ID='YOUR_CLIENT_ID'
YANDEX_CLIENT_SECRET='YOUR_CLIENT_SECRET'
```

4. **Запуск приложения**\
После установки зависимостий выполните команду:
```bash
python starter.py
```
   ## После чего приложение запустится локально и порт будет прокинут в сеть с помощью Ngrok! 

### Важно! <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Symbols/Warning.png" alt="Warning" width="25" height="25" />
> **Внимание:** После запуска приложения БД создастся автоматически.
> Администратора необходимо добавить вручную, указав в файле '.env'.
> Параметры:
> ADMIN_USERNAME
> ADMIN_EMAIL
> ADMIN_PASS


## Тестирование <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Bar%20Chart.webp" alt="Bar Chart" width="25" height="25" />

Проект использует pytest для реализации модульного тестирования. Тесты можно найти в `/src/tests` 

Для запуска тестов выполните:
``` 
pytest 
```

#  Поднятие докер контейнера <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Toolbox.webp" alt="Toolbox" width="25" height="25" />
### Важно! <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Symbols/Warning.png" alt="Warning" width="25" height="25" />
> Убедитесь, что на вашей машине установлен Docker и Docker Compose.

Как только вы клонировали репозиторий и назначили переменные окружения, можно перейти к деплою.

Если все приготовления выполнены, используйте команды:
```
docker-compose build
docker-compose up
```
## Если все сделано верно, то будут запущены:
### web-app через Gunicorn и прокси-сервер Nginx (port:80)

<img class=" lazyloaded" src="https://github.com/Tarikul-Islam-Anik/Microsoft-Teams-Animated-Emojis/blob/master/Emojis/Activities/Party%20Popper.png?raw=true" alt="Party Popper" title="Party Popper" width="31" height="31"><img class=" lazyloaded" src="https://github.com/Tarikul-Islam-Anik/Microsoft-Teams-Animated-Emojis/blob/master/Emojis/Activities/Party%20Popper.png?raw=true" alt="Party Popper" title="Party Popper" width="31" height="31"><img class=" lazyloaded" src="https://github.com/Tarikul-Islam-Anik/Microsoft-Teams-Animated-Emojis/blob/master/Emojis/Activities/Party%20Popper.png?raw=true" alt="Party Popper" title="Party Popper" width="31" height="31">


