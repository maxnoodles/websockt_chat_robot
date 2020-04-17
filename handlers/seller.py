# -*- coding:utf-8 -*-
#
# Copyright: yiguotech.com
# Author: chenjiaxin
# Date: 2020-04-15
import tornado.escape

from const import CONST
from handlers.comm import MongoHandlerMixin, BaseHandler
from orm import mongo_op


class SellerHandler(BaseHandler, MongoHandlerMixin):

    def options(self):
        # ajax post 会先提交 post 前会先提交一个 options 方法
        self.set_status(200)
        self.finish()

    def post(self):
        param = self.request.body.decode('utf8')
        json_dict = tornado.escape.json_decode(param)
        seller_id = json_dict.get(CONST.SELLER_ID)
        seller = mongo_op.find_one(self.seller_coll, {CONST.SELLER_ID: seller_id})
        if not seller:
            mongo_op.insert_one(self.seller_coll, json_dict)
        self.success()
