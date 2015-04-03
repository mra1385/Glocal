import requests
from instagram.client import InstagramAPI
import foursquare
import tweepy
import eventful
import pylast
from eventbrite import Eventbrite
from datetime import datetime

###  -----  API Keys  -----   ###

Twitter_API_Key = 'XpP7VNPUUak2YMMjZkW0sKA15'
Twitter_API_Secret = '2WOkIe7KkZ2B36bVcUsBEZA31LKQqHgCPWJJAF17G3E6ttZXrP'
Twitter_Token = '776228798-XCOTz36pFolEUeygxt7Os19oY3GgQSaCH2TriwKM'
Twitter_Token_Secret = 'jn43lDUZEDcoHSxmy20v2oR3EsoBdgXPwUlxni8OzOuUv'

Google_API = 'AIzaSyDBpDaj4GWXn8ApFULeB0GkvYTLWROpxVA'

Insta_Client_ID = "ed547816012648db9011d08fc0df709f"
Insta_Client_Secret = "d7e8ffe769074807b630942796d8d0d7"

FrSquare_Client_ID ="0CVJC4C44DABYTEWSG3DR54AIFAK53NZJ3KVZL1B0CBZXVSE"
FrSquare_Client_Secret = "FTJZCTBXGVA4FGFULBSW11HZECTU3Z3SSYSDLCWED3IYAROT"

Eventful_Key = "g8PVTcPJbmnRdtdt"

Last_fm_Key = 'a11eadd8a8429ad429e41385918f9fa1'
Last_fm_Secret = '4ea3db3bb840ff0ef8e84021425068d1'

Eventbrite_API = "HURARHPPK3AG2G5WJR3H"

###  -----  API Class  -----   ###

