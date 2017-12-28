# -*- coding: utf-8 -*-
import requests
import json

# CONFIG =========================================
# 定义认证corpid
corp = {
'corpid': 'wwd6faf4d1ced52201',
'corpsecret': 'h9pz4UOGU_XASk-_FgFluUMZF6HWYdN_UVLLW3b7_ps'
}


# FUNCTION =======================================
def get_token():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid='+corp['corpid']+'&corpsecret='+corp['corpsecret']
    req = requests.get(url)
    data = json.loads(req.text)
    return data['access_token']


def send_msg(CONTENT):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
    values = """{
            "touser": "@all",
            "msgtype": "text",
            "agentid": 1000002,
            "text":{
                "content": "%s"
                },
            "safe": "0"
            }""" % CONTENT
    req = requests.post(url, data=values)
    return req.json()