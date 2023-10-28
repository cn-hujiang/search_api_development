#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

import pandas as pd
# 创建es连接，默认使用Transport的连接池机制
from elasticsearch_dsl import connections, Search
from src.conf.config import ESConf

es_name = "BIGDATA"
es_host = ESConf.ENTERPRISE_BASIC_DICT.get("host")
es_port = ESConf.ENTERPRISE_BASIC_DICT.get("port")
es_http_auth = ESConf.ENTERPRISE_BASIC_DICT.get("http_auth")
hosts = ["http://{}:{}".format(es_host, es_port)]
connections.create_connection(es_name, hosts=["http://{}:{}".format(es_host, es_port)], http_auth=es_http_auth)


class ESUtil(object):
    specialchars = r'+-!(){}[]^"~*?\/:\t'
    doublechars = '&&||'

    @classmethod
    def escape(cls, s, allow_wildcard=False):
        if sys.version_info > (3, 0):
            basestring = str
        if isinstance(s, basestring):
            rv = ''
            if allow_wildcard:
                if sys.version_info > (3, 0):
                    trans_table = str.maketrans("", "", "*?")
                    specialchars = cls.specialchars.translate(trans_table)
                else:
                    specialchars = cls.specialchars.translate(None, '*?')
            else:
                specialchars = cls.specialchars

            for c in s:
                if c in specialchars:
                    rv += '\\' + c
                else:
                    rv += c
            return rv
        return s

    @staticmethod
    def search(dsl: dict, index: str):
        return Search.from_dict(dsl) \
            .using(connections.get_connection(es_name)) \
            .index(index) \
            .params(request_timeout=300) \
            .execute(ignore_cache=True)

    @staticmethod
    def search_to_df(dsl: dict, index: str):
        hits = Search.from_dict(dsl) \
            .using(connections.get_connection(es_name)) \
            .index(index) \
            .params(request_timeout=300) \
            .execute(ignore_cache=True)
        df = pd.DataFrame(map(lambda x: x.to_dict(), hits.hits))
        return df

    @staticmethod
    def update_by_query(dsl: dict, index: str):
        return connections.get_connection(es_name).update_by_query(index=index, body=dsl)

    @staticmethod
    def index_info(index: str):
        return connections.get_connection(es_name).indices.get(index)
