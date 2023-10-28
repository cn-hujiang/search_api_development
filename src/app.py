#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2023/10/24
# @Author : jiang.hu
# @File : app.py
import os

from flask import Flask
from flasgger import Swagger

from src.api import search_api

app = Flask(__name__)
# 访问swagger
Swagger(app)

# 注册蓝图，即多个模块
blueprints = [
    search_api.blueprint,  # 蓝图注册接口
]
for blueprint in blueprints:
    app.register_blueprint(blueprint)


if __name__ == '__main__':
    env_port = os.environ.get('APP_PORT', 5000)
    print('Server will run on port:', env_port)
    debug = os.environ.get('DEBUG', False)
    app.run(host='0.0.0.0', port=env_port, debug=debug)

