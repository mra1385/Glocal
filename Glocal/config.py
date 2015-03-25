import os
basedir = os.path.abspath(os.path.dirname(__file__))

# This is the path of the database file
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir,
                                                       'Database/glocal_user.db'
)

APP_NAME = 'Glocal'
CHOSEN_MEDIA = ['Twitter', 'Instagram', 'Yelp', 'Facebook']

# Security for login/registration pages.
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

