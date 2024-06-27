from typing import Annotated

from fastapi import Depends, FastAPI, Cookie, Header
from fastapi.exceptions import HTTPException

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]


@app.get("/items/")
async def read_items(commons: CommonsDep):
    print(commons)
    return commons


@app.get("/users/")
async def read_users(commons: CommonsDep):
    print(commons)
    return commons


######################################################
"""Классы как зависимости"""

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items-class/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response


###################################################################################

def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(q: Annotated[str, Depends(query_extractor)],
                              last_query: Annotated[str | None, Cookie()] = None,
                              ):
    """Используем зависимость для того что бы отдать новые данные или из cookie"""
    if not q:
        return last_query
    return q


@app.get("/items-fist-depends/")
async def read_query(
        query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}


######################################################################################

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items-two-dependencies/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    """Будут проверены оба условия в зависимостях"""
    return [{"item": "Foo"}, {"item": "Bar"}]


"""
Возвращаемые значения
И они могут возвращать значения или нет, эти значения использоваться не будут.
Таким образом, вы можете переиспользовать обычную зависимость (возвращающую значение), которую вы уже используете 
где-то в другом месте, и хотя значение не будет использоваться, зависимость будет выполнена.
"""

##########################################################################################################
# GLOBAL DEPENDS

app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get('/test-global-depends')
async def get_route():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]
