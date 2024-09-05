import time

from data.baucenter_data.baucenter_parser import parse_baucenter_data
from data.news_data.rbk_news_parser import parse_news_json
from data.sotohit_data.sotohit_parser import create_main_data
from logger import logger
from workers.worker_sotohit.worker_sotohit import WorkerSotohit

if __name__ == "__main__":
    # logger.info("______________________________________")
    # logger.info("Сейчас запустится парсер сайта sotohit")
    # logger.info("______________________________________")
    # time.sleep(3)
    #
    # create_main_data()
    # logger.info("______________________________________")
    # logger.info("Сейчас запустится парсер новостей")
    # logger.info("______________________________________")
    # time.sleep(3)
    # parse_news_json()
    #
    # logger.info("______________________________________")
    # logger.info("Сейчас запустится парсер сайта Бауентр")
    # logger.info("______________________________________")
    # time.sleep(3)
    # parse_baucenter_data()

    logger.info("______________________________________")
    logger.info("Сейчас запустится парсер сайта Sotohit")
    logger.info("______________________________________")
    worker_sotohit = WorkerSotohit(
        url="https://sotohit.ru/internet-magazin2/product/apple-iphone-15-pro-max-256gb-natural-titanium-naturalnyj-titan-nano-sim-esim",
        data_count=5,
    )

    # time.sleep(2)
    # logger.info("______________________________________")
    # logger.info("Сейчас будут создавать страницы html")
    # logger.info("______________________________________")
    # worker_sotohit.create_pages_htmls()
    time.sleep(2)
    logger.info("______________________________________")
    logger.info("Сейчас будет создавать json с карточками")
    logger.info("______________________________________")
    worker_sotohit.create_json_data()
    time.sleep(2)
    logger.info("______________________________________")
    logger.info("Сейчас получим рандомную карточку")
    logger.info("______________________________________")
    worker_sotohit.get_random_card()
