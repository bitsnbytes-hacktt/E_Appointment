
from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user,login_required
from test1 import db



#----- Databases ----- 

#----- Databases ----- 

link1= db.Table('link1',
    db.Column('department_id', db.Integer, db. ForeignKey('department.id')),
    db.Column('location_id', db.Integer, db. ForeignKey('location.id'))
)


#----- Databases ----- 


class User(UserMixin,db.Model):
    id = db.Column(db.Integer , primary_key=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    email = db.Column(db.String(30) , unique=True)
    password = db.Column(db.String(30))
    roles = db.relationship('Role' , backref='theuser')
    appointments = db.relationship('Appointment' , backref='theuser')

class Role(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30))
    admin = db.Column(db.Boolean)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))


#---------------------------------------------------------------------------------------------- 
class Ministry(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30) , unique=True)
    departments = db.relationship('Department' , backref='ministry')

class Location(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30) , unique=True)
    department_location = db.relationship('Department', secondary=link1, backref=db.backref('department_location', lazy='dynamic'))

class Department(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30))
    ministry_id = db.Column(db.Integer , db.ForeignKey('ministry.id'))
    settings = db.relationship('Setting' , backref='department')
    appointments = db.relationship('Appointment' , backref='department')
    
#---------------------------------------------------------------------------------------------- 
class Setting(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    time_period = db.Column(db.Integer)
    limit = db.Column(db.Integer)
    department_id = db.Column(db.Integer , db.ForeignKey('department.id'))
    app_type = db.Column(db.String(30))

class Appointment(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    time = db.Column(db.Integer)
    date = db.Column(db.String(30))
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    department_id = db.Column(db.Integer , db.ForeignKey('department.id'))

class Service_Time(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    start_time = db.Column(db.Integer)
    department_id = db.Column(db.Integer , db.ForeignKey('department.id'))
