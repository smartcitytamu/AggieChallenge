from flask import Flask, render_template, request, json, jsonify
from bson.json_util import dumps
import tweetCrawler
import json
from nltk.tokenize import word_tokenize
import re
import operator
from nltk.corpus import stopwords
import JsonWordFrequencies
import pymongo

global latestTweetId, connected

myTweets=[]

app = Flask(__name__)
connected = False


stop = stopwords.words('english')
newstop = []
for each in stop:
    try:
        newstop.append(each)
    except:
        continue
stop = newstop

client = pymongo.MongoClient("mongodb://TAMU:aggie123@weatherdata-shard-00-00-vhgp9.mongodb.net:27017,weatherdata-shard-00-01-vhgp9.mongodb.net:27017,weatherdata-shard-00-02-vhgp9.mongodb.net:27017/test?ssl=true&replicaSet=WeatherData-shard-0&authSource=admin")
db = client["WeatherData"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/openTweetConnection.js")
def openTweetConnection():
    global latestTweetId, connected
    NElat = float(request.args.get('NElat'))
    NElng = float(request.args.get('NElng'))
    SWlat = float(request.args.get('SWlat'))
    SWlng = float(request.args.get('SWlng'))
    tweetCrawler.connectMongo()
    # tweetCrawler.startListener(NElat, NElng, SWlat, SWlng)
    connected = True
    latestTweetId = 0
    return 'Success'

"""
@app.route("/updateTweetConnection.js")
def updateTweetConnection():
    global latestTweetId, connected
    NElat = float(request.args.get('NElat'))
    NElng = float(request.args.get('NElng'))
    SWlat = float(request.args.get('SWlat'))
    SWlng = float(request.args.get('SWlng'))
    tweetStream.updateListener(NElat, NElng, SWlat, SWlng)
    return 'Success'
"""

@app.route("/querybox.json")
def querybox():
    NElat = float(request.args.get('NElat'))
    NElng = float(request.args.get('NElng'))
    SWlat = float(request.args.get('SWlat'))
    SWlng = float(request.args.get('SWlng'))
    queryback = db.testTrial3.find({'coordinates': {"$geoWithin": {"$box": [[SWlng,SWlat],[NElng,NElat]]}}})

    res = dumps(queryback)

    res2 = json.loads(res)
    myTweets.extend(res2)
    return res

@app.route("/tweets.json")
def tweets():
    global latestTweetId, connected
    new_tweets = []
    if(connected):
        new_tweets = tweetCrawler.tweets.find({"id" : {"$gt": latestTweetId}})
        orderedTweets = tweetCrawler.tweets.find().sort([("id", -1)]).limit(1)
        # updated latest tweet id
        for tweet in orderedTweets:
            latestTweetId = int(tweet["id"])

        # get sentiment
        #if(new_tweets != []):
        #    new_tweets = microsoftSentiment.getTweetSentiment(new_tweets)

        json = dumps(new_tweets)
        if(json != []):
            print(json)
            print(latestTweetId)

    return json

def load_tweets(filename):
    tweets_file = open(filename,'r')
    tweets = []
    for tweet in tweets_file:
        json_tweet = json.loads(tweet)
        if "text" in json_tweet.keys():
            text = json_tweet["text"]
            tweets.append(text)
    return tweets


def load_tweets_from_list(input):
    tweets = []
    for tweet in input:
        if "text" in tweet.keys():
            text = tweet["text"]
            tweets.append(text)
    return tweets

def clean_tweet(tweet):
    cleaned = []
    for word in tweet:
        word = word.lower()
        word = re.sub('[!@?#$/()1234567890:.,-]', '', word)
        try:
            if word and len(word) > 2 and (word not in stop):
                cleaned.append(word)
        except(UnicodeWarning):
            continue

    return cleaned

#tweetsx=load_tweets("static/data1218.json")
#print(tweetsx)
@app.route("/WordFrequency.json")
def WordFrequencies():
    print("wordfreq")
    unique_words = {}

    tweetsx=load_tweets_from_list(myTweets)

    for tweet in tweetsx:
        tweet = word_tokenize(tweet)
        cleaned_tweet = clean_tweet(tweet)
        for word in cleaned_tweet:
            try:
                if word in unique_words.keys():
                    unique_words[word] = unique_words[word] + 1
                else:
                    unique_words[word] = 1;

            except:
                continue
    final_dictx = sorted(unique_words.items(), key = operator.itemgetter(1), reverse = True)
    final_dictx = final_dictx[:40]
    print(final_dictx)
    return json.dumps(final_dictx)

if __name__ == "__main__":
    app.run()