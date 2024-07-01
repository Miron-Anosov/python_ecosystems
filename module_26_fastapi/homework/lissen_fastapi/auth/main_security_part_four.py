# pyjwt==2.8.0
# bcrypt==4.1.3
import jwt
import bcrypt
from pydantic import BaseModel, EmailStr, ConfigDict
from pathlib import Path
from typing import Annotated
from annotated_types import MaxLen, MinLen


class CreateUser(BaseModel):
    username: str = Annotated[str, MinLen(3), MaxLen(9)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


class JWTToken(BaseModel):
    private_key: Path = Path('./jwt-private.pem')
    public_key: Path = Path('./jwt-public.pem')
    algorithm_jwt: str = "RS256"


setting = JWTToken()


# encoded = jwt.encode({"some": "payload"}, private_key, algorithm="RS256")
#
# decoded = jwt.decode(encoded, public_key, algorithms=["RS256"])

def encode_jwt(payload: dict, private_key: str = setting.private_key.read_text(),
               algorithm: str = setting.algorithm_jwt) -> str:
    return jwt.encode(payload=payload, private_key=private_key, algorithm=algorithm)


def decode_jwt(encoding_token: str | bytes, public_key: str = setting.public_key.read_text(),
               algorithm: str = setting.algorithm_jwt) -> str:
    return jwt.decode(encoding=encoding_token, public_key=public_key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    print(salt)
    pwd_bytes: bytes = password.encode()
    print(bcrypt.hashpw(pwd_bytes, salt))
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes, ) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
