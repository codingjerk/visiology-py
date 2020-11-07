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
elements = api.get_dimension_elements("dim_Status", None)

# ... работаем с elements ...
```

### ViQube

#### Получение показателей из группы показателей

```
import visiology_py as vi
import visiology_py.viqube as vq

connection = vi.Connection(...)
api = vq.ApiV3(connection)

# Пример запроса, ГП вымышленная, для наглядности использованы русифицированные имена вместо транслита
result = api.post_metadata_rawdata_query(
    {
        "database": "1",
        "mgid": "Цены",

        "columns": [
            { "mid": "Цена без НДС" },
            { "mid": "Цена с НДС" },

            { "attrid": "Имя продукта", "dlid": "Продукты" },
            { "attrid": "Имя магазина", "dlid": "Магазины" },
        ],
    },
)

# ... работаем с result ...
```

### Автоматический выпуск токена

При использовании методов API, требующих аутентификации (передачи токена), его можно не указывать.

В таком случае токен будет выпущен (emit) автоматически и он же продолжит использоваться до тех пор, пока будет оставаться действительным. Токен будет выпускаться только по необходимости (не каждый запрос).

### Декорирование API

Для задействования дополнительных возможностей, повышающих удобство использования API, существуют декораторы, оборачивающие все методы API. Все определены в модуле `visiology_py.decorators`.

#### Кеширование

Библиотека может кешировать результаты тяжелых запросов, для любого нужного TTL (time to live), для этого существует декоратор `cached`:

```
from datetime import timedelta

import visiology_py.datacollection as dc
from visiology_py.decorators import decorate_api, cached


# Декорируем API декоратором `cached`
decorate_api(
    dc.ApiV2,
    cached(timedelta(minutes=5)),
)


# ... работаем с dc.ApiV2 ...
```

#### Повтор запроса

Библиотека может повторить запрос несколько раз, в случае если предыдущее выполнение завершилось неудачей, для этого существует декоратор `retried`:

_Запросы выполняются с задержкой, которая определяется функцией `timeout_function`, передаваемой декоратору_

По-умолчанию используется эксоненциальная функция, которая делает задержки равными 0.1с, 0.2с, 0.4с, 0.8с и т.д., до максимального значения в 300с (5 минут).

Это позволяет использовать большие значения `max_tries`, без риска перегрузить API.

```
from datetime import timedelta

import visiology_py.viqube as vq
from visiology_py.decorators import decorate_api, retried


# Декорируем API декоратором `cached`
decorate_api(
    vq.ApiV3,
    retried(max_tries=5),
)


# ... работаем с vq.ApiV3 ...
```


## Внесение изменений в библиотеку

### Подготовка к разработке

1. Создание venv: `$ python3 -m venv venv`
1. Установка зависимостей: `$ pip3 install -r requirements.txt`

### Проверка

1. `$ make test` — тесты (`pytest`)
1. `$ make lint` — линтинг (`pycodestyle`)
1. `$ make typecheck` — проверка типов (`mypy`)
1. `$ make coverage` — проверка покрытия тестами (`pytest-cov`)
1. `$ make quality` — проверка различных метрик качества кода (`radon`)
1. `$ make build` — сборка пакета для публикации в PyPi
1. `$ make` — всё вышеперечисленное

### Общая информация

По-возможности, пишите тесты и тайп-хинты, проверяйте код перед тем как коммитить, коммитьте в develop/feature-ветки и делайте merge-реквесты в master.

Если нужно использовать внесённые изменения, через pip можно поставить пакет из локальной директории и продолжать редактирование кода:

`# pip install -e .` (от рута)
