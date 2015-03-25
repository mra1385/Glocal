from flask import Flask
from . import config
from flask_sqlalchemy import SQLAlchemy

app = Flask("Glocal")
app.config.from_object(config)
db = SQLAlchemy(app)

from Glocal import views

# # For error logging when debugging is False
# if not app.debug:
#     import logging
#     from logging.handlers import RotatingFileHandler
#     file_handler = RotatingFileHandler('Glocal/tmp/{}.log'.format(app.config['APP_NAME']),
#                                        'a', 1 * 1024 * 1024, 10)
#     file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: '
# '%(message)s [in %(pathname)s:%(lineno)d]'))
#     app.logger.setLevel(logging.INFO)
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#     app.logger.info('{} startup'.format(app.config['APP_NAME']))
