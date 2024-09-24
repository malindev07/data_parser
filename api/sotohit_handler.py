from fastapi import APIRouter


from workers.kafka_action.producer import send_one

sotohit_router = APIRouter(prefix="/sotohit", tags=["Sotohit"])


@sotohit_router.get("/sotohit")
async def get_sotohit_card(url: str):
    topic = "sotohit"

    await send_one(url=url, topic=topic)
