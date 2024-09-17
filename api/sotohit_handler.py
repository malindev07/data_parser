from fastapi import APIRouter, Request

from workers.kafka_action.consumer import consume
from workers.kafka_action.producer import send_one

sotohit_router = APIRouter(prefix="/sotohit", tags=["Sotohit"])


@sotohit_router.get("/sotohit")
async def get_sotohit_card(req: Request, url: str):
    topic = "sotohit"
    await send_one(url=url, topic=topic)
    res = await consume()
    return res


# @sotohit_router.post("/test")
# async def test(req: Request, topic: str):
#     a = {"123": 4444}
#     req.state.con.db[topic].insert_one(a)
