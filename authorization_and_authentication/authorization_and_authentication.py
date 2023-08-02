from CRUD import technician_CRUD
from DB import db_access
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status, Request, Response, encoders
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from passlib.context import CryptContext

from authorization_and_authentication.authorization_and_authentication_patterns import MyToken, \
    OAuth2PasswordBearerWithCookie, Technician, TechnicalInDB
from exception_decorators.catch_exception import catch_exception

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@catch_exception
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
    return MyToken(access_token=access_token, token_type="bearer")


@catch_exception
async def signup(name, password):
    hash_password = get_password_hash(password)
    await technician_CRUD.add_technician(name, hash_password)


@catch_exception
def get_password_hash(password):
    return pwd_context.hash(password)


@catch_exception
async def check_permission(client_id, technician_id):
    # permission = await db_access.execute_query("SELECT * FROM permission WHERE technician_id=%s AND client_id=%s",
    #                                            (technician_id, client_id))
    # if not permission:  # if permission = None - there is no permission
    #     return False
    return True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_cookie_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


@catch_exception
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@catch_exception
async def get_technician_from_db(technician_name: str):
    user_dict = await db_access.execute_query("SELECT * FROM technician WHERE technician.name = %s", technician_name)
    if user_dict:
        return TechnicalInDB(**user_dict[0])


@catch_exception
async def authenticate_technician(technical_name: str, password: str):
    technical = await get_technician_from_db(technical_name)
    if not technical:
        return None
    if not verify_password(password, technical.password):
        return None
    return technical


@catch_exception
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_technician(token: str = Depends(oauth2_cookie_scheme)):
@catch_exception
async def get_current_technician_name():
    # cookies = await get_cookies()
    # print("------------------------------------------")
    # print(cookies["Authorization"])
    # token = cookies["Authorization"]
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     technician_name: str = payload.get("sub")
    #     print("**********************")
    #     print("technician_name-info from cookie:", technician_name)
    #     if technician_name is None:
    #         raise credentials_exception
    #     token_data = TokenData(username=technician_name)
    #     print("token data", token_data)
    # except JWTError:
    #     raise credentials_exception
    # technician = get_technician_from_db(technician_name)
    # if technician is None:
    #     raise credentials_exception
    # return technician
    return 'Yosi'


@catch_exception
async def get_cookies(request: Request) -> dict:
    print("-------------cookies:", request.cookies)
    return dict(request.cookies)


# TODO: complete this function!!!!!!!!!!!!
@catch_exception
async def get_current_active_technician(current_user: Technician):
    if current_user and current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
