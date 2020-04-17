# -*- coding:utf-8 -*-
#
# Copyright: yiguotech.com
# Author: chenjiaxin
# Date: 2020-04-13
import tornado.escape

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
        data = tornado.escape.json_decode(json_data)
        buyer_id = data.get(CONST.BUYER_ID)
        seller_id = data.get(CONST.SELLER_ID, 'abc')
        filter_dict = {
            CONST.BUYER_ID: buyer_id
        }
        buyer = mongo_op.find_one(self.buyer_coll, filter_dict)
        if buyer:
            mongo_op.update_one(self.buyer_coll,
                                {CONST.BUYER_ID: buyer_id},
                                {CONST.SELLER_LIST: seller_id},
                                op="$addToSet")
        else:
            _data = dict(data)
            # 创建用户的时候顺便写入新的商家ID
            _data[CONST.SELLER_LIST] = [seller_id]
            mongo_op.insert_one(self.buyer_coll, _data)
        self.success()
