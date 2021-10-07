import pymongo
import json
import tweepy
import twitter
import re
import urllib.parse

#Extract Engine
CONSUMER_KEY      = ""
CONSUMER_SECRET   = ""
OAUTH_TOKEN       = ""
OATH_TOKEN_SECRET = ""

rest_auth = twitter.oauth.OAuth(OAUTH_TOKEN,OATH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
rest_api = twitter.Twitter(auth=rest_auth)

count = 100
q = [["covid"],["emergency"],["immune"],["vaccine"],["flu"],["snow"],["covid","emergency"],["covid","immune"],["covid","vaccine"],["covid","flu"],["covid","snow"],["emergency","immune"],["emergency","vaccine"],
     ["emergency","flu"],["emergency","snow"],["immune","vaccine"],["immune","flu"],["immune","snow"],["vaccine","flu"],["vaccine","snow"],["flu","snow"],["covid","emergency","immune"],["covid","emergency","vaccine"],
     ["covid","emergency","flu"],["covid","emergency","snow"],["covid","immune","vaccine"],["covid","immune","flu"],["covid","immune","snow"],["covid","vaccine","flu"],["covid","vaccine","snow"],["covid","flu","snow"],["flu","snow","emergency"]]
all_tweets = []
total_text = ""

for topic in q:
    search_results = rest_api.search.tweets( count=count,q=topic)
    for tweets in search_results["statuses"]:
        all_tweets.append(tweets)

counter = 0
file_name_counter = 0;
hundered_tweets = []


#Filter Engine

password = urllib.parse.quote_plus('')

client = pymongo.MongoClient("mongodb+srv://<user-name>:%s@cluster5408.i4cl2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" % (password))

db = client["myMongoTweet"]

col = db["tweets"]

col.create_index([("id",pymongo.ASCENDING)],unique=True)

for indi_tweets in all_tweets:
    counter = counter+1
    if(counter % 100 == 0):
        file_name_counter = file_name_counter +1
        col.insert_many(hundered_tweets)
        hundered_tweets = []
    else:
        indi_tweets["text"] = re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', '', indi_tweets["text"])
        hundered_tweets.append(indi_tweets)

