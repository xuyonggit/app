# -*- coding:utf-8 -*-
import configparser
import threading
import os, json
from app import app
from app import getdata
from app import forms
from flask import Flask, render_template, flash, redirect, request, url_for, make_response, send_file, session
from flask_uploads import UploadSet, DOCUMENTS, configure_uploads, patch_request_class


cf = configparser.ConfigParser()
cf.read(app.config.get('config'), encoding="utf-8")
datadir = cf.get('data', 'datadir')
app.config['UPLOADS_DEFAULT_DEST'] = cf.get('app', 'file_dir')
app.config['SECRET_KEY'] = 'a random string'
file = UploadSet('data', DOCUMENTS)
configure_uploads(app, file)
patch_request_class(app, size=64 * 1024 * 1024)
if not os.path.exists(datadir):
    os.mkdir(datadir)


@app.route('/')
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if len(request.args) > 0:
        userid = request.args.get('userid')
        if userid:
            session['userid'] = userid
            username = getdata.get_data().get_username(userid)
    else:
        username = ""
    template_url = url_for('download', filename='data', _external=True)
    form = forms.UploadForm()
    if form.validate_on_submit():
        filename = file.save(form.file.data)
        file_url = file.url(filename)
        return str(os.path.split(file_url)[1])
    else:
       file_url = None
    return render_template('index.html', form=form, url=template_url, username=username)


@app.route('/input/<filename>', methods=['GET', 'POST'])
def input(filename):
    if session['userid']:
        userid = session['userid']
        if request.method == 'POST':
            filepath = os.path.join(datadir, filename)
            mkdata = getdata.get_data(excelfile=filepath, delfile=1)
            results = mkdata.add_db(mkdata.read_xlsx(), userid=userid)
            result = results['results']
        if result == 0:
            return json.dumps({'errcode': 0, "result": results['num']})
        else:
            return json.dumps({'errcode': 1})
    else:
        return json.dumps({'errcode': 2})


@app.route('/searchall', methods=['GET', 'POST'])
def searchall():
    if 'userid' in session:
        userid = session['userid']
        templates = ['name', 'sex', 'indate', 'outdate', 'other', 'status']
        tmp_L = []
        l = getdata.get_data().get(userid)
        for i in l:
            t_dic = {}
            for s in range(6):
                t_dic[templates[s]] = i[s]
            tmp_L.append(t_dic)
        return json.dumps(tmp_L)
    else:
        return 'error'


@app.route('/download/<filename>')
def download(filename):
    if filename == 'data':
        response = make_response(send_file(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), 'data', 'data.xlsx')))
    return response


@app.route('/modify', methods=['GET', 'POST'])
def modify():
    pass