# -*- coding:utf-8 -*-
#
# Author: chenjiaxin
# Date: 2020-04-16


def build_robot(pro_name, seller_id):
    # flow = {
    #     "keyword_list": [
    #         {
    #             "keyword": "test"
    #         }
    #     ],
    #     "name": "snapchat",
    #     "status": "stop",
    #     "action_list": [
    #         {
    #             "action_id": "e8d29846675d4d4891145d56025b9137",
    #             "action_data": {
    #                 "keyword_list": [
    #                     {
    #                         "keyword": "test"
    #                     }
    #                 ]
    #             },
    #             "action_type": "flow_start",
    #             "next_id_list": [
    #                 "88f81a0bbe034c6ab32af1e1e419fa04"
    #             ]
    #         },
    #         {
    #             "previous_id": "88f81a0bbe034c6ab32af1e1e419fa04",
    #             "action_id": "b50e89fbab7543e0911c2291d1652b1f",
    #             "action_data": {
    #                 "send_continue": "F",
    #                 "is_validate_reply": "F",
    #                 "validate_failure_msg": "",
    #                 "is_reply": "T",
    #                 "message": "Hi, thanks for your message. This is Flora from imoosoo. "
    #                            "Thank you very much for your interest in our latest 【{}】.\n"
    #                            "Please complete following steps to get it with only shipping fee \n"
    #                            "1.Open www.amazon.com\n"
    #                            "2. Searching for the keyword：【{}】\n"
    #                            "3.Find our product (see the picture) sold by 【VO***】and buy it.\n"
    #                            "4. Send us your order id and your paypal account, we will refund you after you receive it.\n"
    #                            "PS: You’ll g get half refund when you send us your order NO. and get full refund when you receive our product. We won’t joke about this as a Prime Seller on Amazon.".format(
    #                     pro_name, pro_name),
    #                 "validate_type": "",
    #                 "validate_success_msg": "",
    #                 "reply_type": "text",
    #                 "short_reply": [
    #                     {
    #                         "keyword": "Order placed",
    #                         "action_id": "fc273cc6fbc14e2d989fbf2b95442512"
    #                     }
    #                 ],
    #                 "is_random_message": "F",
    #                 "random_message_list": [
    #
    #                 ]
    #             },
    #             "action_type": "send_msg",
    #             "next_id_list": [
    #                 "fc273cc6fbc14e2d989fbf2b95442512"
    #             ]
    #         },
    #         {
    #             "previous_id": "e8d29846675d4d4891145d56025b9137",
    #             "action_id": "88f81a0bbe034c6ab32af1e1e419fa04",
    #             "action_data": {
    #                 "send_continue": "T",
    #                 "file_url": "https://tmf.yiguotech.com/472d4d76a66d3cd22cb16d6a9d6b3a00/20200416/472d4d76a66d3cd22cb16d6a9d6b3a00202004161587004785521882.png"
    #             },
    #             "action_type": "send_img",
    #             "next_id_list": [
    #                 "b50e89fbab7543e0911c2291d1652b1f"
    #             ]
    #         },
    #         {
    #             "previous_id": "b50e89fbab7543e0911c2291d1652b1f",
    #             "action_id": "fc273cc6fbc14e2d989fbf2b95442512",
    #             "action_data": {
    #                 "send_continue": "F",
    #                 "is_validate_reply": "F",
    #                 "validate_failure_msg": "",
    #                 "is_reply": "T",
    #                 "message": "Please send us the order No. Thanks!",
    #                 "validate_type": "",
    #                 "validate_success_msg": "",
    #                 "reply_type": "text",
    #                 "short_reply": [
    #                     {
    #                         "keyword": "Order No. sent",
    #                         "action_id": "8f94d1d4392f49b78c62171e8b951e89"
    #                     }
    #                 ]
    #             },
    #             "action_type": "send_msg",
    #             "next_id_list": [
    #                 "8f94d1d4392f49b78c62171e8b951e89"
    #             ]
    #         },
    #         {
    #             "previous_id": "fc273cc6fbc14e2d989fbf2b95442512",
    #             "action_id": "8f94d1d4392f49b78c62171e8b951e89",
    #             "action_data": {
    #                 "send_continue": "F",
    #                 "is_validate_reply": "F",
    #                 "validate_failure_msg": "",
    #                 "is_reply": "F",
    #                 "message": "Thank you, please let me know when you receive our product.\nEmail address：flora.zhao@touchdata.io",
    #                 "validate_type": "",
    #                 "validate_success_msg": "",
    #                 "reply_type": "",
    #                 "short_reply": None,
    #                 "is_random_message": "F",
    #                 "random_message_list": [
    #
    #                 ]
    #             },
    #             "action_type": "send_msg",
    #             "next_id_list": [
    #
    #             ]
    #         }
    #     ],
    #     "is_active": "T",
    #     "is_check_black": "F",
    #     "flow_version": 7,
    #     "trigger_type": "key_accurate",
    #     'seller_id': seller_id
    # }
    flow = {
        "keyword_list": [
            {
                "keyword": "test"
            }
        ],
        "name": "snapchat",
        "status": "stop",
        "action_list": [
            {
                "action_id": "e8d29846675d4d4891145d56025b9137",
                "action_data": {
                    "keyword_list": [
                        {
                            "keyword": "test"
                        }
                    ]
                },
                "action_type": "flow_start",
                "next_id_list": [
                    "88f81a0bbe034c6ab32af1e1e419fa04"
                ]
            },
            {
                "previous_id": "88f81a0bbe034c6ab32af1e1e419fa04",
                "action_id": "b50e89fbab7543e0911c2291d1652b1f",
                "action_data": {
                    "send_continue": "F",
                    "is_validate_reply": "F",
                    "validate_failure_msg": "",
                    "is_reply": "F",
                    "message": "Thanks for your message. "
                               "We're running this activity to spread the word about our best products. Promotions like this help us get the word out and increase our products' popularity on Amazon.\n\n"
                               "Once your order is shipped, you'll get 50% rebate. When your review is alive, you'll get the left 50%.\n\n"
                               "Please leave your contact such as email address to us for more detail information.",
                    "validate_type": "",
                    "validate_success_msg": "",
                    "reply_type": "text",
                },
                "action_type": "send_msg",
                "next_id_list": [
                    "fc273cc6fbc14e2d989fbf2b95442512"
                ]
            },
            {
                "previous_id": "e8d29846675d4d4891145d56025b9137",
                "action_id": "88f81a0bbe034c6ab32af1e1e419fa04",
                "action_data": {
                    "send_continue": "T",
                    "file_url": "http://reb.vcitsing.com/claim/images/banner/banner-1.jpg"
                },
                "action_type": "send_img",
                "next_id_list": [
                    "b50e89fbab7543e0911c2291d1652b1f"
                ]
            },
            {
                "previous_id": "b50e89fbab7543e0911c2291d1652b1f",
                "action_id": "fc273cc6fbc14e2d989fbf2b95442512",
                "action_data": {
                    "send_continue": "F",
                    "is_validate_reply": "F",
                    "validate_failure_msg": "",
                    "is_reply": "F",
                    "message": "Thank you. We're away and can't respond right now, we will contact you ASAP.\n\n"
                               "You can also follow our Facebook Page or send us message via Facebook Messenger\n\n"
                               "Page: https://www.facebook.com/quanwby.cc\n"
                               "Messenger Link: https://m.me/quanwby.cc",
                    "validate_type": "",
                    "validate_success_msg": "",
                    "reply_type": "text",
                },
                "action_type": "send_msg",
                "next_id_list": [
                ]
            }
        ],
        "is_active": "T",
        "is_check_black": "F",
        "flow_version": 7,
        "trigger_type": "key_accurate",
        'seller_id': seller_id
    }
    return flow


def insert_robot():
    from orm import mongo_op
    from handlers.comm import MongoHandlerMixin

    seller_id = 'reb_vcitsing_com'
    pro_name = 'Trogonic TE1 Wireless Earbuds'

    filter_dict = {'seller_id': seller_id}
    robot = build_robot(pro_name, seller_id)
    mongo_op.update_one(MongoHandlerMixin.auto_flow_coll, filter_dict, robot, upsert=True)


if __name__ == "__main__":
    insert_robot()
