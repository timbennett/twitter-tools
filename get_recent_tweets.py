'''
export user's last 3240 tweets to CSV (full structure)
usage: python get_recent_tweets.py screenname
requires pandas because why reinvent to_csv()?
'''

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys
import json
import pandas as pd

# make sure twitter_auth.py exists with contents:
#
#   access_key = ""
#   access_secret = ""
#   consumer_key = ""
#   consumer_secret = ""
#

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

alltweets = []
screenname=sys.argv[1]
new_tweets = api.user_timeline(screen_name = screenname,count=200)
alltweets.extend(new_tweets)
oldest = alltweets[-1].id - 1

while len(new_tweets) > 0:
    print "getting tweets before %s" % (oldest)
    
    #all subsiquent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(screen_name = screenname,count=200,max_id=oldest)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    print "...%s tweets downloaded so far" % (len(alltweets))
    
json_strings = json.dumps([tweet._json for tweet in alltweets])
df = pd.read_json(json_strings)
df.to_csv('{}.csv'.format(screenname), encoding='utf-8')

