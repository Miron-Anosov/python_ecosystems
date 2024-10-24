from typing import Union, Annotated
from enum import Enum

from fastapi import FastAPI, Query
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """FastAPI распознает, какие параметры функции соответствуют параметрам пути и должны быть получены из пути,
     а какие параметры функции, объявленные как модели Pydantic, должны быть получены из тела запроса."""
    return {"item_id": item_id, **item.dict()}


@app.post("/items_with_params/{item_id}")
async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    print(result)
    return result


@app.get("/somethings/")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    """Теперь, когда у нас есть Annotated, где мы можем добавить больше метаданных,
        добавим Query со значением параметра max_length равным 50:"""
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
        print(results)
    return results


@app.get("/regex/")
async def read_items(
        q: Annotated[
            str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
        ] = None,
):
    """
    Вы можете определить регулярное выражение, которому должен соответствовать параметр:
        Данное регулярное выражение проверяет, что полученное значение параметра:

        ^: начало строки.
        fixedquery: в точности содержит строку fixedquery.
        $: конец строки, не имеет символов после fixedquery.
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/default-items/")
async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
    """
    Вы точно также можете указать любое значение по умолчанию, как ранее указывали None.
    Например, вы хотите для параметра запроса q указать, что он должен состоять минимум из 3 символов (min_length=3)
    и иметь значение по умолчанию "fixedquery"
    Наличие значения по умолчанию делает параметр необязательным.
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/ellipsis-default/")
async def read_items(q: Annotated[str, Query(min_length=3)] = ...):
    """Обязательный параметр с Ellipsis (...).
    Таким образом, FastAPI определяет, что параметр является обязательным."""
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/none/")
async def read_items(q: Annotated[Union[str, None], Query(min_length=3)] = ...):
    """
    Обязательный параметр с None¶
    Вы можете определить, что параметр может принимать None, но всё ещё является обязательным. Это может потребоваться
    для того, чтобы пользователи явно указали параметр, даже если его значение будет None.

    Чтобы этого добиться, вам нужно определить None как валидный тип для параметра запроса, но также указать
    default=...:
    Args:
        q: text

    Returns:
        json obj

    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/required/")
async def read_items(q: Annotated[str, Query(min_length=3)]):
    """
    Запомните, когда вам необходимо объявить query-параметр обязательным, вы можете просто не указывать
    параметр default. Таким образом, вам редко придётся использовать ... или Required.
    Args:
        q: Any

    Returns:
        JSON

    Notes:

        from pydantic import Required
          File "/home/miron/PycharmProjects/python_advanced/.venv/lib/python3.12/site-packages/pydantic/_migration.py",
            line 302, in wrapper
                raise PydanticImportError(f'`{import_path}` has been removed in V2.')
        pydantic.errors.PydanticImportError: `pydantic:Required` has been removed in V2.

        For further information visit https://errors.pydantic.dev/2.7/u/import-error

    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/many-params/")
async def read_items(q: list[str] = Query(None, description="Можно добавлять много аргументов")):  # так работает
    """
    Для query-параметра Query можно указать, что он принимает список значений (множество значений).
    Например, query-параметр q может быть указан в URL несколько раз. И если вы ожидаете такой формат запроса,
    то можете указать это следующим образом:
    http://localhost:8000/many-params/?q=foo&q=bar
    result: ['foo', 'bar']


    Чтобы объявить query-параметр типом list, как в примере выше, вам нужно явно использовать Query,
    иначе он будет интерпретирован как тело запроса.

    Интерактивная документация API будет обновлена(нет) соответствующим образом, где будет разрешено множество значений.

    read_items(q: Annotated[Union[list[str], None], Query()] = None) - так не работает.
    """
    query_items = {"q": q}
    print(q)
    return query_items


@app.get("/items-many-default/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    """
    Query-параметр со множеством значений по умолчанию¶
    Вы также можете указать тип list со списком значений по умолчанию на случай, если вам их не предоставят
    """
    query_items = {"q": q}
    return query_items


@app.get("/custom-title/")
async def read_items(
        q: Annotated[str | None, Query(title="Query string", min_length=3)] = None,
):
    """Вы можете указать название query-параметра, используя параметр title-НЕ РАБОТАЕТ"""
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/description/")
async def read_items(
        q: Annotated[
            str | None,
            Query(
                title="Query string",
                description="Query string for the items to search in the database that have a good match",
                min_length=3,
            ),
        ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/alias/")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    """
    Псевдонимы параметров¶

    Представьте, что вы хотите использовать query-параметр с названием item-query.

    Например:

    http://127.0.0.1:8000/items/?item-query=foobaritems

    Но item-query является невалидным именем переменной в Python.

    Наиболее похожее валидное имя item_query.

    Но вам всё равно необходим item-query...

    Тогда вы можете объявить псевдоним, и этот псевдоним будет использоваться для поиска значения параметра запроса:
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/old-items/")
async def read_items(
        q: Annotated[
            str | None,
            Query(
                alias="item-query",
                title="Query string",
                description="Query string for the items to search in the database that have a good match",
                min_length=3,
                max_length=50,
                pattern="^fixedquery$",
                deprecated=True,
            ),
        ] = None,
):
    """
    Устаревшие параметры

    Предположим, вы больше не хотите использовать какой-либо параметр.

    Вы решили оставить его, потому что клиенты всё ещё им пользуются. Но вы хотите отобразить это в документации
    как устаревший функционал.

    Тогда для Query укажите параметр deprecated=True:
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/include-items/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    """
    Исключить из OpenAPI.
    Чтобы исключить query-параметр из генерируемой OpenAPI схемы
    (а также из системы автоматической генерации документации), укажите в Query параметр include_in_schema=False:
    """
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}


" http://127.0.0.1:8000/openapi.json"
" http://127.0.0.1:8000/docs"
" http://127.0.0.1:8000/redoc"
"uvicorn main:app --reload"
"fastapi dev main.py"
