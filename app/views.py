# -*- coding:utf-8 -*-
import configparser
import threading
import os, json
from app import app
from app import getdata
from app import forms
from flask import Flask, render_template, flash, redirect, request, url_for, make_response, send_file
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
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    template_url = url_for('download', name='data', _external=True)
    form = forms.UploadForm()
    l = getdata.get_data().get()
    for i in l:
        if i[5] == 0:
            i[5] = u"是"
        else:
            i[5] = u"否"
    if form.validate_on_submit():
        filename = file.save(form.file.data)
        file_url = file.url(filename)
    else:
       file_url = None
    return render_template('index.html', form=form, List=l, url=template_url)


@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        files = os.listdir(datadir)
        if len(files) == 1:
            filepath = os.path.join(datadir, files[0])
        else:
            os.remove(datadir)
            return json.dumps({'errcode': 1})
        mkdata = getdata.get_data(excelfile=filepath, delfile=1)
        results = mkdata.add_db(mkdata.read_xlsx())
        result = results['results']
    if result == 0:
        return json.dumps({'errcode': 0, "result": results['num']})
    else:
        return json.dumps({'errcode': 1})


@app.route('/searchall', methods=['GET', 'POST'])
def searchall():
    templates = ['name', 'sex', 'indate', 'outdate', 'other', 'status']
    tmp_L = []
    l = getdata.get_data().get()
    for i in l:
        t_dic = {}
        if i[5] == 0:
            i[5] = u"是"
        else:
            i[5] = u"否"
        for s in range(5):
            t_dic[templates[s]] = i[s]
        tmp_L.append(t_dic)
    return json.dumps(tmp_L)


@app.route('/download/data')
def download():
    response = make_response(send_file(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), 'data', 'data.xlsx')))
    return response