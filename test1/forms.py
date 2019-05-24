#----- Imports ----- 
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,Length,Email
from wtforms import SelectField



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
    ministry=SelectField('ministry', choices=[])
    department=SelectField('department', choices=[])
    location=SelectField('location', choices=[])
    time=SelectField('date', choices=[])