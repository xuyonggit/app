# -*- coding:utf-8 -*-
import pymysql
from app import app
import configparser


def conn():
    configfile = app.config.get('config')
    cf = configparser.ConfigParser()
    cf.read(configfile)
    return pymysql.connect(
        host=cf.get('db', 'db_host'),
        port=cf.getint('db', 'db_port'),
        user=cf.get('db', 'db_user'),
        password=cf.get('db', 'db_passwd'),
        db=cf.get('db', 'db_name'),
        charset=cf.get('db', 'db_charset')
    )
