# -*- coding:utf-8 -*-
from app import app
from flask import render_template, flash, redirect, request
import configparser
from app import getdata

cf = configparser.ConfigParser()
cf.read(app.config.get('config'))
datadir = cf.get('data', 'datadir')



@app.route('/')
def index():
    pass
    return render_template('index.html')


@app.route('/notify', methods=['GET', 'POST'])
def notify():
    pass

@app.route('/input', methods=['GET', 'POST'])
def input():
    mkdata = getdata.get_data(excelfile=datadir)
    results = mkdata.add_db(mkdata.read_xlsx())
    result = results['results']
    if result == 0:
        return 'success'
    else:
        return {'results': 1}