import os
import sys

import uvicorn
from fastapi import FastAPI

from API import network_router, tecnichian_router

curr_path = os.path.dirname(__file__)
root_path = os.path.join(curr_path, "../..")
sys.path.append(root_path)

app = FastAPI()

app.include_router(network_router.router)
app.include_router(tecnichian_router.router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
