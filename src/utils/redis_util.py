#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
redis 相关工具
"""

import redis
from redis.connection import Encoder

from src.conf.config import RedisConf

pool_config = RedisConf.ALGORITHMS_DICT.copy()
pool_config.update({'decode_responses': False})
POOL = redis.ConnectionPool(**pool_config, max_connections=1000, socket_connect_timeout=1, health_check_interval=30)

encoder = Encoder("utf-8", "strict", True)


def byte_2_str_wrap(fun):
    def _inner_fun(*args, **kwargs):
        r = fun(*args, **kwargs)
        if isinstance(r, (list, tuple, set)):
            return [encoder.decode(i) if isinstance(i, bytes) else i for i in r]
        return encoder.decode(r) if isinstance(r, bytes) else r

    return _inner_fun


# pylint: disable=C0116,R0205,R0904
class RedisUtil(object):
    """
    redis 常用操作
    """

    @staticmethod
    def get_conn(connection_pool=None):
        if connection_pool:
            return redis.Redis(connection_pool=connection_pool)
        return redis.Redis(connection_pool=POOL)

    @staticmethod
    @byte_2_str_wrap
    def set(key, value):
        return RedisUtil.get_conn().set(key, value)

    @staticmethod
    @byte_2_str_wrap
    def get(key):
        result = RedisUtil.get_conn().get(key)
        if isinstance(result, bytes):
            result = result.decode('utf-8')
        return result

    @staticmethod
    @byte_2_str_wrap
    def delete(key):
        return RedisUtil.get_conn().delete(key)

    @staticmethod
    @byte_2_str_wrap
    def expire(key, time):
        return RedisUtil.get_conn().expire(key, time)


if __name__ == '__main__':
    pass
