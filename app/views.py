# -*- coding:utf-8 -*-
import configparser
import os, json
from app import app
from app import getdata
from flask import Flask, render_template, flash, redirect, request, url_for
from app import forms
from flask_uploads import UploadSet, DOCUMENTS, configure_uploads, patch_request_class

cf = configparser.ConfigParser()
cf.read(app.config.get('config'), encoding="utf-8")
datadir = cf.get('data', 'datadir')
app.config['UPLOADS_DEFAULT_DEST'] = cf.get('app', 'file_dir')
app.config['SECRET_KEY'] = 'a random string'
file = UploadSet('data', DOCUMENTS)
configure_uploads(app, file)
patch_request_class(app, size=64 * 1024 * 1024)


@app.route('/')
def index():
    pass
    return "It is working"


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = forms.UploadForm()
    if form.validate_on_submit():
        filename = file.save(form.file.data)
        file_url = file.url(filename)
    else:
       file_url = None
    return render_template('index.html', form=form)


@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        mkdata = getdata.get_data(excelfile=datadir, delfile=1)
        results = mkdata.add_db(mkdata.read_xlsx())
        result = results['results']
    if result == 0:
        return json.dumps({'errcode': 0, "result": results['num']})
    else:
        return json.dumps({'errcode': 1})