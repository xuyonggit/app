# -*- coding: utf-8 -*-
from app import app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, DOCUMENTS, configure_uploads, patch_request_class
from wtforms import SubmitField


file = UploadSet('data', DOCUMENTS)


class UploadForm(FlaskForm):
    file = FileField(validators=[
        FileAllowed(file, u'只能导入.xlsx结尾的文件'),
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'导入')