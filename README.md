# Работа с открытыми данными

## Установка зависимостей

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Активировать виртуальное окружение в Windows:

```bash
.venv\Scripts\activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

## Запуск программы

Запустить FastAPI-приложение:

```bash
uvicorn app.main:app --reload
```

После запуска приложение доступно по адресу:

```text
http://localhost:8000
```

Динамическая страница:

```text
http://localhost:8000/dynamic
```

## Запуск клиентов

Обработка и нормализация данных:

```bash
python src/formats.py
```

Работа с REST API:

```bash
python src/api_client.py
```

Получение данных с помощью Selenium:

```bash
python src/selenium_client.py
```

## Jupyter Notebook

Основные этапы работы с данными, REST API, Selenium и сравнение способов получения данных представлены в Jupyter Notebook.
