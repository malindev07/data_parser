import json
import pathlib
import time

import requests
from bs4 import BeautifulSoup

from data.sotohit_data.sotohit_parser import format_str
from logger import logger


def get_url() -> str:
    url = "https://baucenter.ru/catalog/dreli-ctg-29290-29342-29343/"
    return url


def get_headers() -> dict[str, str]:
    headers: dict[str, str] = {
        "Accept": "*/*",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
    return headers


def parse_baucenter_data():
    res = get_pagination_number()
    count_item = 0
    count_pagen = int(res[0])
    category = res[1]

    electric_instrument_list_dict: list[dict[str, str]] = []

    p_file = pathlib.Path().cwd().joinpath(f"data/baucenter_data/baucenter_{category}")
    p_file.mkdir(exist_ok=True)

    for item_pagen in range(1, int(count_pagen) + 1):

        req = requests.get(url=get_url(), headers=get_headers())

        time.sleep(1)
        src = req.text

        # print(req.url)

        p_file_html = (
            pathlib.Path()
            .cwd()
            .joinpath(
                f"data/baucenter_data/baucenter_{category}/{category}_pagen{item_pagen}.html"
            )
        )
        p_file_html.write_text(src, encoding="utf-8")

        code_html = p_file_html.read_text(encoding="utf-8")

        soup = BeautifulSoup(code_html, "lxml")
        #
        electric_instrument_list = soup.find_all(
            "div", class_="catalog_item with-tooltip"
        )

        for item in electric_instrument_list:
            count_item += 1
            new_electric_device: dict[str, str] = {
                "Внутренний номер": str(count_item),
                "Наименование товара": item["data-name"],
                "Артикул": item["data-article"],
                "Стоимость": item["data-price"],
                "Бренд": item["data-brand"],
                "Категория": item["data-category"],
            }

            electric_instrument_list_dict.append(new_electric_device)
        # print(json.dumps(electric_instrument_list_dict, indent=4, ensure_ascii=False))
    count_upd = 0
    if (
        pathlib.Path()
        .cwd()
        .joinpath(f"data/baucenter_data/baucenter_{category}/{category}.json")
        .exists()
    ):
        old_data = check_upd(category=category)

        for item in range(len(electric_instrument_list_dict)):
            if (
                electric_instrument_list_dict[item]["Наименование товара"]
                == old_data[item]["Наименование товара"]
            ):
                if (
                    electric_instrument_list_dict[item]["Стоимость"]
                    != old_data[item]["Стоимость"]
                ):
                    logger.info(
                        f"У товара {electric_instrument_list_dict[item]["Наименование товара"]} изменилась цена! Старая цена: {old_data[item]["Стоимость"]}, Новая цена: {electric_instrument_list_dict[item]["Стоимость"]} "
                    )
                    count_upd += 1

            p_file_json = (
                pathlib.Path()
                .cwd()
                .joinpath(f"data/baucenter_data/baucenter_{category}/{category}.json")
            )
            p_file_json.write_text(
                json.dumps(electric_instrument_list_dict, indent=4, ensure_ascii=False),
                encoding="utf-8",
            )

            # print(electric_instrument_list_dict[item]["Стоимость"])
    else:
        p_file_json = (
            pathlib.Path()
            .cwd()
            .joinpath(f"data/baucenter_data/baucenter_{category}/{category}.json")
        )
        p_file_json.write_text(
            json.dumps(electric_instrument_list_dict, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )
    logger.info(f"Колиечство изменений в Бауцентр {count_upd}")


def get_pagination_number():
    req = requests.get(url=get_url(), headers=get_headers())
    src = req.text
    # p_file = p_file = pathlib.Path().cwd().joinpath("baucenter_test.html")
    # p_file.write_text(src, encoding="utf-8")
    #
    # p_file_html = p_file = pathlib.Path().cwd().joinpath("baucenter_test.html")
    # src = p_file_html.read_text(encoding="utf-8")

    soup = BeautifulSoup(src, "lxml")
    category = format_str(soup.find("h1", class_="paddings").text)
    pagen_count = soup.find(class_="pagination")

    if pagen_count is None:
        return [1, category]

    pagen_list = pagen_count.find_all(class_="hidden-xs pagination_button")

    pagen_count_num = pagen_list[-1].text

    return [pagen_count_num, category]


def check_upd(category: str):
    category = format_str(category)
    p_file = (
        pathlib.Path()
        .cwd()
        .joinpath(f"data/baucenter_data/baucenter_{category}/{category}.json")
    )
    # print(p_file)
    src = p_file.read_text(encoding="utf-8")

    data_json = json.loads(src)
    # print(json.dumps(data_json, indent=4, ensure_ascii=False))
    return data_json


# get_pagination_number()
# parse_baucenter_data()
# check_upd("Шуруповерты, гайковерты")
