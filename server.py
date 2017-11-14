from flask import Flask, render_template, request, json, jsonify
from bson.json_util import dumps
import tweetCrawler

global latestTweetId, connected

app = Flask(__name__)
connected = False

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

if __name__ == "__main__":
    app.run()