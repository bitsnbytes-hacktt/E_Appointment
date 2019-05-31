#----- Imports ----- 
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,Length,Email
from wtforms import SelectField
from wtforms import DateField
from wtforms.fields.html5 import TimeField
from wtforms import IntegerField
from wtforms import DateTimeField
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail , Message



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
    
class MakeMinistryForm(FlaskForm):
    ministry= StringField('ministry',validators=[InputRequired(),])
    department= StringField('department',validators=[InputRequired(),])
    location= StringField('location',validators=[InputRequired(),])

class MinistryPickForm(FlaskForm):
    ministry=SelectField('ministry',choices=[])
    department=SelectField('department',choices=[])
    location=SelectField('location',choices=[])
    date=StringField('date')
    #date=DateField('date',format='%m/%d/%Y')
    startTime=TimeField('startTime')
    endTime=TimeField('endTime')
    #startTime=SelectField('startTime',choices=[('8','8:00 am'),('9','9:00 am'),('10','10:00 am'),('11','11:00 am'),('12','12:00 am')])
    # endTime=SelectField('endTime',choices=[('14','2:00 pm'),('15','3:00 pm'),('16','4:00 pm'),('17','5:00 pm'),('18','6:00 pm')])
    capacity= IntegerField('capacity',validators=[InputRequired()])
    periodH= SelectField('periodH',choices=[('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6')])
    periodM= SelectField('periodM',choices=[('0','0'),('10','10'),('15','15'),('20','20'),('30','30'),('45','45'),('50','50')])

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Email()])

class ResetPasswordForm(FlaskForm):    
    password = PasswordField('Password',validators=[InputRequired()])