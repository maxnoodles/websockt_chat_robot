# -*- coding:utf-8 -*-
#
# Copyright: yiguotech.com
# Author: chenjiaxin
# Date: 2020-04-13
import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def logger_init():
    logging.basicConfig(handlers=[InterceptHandler(level='DEBUG')], level='DEBUG')
    logger.configure(handlers=[
        {"sink": sys.stderr,
         'colorize': True,
         'format': "<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | {file} | <lvl>{level}</lvl> | <lvl>{message}</lvl>",
         "level": 'DEBUG'}])
    logger.add(
        './data/file.log', rotation="500 MB", encoding='utf-8', colorize=False, level='INFO'
    )
