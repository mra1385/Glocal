from Glocal import app
from flask import render_template

# When debugging is set to off, these pages will show when the respective errors
# are raised
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='Error 404',
                           app_name=app.config['APP_NAME']), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', title='Error 500',
                           app_name=app.config['APP_NAME']), 500