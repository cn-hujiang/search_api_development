#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2023/10/27
# @Author : jiang.hu
# @File : __init__.py.py
import re
from typing import Union

from src.recalling.user import User


class BaseRecallLayer:
    def __init__(self):
        pass

    def calc(self, user: Union[User, None], **kwargs):
        """具体召回实现"""
        raise NotImplementedError


# 特殊字符
PUNCTUATION_TAG = re.compile(
    r"""[�ǻԸˮȫԴΪ，。；！‘“、!#$%&'()*+,-./:;<=>?@\[\]^_`{|}~？：”’￥…（）《\"》【】，-；\u0139\xa0\u25ca\u200b\u3000\t\n\r②丨.,—\s]+""",
    re.DOTALL)

LOGICAL_OPERATOR = re.compile(r"""[^a-zA-Z](AND|OR)[^a-zA-Z]""", re.DOTALL)


OUTPUT = {
    "rec_id": "",       # 商品ID
    "res_type": None,   # 内容类型
    "rec_type": "",     #
    "score": 0.0,       # 得分
    "extra": {}         # 拓展字段
}


if __name__ == '__main__':
    pass
