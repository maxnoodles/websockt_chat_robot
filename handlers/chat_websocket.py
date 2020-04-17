# -*- coding:utf-8 -*-
#
# Copyright: yiguotech.com
# Author: chenjiaxin
# Date: 2020-04-13
import time
from collections import defaultdict
from copy import deepcopy

from const import CONST
from orm import mongo_op
from util.logger_util import logger

import tornado.escape
import tornado.websocket

from handlers.comm import RedisHandlerMixin, MongoHandlerMixin
from util.chat_util import join_key


class ChatSocketHandler(tornado.websocket.WebSocketHandler, RedisHandlerMixin, MongoHandlerMixin):
    chat_container = defaultdict(list)

    def initialize(self) -> None:
        self.seller_id = self.get_argument(CONST.SELLER_ID)
        self.buyer_id = self.get_argument(CONST.BUYER_ID, default='')

    @property
    def client_key(self):
        return self.buyer_id if self.buyer_id else self.seller_id

    @staticmethod
    def get_chat_room_key(seller_id, buyer_id):
        return join_key(seller_id, buyer_id)

    def is_new_user(self, seller_id, buyer_id):
        chat_room_key = self.get_chat_room_key(seller_id, buyer_id)
        result = mongo_op.find_one(self.chat_msg_record_coll, {CONST.CHAT_ROOM_KEY: chat_room_key})
        return True if not result else False

    def greet_by_robot(self):
        msg = self.build_msg(self.seller_id, self.buyer_id, 'hello, can I help you?')
        self.reply_by_robot(msg)

    def reply_by_robot(self, msg):
        msg[CONST.IS_ROBOT] = CONST.TRUE_STATUS
        self.send_msg_and_to_db(msg)

    def send_msg_and_to_db(self, msg):
        self.msg_record_to_db(msg)
        self.send_msg(msg)

    def msg_record_to_db(self, chat_msg):
        mongo_op.insert_one(self.chat_msg_record_coll, chat_msg)

    def send_msg(self, chat_msg):
        logger.info('ready send messenger %s' % chat_msg)
        waiter_set = set()
        for send_key in [chat_msg.get(CONST.MSG_FROM), chat_msg.get(CONST.MSG_TO)]:
            for waiter in self.chat_container.get(send_key, []):
                waiter_set.add(waiter)
        for waiter in waiter_set:
            _chat_msg = dict(chat_msg)
            try:
                waiter.write_message(_chat_msg)
            except:
                logger.error("Error sending message", exc_info=True)

    async def open(self):
        # buyer_id 就是买家的标识符， seller_id 是卖家的主页
        logger.info('new websocket uri:{} coming'.format(self.request.uri))
        if self.buyer_id:
            self.chat_container[self.buyer_id].append(self)
            is_new = self.is_new_user(self.seller_id, self.buyer_id)
            if is_new:
                # 拷贝机器人
                self.greet_by_robot()
                self.copy_flow_to_status()
                msg = self.build_msg(self.buyer_id, self.seller_id, 'Get start')
                # fake_msg = deepcopy(msg)
                # fake_msg[CONST.MSG_FROM] = ''
                # self.send_msg(fake_msg)
                self.check_robot_reply(msg)
        else:
            self.chat_container[self.seller_id].append(self)

    def copy_flow_to_status(self, keyword='test'):
        filter_dict = {
            CONST.SELLER_ID: self.seller_id,
            '{}.{}'.format(CONST.KEYWORD_LIST, CONST.KEYWORD): keyword
        }
        flow = mongo_op.find_one(self.auto_flow_coll, filter_dict)
        if flow:
            flow[CONST.BUYER_ID] = self.buyer_id
            flow[CONST.STATUS] = 'processing'
            flow[CONST.KEYWORD] = keyword
            flow['origin_flow_id'] = str(flow.pop(CONST.ID, ''))
            for action in flow.get(CONST.ACTION_LIST, []):
                if action.get('action_type') == 'flow_start':
                    flow['current_action_id'] = action.get('action_id')
            old_action_list = flow['action_list']
            flow['action_list'] = {i['action_id']: i for i in old_action_list}
            mongo_op.insert_one(self.auto_flow_coll_status, flow)

    def on_close(self):
        client_key = self.client_key
        logger.info('on_close client_key: {}'.format(client_key))
        self.chat_container.pop(client_key, '')

    async def on_message(self, message):

        logger.info("got message %s", message)
        try:
            msg = tornado.escape.json_decode(message)
        except Exception:
            await self.write_message({CONST.REASON: "the message isn't a json"})
            return

        msg_from = self.client_key
        msg_to = msg.get(CONST.MSG_TO)
        msg_content = msg.get(CONST.MSG_CONTENT)
        msg_type = msg.get(CONST.MSG_TYPE, 'text')

        chat_msg = self.build_msg(msg_from, msg_to, msg_content, msg_type)
        self.send_msg_and_to_db(chat_msg)

        self.check_robot_reply(chat_msg)

    def check_robot_reply(self, msg):
        logger.info('ready check_robot_reply, seller_id:{}, buyer_id:{}'.format(self.seller_id, self.buyer_id))
        if msg[CONST.MSG_FROM] != self.buyer_id:
            return
        filter_dict = {
            CONST.BUYER_ID: self.buyer_id,
            CONST.SELLER_ID: self.seller_id,
            CONST.STATUS: 'processing',
        }
        flow = mongo_op.find_one(self.auto_flow_coll_status, filter_dict)
        if not flow:
            logger.info("Can't find flow")
            return
        keyword = msg[CONST.MSG_CONTENT]
        action_dict = flow[CONST.ACTION_LIST]
        action = action_dict[flow['current_action_id']]
        action_data = action['action_data']

        # 判断关键词
        if action_data.get('is_reply') == 'T':
            for i in action_data.get('short_reply', []):
                if i[CONST.KEYWORD] == keyword:
                    action = action_dict[i['action_id']]
                    break
            else:
                return

        while True:
            # 先判断关键词
            action_data = action['action_data']
            logger.info(action_data)
            # if action_data.get('is_reply') == 'T':
            #     if keyword not in [i[CONST.KEYWORD] for i in action_data['short_reply']]:
            #         if action['action_type'] != 'flow_start':
            #             break
            if action['action_type'] == 'send_img':
                robot_msg = self.build_msg(self.seller_id, self.buyer_id, [{"url": action_data['file_url']}], msg_type='image')
                self.reply_by_robot(robot_msg)

            elif action['action_type'] == 'send_msg':
                if action_data['is_reply'] == 'T':
                    robot_msg = self.build_msg(self.seller_id,
                                               self.buyer_id,
                                               action_data['message'],
                                               msg_type='reply',
                                               reply_content=[i[CONST.KEYWORD] for i in action_data['short_reply']]
                                               )
                else:
                    robot_msg = self.build_msg(self.seller_id,
                                               self.buyer_id,
                                               action_data['message'])
                self.reply_by_robot(robot_msg)

            if action_data.get('send_continue', 'T') == 'T' and action['next_id_list']:
                if action_data.get('is_reply') == 'T':
                    for i in action_data.get('short_reply'):
                        if i[CONST.KEYWORD] == keyword:
                            action = action_dict[i['action_id']]
                else:
                    action = action_dict[action['next_id_list'][0]]
            else:
                update_dict = {
                    'current_action_id': action['action_id']
                }
                if not action['next_id_list']:
                    update_dict['status'] = 'done'
                mongo_op.update_one(self.auto_flow_coll_status, filter_dict, update_dict)
                break

    def check_origin(self, origin: str):
        return True

    def build_msg(self, msg_from, msg_to, msg_content, msg_type='text', is_robot='F', reply_content=None):
        seller_id = self.seller_id
        buyer_id = self.buyer_id or msg_to
        # 根据发送人获取姓名和邮箱
        chat_room_key = self.get_chat_room_key(seller_id, buyer_id)
        msg_from_info = self.get_msg_from_info(msg_from)

        msg = {
            CONST.SEND_TIME: time.time(),
            CONST.MSG_FROM: msg_from,
            CONST.MSG_TO: msg_to,
            CONST.MSG_CONTENT: msg_content,
            CONST.CHAT_ROOM_KEY: chat_room_key,
            CONST.MSG_TYPE: msg_type,
            CONST.NAME: msg_from_info.get(CONST.NAME),
            CONST.EMAIL: msg_from_info.get(CONST.EMAIL),
            CONST.IS_ROBOT: is_robot
        }
        if msg_type == CONST.REPLY:
            msg[CONST.REPLY_CONTENT] = reply_content or []
        return msg

    def get_msg_from_info(self, msg_from):
        if msg_from == self.seller_id:
            filter_dict = {CONST.SELLER_ID: msg_from}
            msg_from_info = mongo_op.find_one(self.seller_coll, filter_dict) or {}
        else:
            filter_dict = {CONST.BUYER_ID: msg_from}
            msg_from_info = mongo_op.find_one(self.buyer_coll, filter_dict) or {}

        msg_from_info[CONST.NAME] = msg_from_info.get(CONST.NAME, msg_from)
        msg_from_info[CONST.EMAIL] = msg_from_info.get(CONST.EMAIL, msg_from)
        return msg_from_info
