# -*- coding:utf-8 -*-
#
# Author: chenjiaxin
# Date: 2020-04-13
import tornado.ioloop
import tornado.web
# import sentry_sdk
# from sentry_sdk.integrations.tornado import TornadoIntegration
# from sentry_sdk.integrations.redis import RedisIntegration

from handlers.seller import SellerHandler
from handlers.test import MainHandler
from handlers.chat_websocket import ChatSocketHandler
from orm import mongo_op
from script.delete_buyer import delete_buyer
from script.robot import build_robot, insert_robot
from setting import settings
from handlers.buyer import BuyerHandler
from handlers.chat_list import ChatListHandler
from handlers.chat_history import ChatHistoryHandler
from handlers.comm import MongoHandlerMixin
from util.logger_util import logger_init
from loguru import logger


class Application(tornado.web.Application):
    def __init__(self, **setting):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
            (r"/buyer", BuyerHandler),
            (r"/seller", SellerHandler),
            (r"/chat_list", ChatListHandler),
            (r"/chat_history", ChatHistoryHandler)
        ]
        MongoHandlerMixin.create_index()
        super(Application, self).__init__(handlers, **setting)


def run_script():
    insert_robot()
    delete_buyer()


def main():
    # sentry_sdk.init(
    #     'https://adb05e0a4d944c9b9843b011e3e287af@o377358.ingest.sentry.io/5199404',
    #     integrations=[RedisIntegration()]
    # )
    logger_init()
    run_script()

    logger.info('启动 tornado')
    app = Application(**settings)
    app.listen(8888, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
