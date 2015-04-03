from Glocal import app
from flask import render_template, request
import collections
from Glocal.API import API

def setup_page_dict():
    """Make a dictionary of all the pages in the file for links at the top of
    the web page. Add the name and address of every new page here"""
    page_dict = collections.OrderedDict()
    page_dict['Home'] = '/'
    return page_dict

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
        lst_local_tweets, lst_trending_tweets = user_query.get_twitter()
        lst_local_insta = user_query.get_instagram()
        lst_four_square_trending, lst_four_square_explore = user_query.get_four_square()
        lst_events = user_query.get_events()
        return render_template('results.html', title='Home',
                               page_dict=setup_page_dict(),
                               app_name=app.config['APP_NAME'],
                               lst_local_tweets=lst_local_tweets,
                               lst_trending_tweets=lst_trending_tweets,
                               lst_local_insta=lst_local_insta,
                               lst_four_square_trending=lst_four_square_trending,
                               lst_four_square_explore=lst_four_square_explore,
                               lst_events = lst_events,
                               st_address = st_address,
                               city = city,
                               state = state)
