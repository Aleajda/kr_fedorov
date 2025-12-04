## Структура проекта

    project/
    ├── thread_server.py
    ├── async_server.py
    ├── client.py
    ├── config.py
    └── README.md

## Настройка

URLS задаются в config.py.

## Инструкции

Сначала запускаются серверы, после клиент для проверки работоспособности серверов

## Запуск
```commandline
python async_server.py
```
```commandline
python thread_server.py
```
```commandline
python client.py
```

## Ендпоинты

GET http://localhost:8081/parse

GET http://localhost:8082/parse
