import uvicorn
from fastapi import FastAPI, Form

import server

app = FastAPI()


@app.get("/")
async def root():
    print("server is running!!!")
    return {"message": "hello"}


@app.get("/login")
async def login(name, password):
    return await server.login(name, password)


@app.get("/signup")
async def login(name: str = Form(...), password: str = Form(...)):
    return await server.signup(name, password)


@app.get("/network/information/{client_id}/{network_name}")
async def get_network_information(technician_id: int, client_id: int, network_name: str):
    return await server.get_network_information(technician_id, client_id, network_name)


@app.get("/network/connections/{client_id}/{network_name}")
async def get_network_connections(technician_id: int, client_id: int, network_name: str):
    return await server.get_connections(technician_id, client_id, network_name)


@app.get("/network/devices/{client_id}/{network_name}")
async def get_network_devices(technician_id: int, client_id: int, network_name: str):
    return await server.get_devices(technician_id, client_id, network_name)


@app.post("/network/add_network/{client_id}")
async def add_network(technician_id: int, client_id: int, network_name: str, network_location: str):
    return await server.add_network(technician_id, client_id, network_name, network_location)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
