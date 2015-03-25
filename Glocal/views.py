from Glocal import app, db
from flask import render_template, request, flash, redirect
from .forms import RegistrationForm
import collections
from Glocal.API import API
from models import User

def setup_page_dict():
    """Make a dictionary of all the pages in the file for links at the top of
    the web page. Add the name and address of every new page here"""
    page_dict = collections.OrderedDict()
    page_dict['Home'] = '/'
    page_dict['Registration'] = '/Registration'
    page_dict['Contact'] = '/Contact'
    return page_dict


def add_to_database(username, password, first_name, last_name):
    db.create_all()
    db.session.add(User(username=username, password=password,
                        first_name=first_name, last_name=last_name))
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'GET':
        return render_template('home.html', title='Home',
                               page_dict=setup_page_dict(),
                               app_name=app.config['APP_NAME'])

    elif request.method == 'POST':
        st_address = request.form['st_address']
        city = request.form['city']
        state = request.form['state']
        miles = request.form['miles']
        user_query = API.GlocalAPI(st_address, city, state, miles)
        lst_local_tweets = user_query.get_tweets()
        lst_local_insta = user_query.get_instagram()
        lst_four_square = user_query.get_four_square()
        return render_template('results.html', title='Home',
                               page_dict=setup_page_dict(),
                               app_name=app.config['APP_NAME'],
                               lst_local_tweets=lst_local_tweets,
                               lst_local_insta=lst_local_insta,
                               lst_four_square=lst_four_square,
                               st_address = st_address,
                               city = city,
                               state = state)

@app.route('/Registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        add_to_database(form.username.data, form.password.data,
                        form.first_name.data, form.last_name.data)
        flash('Welcome {first_name}!'.format(first_name=form.first_name.data))
        return redirect('/')
    return render_template('registration.html', title='Registration',
                           page_dict=setup_page_dict(),
                           chosen_media=app.config['CHOSEN_MEDIA'],
                           form=form)


