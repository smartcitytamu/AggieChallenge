import pymongo
import json
from bson.json_util import dumps
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from collections import OrderedDict

#Geoquery
#{coordinates: {$geoWithin: { $centerSphere: [ [ -81.30241655278206, 28.24823404323392 ], 0.009138259359688778 ]}}}

#{coordinates: {$geoWithin: { $box: [ [ -82.30241655278206, 28.24823404323392 ], [-80.30241655278206,29.24823404323392]] }}}
client = pymongo.MongoClient("mongodb://TAMU:aggie123@weatherdata-shard-00-00-vhgp9.mongodb.net:27017,weatherdata-shard-00-01-vhgp9.mongodb.net:27017,weatherdata-shard-00-02-vhgp9.mongodb.net:27017/test?ssl=true&replicaSet=WeatherData-shard-0&authSource=admin")
db = client["WeatherData"]

#Look up things in the bounding box
def querybox(box):
    queryback=db.testTrial3.find({'coordinates': {"$geoWithin": { "$box": box }}})

    res=dumps(queryback)
    res=json.loads(res)
    return res

def queryfilter(keyword):
    queryback=db.testTrail3.find({'text':'/.*'+keyword+'.*/'})
    res=dumps(queryback)
    return res

input=[[-82.30241655278206, 28.24823404323392 ], [-80.30241655278206,29.24823404323392]]
querybox(input)