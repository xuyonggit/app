# -*- coding:utf-8 -*-
import datetime
import pymysql
import time, sched
from .notify import send_msg
schedule = sched.scheduler(time.time, time.sleep)


def conn():
    return pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='app',
        password='lanmeimei_app',
        db='app_db',
        charset='utf8',
    )

def func(inc=5):
    now = datetime.date.today()
    tmp_list = []
    try:
        conn = conn()
        cur = conn.cursor()
        sql = "SELECT name,outdate from user_data where `status`=0"
        cur.execute(sql)
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
                    msg = msg + "<a href=\'http://www.baidu.com/{}\'>{}</a>".format(i[0], i[0])
                else:
                    msg = msg + "-<a href=\'http://www.baidu.com/{}\'>{}</a>".format(i[0], i[0])
            send_msg(msg)
        schedule.enter(inc, 0, func)
        print("[ {} ]定时器执行-------------".format(datetime.datetime.now()))
        schedule.run()
    finally:
        conn.close()

if __name__ == '__main__':
    func()
