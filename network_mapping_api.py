from typing import Union, Dict

import uvicorn
from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi import Response
from pydantic import BaseModel
from requests import Request

import server
# from authorization_and_authentication import OAuth2PasswordBearerWithCookie

app = FastAPI()


@app.get("/")
async def root():
    print("server is running!!!")
    return {"message": "hello"}


class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/login", response_model=Token)
async def login(request: Request, response: Response, name: str = Form(...), password: str = Form(...)):
    # cookies = dict(request.cookies)
    return await server.login(response, name, password)


@app.post("/signup")
async def signup(name: str = Form(...), password: str = Form(...)):
    return await server.signup(name, password)


@app.get("/network/information/{client_id}/{network_name}")
async def get_network_information(client_id: int, network_name: str):
    return await server.get_network_information(client_id, network_name)


@app.get("/network/connections/{client_id}/{network_name}")
async def get_network_connections(client_id: int, network_name: str):
    return await server.get_connections(client_id, network_name)


@app.get("/network/devices/{client_id}/{network_name}")
async def get_network_devices(client_id: int, network_name: str):
    return await server.get_devices(client_id, network_name)


@app.post("/network/add_network", )
async def add_network(request: Request(), client_id: int, network_name: str = Form(...), network_location: str = Form(...)):
    return await server.add_network(request, client_id, network_name, network_location)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
