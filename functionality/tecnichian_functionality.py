from authorization_and_authentication import authorization_and_authentication


async def login(response, name, password):
    return await authorization_and_authentication.login(response, name, password)


async def signup(name, password):
    return await authorization_and_authentication.signup(name, password)