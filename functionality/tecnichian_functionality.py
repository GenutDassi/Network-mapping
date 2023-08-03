from authorization_and_authentication import authorization_and_authentication
from exception_decorators.catch_exception import catch_exception



async def login(response, name, password):
    return await authorization_and_authentication.login(response, name, password)


# @catch_exception
async def signup(name, password):
    return await authorization_and_authentication.signup(name, password)