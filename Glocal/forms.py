from wtforms import TextField, PasswordField, validators, ValidationError
from flask_wtf import Form
from flask import flash
from models import User
from Glocal import db
import re


def check_unique(form, field):
    """Checks that the username is not already in the database"""
    if user_in_database(field.data):
        raise ValidationError('\'{}\' already chosen. Please choose another '
                              'Username'.format(field.data))


def user_in_database(username):
    """Checks to see if user is already in database"""
    try:
        User.query.filter_by(username=username).first()
        flash('Database is not empty, success!')

    # If the database is empty, then it cannot search for usernames. If it's
    # empty, then the username must be unique.
    except:
        flash('Database is empty')


def letters_only(form, name):
    """Checks that field only contains letters"""
    if not re.search(r'^[a-zA-Z]*$', name.data):
        raise ValidationError('Name must only contain letters.')


class RegistrationForm(Form):
    username = TextField('Username', [validators.length(min=4, max=20,
                        message='Username must be between 4 and 20 characters'),
                                      check_unique])

    # Ensures the password contains at least one number and capital letter
    password = PasswordField('Password',
                             [validators.required(),
                              validators.regexp(
                                  r'([a-z]*[A-Z]+\w*\d+)|([a-z]*\d+\w*[A-Z]+)',
                                message='Password must alphanumeric and contain'
                                        'at least one number and capital letter'
                              )])

    first_name = TextField('First name',
                           [validators.required(message='Please enter your first'
                                                        'name'), letters_only])

    last_name = TextField('Last name',
                          [validators.required(message='Please enter your last'
                                                       'name'), letters_only])
