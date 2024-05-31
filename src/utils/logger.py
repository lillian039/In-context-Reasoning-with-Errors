import logging
from datetime import datetime
import os

def get_logger(name, args=None):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logger = logging.getLogger('my_logger')

    logger.setLevel(logging.DEBUG)

    os.makedirs('log',exist_ok=True)
    file_handler = logging.FileHandler(f'log/{name}_{current_time}.log')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    if args is not None:
        for arg, value in vars(args).items():
            logger.info(f"{arg}: {value}")
    return logger
