import json
import tweepy

with open("learning/twitter_config.json") as p:
    params = json.load(p)

consumer_key = params["API_KEY"]
consumer_secret = params["APP_SECRET_KEY"]
access_token = params["ACCESS_TOKEN"]
access_token_secret = params["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)