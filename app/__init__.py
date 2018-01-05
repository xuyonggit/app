from flask import Flask
from flask import config
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder='', static_path='')
bootstrap = Bootstrap(app)
app.config['config'] = 'E:\\xiaoxu\\app\\app\\config'


from app import views
