# coding=utf-8
"""
@Time : 2020/10/29
@Author : HeXW
"""
import logging
import logging.handlers
import datetime
from config.Commom import all_logger_path, error_logger_path


def get_loger(loginName="myLogger"):
    logger = logging.getLogger(loginName)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        rf_handler = logging.handlers.TimedRotatingFileHandler(all_logger_path, when='midnight', interval=1,
                                                               backupCount=2, atTime=datetime.time(0, 0, 0, 0))
        # rf_handler = logging.handlers.RotatingFileHandler(all_logger_path, maxBytes=10240, backupCount=1)
        rf_handler.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(message)s"))

        f_handler = logging.FileHandler(error_logger_path)
        f_handler.setLevel(logging.ERROR)
        f_handler.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(filename)s[:%(lineno)d]-%(message)s"))

        logger.addHandler(rf_handler)
        logger.addHandler(f_handler)
    return logger
