import json
import pathlib
import random
from dataclasses import dataclass
from html.parser import HTMLParser
from w3lib.html import replace_entities
from bs4 import BeautifulSoup, NavigableString
import requests


@dataclass
class WorkerBaucenter:
    url: str
    data_count: int

    @staticmethod
    def get_headers() -> dict[str, str]:
        headers = {
            "Accept": "*/*",
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }
        return headers

    def create_pages_htmls(self) -> None:
        req = requests.get(url=self.url, headers=self.get_headers())
        src = req.text

        for i in range(1, self.data_count + 1):
            p_file_html = (
                pathlib.Path()
                .cwd()
                .joinpath("workers")
                .joinpath("worker_baucenter")
                .joinpath(f"worker_baucenter_{i}.html")
            )

            p_file_html.write_text(src, encoding="utf-8")

    def create_json_data(self) -> None:
        product_cards_dict: list[dict[str, str]] = []

        for i in range(1, self.data_count + 1):
            product_card_dict: dict[str, str] = {}

            p_file_html = (
                pathlib.Path()
                .cwd()
                .joinpath("workers")
                .joinpath("worker_baucenter")
                .joinpath(f"worker_baucenter_{i}.html")
            )
            code_html = p_file_html.read_text(encoding="utf-8")

            soup = BeautifulSoup(code_html, "lxml")

            search_product_title = soup.find("section", class_="product")
            if search_product_title is not None:

                search_product_title_2 = search_product_title.find("h1")

                if search_product_title_2 is not None and not isinstance(
                    search_product_title_2, int
                ):
                    product_title = search_product_title_2.text
                    product_card_dict["Название"] = product_title
                else:
                    break
            else:
                break

            price: str

            search_price = soup.find("span", class_="price-block_price_text")

            if search_price is not None and not isinstance(search_price, int):
                search_price.extract()
                search_price_3 = soup.find("div", class_="price-block__price-text-wrap")
                if search_price_3 is not None:

                    price = search_price_3.text
                    price = price.strip().replace(" ", "")[:-2]
                    product_card_dict["Стоимость"] = price
                    # print(price)
                else:
                    break
            else:
                break

            search_short_list = soup.find("div", class_="product-collapse_drop")

            if search_short_list is not None:
                short_list = search_short_list.text.strip()
                product_card_dict["Описание"] = short_list
                # print(short_list)
            else:
                break

            search_tables_row = soup.find_all(class_="description-more_table-row")

            if search_tables_row is not None:

                for item in search_tables_row:
                    row = item.text.strip().split(":")
                    row_list: list[str] = []

                    for i in row:
                        if not isinstance(i, int):
                            row_list.append(i.strip())

                    product_card_dict[row_list[0]] = row_list[1]
            product_cards_dict.append(product_card_dict)

        p_file_json_data = (
            pathlib.Path()
            .cwd()
            .joinpath("workers")
            .joinpath("worker_baucenter")
            .joinpath(f"worker_baucenter.json")
        )
        p_file_json_data.write_text(
            json.dumps(product_cards_dict, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

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

        random_num = random.randint(0, self.data_count - 1)

        print(json.dumps(json_data[random_num], ensure_ascii=False, indent=4))
        return json_data[random_num]
