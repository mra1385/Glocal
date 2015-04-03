from Glocal.API import API
import unittest

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.st_address = "1500 Massachusetts Ave NW"
        self.city = "Washington"
        self.state = "DC"
        self.user_query = API.GlocalAPI(self.st_address,self.city, self.state)
        self.latitude, self.longitude = self.user_query.get_coordinates()

    def test_get_coordinates(self):
        self.assertEqual((self.latitude,self.longitude),
                         (38.9064936, -77.03541179999999))

    def test_get_tweets(self):
        self.assertIsNotNone(self.user_query.get_twitter())

    def test2_local_tweets(self):
        self.assertTrue(len(self.user_query.get_twitter()) > 1)

    def test_get_instagram(self):
        self.assertIsNotNone(self.user_query.get_instagram())

    def test2_get_instagram(self):
        self.assertTrue(len(self.user_query.get_instagram()) > 1)

## Add unittests for other GlocalAPI class methods ##

if __name__ == '__main__':
    unittest.main()
