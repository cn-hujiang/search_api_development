#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:
@time:
@function:
"""
import os
from pathlib import Path
from src.conf import ConfigWrapper

# 根目录
BASE_DIR = Path(os.path.realpath(__file__)).parent.parent.parent

# 配置文件
CONFIG_FILE_PATH = BASE_DIR.joinpath('config', 'ops.conf').__str__()
parser = ConfigWrapper(CONFIG_FILE_PATH)


class ESConf(object):
    # 企业信息ES库
    ENTERPRISE_BASIC_DICT = parser.parse_to_es_dict('elasticsearch-bigdata', 'product_basic_index')


class RedisConf(object):
    # 算法组-Redis库
    ALGORITHMS_DICT = parser.parse_to_redis_dict('redis-algorithms')
