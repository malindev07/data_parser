import time

from data.baucenter_data.baucenter_parser import parse_baucenter_data
from data.news_data.rbk_news_parser import parse_news_json
from data.sotohit_data.sotohit_parser import create_main_data
from logger import logger

if __name__ == "__main__":
    logger.info("______________________________________")
    logger.info("Сейчас запустится парсер сайта sotohit")
    logger.info("______________________________________")
    time.sleep(3)

    create_main_data()
    logger.info("______________________________________")
    logger.info("Сейчас запустится парсер новостей")
    logger.info("______________________________________")
    time.sleep(3)
    parse_news_json()

    logger.info("______________________________________")
    logger.info("Сейчас запустится парсер сайта Бауентр")
    logger.info("______________________________________")
    time.sleep(3)
    parse_baucenter_data()
