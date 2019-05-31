#----- Imports ----- 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail 

#----- Config ----- 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'welcome'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'puremaster007@gmail.com'
app.config['MAIL_PASSWORD'] = '!Nception528491'
mail = Mail(app)


#----- Imports ----- 
from test1 import routes
#from test1.models import User