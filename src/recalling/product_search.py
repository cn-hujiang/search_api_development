#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2023/10/27
# @Author : jiang.hu
# @File : product_search.py
from copy import deepcopy
from typing import Union, List

import jieba
from datetime import timedelta

import pandas as pd

from src.recalling import BaseRecallLayer, User, PUNCTUATION_TAG, LOGICAL_OPERATOR, OUTPUT
from src.utils.es_util import ESUtil
from src.utils.redis_util import RedisUtil


class ProductSearchRecall(BaseRecallLayer):
    def __init__(self, visit_threshold: int = 100, cooling_time: int = 2):
        super().__init__()
        self.index = "product_basic_index"
        self.redis_key = "RS:RC:{}"
        self.visit_threshold = visit_threshold
        self.cooling_time = self.days_to_seconds(cooling_time)

    def calc(self, user: Union[User, None], **kwargs):
        """
        根据用户输入关键词查询商品内容
        :param user:
        :param kwargs:
        :return:
        """
        # 用户id 或 搜索词为空时返回 空
        message = "查询成功"
        if not user.id or not user.search_key:
            message = "用户id 或 搜索词为空"
            return [], message

        # 用户访问次数校验
        redis_key = self.redis_key.format(user.id)
        try:
            user_visit = int(RedisUtil.get(redis_key))
        except:
            user_visit = 0

        if user_visit and user_visit > self.visit_threshold:
            message = "用户访问次数超过限制阈值"
            return [], message

        user_visit += 1
        # redis 缓存用户访问次数
        RedisUtil.set(redis_key, user_visit)
        if user_visit == self.visit_threshold:
            # 访问次数达到 限制阈值后，用户冷却 2天
            RedisUtil.expire(redis_key, self.cooling_time)
        else:
            RedisUtil.expire(redis_key, 86400)

        # 查询
        df = self.query_by_search_key(search_key=user.search_key)
        if df.empty:
            message = "用户查询结果为空"
            return [], message
        df.rename(columns={"sku_id": "content_id"}, inplace=True)
        result = self.normalize_output(df, size=user.size)
        return result, message

    def query_by_search_key(self, search_key: str = None):
        """
        根本用户输入词查询
        :param search_key:
        :return:
        """
        # 特殊字符及运算符处理
        search_key = PUNCTUATION_TAG.sub(" ", search_key)
        search_key = LOGICAL_OPERATOR.sub(" ", search_key.upper())
        search_key = self.cut_search_key(search_key)
        keywords = list(map(lambda x: "(" + x + ")", search_key))
        query_string = " OR ".join(keywords)
        dsl = {
            "_source": ["title", "description", "sku_id"],
            "query": {
                "bool": {
                    "filter": [
                        {
                            "query_string": {
                                "query": query_string,
                                "type": "phrase",
                                "fields": [
                                    "title"
                                ]
                            }
                        }
                    ]
                }
            }
        }
        df = ESUtil.search_to_df(dsl, index=self.index)
        return df

    @classmethod
    def cut_search_key(cls, search_key) -> List[str]:
        """
        jieba 分词
        :param search_key:
        :return:
        """
        words = [w.strip() for w in jieba.cut(search_key) if w.strip()]
        return words

    @classmethod
    def days_to_seconds(cls, days):
        # 创建 timedelta 对象，表示指定天数的时间间隔
        time_delta = timedelta(days=days)

        # 获取时间间隔对应的总秒数
        total_seconds = time_delta.total_seconds()

        return int(total_seconds)

    def normalize_output(self, df: pd.DataFrame, size=None) -> List[dict]:
        """
        预处理输出数据，格式标准化
        Args:
            df:                 待缓存数据
            size:               缓存大小
        """
        if df.empty:
            return []
        df = df.head(size)
        return self.format_output(df.to_dict(orient='records'))

    @classmethod
    def format_output(cls, records: List[dict]) -> List[dict]:
        """
        Args:
            records:     资源
        """
        res = []
        n = len(records)
        for pos, record in enumerate(records, start=0):
            extra = {}
            res_type = None
            rec_id = str(record.pop('content_id'))
            d = deepcopy(OUTPUT)
            d['rec_id'] = rec_id
            if 'score' in record:
                d['score'] = record.pop('score')
            else:
                d['score'] = n - pos
            if 'res_type' in record:
                res_type = int(record.pop('res_type'))
            d['res_type'] = res_type

            # 拓展字段
            for k, v in record.items():
                extra[k] = v
            d['extra'] = extra
            res.append(d)
        return res


if __name__ == '__main__':
    threshold = 100

    recall = ProductSearchRecall(visit_threshold=threshold)
    df = recall.query_by_search_key("商品名称001")
