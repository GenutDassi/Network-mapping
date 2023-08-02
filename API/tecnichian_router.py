from API.network_router import router
from fastapi import Response, Form

from authorization_and_authentication.authorization_and_authentication_patterns import MyToken, Technician
from authorization_and_authentication.authorization_and_authentication_patterns import MyToken
from exception_decorators.catch_exception import catch_exception
from functionality import tecnichian_functionality


@catch_exception
@router.post("/login", response_model=MyToken)
async def login(response: Response, name: str = Form(...), password: str = Form(...)):
    return await tecnichian_functionality.login(response, name, password)

@catch_exception
@router.post("/signup")
async def signup(name: str = Form(...), password: str = Form(...)):
    return await tecnichian_functionality.signup(name, password)
