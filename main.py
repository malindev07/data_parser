import json
import pathlib

import requests
from bs4 import BeautifulSoup, ResultSet

from pathlib import *

from requests import Response


def format_str(entry_str: str) -> str:
    rep = [" / ", "/", ",", " ", ".", "!", "@", "?", "+"]

    for znak in rep:
        if znak in entry_str:
            entry_str = entry_str.replace(znak, "_")

    return entry_str


# cобираем карточку товара
def create_product_card(path: Path, sub_category_name: str):
    p_file = pathlib.Path(path)
    src = p_file.read_text(encoding="utf-8")
    data = json.loads(src)

    product_card_with_name_dict: dict = {}

    for item in data:
        item_text = format_str(item)

        # req = requests.get(data[item])
        # src = req.text
        p_file = pathlib.Path(f"{path.parent}/{item_text}.html")
        # p_file.write_text(src, encoding="utf-8")

        code_html: str = p_file.read_text(encoding="utf-8")
        soup: BeautifulSoup = BeautifulSoup(code_html, "lxml")
        price = soup.find("div", class_="price-current").text
        price = price[1:]
        article = soup.find("div", class_="shop2-product-article").text
        price = price.replace(" Р ", "")
        article = article.replace("Артикул: ", "")
        # print(article)
        # print(price)

        exit_list_categories: list = ["iMac", "Стекла_для_Apple_Watch"]
        exit_list_articles: list = [
            "ILC-IP13PM-CARD",
            "GRAVRU",
            "GRAVRU",
            "ILC-IP14PM-CARD",
            "iL-MAGN-13P-CLN",
            "ILC-IP13-CARD",
            "ILC-IP11-CARD",
            "EU-ADAPTER",
        ]
        if sub_category_name in exit_list_categories or article in exit_list_articles:
            break

        table_head = soup.find(
            "table", class_="product-item-options reset-table"
        ).find_all("tr")

        product_card_dict: dict = {}

        for item in table_head:
            row_name = item.find("th").text
            row_contains = item.find("td").text

            if row_name == "Цвет товара":
                row_contains = item.find("p", class_="tit_color").text

            product_card_dict[row_name] = row_contains

        product_card_dict["price"] = price
        product_card_dict["article"] = article
        product_card_with_name_dict[item_text] = product_card_dict

        print(product_card_with_name_dict)

        p_json_file = pathlib.Path((f"{path.parent}/{sub_category_name}_cards.json"))
        p_json_file.write_text(
            json.dumps(product_card_with_name_dict, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )


## собираем все товары в категории
def create_data_sub_sub_category(
    parent_category_name: str, sub_category_name: str, sub_category_url: str
):
    # req: Response = requests.get(sub_category_url)
    # src = req.text

    # p_dir = pathlib.Path(
    #     f"data/sotohit_data/{parent_category_name}/{sub_category_name}"
    # )
    # p_dir.mkdir(parents=True, exist_ok=True)

    p_file = pathlib.Path(
        f"data/sotohit_data/{parent_category_name}/{sub_category_name}/{sub_category_name}.html"
    )

    # p_file.write_text(src, encoding="utf-8")

    code_html: str = p_file.read_text(encoding="utf-8")
    soup: BeautifulSoup = BeautifulSoup(code_html, "lxml")

    all_products_in_category: ResultSet = soup.find_all(
        "div", class_="uk-grid-item shop2-product-item"
    )
    all_products_in_category_dict: dict = {}

    for item in all_products_in_category:
        item_text = item.find("div", class_="product-item-name").text
        item_link = "https://sotohit.ru" + item.find(
            "div", class_="product-item-name"
        ).find("a").get("href")
        all_products_in_category_dict[item_text] = item_link
        # print(item_text, item_link)

    p_json_file = pathlib.Path(
        f"data/sotohit_data/{parent_category_name}/{sub_category_name}/{sub_category_name}.json"
    )
    # p_json_file.write_text(
    #     json.dumps(all_products_in_category_dict, ensure_ascii=False, indent=4),
    #     encoding="utf-8",
    # )
    # print(p_json_file)
    # print(sub_category_name)
    create_product_card(p_json_file, sub_category_name)


## для тех категорий у которых нет саб категорий
def create_data_wo_sub_categories(category_name: str):
    code_html: str = pathlib.Path(
        f"data/sotohit_data/{category_name}/{category_name}.html"
    ).read_text(encoding="utf-8")

    soup = BeautifulSoup(code_html, "lxml")

    all_products = soup.find_all("div", class_="uk-grid-item shop2-product-item")

    all_products_dict: dict = {}

    for item in all_products:
        item_text = item.find(class_="product-item-name").text
        item_link = item.find(class_="product-item-name").find("a").get("href")
        all_products_dict[item_text] = item_link

    json_data = pathlib.Path(f"data/sotohit_data/{category_name}/{category_name}.json")
    "data/sotohit_data/Игровые_приставки/Игровые_приставки.json"
    # json_data.write_text(
    #     json.dumps(all_products_dict, ensure_ascii=False, indent=4),
    #     encoding="utf-8",
    # )


## собираем все подкатегории кглавных категории товаров
def create_data_sub_categories(url: str, all_categories_with_link: dict):
    exit_list: list = ["Игровые_приставки", "Цифровые_плееры", "Портативная_акустика"]

    for category_name, category_link in all_categories_with_link.items():
        rep = [" / ", " ", ",", "-"]

        for znak in rep:
            if znak in category_name:
                category_name = category_name.replace(znak, "_")

        if category_name in exit_list:
            create_data_wo_sub_categories(category_name)
        else:

            code_html: str = pathlib.Path(
                f"data/sotohit_data/{category_name}/{category_name}.html"
            ).read_text(encoding="utf-8")

            soup = BeautifulSoup(code_html, "lxml")

            all_sub_categories = soup.find_all("div", class_="main-categories-item")

            all_sub_categories_dict: dict = {}

            for item in all_sub_categories:

                sub_category_name: str = item.find(
                    "div", class_="main-categories-item-name"
                ).text

                sub_category_name = format_str(sub_category_name)

                sub_category_link: str = url + item.find(
                    "a", class_="main-categories-item-link"
                ).get("href")

                create_data_sub_sub_category(
                    parent_category_name=category_name,
                    sub_category_name=sub_category_name,
                    sub_category_url=sub_category_link,
                )

                all_sub_categories_dict[sub_category_name] = sub_category_link
                # print(all_sub_categories_dict[sub_category_name])
            json_data = pathlib.Path(
                f"data/sotohit_data/{category_name}/{category_name}.json"
            )
            # json_data.write_text(
            #     json.dumps(all_sub_categories_dict, ensure_ascii=False, indent=4),
            #     encoding="utf-8",
            # )

            # req: Response = requests.get(category_link)
            # src: str = req.text

            # p_dir = pathlib.Path(f"data/sotohit_data/{category_name}")
            # p_dir.mkdir(parents=True, exist_ok=True)

            p_file = pathlib.Path(
                f"data/sotohit_data/{category_name}/{category_name}.html"
            )
            # p_file.write_text(src, encoding="utf-8")


## собираем все главные категории товаров
def create_data_category(url: str):
    p: Path = pathlib.Path("data/sotohit_data/index.html")
    code_html: str = p.read_text(encoding="utf-8")

    soup: BeautifulSoup = BeautifulSoup(code_html, "lxml")

    all_categories: ResultSet = soup.find_all(
        "li", class_="has-child dontsplit", id="q111"
    )

    all_categories_with_link: dict = {}

    for item in all_categories:
        category_name: str = item.find("a").text
        category_link: str = item.find("a").get("href")
        all_categories_with_link[category_name] = url + category_link
        # print(category_name, category_link)

    json_file: Path = pathlib.Path(f"data/sotohit_data/sotohit_categories.json")
    # json_file.write_text(
    #     json.dumps(all_categories_with_link, ensure_ascii=False, indent=4),
    #     encoding="utf-8",
    # )

    create_data_sub_categories(
        url=url, all_categories_with_link=all_categories_with_link
    )


def get_url() -> str:
    url: str = "https://sotohit.ru"
    return url


def get_headers():
    headers: dict = {
        "Accept": "*/*",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
    return headers


def create_main_data():
    # req: Response = requests.get(url=get_url(), headers=get_headers())
    #
    # src: str = req.text

    p: Path = pathlib.Path("data/sotohit_data/index.html")
    # p.write_text(src, encoding="utf-8")

    create_data_category(url=get_url())


if __name__ == "__main__":
    create_main_data()
    # create_data_sub_sub_category(
    #     parent_category_name="Apple_iPhone",
    #     sub_category_name="iPhone_15",
    #     sub_category_url="https://sotohit.ru/folder/iphone-15",
    # )
