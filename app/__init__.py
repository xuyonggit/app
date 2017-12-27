from flask import Flask
from flask import config

app = Flask(__name__)
app.config['config'] = 'E:\\xiaoxu\\app\\app\\config'


from app import views