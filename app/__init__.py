from flask import Flask
from flask import config

app = Flask(__name__, static_folder='', static_path='')
app.config['config'] = '/data/config/config'


from app import views
