from datetime import datetime

from pymongo import MongoClient


class DataBaseConnection:
    db = None
    host: str
    port: int
    db_name: str

    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.db = self.return_db()

    def return_client(self):
        return MongoClient(host=self.host, port=self.port)

    def return_db(self):
        con = self.return_client()
        db = con[self.db_name]
        return db


con = DataBaseConnection(host="localhost", port=27017, db_name="parser_db")
# con = DataBaseConnection(host="mongodb", port=27017, db_name="parser_db")
Database = con.return_db()


async def save_data_to_db(old_price: str, new_price: str, topic: str, title: str):
    res = {
        "title": title,
        "old_price": old_price,
        "new_price": new_price,
        "date_time": datetime.now(),
    }
    Database[topic][title].insert_one(res)
