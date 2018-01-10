# -*- coding:utf-8 -*-
import datetime
import pymysql
import time, sched
import requests
import json
schedule = sched.scheduler(time.time, time.sleep)


def connection():
    return pymysql.connect(
        host='47.94.222.254',
        port=3306,
        user='app',
        password='lanmeimei_app',
        db='app_db',
        charset='utf8',
    )


def func(inc=5):
    now = datetime.date.today()
    tmp_list = []
    udic = {}
    try:
        conn = connection()
        cur = conn.cursor()
        sql_search = "SELECT userid,agentid from tb_user;"
        sql = "SELECT name,outdate from user_data where `status`=0 and userid='{}'"
        cur.execute(sql_search)
        for x in cur:
            uid = x[0]
            aid = x[1]
            print(uid, aid)
            udic[uid] = aid
        for uid in udic.keys():
            aid = udic[uid]
            cur.execute(sql.format(uid))
            for i in cur:
                x = (i[1] - now).days
                if x <= 7:
                    ll = list()
                    for s in i:
                        ll.append(s)
                    ll.append(x)
                    tmp_list.append(ll)
                num = len(tmp_list)
                if num != 0:
                    msg = "有{}位同学将在近期结束试用期：\\n".format(num)
                    for i in tmp_list:
                        if i == tmp_list[0]:
                            msg = msg + i[0]
                        else:
                            msg = msg + '-' + i[0]
                    msg = msg + "\n<a href=\'http://47.94.233.36:5000/?userid={}\'>点击查看详情</a>"
                    print(msg, aid)
                    send_msg(msg, aid)
#        schedule.enter(inc, 0, func)
        print("[ {} ]定时器执行-------------".format(datetime.datetime.now()))
        schedule.run()
    finally:
        conn.close()


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


def send_msg(CONTENT, aid):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
    values = """{
            "touser": "%s",
            "msgtype": "text",
            "agentid": "1000002",
            "text":{
                "content": "%s",
                },
            "safe": "0"
            }""" % (aid, str(CONTENT))
    req = requests.post(url, values)
    return req.json()

if __name__ == '__main__':
    func()
