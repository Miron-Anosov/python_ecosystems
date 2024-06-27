from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    print(update_item_encoded)
    items[item_id] = update_item_encoded
    return update_item_encoded


"""
Это означает, что если вы хотите обновить элемент bar, используя PUT с телом, содержащим:
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
поскольку оно не включает уже сохраненный атрибут "tax": 20.2, входная модель примет значение по умолчанию "tax": 10.5.
И данные будут сохранены с этим "новым" tax, равным 10,5.
"""


#####################################################################

@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]  # извлекли данные из базы.
    stored_item_model = Item(**stored_item_data)  # распаковали данные в модель (оригинал)
    update_data = item.dict(exclude_unset=True)
    # будет сгенерирован словарь, содержащий только те данные, которые были заданы при создании модели item
    print(update_data)
    updated_item = stored_item_model.copy(update=update_data)  # обновляем оригинальные данные
    print(updated_item)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


"""
Кратко о частичном обновлении

В целом, для применения частичных обновлений необходимо:

    (Опционально) использовать PATCH вместо PUT.
    Извлечь сохранённые данные.
    Поместить эти данные в Pydantic модель.
    Сгенерировать dict без значений по умолчанию из входной модели (с использованием exclude_unset).
        Таким образом, можно обновлять только те значения, которые действительно установлены пользователем, вместо того 
        чтобы переопределять значения, уже сохраненные в модели по умолчанию.
    Создать копию хранимой модели, обновив ее атрибуты полученными частичными обновлениями (с помощью параметра update).
    Преобразовать скопированную модель в то, что может быть сохранено в вашей БД (например, с помощью jsonable_encoder).
        Это сравнимо с повторным использованием метода модели dict(), но при этом происходит проверка (и преобразование)
        значений в типы данных, которые могут быть преобразованы в JSON, например, datetime в str.
    Сохранить данные в своей БД.
    Вернуть обновленную модель.
"""