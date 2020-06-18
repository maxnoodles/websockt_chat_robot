# -*- coding:utf-8 -*-
#
# Author: chenjiaxin
# Date: 2020-04-15

from const import CONST
from handlers.comm import BaseHandler, MongoHandlerMixin
from orm import mongo_op


class AutoFlowListHandler(BaseHandler, MongoHandlerMixin):

    async def get(self):
        seller_id = self.get_argument(CONST.SELLER_ID)
        filter_dict = {
            CONST.SELLER_ID: seller_id
        }
        projection = {
            CONST.ID: 0
        }
        cursor = mongo_op.find(self.auto_flow_coll, filter_dict, projection)
        auto_flow_list = list(cursor)
        count = mongo_op.count_documents(self.auto_flow_coll, filter_dict)
        self.success(auto_flow_list=auto_flow_list, count=count)
