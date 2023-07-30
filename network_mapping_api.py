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
async def network_information(technician_id, client_id, network_name):
    return server.get_network_information(technician_id, client_id, network_name)

@app.get("")
@app.post("/add_network")
async def add_network(technician_id, client_id, network_name, network_location, path):
    return server.add_network(technician_id, client_id, network_name, network_location, path)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
