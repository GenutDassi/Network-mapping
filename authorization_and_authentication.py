import db_access
from datetime import datetime, timedelta
from typing import Union, Optional, Dict

from fastapi import Depends, HTTPException, status, Request, Response, encoders
from fastapi.security import OAuth2PasswordBearer, OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import technician_in_db
from network_mapping_api import Token

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    username: Union[str, None] = None


class Technician(BaseModel):
    name: str
    id: int


class TechnicalInDB(Technician):
    password: str


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("Authorization")  # changed to accept access token from httpOnly Cookie

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


async def login(response: Response, name: str, password: str):
    technician = await authenticate_technician(name, password)
    if not technician:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": technician.name}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    return Token(access_token=access_token, token_type="bearer")


async def signup(name, password):
    hash_password = get_password_hash(password)
    await technician_in_db.add_technician(name, hash_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def check_permission(client_id, technician_id):
    permission = db_access.execute_query("SELECT * FROM permission WHERE technician_id=%s AND client_id=%s",
                                         (technician_id, client_id))
    if not permission:  # if permission = None - there is no permission
        return False
    return True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_cookie_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_technician_from_db(technician_name: str):
    user_dict = await db_access.execute_query("SELECT * FROM technician WHERE technician.name = %s", technician_name)
    # print(user_dict[0])
    print("------------------")
    print(user_dict)
    if user_dict:
        print("technical in db", user_dict)
        return TechnicalInDB(**user_dict[0])


async def authenticate_technician(technical_name: str, password: str):
    technical = await get_technician_from_db(technical_name)
    if not technical:
        return None
    if not verify_password(password, technical.password):
        return None
    return technical


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_technician(token: str = Depends(oauth2_cookie_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        technician_name: str = payload.get("sub")
        if technician_name is None:
            raise credentials_exception
        token_data = TokenData(username=technician_name)
    except JWTError:
        raise credentials_exception
    user = get_technician_from_db(technician_name)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_technician(current_user: Technician = Depends(get_current_technician)):
    if current_user and current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


