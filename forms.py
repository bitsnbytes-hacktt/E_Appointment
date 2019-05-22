#----- Imports ----- 
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,Length,Email



#----- Forms ----- 
class PublicUserRegisterationForm(FlaskForm):
    name = StringField('Name',validators=[InputRequired(),Length(min=2,max=30)])
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
