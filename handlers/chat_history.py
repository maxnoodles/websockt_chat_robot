# -*- coding:utf-8 -*-
#
# Copyright: yiguotech.com
# Author: chenjiaxin
# Date: 2020-04-13
from const import CONST
from orm import mongo_op
from util.chat_util import join_key
from handlers.comm import MongoHandlerMixin, BaseHandler


class ChatHistoryHandler(BaseHandler, MongoHandlerMixin):

    def get(self):
        seller_id = self.get_argument(CONST.SELLER_ID)
        buyer_id = self.get_argument(CONST.BUYER_ID)
        chat_room_key = join_key(seller_id, buyer_id)
        # page_size = int(self.get_argument('page_size', default='10'))
        # page_num = int(self.get_argument('page_num', default='1'))
        # ret_list = self.chat_msg_record_coll.find(
        #     {'chat_room': chat_room}, {CONST._ID: 0}
        #     ).sort(CONST._ID, -1).skip((page_num - 1) * page_size).limit(page_size)
        filter_dict = {
            CONST.CHAT_ROOM_KEY: chat_room_key
        }
        # if search:
        #     filter_dict[]
        projection = {
            CONST.ID: 0
        }
        ret_list = mongo_op.find(
            self.chat_msg_record_coll,
            filter_dict,
            projection=projection
        ).sort(CONST.ID, -1)

        chat_history = list(ret_list)
        count = mongo_op.count_documents(self.chat_msg_record_coll, filter_dict)
        self.success(**{'chat_history': chat_history, CONST.COUNT: count})