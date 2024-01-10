from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, DateField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError

class simpleForm(FlaskForm):
    firstname = StringField()
    lastname = StringField()
    username = StringField()
    password = PasswordField()
    confirmpassword = PasswordField()
    consumer = RadioField('Choose the one that applies to you', 
                          choices=[
                              ('Student', 'Student'), ('Facilitator', 'Facilitator')
                          ])
    submit = SubmitField('sign up')

class loginForm(FlaskForm):
    username = StringField()
    password = StringField()
    submit = SubmitField('Sign in')
    
    