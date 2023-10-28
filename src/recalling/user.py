#!/usr/bin/env python
# -*- coding:utf-8 -*-

class User(object):
    """ 用户类(输入) """

    def __init__(self, user_id: str = None, search_key: str = None, size: int = None, extra: dict = None):
        """
        定义统一输入参数
        Args:
            user_id:                        用户ID
            search_key:                     用户输入搜索词
        """
        self._user_id = user_id
        self._search_key = search_key
        self._size = size
        # 扩展字段
        self._extra = extra

    @property
    def id(self) -> str:
        return self._user_id

    @property
    def extra(self) -> dict:
        return self._extra

    @property
    def search_key(self):
        return self._search_key

    @property
    def size(self):
        return self._size

    def __str__(self):
        """ 打印格式 """
        return "id=%s, search_key=%s,size=%s, extra=%s" % (self.id, self.search_key, self.size, self.extra)

    def json(self):
        return {
            "user_id": self._user_id,
            "user_type": self._search_key,
            "size": self._size,
            "extra": self._extra
        }
