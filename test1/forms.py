#----- Imports ----- 
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,Length,Email
from wtforms import SelectField
from wtforms import DateField
from wtforms import TimeField
from wtforms import IntegerField
from wtforms import DateTimeField




#----- Forms ----- 
class PublicUserRegisterationForm(FlaskForm):
    fname = StringField('First Name',validators=[InputRequired(),Length(min=2,max=30)])
    lname = StringField('Last Name',validators=[InputRequired(),Length(min=2,max=30)])
    email = StringField('Email',validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators=[InputRequired()])

class PublicUserLoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators=[InputRequired()])

class AdminUserLoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators=[InputRequired()])

class AdminUserCreateForm(FlaskForm):
    name = StringField('Name',validators=[InputRequired(),Length(min=2,max=30)])
    email = StringField('Email',validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators=[InputRequired()])

class AdminUserDeleteForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Email()])

class MinistryPickForm(FlaskForm):
    ministry=SelectField('ministry',choices=[])
    department=SelectField('department',choices=[])
    location=SelectField('location',choices=[])
    date=DateField('date',format=' %Y-%m-%d ')
    #startTime=DateTimeField('startTime', format="MM/dd/yyyy HH:mm:ss PP")
    startTime=SelectField('startTime',choices=[('8','8:00 am'),('9','9:00 am'),('10','10:00 am'),('11','11:00 am'),('12','12:00 am')])
    endTime=SelectField('endTime',choices=[('14','2:00 pm'),('15','3:00 pm'),('16','4:00 pm'),('17','5:00 pm'),('18','6:00 pm')])
    capacity= IntegerField('capacity',validators=[InputRequired()])
    period= IntegerField('period',validators=[InputRequired()])   