import tweepy
import pymongo
import ssl
import json
from threading import Thread

global tweets

# Twitter connection
ACCESS_TOKEN = os.environ['Twitter_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['Twitter_ACCESS_SECRET']
CONSUMER_KEY = os.environ['Twitter_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['Twitter_CONSUMER_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def connectMongo():
    global tweets
    # pymongo connection
    client = pymongo.MongoClient(
        os.environ['MONGODB_ENDPOINT'],
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE)

    db = client["Cluster0"]
    tweets = db['test']  # TODO handle sessions by making new collection

class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        global tweets
        tweet_json = json.loads(data)
        print("Tweet :" + str(tweet_json))
        tweets.insert_one(tweet_json)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())

def startListener(NElat, NElng, SWlat, SWlng):
    print('Tweet Crawler connected to mongo')
    thread = Thread(target = updateListener, args = (NElat, NElng, SWlat, SWlng))
    thread.start()

def updateListener(NElat, NElng, SWlat, SWlng):
    myStream.filter(locations=[SWlng, SWlat, NElng, NElat])

