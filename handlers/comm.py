# -*- coding:utf-8 -*-
#
# Copyright: yiguotech.com
# Author: chenjiaxin
# Date: 2020-04-13
import logging

import pymongo
import redis
import tornado.web

from const import CONST
from setting import settings


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST')
        self.set_header('Access-Control-Allow-Headers',
                        'x-requested-with, authorization, '
                        'Authorization, Content-Type, '
                        'Access-Control-Allow-Origin, '
                        'Access-Control-Allow-Headers, '
                        'X-Requested-By, Access-Control-Allow-Methods')

    def prepare(self):
        pass

    def write_error(self, status_code: int, **kwargs) -> None:
        self.fail(reason='system error')

    def success(self, **kwargs):
        self.finish({'result': 'success', **kwargs})

    def fail(self, **kwargs):
        self.finish(
            {
                'result': 'fail',
                'error_code': 10001,
                **kwargs
            }
        )


class RedisHandlerMixin:
    redis_conn = redis.StrictRedis(**settings['redis'])


class MongoHandlerMixin:
    mongo_conn = pymongo.MongoClient(**settings['mongo'])
    db = mongo_conn['ws']
    chat_msg_record_coll = db['chat_msg_record']
    buyer_coll = db['buyer']
    seller_coll = db['seller']
    auto_flow_coll = db['auto_flow']
    auto_flow_coll_status = db['auto_flow_status']

    @classmethod
    def create_index(cls):
        logging.info('ready creat index')
        cls.seller_coll.create_index([(CONST.SELLER_ID, 1)], background=True)

        cls.buyer_coll.create_index([(CONST.BUYER_ID, 1)], background=True)
        cls.buyer_coll.create_index([(CONST.SELLER_ID, 1)], background=True)
        cls.buyer_coll.create_index([(CONST.BUYER_ID, 1), (CONST.SELLER_ID, 1)], background=True)

        cls.chat_msg_record_coll.create_index([(CONST.CHAT_ROOM_KEY, 1), (CONST.ID, -1)], background=True)

        cls.auto_flow_coll.create_index([(CONST.KEYWORD_LIST, 1)], background=True)
        cls.auto_flow_coll.create_index([(CONST.SELLER_ID, 1), (CONST.BUYER_ID, 1)], background=True)
        cls.auto_flow_coll_status.create_index([(CONST.SELLER_ID, 1), (CONST.BUYER_ID, 1), (CONST.STATUS, 1)], background=True)
