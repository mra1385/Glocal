from Glocal import db
def clear_db():
    db.drop_all()
    print "Database has been emptied"

clear_db()
