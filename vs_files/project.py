##########################################################################################
################################### Importing Packages ####################################
##########################################################################################
import tweepy
import json
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from textblob import TextBlob
import io

import re

##########################################################################################
################################# Load configuration file #################################
##########################################################################################


with open('twitter_config.json') as c:
    params = json.load(c)
    
consumer_key = params["API_KEY"]
consumer_secret = params["APP_SECRET_KEY"]
access_token = params["ACCESS_TOKEN"]
access_token_secret = params["ACCESS_TOKEN_SECRET"]

class Authenticator():
    '''
    To authenticate the access to twitter
    '''
    def authenticate(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

class Client():
    '''
    A class to fetch data from twitter
    '''
    def __init__(self, username=None):
        self.auth = Authenticator().authenticate()
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.username = username

    
    def get_user_info(self):
        """Returns the information of given twitter user"""
        user = self.api.get_user(self.username)
        first_name, *_ = user.name.split(" ")
        info = {
            'Name': user.name,
            'Description': user.description,
            'Created_at': user.created_at.strftime("%d %b, %Y, %H:%M:%S"),
            f'Total Likes by {first_name}': user.favourites_count,
            'Followers': user.followers_count,
            'Friends': user.friends_count,
            'Id': user.id,
            'Location': user.location,
            'Total statuses': user.statuses_count
        }
        return info


    def get_followers(self, minfollower=50, minfriend=50):
        """Returns the followers of given twitter user"""
        info = []
        def process_page(page_results):
            for follower in page_results:
                if follower.followers_count > minfollower and follower.friends_count > minfriend:
                    username = follower.screen_name
                    name = follower.name
                    followers = follower.followers_count
                    friends = follower.friends_count
                    info.append([name, username, followers, friends])
            return info                    
        for i, page in enumerate(tweepy.Cursor(self.api.followers, screen_name=self.username, per_page=5).pages(3)):
            print(i, "page")
            process_page(page)
        return info

    def get_friends(self, minfollower=50, minfriend=50):
        """Returns the friends of given twitter user"""
        info = []
        def process_page(page_results):
            for friend in page_results:
                if friend.followers_count > minfollower and friend.friends_count > minfriend:
                    username = friend.screen_name
                    name = friend.name
                    followers = friend.followers_count
                    friends = friend.friends_count
                    info.append([name, username, followers, friends])
            return info                    
        for i, page in enumerate(tweepy.Cursor(self.api.followers, screen_name=self.username, per_page=5).pages(3)):
            print(i, "page")
            process_page(page)
        return info

    def get_timeline_tweets(self, num_tweets=10, min_likes=100):
        '''Returns tweets from user's timeline'''
        num_tweets = int(num_tweets)
        min_likes = int(min_likes)
        info = []
        num_page = int(num_tweets/5)
        def process_page(page_results):
            i = 1
            for tweet in page_results:
                if tweet.favorite_count > min_likes:
                    info.append({'s.no.':i ,'tweet':tweet.text, 'author':tweet.author.screen_name, 'name':tweet.author.name, 'likes':tweet.favorite_count})
                    i += 1
            return info                    
        for i, page in enumerate(tweepy.Cursor(self.api.home_timeline, screen_name=self.username, count=5).pages(num_page)):
            print(i, "page")
            process_page(page)
        return info
    
    def get_tweets_with_keywords(self, num_tweets, keywords):
        '''Fetch tweets related to keywords'''
        tweets = []
        query = str(keywords)
        for i, status in enumerate(tweepy.Cursor(self.api.search, q=query).items(num_tweets)):
            tweets.append({'s_no':i, 'tweet':status.text, 'author':status.author.screen_name, 'name':status.author.name})
        return tweets

class TweetAnalyzer():
    """
    Analyzing and categorizing content from tweets
    """
    def tweets_to_df(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


    def clean_tweet(self, tweet):
        '''Cleaning the fetched tweets'''
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        '''Analyse the sentiments of fetched tweets'''
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1



class Visualize(Client,TweetAnalyzer):
    '''
    To visualize the data by plots
    '''        

    def get_tweet_df(self):
        '''Create dataframe of tweets to plot'''
        tweets = self.api.user_timeline(screen_name=self.username, count=10)
        df = self.tweets_to_df(tweets)
        return df

    def tweets_for_keywords(self, keywords):
        '''Dataframe of tweets related to keywords'''
        query = str(keywords)
        tweets_for_keywords = self.api.search(q=query, count=10)
        return tweets_for_keywords



    def visualize_likes(self):
        '''
        Plot likes on the fetched tweets
        '''
        plt.figure(figsize=(20,10))
        df = self.get_tweet_df()
        time_likes = pd.Series(data=df['likes'].values, index=df['date'])
        plt.plot(time_likes, color='r')
        plt.title('Visualizing Likes')
        plt.xticks(rotation=25)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def visualize_retweets(self):
        '''
        Plot retweets on fetched tweets
        '''
        plt.figure(figsize=(20,10))
        df = self.get_tweet_df()
        time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
        plt.plot(time_retweets, color='r')
        plt.title('Visualizing Retweets')
        plt.xticks(rotation=25)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def visualize_like_retweets(self):
        '''
        Plot likes and retweets on fetched tweets
        '''
        plt.figure(figsize=(20,10))
        df = self.get_tweet_df()
        time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
        time_likes = pd.Series(data=df['likes'].values, index=df['date'])
        plt.plot(time_retweets, color='b', label='retweets')
        plt.legend()
        plt.plot(time_likes, color='r', label='likes')
        plt.legend()
        plt.title('Visualize Likes and Retweets')
        plt.xticks(rotation=25)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf


    def visualize_sentiments(self):
        '''
        Plot sentiments on fetched tweets
        '''
        plt.figure(figsize=(20,10))
        df = self.get_tweet_df()
        df['sentiment'] = np.array([self.analyze_sentiment(tweet) for tweet in df['tweets']])
        time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
        plt.hist(time_sentiment, color='r')
        plt.title('test')
        plt.xticks([-1,0,1], labels=['Negative', 'Neutral', 'Positive'])
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def visualize_keyword_sentiments(self, keywords):
        '''
        Plot sentiments on tweets related to given keywords
        '''
        plt.figure(figsize=(20,10))
        df = self.tweets_to_df(self.tweets_for_keywords(keywords=keywords))
        df['sentiment'] = np.array([self.analyze_sentiment(tweet) for tweet in df['tweets']])
        time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
        plt.hist(time_sentiment, color='r')
        plt.title('test')
        plt.xticks([-1,0,1], labels=['Negative', 'Neutral', 'Positive'])
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf


##########################################################################################
################################### Code Ends Here ######################################
##########################################################################################