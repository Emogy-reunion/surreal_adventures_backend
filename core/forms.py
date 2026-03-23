from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo



class RegistrationForm(FlaskForm):
    '''
    validates the email and password fields
    '''
    email = StringField('Email', validators=[
        Length(min=4, max=50, message='Email must be between 4 and 50 characters!'),
        Email(),
        DataRequired()
        ])
     password = PasswordField('Password: ', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long!"),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter!"),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter!"),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character!")
        ])

    confirmpassword = PasswordField('Confirm Password:', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords do no match!')
        ])
