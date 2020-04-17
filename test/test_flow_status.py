import time
import unittest
import pymongo

from const import CONST
from orm import mongo_op


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.mongo_conn = pymongo.MongoClient()
        self.db = self.mongo_conn['ws']
        self.auto_flow_coll = self.db['auto_flow']
        self.auto_flow_coll_status = self.db['auto_flow_status']
        self.buyer_id = '123'
        self.keyword = 'unittest'
        self.seller_id = 'dou_imoosoo_net'

    # def tearDown(self) -> None:
    #     filter_dict = {
    #         '{}.{}'.format(CONST.KEYWORD_LIST, CONST.KEYWORD): self.keyword
    #     }
    #     self.auto_flow_coll_status.delete_one(filter_dict)

    def test_copy_flow(self):
        expect_result = {'seller_id': 'dou_imoosoo_net', 'action_list': {'e8d29846675d4d4891145d56025b9137': {'action_id': 'e8d29846675d4d4891145d56025b9137', 'action_data': {'keyword_list': [{'keyword': 'test'}]}, 'action_type': 'flow_start', 'next_id_list': ['88f81a0bbe034c6ab32af1e1e419fa04']}, 'b50e89fbab7543e0911c2291d1652b1f': {'previous_id': '88f81a0bbe034c6ab32af1e1e419fa04', 'action_id': 'b50e89fbab7543e0911c2291d1652b1f', 'action_data': {'send_continue': 'F', 'is_validate_reply': 'F', 'validate_failure_msg': '', 'is_reply': 'T', 'message': 'Hi, thanks for your message. This is Flora from imoosoo. Thank you very much for your interest in our latest 【Electric Razor】.\nPlease complete following steps to get it with only shipping fee \n1.Open www.amazon.com\n2. Searching for the keyword：【Electric Razor】\n3.Find our product (see the picture) sold by 【VO***】and buy it.\n4. Send us your order id and your paypal account, we will refund you after you receive it.\nPS: You’ll g get half refund when you send us your order NO. and get full refund when you receive our product. We won’t joke about this as a Prime Seller on Amazon.', 'validate_type': '', 'validate_success_msg': '', 'reply_type': 'text', 'short_reply': [{'keyword': 'Order placed', 'action_id': 'fc273cc6fbc14e2d989fbf2b95442512'}], 'is_random_message': 'F', 'random_message_list': []}, 'action_type': 'send_msg', 'next_id_list': ['fc273cc6fbc14e2d989fbf2b95442512']}, '88f81a0bbe034c6ab32af1e1e419fa04': {'previous_id': 'e8d29846675d4d4891145d56025b9137', 'action_id': '88f81a0bbe034c6ab32af1e1e419fa04', 'action_data': {'send_continue': 'T', 'file_url': 'https://tmf.yiguotech.com/472d4d76a66d3cd22cb16d6a9d6b3a00/20200416/472d4d76a66d3cd22cb16d6a9d6b3a00202004161587004785521882.png'}, 'action_type': 'send_img', 'next_id_list': ['b50e89fbab7543e0911c2291d1652b1f']}, 'fc273cc6fbc14e2d989fbf2b95442512': {'previous_id': 'b50e89fbab7543e0911c2291d1652b1f', 'action_id': 'fc273cc6fbc14e2d989fbf2b95442512', 'action_data': {'send_continue': 'F', 'is_validate_reply': 'F', 'validate_failure_msg': '', 'is_reply': 'T', 'message': 'Please send us the order No. Thanks!', 'validate_type': '', 'validate_success_msg': '', 'reply_type': 'text', 'short_reply': [{'keyword': 'Order No. sent', 'action_id': '8f94d1d4392f49b78c62171e8b951e89'}]}, 'action_type': 'send_msg', 'next_id_list': ['8f94d1d4392f49b78c62171e8b951e89']}, '8f94d1d4392f49b78c62171e8b951e89': {'previous_id': 'fc273cc6fbc14e2d989fbf2b95442512', 'action_id': '8f94d1d4392f49b78c62171e8b951e89', 'action_data': {'send_continue': 'F', 'is_validate_reply': 'F', 'validate_failure_msg': '', 'is_reply': 'F', 'message': 'Thank you, please let me know when you receive our product.\nEmail address：flora.zhao@touchdata.io', 'validate_type': '', 'validate_success_msg': '', 'reply_type': '', 'short_reply': None, 'is_random_message': 'F', 'random_message_list': []}, 'action_type': 'send_msg', 'next_id_list': []}}, 'flow_version': 7, 'is_active': 'T', 'is_check_black': 'F', 'keyword_list': [{'keyword': 'unittest'}], 'name': 'snapchat', 'status': 'processing', 'trigger_type': 'key_accurate', 'update_time': 1587095819.4108243, 'buyer_id': '123', 'keyword': 'unittest', 'origin_flow_id': '5e9953b15aa7567ea1372966', 'current_action_id': 'e8d29846675d4d4891145d56025b9137'}

        result = self.copy_flow_to_status()
        self.assertEqual(result, expect_result)

    def copy_flow_to_status(self, keyword='unittest'):
        filter_dict = {
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
            print(flow)
            mongo_op.insert_one(self.auto_flow_coll_status, flow)
            return flow

    def test_robot_reply(self):
        msg = self.build_msg(self.buyer_id, self.seller_id, '123')
        self.check_robot_reply(msg)
        print('111111')

        msg = self.build_msg(self.buyer_id, self.seller_id, 'Order placed')
        self.check_robot_reply(msg)
        print('2222222')

        msg = self.build_msg(self.buyer_id, self.seller_id, 'Order No. sent')
        self.check_robot_reply(msg)
        print('3333333')

    def check_robot_reply(self, msg):
        if msg[CONST.MSG_FROM] != self.buyer_id:
            return
        filter_dict = {
            CONST.BUYER_ID: self.buyer_id,
            CONST.SELLER_ID: self.seller_id,
            CONST.STATUS: 'processing',
        }
        flow = mongo_op.find_one(self.auto_flow_coll_status, filter_dict)
        if not flow:
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
            # if action_data.get('is_reply') == 'T':
            #     if keyword not in [i[CONST.KEYWORD] for i in action_data['short_reply']]:
            #         if action['action_type'] != 'flow_start':
            #             break
            if action['action_type'] == 'send_img':
                robot_msg = self.build_msg(self.seller_id, self.buyer_id, action_data['file_url'], msg_type='image')
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

    def build_msg(self, msg_from, msg_to, msg_content, msg_type='text', is_robot='F', reply_content=None):
        msg = {
            CONST.SEND_TIME: time.time(),
            CONST.MSG_FROM: msg_from,
            CONST.MSG_TO: msg_to,
            CONST.MSG_CONTENT: msg_content,
            CONST.MSG_TYPE: msg_type,
            CONST.IS_ROBOT: is_robot
        }
        if msg_type == CONST.REPLY:
            msg[CONST.REPLY_CONTENT] = reply_content or []
        return msg

    def reply_by_robot(self, msg):
        print(msg)


if __name__ == '__main__':
    unittest.main()
