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

    def add_db(self, ll):
        print(ll)
        data = ll
        num = 0
        conn = dbconn.conn()
        cursor = conn.cursor()
        insert_sql = "INSERT INTO app_db.user_data(name, sex, indate, outdate, other) VALUES ('{}','{}','{}','{}', '{}')"
        update_sql = "UPDATE app_db.user_data SET `name`='{}', `sex`='{}', `indate`='{}', `outdate`='{}', `other`='{}' WHERE (`name`='{}')"
        for i in data:
            cursor.execute("SELECT count(*) from app_db.user_data where `name`='{}'".format(i[0]))
            n = int(cursor.fetchone()[0])
            if n > 0:
                if i[3]:
                    ret = cursor.execute(update_sql.format(i[0], i[1], i[2], i[3], i[4], i[0]))
                else:
                    ret = cursor.execute(update_sql.format(i[0], i[1], i[2], i[3], 'NULL', i[0]))
            else:
                if i[3]:
                    ret = cursor.execute(insert_sql.format(i[0], i[1], i[2], i[3], i[4]))
                else:
                    ret = cursor.execute(insert_sql.format(i[0], i[1], i[2], i[3], 'NULL'))
                num = num + 1
        conn.commit()
        cursor.close()
        conn.close()
        return {'results': 0, 'num': num}
