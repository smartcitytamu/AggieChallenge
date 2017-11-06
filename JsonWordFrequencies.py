import sys
import json
from nltk.tokenize import word_tokenize
import re
import itertools
import operator
from nltk.corpus import stopwords
import string
import PIL

#PUNCTUATION = list(string.punctuation)
#STOP = (stopwords.words('english') + PUNCTUATION + ['rt', 'via'])
'''for each in STOP:
   each = each.encode('utf-8')
    STOP.append(each)'''


stop = stopwords.words('english')
newstop = []
for each in stop:
    try:
        each = each.encode('utf-8')
        newstop.append(each)
    except:
        continue
stop  = newstop

def load_tweets(filename):
	tweets_file = open(filename)
	tweets = []
	for tweet in tweets_file:
		json_tweet = json.loads(tweet)
		if "text" in json_tweet.keys():
			text = json_tweet["text"].encode('utf-8')
			tweets.append(text)
	return tweets
def clean_tweet(tweet):
    cleaned_tweet = []
    for word in tweet:
        word = word.lower()
        word = re.sub('[!@?#$/()1234567890:.,-]', '', word)
        try:
            if word and len(word)>2 and (word not in stop)  :
                cleaned_tweet.append(word)
        except(UnicodeWarning):
            continue

    return cleaned_tweet

tweets = load_tweets("C:\Users\Sriram\Desktop\Twitter\data1218.json")
unique_words = {}
for tweet in tweets:
    try:
        tweet = word_tokenize(tweet)
        cleaned_tweet = clean_tweet(tweet)
    except:
        continue
    for word in cleaned_tweet:
        try:
            if word in unique_words.keys():
                unique_words[word] = unique_words[word] + 1
            else:
                unique_words[word] = 1;
                unique_word
        except:
            continue
final_dict = sorted(unique_words.items(), key = operator.itemgetter(1), reverse = True)
final_dict = final_dict[:40]
import json
with open("C:\Users\Sriram\Desktop\Twitter\pesult.json", 'w') as fp:
    json.dump(dict(final_dict), fp)