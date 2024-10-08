import json
import pathlib
import random
from dataclasses import dataclass

from bs4 import BeautifulSoup
import requests

from db.mongo_db_parser import save_data_to_db


@dataclass
class WorkerBaucenter:

    url: str
    data_count: int
    topic: str = "baucenter"

    @staticmethod
    def get_headers() -> dict[str, str]:
        headers = {
            "Accept": "*/*",
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }
        return headers

    def create_pages_htmls(self) -> None:
        # req = requests.get(url=self.url, headers=self.get_headers())
        # src = req.text
        #
        # for i in range(1, self.data_count + 1):
        #     p_file_html = (
        #         pathlib.Path()
        #         .cwd()
        #         .joinpath("workers")
        #         .joinpath("worker_baucenter")
        #         .joinpath(f"worker_baucenter_{i}.html")
        #     )
        #
        #     p_file_html.write_text(src, encoding="utf-8")
        pass

    def create_json_data(self) -> None:
        # product_cards_dict: list[dict[str, str]] = []
        #
        # for i in range(1, self.data_count + 1):
        #     product_card_dict: dict[str, str] = {}
        #
        #     p_file_html = (
        #         pathlib.Path()
        #         .cwd()
        #         .joinpath("workers")
        #         .joinpath("worker_baucenter")
        #         .joinpath(f"worker_baucenter_{i}.html")
        #     )
        #     print(p_file_html)
        #     code_html = p_file_html.read_text(encoding="utf-8")
        #
        #     soup = BeautifulSoup(code_html, "lxml")
        #
        #     search_product_title = soup.find("section", class_="product")
        #     if search_product_title is not None:
        #
        #         search_product_title_2 = search_product_title.find("h1")
        #
        #         if search_product_title_2 is not None and not isinstance(
        #             search_product_title_2, int
        #         ):
        #             product_title = search_product_title_2.text
        #             product_card_dict["Название"] = product_title
        #         else:
        #             break
        #     else:
        #         break
        #
        #     price: str
        #
        #     search_price = soup.find("span", class_="price-block_price_text")
        #
        #     if search_price is not None and not isinstance(search_price, int):
        #         search_price.extract()
        #         search_price_3 = soup.find("div", class_="price-block__price-text-wrap")
        #         if search_price_3 is not None:
        #
        #             price = search_price_3.text
        #             price = price.strip().replace(" ", "")[:-2]
        #             product_card_dict["Стоимость"] = price
        #             if i % 2 == 1:
        #                 product_card_dict["Стоимость"] = str(random.randint(1, 100000))
        #             # print(price)
        #         else:
        #             break
        #     else:
        #         break
        #
        #     search_short_list = soup.find("div", class_="product-collapse_drop")
        #
        #     if search_short_list is not None:
        #         short_list = search_short_list.text.strip()
        #         product_card_dict["Описание"] = short_list
        #         # print(short_list)
        #     else:
        #         break
        #
        #     search_tables_row = soup.find_all(class_="description-more_table-row")
        #
        #     if search_tables_row is not None:
        #
        #         for item in search_tables_row:
        #             row = item.text.strip().split(":")
        #             row_list: list[str] = []
        #
        #             for i in row:
        #                 if not isinstance(i, int):
        #                     row_list.append(i.strip())
        #
        #             product_card_dict[row_list[0]] = row_list[1]
        #     product_cards_dict.append(product_card_dict)
        #
        # p_file_json_data = (
        #     pathlib.Path()
        #     .cwd()
        #     .joinpath("workers")
        #     .joinpath("worker_baucenter")
        #     .joinpath(f"worker_baucenter.json")
        # )
        # p_file_json_data.write_text(
        #     json.dumps(product_cards_dict, indent=4, ensure_ascii=False),
        #     encoding="utf-8",
        # )
        pass

    def get_random_card(self) -> dict[str, str]:

        p_file_json_data: pathlib.Path = (
            pathlib.Path()
            .cwd()
            .joinpath("workers")
            .joinpath("worker_baucenter")
            .joinpath(f"worker_baucenter.json")
        )
        data: str = p_file_json_data.read_text(encoding="utf-8")

        json_data: list[dict[str, str]] = json.loads(data)
        self.data_count = len(json_data)
        random_num = random.randint(0, self.data_count - 1)

        # logger.info(json.dumps(json_data[random_num], ensure_ascii=False, indent=4))
        return json_data[random_num]

    def update_card(self):
        # req = requests.get(url=self.url, headers=self.get_headers())
        # src = req.text
        #
        # soup = BeautifulSoup(src, "lxml")
        #
        # product_card_dict: dict[str, str] = {}
        #
        # search_product_title = soup.find("section", class_="product")
        # if search_product_title is not None:
        #
        #     search_product_title_2 = search_product_title.find("h1")
        #
        #     if search_product_title_2 is not None and not isinstance(
        #         search_product_title_2, int
        #     ):
        #         product_title = search_product_title_2.text
        #         product_card_dict["Название"] = product_title
        #     else:
        #         return None
        # else:
        #     return None
        #
        # price: str
        #
        # search_price = soup.find("span", class_="price-block_price_text")
        #
        # if search_price is not None and not isinstance(search_price, int):
        #     search_price.extract()
        #     search_price_3 = soup.find("div", class_="price-block__price-text-wrap")
        #     if search_price_3 is not None:
        #
        #         price = search_price_3.text
        #         price = price.strip().replace(" ", "")[:-2]
        #         product_card_dict["Стоимость"] = price
        #         # print(price)
        #     else:
        #         return None
        # else:
        #     return None
        #
        # search_short_list = soup.find("div", class_="product-collapse_drop")
        #
        # if search_short_list is not None:
        #     short_list = search_short_list.text.strip()
        #     product_card_dict["Описание"] = short_list
        #     # print(short_list)
        # else:
        #     return None
        #
        # search_tables_row = soup.find_all(class_="description-more_table-row")
        #
        # if search_tables_row is not None:
        #
        #     for item in search_tables_row:
        #         row = item.text.strip().split(":")
        #         row_list: list[str] = []
        #
        #         for i in row:
        #             if not isinstance(i, int):
        #                 row_list.append(i.strip())
        #
        #         product_card_dict[row_list[0]] = row_list[1]
        #
        #         return product_card_dict
        price: int = random.randint(1, 20000)
        res = {
            "Название": "Дрель безударная Makita 6413, 450 Вт",
            "Стоимость": str(price),
            "Описание": "Безударная дрель предназначена для сверления отверстий в различных материалах.",
            "Тип": "Дрели безударные",
            "Марка": "Makita",
            "Мощность (Вт)": "450",
            "Электронная регулировка оборотов": "Нет",
            "Max диаметр сверления в дереве (мм)": "25",
            "Max диаметр сверления в металле (мм)": "10",
            "Max диаметр сверла в патроне (мм)": "10",
            "Тип патрона": "Быстрозажимной",
            "Диаметр патрона (мм)": "1.5-10",
            "Тип двигателя": "Щеточный",
            "Число скоростей": "1",
            "Число оборотов (об/мин)": "0-3000",
            "Наличие удара": "Нет",
            "Наличие реверса": "Да",
            "Комплектация": "Инструкция, упаковка",
            "Страна производства": "Китай",
            "Гарантия производителя": "1 год",
            "Вес брутто                                        (кг/шт)": "2",
        }
        return res

    def check_changes(self):
        old_data = self.get_random_card()
        new_data = self.update_card()
        res: str = ""

        if old_data["Стоимость"] != new_data["Стоимость"]:
            res = f"Цена изменилась! Старая цена {old_data['Стоимость']}, новая цена {new_data['Стоимость']}"
            save_data_to_db(
                old_price=old_data["Стоимость"],
                new_price=new_data["Стоимость"],
                title=old_data["Название"],
                topic=self.topic,
            )
            return res
        else:
            res = f"Изменений у товара {old_data['Название']} нет"
            return res

    def return_title(self):
        title = self.get_random_card()
        return title["Название"]
