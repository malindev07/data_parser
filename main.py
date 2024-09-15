import asyncio
import contextlib
import time

import uvicorn

from api.baucenter_handler import baucenter_router
from api.sotohit_handler import sotohit_router
from logger import logger

# from workers.kafka_action.consumer import consume

from workers.worker_baucenter.worker_baucenter import WorkerBaucenter
from workers.worker_sotohit.worker_sotohit import WorkerSotohit
from fastapi import FastAPI


# @contextlib.asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield {"123": "123"}


app = FastAPI()


app.include_router(baucenter_router)
app.include_router(sotohit_router)

if __name__ == "__main__":
    uvicorn.run("main:app")
# asyncio.run(consume())
# logger.info("______________________________________")
# logger.info("Сейчас запустится парсер сайта sotohit")
# logger.info("______________________________________")
# time.sleep(3)
#
# create_main_data()
# logger.info("______________________________________")
# logger.info("Сейчас запустится парсер новостей")
# logger.info("______________________________________")
# time.sleep(3)
# parse_news_json()
#
# logger.info("______________________________________")
# logger.info("Сейчас запустится парсер сайта Бауентр")
# logger.info("______________________________________")
# time.sleep(3)
# parse_baucenter_data()

# logger.info("______________________________________")`
# logger.info("Сейчас запустится парсер сайта Sotohit")
# logger.info("______________________________________")
#
# worker_sotohit = WorkerSotohit(
#     url="https://sotohit.ru/internet-magazin2/product/apple-iphone-15-pro-max-256gb-natural-titanium-naturalnyj-titan-nano-sim-esim",
#     data_count=5,
# )
# time.sleep(2)
#
# # logger.info("______________________________________")
# # logger.info("Сейчас будут создавать страницы html")
# # logger.info("______________________________________")
# # time.sleep(2)
# # worker_sotohit.create_pages_htmls()
#
# logger.info("______________________________________")
# logger.info("Сейчас будут создаваться json с карточками")
# logger.info("______________________________________")
# time.sleep(2)
# worker_sotohit.create_json_data()
#
# logger.info("______________________________________")
# logger.info("Сейчас получим случайную карточку")
# logger.info("______________________________________")
# time.sleep(2)
# worker_sotohit.get_random_card()
#
# a = WorkerBaucenter(
#     url="https://baucenter.ru/product/drel-bezudarnaya-makita-6413-450-vt-ctg-29290-29342-29343-706005108/",
#     data_count=3,
# )
#
# time.sleep(4)
# logger.info("______________________________________")
# logger.info("Сейчас запустится парсер сайта Бауцентр")
# logger.info("______________________________________")
# # a.create_pages_htmls()
# time.sleep(2)
#
# logger.info("______________________________________")
# logger.info("Сейчас будут создаваться карточки")
# logger.info("______________________________________")
# time.sleep(2)
#
# a.create_json_data()
#
# logger.info("______________________________________")
# logger.info("Сейчас получим случайную карточку")
# logger.info("______________________________________")
# time.sleep(2)
# a.get_random_card()
