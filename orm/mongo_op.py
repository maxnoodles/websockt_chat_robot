# -*- coding:utf-8 -*-
#
# Copyright: yiguotech.com
# Author: chenjiaxin
# Date: 2020-04-15
import time
from copy import deepcopy

import pymongo

from const import CONST


def insert_one(coll, doc, *args, **kwargs):
    _doc = deepcopy(doc)
    for field in [CONST.CREATE_TIME, CONST.UPDATE_TIME]:
        if not _doc.get(field):
            _doc[field] = time.time()
    if _doc.get(CONST.IS_ACTIVE):
        _doc[CONST.IS_ACTIVE] = True
    return coll.insert_one(_doc, *args, **kwargs)


def update_one(coll, filter_dict, update_dict, op='$set', *args, **kwargs):
    _update = deepcopy(update_dict)
    if op == '$set' and not _update.get(CONST.UPDATE_TIME):
        _update[CONST.UPDATE_TIME] = time.time()
    _update = {op: _update}
    return coll.update_one(filter_dict, _update, *args, **kwargs)


def find(coll, filter_dict, projection=None, *args, **kwargs):
    _filter = deepcopy(filter_dict)
    # if not _filter.get(CONST.IS_ACTIVE):
    #     _filter[CONST.IS_ACTIVE] = CONST.TRUE_STATUS
    return coll.find(_filter, projection=projection, *args, **kwargs)


def find_one(coll, filter_dict, projection=None, *args, **kwargs):
    _filter = deepcopy(filter_dict)
    # if not _filter.get(CONST.IS_ACTIVE):
    #     _filter[CONST.IS_ACTIVE] = CONST.TRUE_STATUS
    return coll.find_one(_filter, projection=projection, *args, **kwargs)


def count_documents(coll, filter_dict, *args, **kwargs):
    _filter = deepcopy(filter_dict)
    # if not _filter.get(CONST.IS_ACTIVE):
    #     _filter[CONST.IS_ACTIVE] = CONST.TRUE_STATUS
    return coll.count_documents(_filter, *args, **kwargs)




