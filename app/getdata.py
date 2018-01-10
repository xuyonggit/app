# -*- coding:utf-8 -*-
import os
import xlrd
from xlrd import xldate_as_tuple
import datetime
from app import dbconn
from app import app


class get_data(object):
    __doc__ = "提取数据存储到数据库"

    def __init__(self, excelfile=None, delfile=0):
        self.delfile = delfile
        self.datadir = excelfile
        self.tmp_list = []

    def read_xlsx(self):
        workbook = xlrd.open_workbook(self.datadir)
        booksheet = workbook.sheet_by_name('Sheet1')
        tmp = list()
        for row in range(1, booksheet.nrows):
            row_data = []
            for col in range(booksheet.ncols):
                ctype = booksheet.cell(row, col).ctype
                cel = booksheet.cell_value(row, col)
                if ctype == 3:
                    data = datetime.datetime(*xldate_as_tuple(cel, 0))
                    val = data.strftime('%Y/%m/%d')
                else:
                    val = cel
                row_data.append(val)
            tmp.append(row_data)
        if self.delfile == 1:
            os.remove(self.datadir)
        return tmp

    def add_db(self, ll, userid):
        data = ll
        num = 0
        userid = userid
        conn = dbconn.conn()
        cursor = conn.cursor()
        try:
            insert_sql = "INSERT INTO app_db.user_data(name, sex, indate, outdate, other, userid) VALUES ('{}','{}','{}','{}', '{}', '{}')"
            update_sql = "UPDATE app_db.user_data SET `name`='{}', `sex`='{}', `indate`='{}', `outdate`='{}', `other`='{}' WHERE (`name`='{}')"
            for i in data:
                cursor.execute("SELECT count(*) from app_db.user_data where `name`='{}' and `userid`='{}'".format(i[0], userid))
                n = int(cursor.fetchone()[0])
                if n > 0:
                    if i[3]:
                        ret = cursor.execute(update_sql.format(i[0], i[1], i[2], i[3], i[4], i[0]))
                    else:
                        ret = cursor.execute(update_sql.format(i[0], i[1], i[2], i[3], 'NULL', i[0]))
                else:
                    if i[3]:
                        ret = cursor.execute(insert_sql.format(i[0], i[1], i[2], i[3], i[4], userid))
                    else:
                        ret = cursor.execute(insert_sql.format(i[0], i[1], i[2], i[3], 'NULL', userid))
                    num = num + 1
            conn.commit()
        finally:
            conn.close()
        return {'results': 0, 'num': num}

    def get(self, userid=None):
        conn = dbconn.conn()
        cur = conn.cursor()
        if userid != None:
            sql = "SELECT name,sex,CAST(indate AS CHAR),CAST(outdate AS CHAR)outdate,other,status from app_db.user_data where userid={};".format(userid)
        else:
            sql = "SELECT name,sex,CAST(indate AS CHAR),CAST(outdate AS CHAR)outdate,other,status from app_db.user_data;"
        try:
            cur.execute(sql)
            for i in cur:
                tmp_l1 = []
                for x in i:
                    tmp_l1.append(x)
                self.tmp_list.append(tmp_l1)
        finally:
            conn.close()
        return self.tmp_list

    def get_username(self, userid):
        conn = dbconn.conn()
        cur = conn.cursor()
        sql = "SELECT username FROM app_db.tb_user WHERE userid=13314;"
        try:
            cur.execute(sql)
            for i in cur:
                username = i
        finally:
            conn.close()
        return username[0]