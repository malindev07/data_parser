from datetime import datetime

from pymongo import MongoClient


class DataBaseConnection:
    db = None
    host: str
    port: int
    db_name: str

    def __init__(self, host: str, port: int, db_name: str) -> None:
        self.host = host
        self.port = port
        self.db_name = db_name
        self.db = self.return_db()

    @staticmethod
    def return_client():  # название лучше get
        return MongoClient("mongodb://localhost:27017/")
        # return MongoClient("mongodb://mongodb:27017/")

    def return_db(self):  # название лучше get
        con = self.return_client()
        db = con[self.db_name]
        return db


# con = DataBaseConnection(host="localhost", port=27017, db_name="parser_db")
con = DataBaseConnection(host="mongo", port=27017, db_name="parser_db")
Database = con.return_db()


def save_data_to_db(old_price: str, new_price: str, topic: str, title: str):
    res = {
        "title": title,
        "old_price": old_price,
        "new_price": new_price,
        "date_time": datetime.now(),
    }
    Database[topic][title].insert_one(res)
