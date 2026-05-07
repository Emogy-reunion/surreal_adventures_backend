from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, DecimalField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo, NumberRange
from flask_wtf.file import FileField, MultipleFileField, FileAllowed
from core.utils.custom_form_validators import validate_multiline_list



ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']

class RegistrationForm(FlaskForm):
    '''
    validates the email and password fields
    '''

    class Meta:
        csrf = False

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
        EqualTo('password', message='Passwords do not match!')
        ])

class LoginForm(FlaskForm):

    class Meta:
        csrf = False

    email = StringField('Email:', validators=[
        Email(),
        DataRequired(),
        Length(max=255)
        ])
    password = PasswordField('Password:', validators=[
        DataRequired()
        ])

class DestinationUploadForm(FlaskForm):
    class Meta:
        csrf = False

    country = StringField('Country', validators=[
        DataRequired(),
        Length(max=100)
        ])
    name = StringField('Name', validators=[
        DataRequired(),
        Length(max=255)
        ])
    location = StringField('Location', validators=[
        DataRequired(),
        Length(max=255)
        ])
    start_price = DecimalField('Start price', validators=[
        DataRequired(message="Price must be greater than 0"),
        NumberRange(min=1, max=10000000, message="Price must be between 1 and 100,000,000")
        ], places=2)
    description = TextAreaField('Description', validators=[
        DataRequired(message="Please provide a detailed description of the tour."),
        Length(min=150, max=3000, message="Description must be between 150 and 3000 characters.")
        ])
    highlights = TextAreaField('Highlights', validators=[
        DataRequired(),
        validate_multiline_list
        ])
    is_featured = BooleanField('Is Featured')
    category = StringField('Category', validators=[
        DataRequired(),
        Length(max=50)
        ])
    images = MultipleFileField('Images', validators=[
        DataRequired(),
        FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')
        ])
