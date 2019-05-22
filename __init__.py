#----- Imports ----- 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user,login_required


#----- Config ----- 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'welcome'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#----- Imports ----- 
from test1 import routes
from test1.models import User