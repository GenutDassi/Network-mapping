from API.network_router import router
from fastapi import Response, Form

from authorization_and_authentication.authorization_and_authentication_patterns import MyToken, Technician
from functionality import tecnichian_functionality


@router.post("/login", response_model=MyToken)
async def login(response: Response, name: str = Form(...), password: str = Form(...)):
    return await tecnichian_functionality.login(response, name, password)


@router.post("/signup")
async def signup(name: str = Form(...), password: str = Form(...)):
    return await tecnichian_functionality.signup(name, password)