class GlocalAPI:
    def __init__(self, st_address, city, state, miles='1'):
        self.st_address = st_address
        self.city = city
        self.state = state
        self.miles = miles

        """
        GlocalAPI class takes an address and radius as parameters and returns
        class attributes latitude and longitude coordinates for use to query
        social media APIs.
        """

        # Request of Google Maps API to convert address into latitude, longitude
        r = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address=' +
            self.st_address + '+' + self.city + ',+' + self.state
            + '&sensor=FALSE' + Google_API)

        # Converts the data into readable json format
        data = r.json()

        # Pulls the latitude, longitude coordinates from a long stream of json data
        # that includes information other than the coordinates.
        self.latitude = data['results'][0]['geometry']['location']['lat']
        self.longitude = data['results'][0]['geometry']['location']['lng']

    ###  -----  Twitter API  -----   ###
    def get_twitter(self):
        # Queries Twitter and returns tweets and trending topics within an area
        # based on geo parameters
        self.auth = tweepy.OAuthHandler(Twitter_API_Key, Twitter_API_Secret)
        self.auth.set_access_token(Twitter_Token, Twitter_Token_Secret)
        self.twitter_api = tweepy.API(self.auth)


        ###  -----  Local Tweets  -----   ###

        # Queries Twitter for tweets within a certain geographic location using
        # coordinates as parameters
        local_tweets = (self.twitter_api.search(geocode='{0},{1},{2}mi'.format(
                        self.latitude, self.longitude, self.miles)))

        # Appends tweets to list
        lst_local_tweets = []
        for tweet in local_tweets:
            lst_local_tweets.append(tweet)

        ###  -----  Trending Topics  -----   ###

        # Queries Twitter for specific geo ID tag based on lat/long coords
        trending_woeid = (self.twitter_api.trends_closest(self.latitude,self.longitude))

        # Appends geo ID tags to list
        lst_trending_woeid = []
        for i in range(len(trending_woeid)):
            lst_trending_woeid.append(trending_woeid[i]['woeid'])

        # Queries Twitter to extract trending topics based on geo ID.
        # Appends trending topics to list
        lst_trending_tweets = []
        for i in range(len(lst_trending_woeid)):
            trending_topics = (self.twitter_api.trends_place(lst_trending_woeid[i]))
            for i in range(len(trending_topics)):
                trending_topics_2 = trending_topics[i]
                for i in range(len(trending_topics_2)):
                    lst_trending_tweets.append(trending_topics_2['trends'][i]['name'])

        return lst_local_tweets, lst_trending_tweets

    ###  -----  Instagram API  -----   ###
    def get_instagram(self):
        # Queries Instagram and returns images within an area based on geo parameters
        instagram_api = InstagramAPI(client_id=Insta_Client_ID,
                                     client_secret=Insta_Client_Secret)
        # converts user's miles radius input into meters
        dist_meters = str(float(self.miles) * 1609.34)
        local_media = instagram_api.media_search(lat=self.latitude,
                                                 lng=self.longitude,
                                                 distance=dist_meters)
        # 'low resolution' versions of images appended to list
        photos = []
        for media in local_media:
            photos.append(media.images['low_resolution'].url)
        return photos


    def get_four_square(self):
        # Queries Four Square and returns trending and popular venues within an
        # area based on geo parameters
        client = foursquare.Foursquare(client_id=FrSquare_Client_ID,
                                       client_secret=FrSquare_Client_Secret)
        # converts user's miles radius input into meters
        dist_meters = str(float(self.miles) * 1603.34)


        ###  -----  Trending Venues  -----   ###

        # Queries Four Square and returns trending venues within an area based on
        #  geo parameters
        trending_four_square = client.venues.trending(params=
                                                 {'ll': str(self.latitude) + ','
                                                        + str(self.longitude),
                                                  'radius': dist_meters,
                                                  'sortByDistance':'1',
                                                  'openNow':'1'})

        # Creates a dictionary with venue name as key and check-ins as the value
        trending_venues = dict()
        for i in range(len(trending_four_square["venues"])):
            trending_venues[trending_four_square["venues"][i]["name"]] = \
                trending_four_square["venues"][i]["hereNow"]["summary"]

        ###  -----  Popular Venues  -----   ###

        # Queries Four Square and returns popular venues within an area based on
        #  geo parameters
        popular_four_square = client.venues.explore(params=
                                                 {'ll': str(self.latitude) + ','
                                                        + str(self.longitude),
                                                  'radius': dist_meters,
                                                  'sortByDistance':'1',
                                                  'openNow':'1',
                                                  'limit':'20'})

        # Appends certain venue details (rating and check-ins) to a list.
        # Also creates a dictionary with the name of the venue as the key, and the
        # details appended to the list above (rating and check-ins) as the values.
        # Exception handling to prevent error in case no events are found or certain details
        # are not available.
        rating_hereNow = []
        popular_venues = dict()
        for i in xrange(len(popular_four_square['groups'][0]['items'])):
            try:
                venue_details_tmp = []
                venue_details_tmp.append(popular_four_square['groups'][0]['items'][i]['venue']['rating'])
                venue_details_tmp.append(popular_four_square['groups'][0]['items'][i]['venue']['hereNow']['summary'])
                rating_hereNow.append(venue_details_tmp)
                popular_venues[popular_four_square['groups'][0]['items'][i]['venue']['name']] = rating_hereNow[i]
            except:
                continue

        return trending_venues, popular_venues

    ###  -----  Event APIs  -----   ###
    def get_events(self):
        # Queries Eventful, LastFM, and Eventbrite and returns events within an
        # area based on geo parameters

        # Datetime format for event start date/time
        datetime_format = '%b %d,%Y -- %I:%M %p'

        lst_events = []


        ###  -----  Eventful  -----   ###

        # Queries Eventful API and returns events within an area based on geo
        # parameters. Exception handling to prevent error in case no events
        # are found.
        api = eventful.API(Eventful_Key)
        try:
            eventful_events = api.call('/events/search', location=(str(self.latitude) + ','
                                                               + str(self.longitude)),
                                   within=self.miles, sort_order="date")
        except:
            eventful_events = dict({'events':None})

        # Appends Eventful event details to 'lst_events' list. Two different
        # 'For Loops' are used because if only one event is found, it is returned
        # as a dict, otherwise it is returned as a list
        if eventful_events['events'] != None:
            if isinstance(eventful_events['events']['event'], list):
                for event in eventful_events['events']['event']:
                    tmp_event = []
                    tmp_time = []
                    tmp_event.append(event['title'][:35])
                    tmp_event.append(event['venue_name'][:20])
                    # converts datetime format
                    tmp_time = event['start_time']
                    tmp_time_adj = datetime.strptime(tmp_time,'%Y-%m-%d %H:%M:%S').strftime(datetime_format)
                    tmp_event.append(tmp_time_adj)
                    tmp_event.append(event['url'])
                    lst_events.append(tmp_event)

            elif isinstance(eventful_events['events']['event'], dict):
                tmp_event = []
                tmp_time = []
                tmp_event.append(eventful_events['events']['event']['title'][:35])
                tmp_event.append(eventful_events['events']['event']['venue_name'][:20])
                tmp_time = eventful_events['events']['event']['start_time']
                # converts datetime format
                tmp_time_adj = datetime.strptime(tmp_time,'%Y-%m-%d %H:%M:%S').strftime(datetime_format)
                tmp_event.append(tmp_time_adj)
                tmp_event.append(eventful_events['events']['event']['url'])
                lst_events.append(tmp_event)


        ###  -----  LastFM  -----   ###

        # Queries LastFM API and returns events within an area based on geo
        # parameters. Exception handling to prevent error in case no events
        # are found.
        network = pylast.LastFMNetwork(api_key = Last_fm_Key,
                                       api_secret = Last_fm_Secret)
        try:
            lastfm_events = network.get_geo_events(longitude= self.longitude,
                                                   latitude = self.latitude,
                                                   distance=self.miles)
        except:
            lastfm_events = []

        # Appends LastFM event details to 'lst_events' list. Exception handling
        # in case no events are found or etracting certain event details creates
        # an error
        for i in range(len(lastfm_events)):
            try:
                tmp_event = []
                tmp_time = []
                tmp_event.append(lastfm_events[i].get_title())
                tmp_event.append(lastfm_events[i].get_venue().get_name())
                # converts datetime format
                tmp_time = lastfm_events[i].get_start_date()
                tmp_time_adj = datetime.strptime(tmp_time,'%a, %d %b %Y %H:%M:%S').strftime(datetime_format)
                tmp_event.append(tmp_time_adj)
                tmp_event.append(lastfm_events[i].get_url())
                lst_events.append(tmp_event)
            except:
                continue

        ###  -----  Eventbrite  -----   ###

        # Queries Eventbrite API and returns events within an area based on geo
        # parameters.
        eventbrite = Eventbrite(Eventbrite_API)
        eventbrite_within = str(int(float(self.miles)))
        eventbrite_events = eventbrite.event_search(**{'location.within':eventbrite_within + "mi",
                                                       'location.latitude':str(self.latitude),
                                                       'location.longitude':str(self.longitude),
                                                       'popular':'true',
                                                       'sort_by':'date'})

        # Appends Eventbrite event details to 'lst_events' list. Exception handling
        # in case no events are found or etracting certain event details creates
        # an error
        for i in xrange(20):
            try:
                tmp_event = []
                tmp_time = []
                tmp_event.append(eventbrite_events['events'][i]['name']['text'][:35])
                tmp_event.append(eventbrite_events['events'][i]['venue']['name'][:20])
                # converts datetime format
                tmp_time = eventbrite_events['events'][i]['start']['local']
                tmp_time_adj = datetime.strptime(tmp_time,'%Y-%m-%dT%H:%M:%S').strftime(datetime_format)
                tmp_event.append(tmp_time_adj)
                tmp_event.append(eventbrite_events['events'][i]['url'])
                lst_events.append(tmp_event)
            except:
                continue

        # Events in lst_events are sorted by chronological order
        return sorted(lst_events, key=lambda x: datetime.strptime(x[-2], datetime_format))


# x = GlocalAPI("1500 Massachusetts Ave NW", "washington","dc","1" )
# x.get_instagram()
# x.get_events()
# # # # # y = GlocalAPI("","Sanaa","Yemen","10")
# # # y.get_events()
# # z = GlocalAPI("42 mar elias street","al-mina, tripoli", "lebanon","5")
# z.get_events()