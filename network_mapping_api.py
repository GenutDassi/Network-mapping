import uvicorn
from fastapi import FastAPI

import server

app = FastAPI()


@app.get("/")
async def root():
    print("aaaa")
    return {"message": "hello"}


@app.get("/login")
async def login(name, password):
    return server.login(name, password)


@app.get("/signup")
async def login(name, password):
    return server.signup(name, password)


@app.get("network_information")
async def network_information(client_id, network_name):
    return server.network_information(client_id, network_name)


@app.post("/upload_file")
async def upload_file(client_id, path):
    return server.upload_file(client_id, path)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
