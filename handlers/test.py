# -*- coding:utf-8 -*-
#
# Author: chenjiaxin
# Date: 2020-04-13
from handlers.comm import BaseHandler
from loguru import logger


class MainHandler(BaseHandler):
    def get(self):
        logger.info('123')
        self.finish({'hello': 'world'})
