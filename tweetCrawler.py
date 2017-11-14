import tweepy
import pymongo
import ssl
import json
from threading import Thread

global tweets

# Twitter connection
consumer_key = 'CaWuX5AD3IYqWAVAVi4dwY2ra'
consumer_secret = 'BC2ZpQd4bkBAYun5DR2qxUYtKqijXjVVEzn3ElXw9QU3CMPuVb'
access_token = '4839087855-bDPiFAbK3fViPSg6JaTt5w1GFSAxyO2bT81kcOt'
access_token_secret = 'qqTxlQZldRheCc05H4eoxZwMBTbm3TNUwYgkrekw9okUf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def connectMongo():
    global tweets
    # pymongo connection
    client = pymongo.MongoClient(
        "mongodb://HackTX:hacktxalluppercase@cluster0-shard-00-00-f137z.mongodb.net:27017," +
        "cluster0-shard-00-01-f137z.mongodb.net:27017,cluster0-shard-00-02-f137z.mongodb.net:27017" +
        "/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin",
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

