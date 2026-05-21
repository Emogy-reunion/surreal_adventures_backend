'''
create custom validators to validate user input
'''
from wtforms.validators import ValidationError


def validate_multiline_list(form, field):
    '''
    Generic validator for TextArea fields that store data as a list.
    Works for Features, Highlights, Inclusions, and Exclusions.
    '''

    # Clean the data to check if it's empty
    lines = [line.strip() for line in field.data.splitlines() if line.strip()]

    if not lines:
        raise ValidationError(f'Please enter at least one {field.label.text.lower()}.')

    # Check length of each individual item
    for i, line in enumerate(lines):
        if len(line) > 150:  # Slightly higher limit for detailed inclusions
            raise ValidationError(f'Item on line {i+1} is too long (max 150 characters).')

