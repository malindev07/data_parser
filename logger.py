import logging
from logging import getLogger, basicConfig, DEBUG, FileHandler, StreamHandler

logger = getLogger(__name__)
FORMAT = logging.Formatter(
    " %(levelname)s - %(name)s |  %(message)s  |  %(filename)s - def: %(funcName)s - line: %(lineno)d - %(asctime)s "
)

file_handler = FileHandler("main.log")
file_handler.setLevel(DEBUG)

file_handler.setFormatter(FORMAT)

formatter_for_console = logging.Formatter(
    "%(levelname)s - %(name)s - |  %(message)s - %(asctime)s"
)
console_handler = StreamHandler()

console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter_for_console)
basicConfig(
    level=logging.INFO, handlers=[file_handler, console_handler], encoding="utf-8"
)
