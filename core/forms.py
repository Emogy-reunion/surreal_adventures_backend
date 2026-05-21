from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, DecimalField, DateField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo, NumberRange, Optional, ValidationError
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


class TourUploadForm(FlaskForm):

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
    price = DecimalField('Price', validators=[
        DataRequired(message="Price must be greater than 0"),
        NumberRange(min=1, max=10000000, message="Price must be between 1 and 100,000,000")
        ], places=2)
    duration = StringField('Duration', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[Optional()])
    category = StringField('Category', validators=[
        DataRequired(),
        Length(max=50)
        ])
    discount_start = DateField('Discount Start', validators=[Optional()])
    discount_end = DateField('Discount End', validators=[Optional()])
    discount_price = DecimalField('Discount Price', places=2, validators=[Optional()])
    is_featured = BooleanField('Is Featured')
    is_day_trip = BooleanField('Is  Day Trip')
    is_active = BooleanField('Is Active')
    description = TextAreaField('Description', validators=[
        DataRequired(message="Please provide a detailed description of the tour."),
        Length(min=150, max=3000, message="Description must be between 150 and 3000 characters.")
        ])
    highlights = TextAreaField('Highlights', validators=[
        DataRequired(),
        validate_multiline_list
        ])
    includes = TextAreaField('Includes', validators=[
        DataRequired(),
        validate_multiline_list
        ])
    excludes = TextAreaField('Excludes', validators=[
        DataRequired(),
        validate_multiline_list
        ])
    images = MultipleFileField('Images', validators=[
        DataRequired(),
        FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')
        ])

    def validate_end_date(self, field):
        if self.start_date.data and field.data:
            if field.data < self.start_date.data:
                raise ValidationError("End date cannot be earlier than the start date.")

    def validate_discount_end(self, field):
        if self.discount_start.data and field.data:
            if field.data < self.discount_start.data:
                raise ValidationError("Discount end date cannot be earlier than the discount start.")
