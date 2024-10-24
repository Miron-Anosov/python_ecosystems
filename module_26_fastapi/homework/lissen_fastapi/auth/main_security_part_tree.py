import secrets
import uuid

from fastapi import FastAPI, Depends, status, Header, Response, Cookie
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Annotated, Any

app = FastAPI()

security = HTTPBasic()
users = {
    'admin': 'admin',
    'user': 'user'
}

users_stat_token = {
    'c0cc03ace6b08363930b010f578db100d9b6c055927646179271880cd890b340': 'admin',
    '66767de9cd0445c4b54409d6a54a1edd1cd67f91b53dce26eefb86276f55ded2': 'user'
}


def get_user_auth(data_auth: HTTPBasicCredentials = Depends(security)):
    exception_auth = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail='Invalid login or password',
                                   headers={'WWW-Authenticate': 'Basic'})

    if not users.get(data_auth.username):
        raise exception_auth

    correct_password = users.get(data_auth.username).encode('UTF-8')
    input_password = data_auth.password.encode('UTF-8')

    if not secrets.compare_digest(correct_password, input_password):
        raise exception_auth

    return data_auth.username


def get_user_by_static_token_for_handler(user_token: str = Header(alias='x-user-token')):
    if user_name := users_stat_token.get(user_token):
        return user_name
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')


@app.get("/basic-auth/")
def demo_basic_auth_credentials(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }


@app.get('/basic-auth-username/')
def auth_user(user: Annotated[str, Depends(get_user_auth)]):
    return {'hello': user}


@app.get('/some-http-header-auth/')
def auth_user_with_http_header(user: Annotated[str, Depends(get_user_by_static_token_for_handler)]):
    """"Some docs for auth with token"""
    return {'hello': user}


COOKIE_SESSION_ID_KEY = 'WEB-APP-SESSION-KEY'
COOKIES: dict[str, dict[str, Any]] = {}


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(id_cookie: str = Cookie(alias=COOKIE_SESSION_ID_KEY)):
    print(id_cookie)
    if COOKIES.get(id_cookie):
        return COOKIES.get(id_cookie)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='not authentication')


@app.post('/login-cookie/', )
def auth_user_with_cookie(response: Response,
                          user: str = Depends(get_user_auth),
                          # user: str = Depends(get_user_by_static_token_for_handler)  # Не использовать Annotated
                          ):
    """"Some docs for auth with token"""
    print(f"{user=}")
    session_id = generate_session_id()
    COOKIES[session_id] = {"username": user}
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {'result': 'OK'}


@app.get('/check-cookie/')
def check_cookie(cookie_data: dict = Depends(get_session_data)):
    print(f'{cookie_data=}')
    user_name = cookie_data['username']
    return {'Session': True, 'user token': user_name}


@app.get('/logout-cookie/')
def check_cookie(response: Response,
                 cookie_data: dict = Depends(get_session_data),
                 ):
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    return {'Session': False, 'user token': cookie_data.pop('username')}
