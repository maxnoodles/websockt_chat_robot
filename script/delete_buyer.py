# -*- coding:utf-8 -*-
#
# Author: chenjiaxin
# Date: 2020-04-23

from orm import mongo_op
from handlers.comm import MongoHandlerMixin


def delete_buyer():
    buyer_id = 'ab3074f95927e5981712073c1e7234d7'
    chat_room_key = 'reb_vcitsing_com_ab3074f95927e5981712073c1e7234d7'

    MongoHandlerMixin.auto_flow_coll_status.delete_many({"buyer_id": buyer_id})
    MongoHandlerMixin.buyer_coll.delete_many({"buyer_id": buyer_id})
    MongoHandlerMixin.chat_msg_record_coll.delete_many({"chat_room_key": chat_room_key})

