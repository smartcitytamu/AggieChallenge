import pymongo
import json
from bson.json_util import dumps
from threading import Thread, Lock, Event, get_ident
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from collections import OrderedDict

cstat = ['30.622173', '-96.330113']

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '905569300181897217-OLbHfunt8hjIQVMbvpOr3UJukjAuKip'
ACCESS_SECRET = 'dUu95IEKOntDZDJAi1G7ySYPG1F0rv5B0ZTkDwDbZLTYv'
CONSUMER_KEY = 'K3lNkaZT6VDCWbNRreIrSWP16'
CONSUMER_SECRET = 'UwI07Qrrjv0ZYeL670a7qWY7PGDfW4QuxfK7kiJggDbwE5sHi1'

ACCESS_TOKEN2="926230327101665281-rshloZylCnEsO0wV8y2wIQnPPsrOY3D"
ACCESS_SECRET2="cLJyxC10fCg5qhFqFvWRy8pPSvLNJHb466WCBSpmDVclN"
CONSUMER_KEY2="B0K119FNzQHuGQjZt1L7JhLIA"
CONSUMER_SECRET2="VTJMZ8m5DACLAUnkwHoQA541fglzJQ0WLQW3tlFk6LlzvSsPln"

myfilter=["hurricane","harvey"]
myfilter2=["football"]


oauths = [OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET),OAuth(ACCESS_TOKEN2, ACCESS_SECRET2, CONSUMER_KEY2, CONSUMER_SECRET2)]

client = pymongo.MongoClient("mongodb://TAMU:aggie123@weatherdata-shard-00-00-vhgp9.mongodb.net:27017,weatherdata-shard-00-01-vhgp9.mongodb.net:27017,weatherdata-shard-00-02-vhgp9.mongodb.net:27017/test?ssl=true&replicaSet=WeatherData-shard-0&authSource=admin")
db = client["WeatherData"]
streamDB=db.testTrial3
mentionDB=db.testTrial4


def getLocation(center,range,longbias,latbias):
    SELong = 0
    SELat = 0
    NWLong = 0
    NWLat = 0

    #d = feedparser.parse(stormURL)
    # print(d['entries'][0]['nhc_center'])

    # locs = d['entries'][0]['nhc_center'].split(',')



    # Change these if you want to change the size of the 'box'
    SELong = str(float(center[0].strip()) - range+longbias)
    SELat = str(float(center[1].strip()) - range+latbias)
    NWLong = str(float(center[0].strip()) + range+longbias)
    NWLat = str(float(center[1].strip()) + range+latbias)

    return SELat + ',' + SELong + ',' + NWLat + ',' + NWLong

#The thread class
class MyThread(Thread):
    def __init__(self, crawler, exitEvent,tweets,mutex,db):
        ''' Constructor. '''

        Thread.__init__(self)
        self.crawler=crawler
        self.exit=exitEvent
        self.mutex=mutex
        self.tweets=tweets
        self.db=db

    # todo switch to producer consumer model for uploading
    def run(self):
        for tweet in self.crawler:
            if self.exit.is_set():
                break
            self.mutex.acquire()
            if "id" in tweet.keys() and tweet["id"] not in self.tweets:
                self.tweets[tweet["id"]]=tweet
                self.db.insert_one(tweet)
                #if "text" in tweet.keys():
                #    print(str(get_ident()) + " " + str(len(self.tweets)) + " " + tweet["text"])
            self.mutex.release()
        pass

#The thread function
def crawlFunc(thread,crawler,tweets,event,mutex):
    for tweet in crawler:
        mutex.acquire()
        if event.is_set():
            thread.exit()
        tweets.append(tweet)
        mutex.release()
    pass

class tweetCrawler:
    def __init__(self,oauths):
        self.oauths=oauths
        self.tweets=OrderedDict()
        #self.twitterStream = TwitterStream(auth=oauth)
        self.crawler=None
        self.curIndex=0
        self.crawlStop=[]
        self.mutex=Lock()
        self.thread=None
        self.threads=[]
        self.filters=[]
        pass

    def addCrawl(self,box=None,filter=None,db=None):
    # creates and runs a new crawler
    # box is comma separated string with twitter form
    # filter is an array of words used to generate a twitter filter for those words
    # gives tweets that are in box OR pass filter
        if (box!=None or filter!=None) and (len(self.threads)<len(self.oauths)):
            tempEvent=Event()
            self.crawlStop.append(tempEvent)
            self.filters.append(filter)
            tempOauth=self.oauths.pop(0)
            tempCrawler=None
            if box==None and filter!=None:
                tempCrawler = TwitterStream(auth=tempOauth).statuses.filter(track=",".join(filter))
            elif filter==None and box!=None:
                tempCrawler = TwitterStream(auth=tempOauth).statuses.filter(locations=box)
            elif filter!=None and box!=None:
                tempCrawler = TwitterStream(auth=tempOauth).statuses.filter(locations=box, track=",".join(filter))
            self.threads.append(MyThread(tempCrawler,tempEvent,self.tweets,self.mutex,db))
            self.threads[len(self.threads)-1].start()
            self.oauths.append(tempOauth)
        pass

    # stops the i-th crawler
    def stopCrawl(self,i):
        self.crawlStop[i].set()

    # updates the box of i-th crawler
    # box is comma separated string with twitter form
    def updateBox(self, box,i):
        #for i in range(len(self.threads)):
        self.stopCrawl(i)
        self.crawlStop[i].clear()
        self.addCrawl(box,self.filters[i],streamDB)
        pass

    def readTweets(self,container):
        self.mutex.acquire()
        if(self.curIndex<len(self.tweets)-1):
            container=self.tweets[self.curIndex:]
            self.curIndex=len(self.tweets)-1
        self.mutex.release()
        return self.curIndex

    pass

crawler=tweetCrawler(oauths)
container=[]

crawler.addCrawl(getLocation(cstat,0.5,0.0,0.0),None,streamDB)
#crawler.addCrawl(getLocation(cstat,0.5,0.0,10.0),None,streamDB)
crawler.addCrawl(None,["@smartcitytamu"],mentionDB)

#crawler.addCrawl(None,myfilter)
#crawler.addCrawl(None,myfilter2)
#time.sleep(30)
#crawler.updateBox(getLocation(cstat,0.5,5.0,1.0),1)