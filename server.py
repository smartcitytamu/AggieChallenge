from flask import Flask, render_template, request, json, jsonify
from bson.json_util import dumps
import tweetCrawler
import json
from nltk.tokenize import word_tokenize
import re
import operator
from nltk.corpus import stopwords
import JsonWordFrequencies

global latestTweetId, connected

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

tweetsx=load_tweets("static/data1218.json")
print(tweetsx)
@app.route("/WordFrequency.json")
def WordFrequencies():
    print("wordfreq")
    unique_words = {}

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