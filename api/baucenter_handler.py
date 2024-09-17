from fastapi import APIRouter

from workers.kafka_action.consumer import consume
from workers.kafka_action.producer import send_one

baucenter_router = APIRouter(prefix="/baucenter", tags=["Baucenter"])


@baucenter_router.get("/baucenter")
async def get_baucenter_card(url: str):
    topic = "baucenter"
    await send_one(url=url, topic=topic)
    res = await consume()
    return res
