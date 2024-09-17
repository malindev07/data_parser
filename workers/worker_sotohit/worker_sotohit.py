import json
import pathlib
import random
from dataclasses import dataclass
from bs4 import BeautifulSoup, NavigableString
import requests

from db.mongo_db_parser import save_data_to_db
from logger import logger


@dataclass
class WorkerSotohit:
    url: str
    data_count: int
    topic: str = "sotohit"

    @staticmethod
    async def get_headers() -> dict[str, str]:
        headers = {
            "Accept": "*/*",
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }
        return headers

    async def create_pages_htmls(self) -> None:
        req = requests.get(url=self.url, headers=await self.get_headers())
        src = req.text

        for i in range(1, self.data_count + 1):
            p_file_html = (
                pathlib.Path()
                .cwd()
                .joinpath("workers")
                .joinpath("worker_sotohit")
                .joinpath(f"worker_sotohit_{i}.html")
            )
            p_file_html.write_text(src, encoding="utf-8")

    async def create_json_data(self) -> None:
        product_cards_dict: list[dict[str, str]] = []

        for i in range(1, self.data_count + 1):
            p_file_html = (
                pathlib.Path()
                .cwd()
                .joinpath("workers")
                .joinpath("worker_sotohit")
                .joinpath(f"worker_sotohit_{i}.html")
            )
            code_html = p_file_html.read_text(encoding="utf-8")

            soup = BeautifulSoup(code_html, "lxml")

            search_product_title = soup.find(class_="site-content-inner")
            if search_product_title is not None:

                search_product_title_2 = search_product_title.find("h1")

                if search_product_title_2 is not None and not isinstance(
                    search_product_title_2, int
                ):
                    product_title = search_product_title_2.text
                else:
                    break
            else:
                break

            search_price = soup.find("div", class_="price-current")

            price: str
            if search_price is not None:
                price = search_price.text
                price = price[1:]
                price = price.replace(" Р ", "")
            else:
                break

            search_article = soup.find("div", class_="shop2-product-article")

            article: str
            if search_article is not None:
                article = search_article.text
                article = article.replace("Артикул: ", "")
            else:
                break

            search_find_table_head = soup.find(
                "table", class_="product-item-options reset-table"
            )
            if search_find_table_head is not None and not isinstance(
                search_find_table_head, NavigableString
            ):
                search_find_all_table_head = search_find_table_head.find_all("tr")
                if search_find_all_table_head is not None:
                    table_head = search_find_all_table_head
                else:
                    break
            else:
                break

            product_card_dict: dict[str, str] = {"Наименование": product_title}

            for item in table_head:
                row_name = item.find("th").text
                row_contains = item.find("td").text

                if row_name == "Цвет товара":
                    row_contains = item.find("p", class_="tit_color").text

                product_card_dict[row_name] = row_contains

            product_card_dict["price"] = price
            if i % 2 == 1:
                product_card_dict["price"] = str(random.randint(1, 100000))

            product_card_dict["article"] = article

            product_cards_dict.append(product_card_dict)

        p_file_json_data = (
            pathlib.Path()
            .cwd()
            .joinpath("workers")
            .joinpath("worker_sotohit")
            .joinpath(f"worker_sotohit.json")
        )
        p_file_json_data.write_text(
            json.dumps(product_cards_dict, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )
        # print(json.dumps(product_cards_dict, ensure_ascii=False, indent=4))

    async def get_random_card(self) -> dict[str, str]:
        p_file_json_data: pathlib.Path = (
            pathlib.Path()
            .cwd()
            .joinpath("workers")
            .joinpath("worker_sotohit")
            .joinpath(f"worker_sotohit.json")
        )
        data: str = p_file_json_data.read_text(encoding="utf-8")

        json_data: list[dict[str, str]] = json.loads(data)
        self.data_count = len(json_data)
        random_num = random.randint(0, self.data_count - 1)

        # logger.info(json.dumps(json_data[random_num], ensure_ascii=False, indent=4))
        return json_data[random_num]

    async def update_card(self):
        req = requests.get(url=self.url, headers=await self.get_headers())
        src = req.text

        soup = BeautifulSoup(src, "lxml")

        search_product_title = soup.find(class_="site-content-inner")
        if search_product_title is not None:

            search_product_title_2 = search_product_title.find("h1")

            if search_product_title_2 is not None and not isinstance(
                search_product_title_2, int
            ):
                product_title = search_product_title_2.text
            else:
                return None
        else:
            return None

        search_price = soup.find("div", class_="price-current")

        price: str
        if search_price is not None:
            price = search_price.text
            price = price[1:]
            price = price.replace(" Р ", "")
        else:
            return None

        search_article = soup.find("div", class_="shop2-product-article")

        article: str
        if search_article is not None:
            article = search_article.text
            article = article.replace("Артикул: ", "")
        else:
            return None

        search_find_table_head = soup.find(
            "table", class_="product-item-options reset-table"
        )
        if search_find_table_head is not None and not isinstance(
            search_find_table_head, NavigableString
        ):
            search_find_all_table_head = search_find_table_head.find_all("tr")
            if search_find_all_table_head is not None:
                table_head = search_find_all_table_head
            else:
                return None
        else:
            return None

        product_card_dict: dict[str, str] = {"Наименование": product_title}

        for item in table_head:
            row_name = item.find("th").text
            row_contains = item.find("td").text

            if row_name == "Цвет товара":
                row_contains = item.find("p", class_="tit_color").text

            product_card_dict[row_name] = row_contains

        product_card_dict["price"] = price
        product_card_dict["article"] = article

        return product_card_dict

    async def check_changes(self):
        old_data = await self.get_random_card()
        new_data = await self.update_card()

        if old_data["price"] != new_data["price"]:
            res = f"Цена изменилась! Старая цена {old_data['price']}, новая цена {new_data['price']} "
            await save_data_to_db(
                old_price=old_data["price"],
                new_price=new_data["price"],
                title=old_data["Наименование"],
                topic=self.topic,
            )
            return res
        else:
            res = f"Изменений у товара {old_data['Наименование']} нет"
            return res

        # return new_data


# a = WorkerSotohit(
#     url="https://sotohit.ru/internet-magazin2/product/apple-iphone-15-pro-max-256gb-natural-titanium-naturalnyj-titan-nano"
#     "-sim"
#     "-esim",
#     data_count=5,
# )
#
# a.check_changes()
