
from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user,login_required
from test1 import db



#----- Databases ----- 

#----- Databases ----- 
class User(UserMixin,db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30) , unique=True)
    password = db.Column(db.String(30))
    roles = db.relationship('Role' , backref='theuser')

class Role(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30))
    admin = db.Column(db.Boolean)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))