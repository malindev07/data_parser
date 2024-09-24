import asyncio
import threading

import uvicorn


from api.baucenter_handler import baucenter_router

from api.sotohit_handler import sotohit_router

from fastapi import FastAPI

from api.test_db import db_router
from workers.kafka_action.consumer import start_consume

app = FastAPI()


app.include_router(baucenter_router)
app.include_router(sotohit_router)
app.include_router(db_router)

_thread = threading.Thread(target=asyncio.run, args=(start_consume(),))
_thread.start()

if __name__ == "__main__":

    uvicorn.run("main:app")

# https://baucenter.ru/product/drel-bezudarnaya-makita-6413-450-vt-ctg-29290-29342-29343-706005108/
# https://sotohit.ru/internet-magazin2/product/apple-iphone-15-pro-max-256gb-natural-titanium-naturalnyj-titan-nano-sim-esim
