# -*- coding:utf-8 -*-
#
# Author: chenjiaxin
# Date: 2020-04-13
import tornado.escape
from loguru import logger

from const import CONST
from handlers.comm import MongoHandlerMixin, BaseHandler
from orm import mongo_op


class BuyerHandler(BaseHandler, MongoHandlerMixin):

    def options(self):
        # ajax post 会先提交 post 前会先提交一个 options 方法
        self.set_status(200)
        self.finish()

    def post(self):
        json_data = self.request.body.decode('utf8')
        try:
            data = tornado.escape.json_decode(json_data)
        except Exception as e:
            logger.error('data:{} is not a json'.format(json_data))
            return self.fail(reason='data is not a json')

        buyer_id = data.get(CONST.BUYER_ID, '')
        seller_id = data.get(CONST.SELLER_ID, '')
        name = data.get(CONST.NAME, '')
        email = data.get(CONST.EMAIL, '')

        if not all([buyer_id, seller_id, name, email]):
            return self.fail(reason='params error')
        buyer = self.get_buyer(buyer_id, seller_id)
        if not buyer:
            new_buyer = {
                CONST.BUYER_ID: buyer_id,
                CONST.SELLER_ID: seller_id,
                CONST.NAME: name,
                CONST.EMAIL: email
            }
            mongo_op.insert_one(self.buyer_coll, new_buyer)
        self.success()

    def get(self):
        buyer_id = self.get_argument(CONST.BUYER_ID)
        seller_id = self.get_argument(CONST.SELLER_ID)

        buyer = self.get_buyer(buyer_id, seller_id)

        if buyer:
            return self.success(is_new=False, buyer=buyer)
        else:
            return self.success(is_new=True)

    def get_buyer(self, buyer_id, seller_id):
        filter_dict = {
            CONST.BUYER_ID: buyer_id,
            CONST.SELLER_ID: seller_id
        }
        projection = {
            CONST.ID: False
        }
        return mongo_op.find_one(self.buyer_coll, filter_dict, projection)
