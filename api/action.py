import asyncio
from typing import Any

from workers.worker_baucenter.worker_baucenter import WorkerBaucenter
from workers.worker_sotohit.worker_sotohit import WorkerSotohit


async def create_parser(url: str, topic: str, data_count: int):
    parser: WorkerSotohit | WorkerBaucenter = Any
    if topic == "sotohit":
        parser = WorkerSotohit(url=url, data_count=data_count)
    elif topic == "baucenter":
        parser = WorkerBaucenter(url=url, data_count=data_count)

    await parser.create_pages_htmls()
    await parser.create_json_data()
    res = await parser.check_changes()

    return res


# asyncio.run(
#     create_parser(
#         url="https://sotohit.ru/internet-magazin2/product/apple-iphone-15-pro-max-256gb-natural-titanium-naturalnyj"
#         "-titan-nano",
#         topic="sotohit",
#         data_count=5,
#     )
# )
