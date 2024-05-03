from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SECRET_KEY"] = "dbe138dfe3dec2ebcd535a9dd193a22c"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homapage()"

from fakepinterest import routes