# -*- coding:utf-8 -*-
#
# Copyright: yiguotech.com
# Author: chenjiaxin
# Date: 2020-04-13
from copy import deepcopy

from const import CONST
from orm import mongo_op
from util.chat_util import join_key
from handlers.comm import MongoHandlerMixin, BaseHandler


class ChatListHandler(BaseHandler, MongoHandlerMixin):

    def get(self):
        seller_id = self.get_argument(CONST.SELLER_ID, default='')
        keyword = self.get_argument(CONST.KEYWORD, default='')
        filter_dict = {
            CONST.SELLER_LIST: seller_id
        }
        if keyword:
            filter_dict['$or'] = [
                {CONST.NAME: {'$regex': keyword, '$options': 'i'}},
                {CONST.EMAIL: {'$regex': keyword, '$options': 'i'}}
            ]
        projection = {
            CONST.ID: 0,
            CONST.SELLER_LIST: 0,
        }
        cursor = mongo_op.find(self.buyer_coll, filter_dict, projection=projection)
        count = mongo_op.count_documents(self.buyer_coll, filter_dict)
        buyer_list = []
        for buyer in cursor:
            buyer_temp = deepcopy(buyer)
            # 避免数据库存了 None 的情况
            buyer_id = buyer.get(CONST.BUYER_ID, '')
            chat_room_key = join_key(seller_id, buyer_id)
            filter_dict = {
                CONST.CHAT_ROOM_KEY: chat_room_key
            }
            last_msg = mongo_op.find_one(
                self.chat_msg_record_coll,
                filter_dict,
                sort=[(CONST.ID, -1)]
            ) or {}
            buyer_temp[CONST.LAST_MSG] = last_msg.get(CONST.MSG_CONTENT)
            buyer_temp[CONST.LAST_TIME] = last_msg.get(CONST.SEND_TIME)
            buyer_list.append(buyer_temp)

        self.success(**{CONST.BUYER_LIST: buyer_list, CONST.SELLER_ID: seller_id, CONST.COUNT: count})
