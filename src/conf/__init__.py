#!/usr/bin/env python
# -*- coding:utf-8 -*-

# @function:

from configparser import ConfigParser


class ConfigWrapper(ConfigParser):
    def __init__(self, path: str):
        ConfigParser.__init__(self)
        self.path = path
        self.read(self.path, encoding="utf-8")

    def parse_to_es_dict(self, section: str, index: str) -> dict:
        """
        配置转 ES 字典
        Args:
            section:数据库标识
            index:  ES索引
        """
        return {
            'host': self.get(section, 'esHost'), 'port': int(self.get(section, 'esPort')),
            'http_auth': (self.get(section, 'esUser'), self.get(section, 'esPass')),
            'index': index
        }

    def parse_to_redis_dict(self, section: str) -> dict:
        """
        配置转 Redis 字典
        Args:
            section:数据库标识
        """
        return {
            'host': self.get(section, 'host'), 'port': int(self.get(section, 'port')),
            'password': self.get(section, 'password'), 'db': int(self.get(section, 'database')),
            'decode_responses': True
        }
