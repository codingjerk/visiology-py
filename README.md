# visiology-py

[![pipeline status](https://gitlab.com/polymedia-orv/orv/visiology-py/badges/master/pipeline.svg)](https://gitlab.com/polymedia-orv/orv/visiology-py/-/commits/master)
[![PyPI version](https://badge.fury.io/py/visiology-py.png)](https://badge.fury.io/py/visiology-py)

Высокоуровневые обертки и вспомогательные функции для работы с API Visiology: ViQube, ViQube Admin и Datacollection

## Установка

`$ pip install visiology-py`

## Использование

### Datacollection

#### Получение элементов измерений

```
import visiology_py as vi
import visiology_py.datacollection as dc

connection = vi.Connection(
    schema="https",
    host="bi.example.com",
    username="<USERNAME>",
    password="<PASSWORD>",
)

api = dc.ApiV2(connection)
token = api.emit_token()

elements = api.get_dimension_elements(token, "dim_Status")

# ... работаем с elements ...
```

### ViQube

#### Получение 

```
import visiology_py as vi
import visiology_py.viqube as vq

connection = vi.Connection(...)

api = vq.ApiV3(connection)
token = api.emit_token()

# Пример запроса, ГП вымышленная, для наглядности использованы русифицированные имена вместо транслита
result = api.post_metadata_rawdata_query(token, {
    "database": "1",
    "mgid": "Цены",

    "columns": [
        { "mid": "Цена без НДС" },
        { "mid": "Цена с НДС" },

        { "attrid": "Имя продукта", "dlid": "Продукты" },
        { "attrid": "Имя магазина", "dlid": "Магазины" },
    ],
})

# ... работаем с result ...

## Внесение изменений в библиотеку

### Подготовка к разработке

1. Создание venv: `$ python3 -m venv venv`
1. Установка зависимостей: `$ pip3 install -r requirements.txt`

### Проверка

1. `$ make test` — тесты (`pytest`)
1. `$ make lint` — линтинг (`pycodestyle`)
1. `$ make typecheck` — проверка типов (`mypy`)
1. `$ make build` — сборка пакета для публикации в PyPi
1. `$ make` — всё вышеперечисленное

### Общая информация

По-возможности, пишите тесты и тайп-хинты, проверяйте код перед тем как коммитить, коммитьте в develop/feature-ветки и делайте merge-реквесты в master.

Если нужно использовать внесённые изменения, через pip можно поставить пакет из локальной директории и продолжать редактирование кода:

`# pip install -e .` (от рута)