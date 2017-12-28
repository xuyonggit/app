# -*- coding:utf-8 -*-
import time
import datetime
from threading import Timer
from app import dbconn, notify


def func():
    now = datetime.date.today()
    tmp_list = []
    conn = dbconn.conn()
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
    msg = "有{}位同学将在近期结束试用期：\\n".format(num)
    for i in tmp_list:
        msg = msg + "{}同学将在{}天后结束试用期，\\n".format(i[0], i[2])
    msg = msg + "<a href=\"http://www.baidu.com\">点击查看详情</a>"
    notify.send_msg(msg)
#    Timer(60, func, ('Hello', time.time())).start()
    cur.close()
    conn.close()


if __name__ == '__main__':
    func()