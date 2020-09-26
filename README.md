# visiology-py

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

dimensions = api.get_dimension_elements(token, "dim_Status")

# ... работаем с dimensions ...
```

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

По-возможности, пишите тесты и тайп-хинты, проверяйте код перед тем как коммитить и не коммитьте в мастер.

Если нужно использовать внесённые изменения, через pip можно поставить пакет из локальной директории и продолжать редактирование кода:

`# pip install -e .` (от рута)