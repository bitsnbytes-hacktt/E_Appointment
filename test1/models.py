from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from test1 import db, app, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

    def get_reset_token(self , expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

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
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
    time_period = db.Column(db.String)
    limit = db.Column(db.Integer)
    department_id = db.Column(db.Integer , db.ForeignKey('department.id'))
    location_id = db.Column(db.Integer , db.ForeignKey('location.id'))
    app_type = db.Column(db.String(30))

class Appointment(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    time = db.Column(db.Integer)
    date = db.Column(db.String(30))
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    department_id = db.Column(db.Integer , db.ForeignKey('department.id'))
    location_id = db.Column(db.Integer , db.ForeignKey('location.id'))

class Service_Time(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    start_time = db.Column(db.String)
    department_id = db.Column(db.Integer , db.ForeignKey('department.id'))
    location_id = db.Column(db.Integer , db.ForeignKey('location.id'))
