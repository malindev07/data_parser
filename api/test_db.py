from fastapi import APIRouter
from pymongo import MongoClient

from api.plots import get_prices, create_plot

db_router = APIRouter(prefix="/test", tags=["Test"])


@db_router.get("/create_plot")
async def create_lpot_prices(topic: str, title: str):
    await create_plot(
        prices=await get_prices(topic=topic, title=title), topic=topic, title=title
    )


@db_router.get("/test")
async def test_db(topic: str, title: str):
    client = MongoClient("mongodb://mongodb:27017/")
    # client = MongoClient("mongodb://localhost:27017/")
    db = client["parser_db"]
    collection = db[f"{topic}.{title}"]
    all_data = collection.find()

    old_prices: list[int] = []
    dates: list = []
    for item in all_data:

        old_prices.append(int(item["old_price"]))
        dates.append(item["date_time"])

    res = [old_prices, dates]
    print(old_prices)
    return res
