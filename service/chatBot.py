"""
    ChatApis.py
"""
import json

import requests


def get_response(msg):

    # 发起post请求
    sess = requests.get('https://api.ownthink.com/bot?spoken={}'.format(msg))
    message = json.loads(sess.text)
    print(message)
    return message["data"]["info"]["text"]

