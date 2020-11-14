import importlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import config
import sys

importlib.reload(sys)
app = Flask(__name__)
bootstrap=Bootstrap(app)
app.config.from_object(config)
db = SQLAlchemy(app)
from flask_mail import Mail
mail = Mail()
mail.init_app(app)