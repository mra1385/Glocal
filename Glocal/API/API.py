import requests
from instagram.client import InstagramAPI
import foursquare
import tweepy
import eventful
import pylast.pylast

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


class GlocalAPI:
    def __init__(self, st_address, city, state, miles='1'):
        self.st_address = st_address
        self.city = city
        self.state = state
        self.miles = miles

        """
        HTTP GET request used to query Google Maps to convert an address into
        latitude, longitude coordinates. The GET request queries a specific
        Google Maps url (provided in the Google Maps API) with specific
        parameters attached (the address).
        """
        r = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address=' +
            self.st_address + '+' + self.city + ',+' + self.state
            + '&sensor=FALSE' + Google_API)

        # Converts the data into readable json format
        data = r.json()

        # Pulls the latitude, longitude coords from a long stream of json data
        # that includes information other than the coordinates.
        self.latitude = data['results'][0]['geometry']['location']['lat']
        self.longitude = data['results'][0]['geometry']['location']['lng']


    def get_coordinates(self):
        return self.latitude, self.longitude


    def get_tweets(self):
        """
        Queries Tweets using Twitter API 'geocode' coordinates, which takes the
        parameters "latitude,longitude,radius" as strings. Assembles all of the
        search results into a list of tweets in the form of "Username: Tweet".
        Tweets are comprised of 'fields' (tweet, username,
        shared links, hashtag, etc. For example, tweet.text returns the
        'text' field of the tweet, tweet.user.screen_name returns the screen
        name of the tweeter.
        """
        # authenticates Twittery queries
        self.auth = tweepy.OAuthHandler(Twitter_API_Key, Twitter_API_Secret)
        self.auth.set_access_token(Twitter_Token, Twitter_Token_Secret)
        self.twitter_api = tweepy.API(self.auth)
        local_tweets = (self.twitter_api.search(geocode='{0},{1},{2}mi'.format(
                        self.latitude, self.longitude, self.miles)))
        lst_local_tweets = []
        # Assembles all of the search results into a list of tweets in the form of
        # "Username: Tweet". Tweets are comprised of 'fields' (tweet, username,
        # shared links, hashtag, etc. For example, tweet.text returns the 'text'
        # field of the tweet, tweet.user.screen_name returns the screen name of the
        # tweeter.
        for tweet in local_tweets:
            lst_local_tweets.append(tweet)
        return lst_local_tweets


    def get_twitter_topics(self):
        self.auth = tweepy.OAuthHandler(Twitter_API_Key, Twitter_API_Secret)
        self.auth.set_access_token(Twitter_Token, Twitter_Token_Secret)
        self.twitter_api = tweepy.API(self.auth)
        trending_woeid = (self.twitter_api.trends_closest(self.latitude,self.longitude))
        lst_trending_woeid = []
        for i in range(len(trending_woeid)):
            lst_trending_woeid.append(trending_woeid[i]['woeid'])

        lst_trending_topics = []
        for i in range(len(lst_trending_woeid)):
            trending_topics = (self.twitter_api.trends_place(lst_trending_woeid[i]))
            for i in range(len(trending_topics)):
                trending_topics_2 = trending_topics[i]
                for i in range(len(trending_topics_2)):
                    lst_trending_topics.append(trending_topics_2['trends'][i]['name'])
        return lst_trending_topics


    def get_instagram(self):
        """
        Queries latitude, longitude coordinates from Google Maps API using an
        address
        """

        # established link to Instagram using client ID and client secret
        instagram_api = InstagramAPI(client_id=Insta_Client_ID,
                                     client_secret=Insta_Client_Secret)
        # converts user's miles radius input into km
        dist_meters = str(float(self.miles) * 1.60934)
        # queries instagram images using Instagram API with geographic param
        # latitude and longitude as floats, and radius as a string
        local_media = instagram_api.media_search(count=20,
                                                 lat=self.latitude,
                                                 lng=self.longitude,
                                                 distance=dist_meters + "km")

        # appends list of image links to 'photos' list. The image links are to
        # 'standard resolution' versions of images, not thumbnails.
        photos = []
        for media in local_media:
            photos.append(media.images['low_resolution'].url)
        return photos


    def get_four_square_trending(self):
        # Construct the client object
        client = foursquare.Foursquare(client_id=FrSquare_Client_ID,
                                       client_secret=FrSquare_Client_Secret)
        # converts user's miles radius input into meters
        dist_meters = str(float(self.miles) * 1603.34)
        trending_venues = client.venues.trending(params=
                                                 {'ll': str(self.latitude) + ','
                                                        + str(self.longitude),
                                                  'radius': dist_meters})
        places = dict()
        for i in range(len(trending_venues["venues"])):
            places[trending_venues["venues"][i]["name"]] = \
                trending_venues["venues"][i]["hereNow"]["summary"]
        return places


    def get_four_square_explore(self):
        # Construct the client object
        client = foursquare.Foursquare(client_id=FrSquare_Client_ID,
                                       client_secret=FrSquare_Client_Secret)
        # converts user's miles radius input into meters
        dist_meters = str(float(self.miles) * 1603.34)
        explore_venues = client.venues.explore(params=
                                                 {'ll': str(self.latitude) + ','
                                                        + str(self.longitude),
                                                  'radius': dist_meters})
        rating_hereNow = []
        for i in range(len(explore_venues['groups'][0]['items'])):
            try:
                lst_one = []
                lst_one.append(explore_venues['groups'][0]['items'][i]['venue']['rating'])
                lst_one.append(explore_venues['groups'][0]['items'][i]['venue']['hereNow']['summary'])
                rating_hereNow.append(lst_one)
            except:
                continue
        explore_places = dict()
        for i in range(len(explore_venues['groups'][0]['items'])):
            try:
                explore_places[explore_venues['groups'][0]['items'][i]['venue']['name']] = rating_hereNow[i]
            except:
                continue
        return explore_places


    def get_events(self):
        api = eventful.API(Eventful_Key)
        eventful_events = api.call('/events/search', location=(str(self.latitude) + ','
                                                        + str(self.longitude)),
                                   within=self.miles)

        network = pylast.pylast.LastFMNetwork(api_key = Last_fm_Key,
                                              api_secret = Last_fm_Secret)
        lastfm_events = network.get_geo_events(longitude= self.longitude,
                                               latitude = self.latitude,
                                               distance=self.miles)

        lst_events = []

        print eventful_events['events']['event']
        if isinstance(eventful_events['events']['event'], list):
            for event in eventful_events['events']['event']:
                tmp_event = []
                tmp_event.append(event['title'])
                tmp_event.append(event['venue_name'])
                tmp_event.append(event['start_time'])
                tmp_event.append(event['url'])
                lst_events.append(tmp_event)

        elif isinstance(eventful_events['events']['event'], dict):
            tmp_event = []
            tmp_event.append(eventful_events['events']['event']['title'])
            tmp_event.append(eventful_events['events']['event']['venue_name'])
            tmp_event.append(eventful_events['events']['event']['start_time'])
            tmp_event.append(eventful_events['events']['event']['url'])
            lst_events.append(tmp_event)

        for i in range(len(lastfm_events)):
            tmp_event = []
            tmp_event.append(lastfm_events[i][1])
            tmp_event.append(lastfm_events[i][2])
            tmp_event.append(lastfm_events[i][3])
            tmp_event.append(lastfm_events[i][4])
            lst_events.append(tmp_event)

        return lst_events

# x = GlocalAPI("1500 Massachusetts AVe NW", "washington","dc","2" )
# x.get_events()
# y = GlocalAPI("","Sanaa","Yemen","10")
# y.get_events()