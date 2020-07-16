from flask import Flask
from flask_migrate import Migrate
#from config import Config

app = Flask(__name__)
application = app # For beanstalk
#app.config.from_object(Config)

app.secret_key = 'fegrweiugwoibgpiw40pt8940gtbuorwbgo408bg80pw4'
app.config['SESSION_TYPE'] = 'filesystem'

from app import routes, models
