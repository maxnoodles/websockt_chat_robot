# -*- coding:utf-8 -*-
#
# Author: chenjiaxin
# Date: 2020-04-14


class __Const:
    """
    base class of Const
    """

    def __setattr__(self, *_):
        raise ValueError('Trying to change a constant value')

    RESULT = 'result'
    SUCCESS = 'success'
    FAILURE = 'failure'
    ERROR_CODE = 'error_code'
    REASON = 'reason'
    ID = '_id'
    COUNT = 'count'

    SELLER_ID = 'seller_id'
    BUYER_ID = 'buyer_id'
    CHAT_ROOM_KEY = 'chat_room_key'
    BUYER_LIST = 'buyer_list'
    SELLER_LIST = 'seller_list'
    EMAIL = 'email'
    NAME = 'name'
    IS_NEW = 'is_new'

    LAST_MSG = 'last_msg'
    MSG_CONTENT = 'msg_content'
    SEND_TIME = 'send_time'
    MSG_FROM = 'msg_from'
    MSG_TO = 'msg_to'
    LAST_TIME = 'last_time'
    MSG_TYPE = 'msg_type'
    IS_ROBOT = 'is_robot'

    NEW_USER = 'new_user'

    CREATE_TIME = 'create_time'
    UPDATE_TIME = 'update_time'

    IS_ACTIVE = 'is_active'
    TRUE_STATUS = 'T'
    FALSE_STATUS = 'T'

    FLOW_TRIGGER_TYPE = 'flow_trigger_type'
    KEYWORD_ACCURATE = 'keyword_accurate'
    KEYWORD_LIST = 'keyword_list'
    ACTION_LIST = 'action_list'

    SEARCH = 'search'
    KEYWORD = 'keyword'
    REPLY = 'reply'
    REPLY_CONTENT = "reply_content"
    STATUS = 'status'

CONST = __Const

