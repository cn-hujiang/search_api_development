#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2023/10/25
# @Author : jiang.hu
# @File : search_api.py

from copy import deepcopy
from flask import request, Blueprint

from src.api import SUCCESS_1
from src.recalling import BaseRecallLayer
from src.recalling.product_search import ProductSearchRecall
from src.recalling.user import User

blueprint = Blueprint(
    'product',
    __name__,
    url_prefix='/rs/rc/product_search'
)

layer = ProductSearchRecall()


def parse_args(req_args: dict):
    """
    从请求参数中解析用户
    Args:
        req_args:   传入的请求参数
    """
    user = User(
        user_id=req_args.get('user_id'),
        search_key=req_args.get('search_key'),
        size=req_args.get('size'),
        extra=req_args.get('extra', {})
    )

    return user


def process(params: dict, recall_layer: BaseRecallLayer):
    """ 处理逻辑 """
    user = parse_args(params)
    result = []

    # 画像标签召回及热门召回
    data, msg = recall_layer.calc(user)
    result.extend(data)

    return result, msg


@blueprint.route('/1.0.0.0', methods=['POST'])
def v_1_0_0_0():
    """
    用户关键词查找商品
    ---
    tags:
      - 用户关键词查找商品
    description:
        用户关键词查找商品
    parameters:
      - name: body
        in: body
        description: 政策资讯接口参数.
        schema:
            type: object
            required:
              - user_id
              - keyword
            properties:
                user_id:
                  type: string
                  description: 用户id
                  example: 9e1297fdd3a84fbeb5b43e3585050758
                keyword:
                  type: string
                  description: 用户输入关键词
                  example: "商品"

    responses:
      500:
        description: Error Fail
      200:
        description: 请求成功
        schema:
          id: proc
          properties:
            code:
              type: integer
              description: 状态码, 0成功,-1失败
            msg:
              type: string
              description: 状态信息
            status:
              type: integer
              description: 暂定0
            success:
              type: boolean
              description: 是否成功
            data:
              type: array
              description: 推荐商品列表
              items:
                type: object
                properties:
                    sku_id:
                      type: string
                      description: 商品ID
                    title:
                      type: string
                      description: 商品名称
                    Description:
                      type: integer
                      description: 商品描述
    """
    if request.method == "POST":
        params = request.get_json()
        data, msg = process(params, layer)
        rsp = deepcopy(SUCCESS_1)
        rsp.update({'data': data, 'msg': msg})
        return rsp, {'Content-Type': 'application/json; charset=utf-8'}
    raise RuntimeError("接口[/rs/rc/product_search/1.0.0.0]仅支持post方法")


if __name__ == '__main__':
    pass
