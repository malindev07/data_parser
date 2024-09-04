import json
import os
import pathlib
from bs4 import BeautifulSoup
import requests

from logger import logger


def get_url() -> str:
    url = "https://www.rbc.ru/"
    return url


def get_headers() -> dict[str, str]:
    headers: dict[str, str] = {
        "Accept": "*/*",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
    return headers


def pars_all_news() -> None:
    req = requests.get(url=get_url(), headers=get_headers())
    src = req.text

    # print(src)
    p_file = pathlib.Path("rbk_news_page.html")

    p_file.write_text(src, encoding="utf-8")


def parse_news_json() -> list[dict[str, str]]:
    # p_file = pathlib.Path("rbk_news_page.html")
    # src = p_file.read_text(encoding="utf-8")
    #
    # soup = BeautifulSoup(src, "lxml")
    #
    # news_list = soup.findAll(
    #     class_="news-feed__item js-visited js-news-feed-item js-yandex-counter"
    # )
    #
    # all_news_dict: list[dict[str, str]] = []
    #
    # for item in news_list:
    #     item_text = item.find("span", class_="news-feed__item__title").text
    #     item_category_w_time = item.find(
    #         "span", class_="news-feed__item__date-text"
    #     ).text
    #     item_category = item_category_w_time.split(",")[0]
    #     item_time = item_category_w_time.split(",")[1]
    #     item_url = item.get("href")
    #
    #     res_dict: dict = {
    #         "Заголовок новости": item_text,
    #         "Категория новости": item_category,
    #         "Время новости": item_time.strip(),
    #         "Ссылка на новость": item_url,
    #     }
    #     # print(item_text)
    #     all_news_dict.append(res_dict)
    #
    # all_news_dict.reverse()
    p_json_data = pathlib.Path("rbk_news.json")
    src = p_json_data.read_text(encoding="utf-8")
    json_data: list[dict[str, str]] = json.loads(src)

    if os.stat("rbk_news.json").st_size == 0:
        p_json_file = pathlib.Path("rbk_news.json")
        p_json_file.write_text(
            json.dumps(json_data, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )
    else:
        logger.info("File is not empty")
        checked_news = check_new_news()

        for new_news in checked_news:
            if new_news in json_data:
                logger.info("Такая новость уже была")
            else:
                print(new_news)

        p_json_file = pathlib.Path("rbk_news.json")
        p_json_file.write_text(
            json.dumps(checked_news, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    # print(json.dumps(all_news_dict, indent=4, ensure_ascii=False))
    return json_data


def check_new_news() -> list[dict[str, str]]:
    pars_all_news()
    p_file = pathlib.Path("rbk_news_page.html")
    src = p_file.read_text(encoding="utf-8")

    soup = BeautifulSoup(src, "lxml")

    news_list = soup.findAll(
        class_="news-feed__item js-visited js-news-feed-item js-yandex-counter"
    )

    all_news_dict: list[dict[str, str]] = []

    for item in news_list:
        item_text = item.find("span", class_="news-feed__item__title").text
        item_category_w_time = item.find(
            "span", class_="news-feed__item__date-text"
        ).text
        item_category = item_category_w_time.split(",")[0]
        item_time = item_category_w_time.split(",")[1]
        item_url = item.get("href")

        res_dict: dict[str, str] = {
            "Заголовок новости": item_text,
            "Категория новости": item_category,
            "Время новости": item_time.strip(),
            "Ссылка на новость": item_url,
        }
        # print(item_text)
        all_news_dict.append(res_dict)

    all_news_dict.reverse()

    return all_news_dict


# pars_all_news()
parse_news_json()
