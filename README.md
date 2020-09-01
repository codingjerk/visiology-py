# visiology-py

Высокоуровневые обертки и вспомогательные функции для работы с API Visiology: ViQube, ViQube Admin и Datacollection

## Подготовка к разработке

1. Создание venv: `$ python3 -m venv venv`
1. Установка зависимостей: `$ pip3 install -r requirements.txt`

## Проверка

1. `$ make test` — тесты (`pytest`)
1. `$ make lint` — линтинг (`pycodestyle`)
1. `$ make typecheck` — проверка типов (`mypy`)
1. `$ make` — всё вышеперечисленное
