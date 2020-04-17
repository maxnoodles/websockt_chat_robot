# -*- coding:utf-8 -*-
#
# Copyright: yiguotech.com
# Author: chenjiaxin
# Date: 2020-04-13


def join_key(seller_id, buyer_id, _format='_'):
    return _format.join([seller_id, buyer_id])
