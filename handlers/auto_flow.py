# -*- coding:utf-8 -*-
#
# Author: chenjiaxin
# Date: 2020-04-15
import tornado.escape

from const import CONST
from handlers.comm import BaseHandler, MongoHandlerMixin


class AutoFlowHandler(BaseHandler, MongoHandlerMixin):

    def post(self):
        param = self.request.body.decode('utf8')
        json_dict = tornado.escape.json_decode(param)

        name = json_dict.get(CONST.NAME)
        seller_id = json_dict.get(CONST.SELLER_ID)
        flow_trigger_type = json_dict.get(CONST.FLOW_TRIGGER_TYPE, CONST.KEYWORD_ACCURATE)
        keyword_list = json_dict.get(CONST.KEYWORD_LIST)
        action_list = json_dict.get(CONST.ACTION_LIST)

    def hand_action_id(self):
        pass

    def get(self):
        seller_id = self.get_argument(CONST.SELLER_ID)


