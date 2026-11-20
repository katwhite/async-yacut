# Проект YaCut

Сервис для созданию коротких ссылок и асинхронной загрузке файлов на Яндекс.Диск.

## Стек технологий
- Python 3.9+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- aiohttp
- WTForms

## Развертывание проекта
1. Клонировать репозиторий и перейти в него:
   `git clone <ссылка> && cd async-yacut`
2. Создать и активировать виртуальное окружение:
   `python -m venv venv` (и активировать).
3. Установить зависимости:
   `pip install -r requirements.txt`
4. Создать файл `.env` в корне проекта:
   ```env
   FLASK_APP=yacut
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   DATABASE_URI=sqlite:///db.sqlite3
   DISK_TOKEN=ваш_токен_яндекс_диска
5. Создать базу данных и применить миграции:
   `flask db upgrade`
6. Запустить проект:
   `flask run`

## Автор
Пименова Екатерина