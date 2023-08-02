from CRUD import technician_CRUD
from DB import db_access
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status, Request, Response, encoders
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from passlib.context import CryptContext

from authorization_and_authentication.authorization_and_authentication_patterns import MyToken, \
    OAuth2PasswordBearerWithCookie, Technician, TechnicalInDB, TokenData

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 40


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
    _token = encoders.jsonable_encoder(access_token)
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {_token}",
        httponly=True
    )
    return MyToken(access_token=access_token, token_type="bearer")


async def signup(name, password):
    hash_password = get_password_hash(password)
    await technician_CRUD.add_technician(name, hash_password)


async def check_permission(technician_id, client_id):
    permission = await db_access.execute_query("SELECT * FROM permission WHERE technician_id=%s AND client_id=%s",
                                               (technician_id, client_id))
    if not permission:  # if permission = None - there is no permission
        return False
    return True


def get_password_hash(password):
    return pwd_context.hash(password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_cookie_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_technician_from_db(technician_name: str):
    user_dict = await db_access.execute_query("SELECT * FROM technician WHERE technician.name = %s", technician_name)
    if user_dict:
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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    current_technician = await get_technician_from_db(technician_name=token_data.username)
    if current_technician is None:
        raise credentials_exception
    return current_technician


async def get_current_active_technician(current_technician: Technician = Depends(get_current_technician)):
    return current_technician
