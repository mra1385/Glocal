from Glocal import db
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=1, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return 'id {}<username {}, password {}, firstname {}, lastname{}'.\
            format(self.id, self.username, self.password, self.first_name,
                   self.last_name)