import tweepy
import json
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from textblob import TextBlob
import io

import re

with open('twitter_config.json') as c:
    params = json.load(c)
    
consumer_key = params["API_KEY"]
consumer_secret = params["APP_SECRET_KEY"]
access_token = params["ACCESS_TOKEN"]
access_token_secret = params["ACCESS_TOKEN_SECRET"]

class Authenticator():
    def authenticate(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

class Client():
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
            'Total Likes by '+first_name: user.favourites_count,
            'Followers': user.followers_count,
            'Friends': user.friends_count,
            'Id': user.id,
            'Location': user.location,
            'Total statuses': user.statuses_count
        }
        return info

    def get_followers(self):
        """Returns the followers of given twitter user"""
        info = []
        for follower in tweepy.Cursor(self.api.followers, screen_name = self.username).items(10):
            username = follower.screen_name
            name = follower.name
            followers = follower.followers_count
            friends = follower.friends_count
            info.append([name, username, followers, friends])
        return info

    def get_friends(self):
        """Returns the friends of given twitter user"""
        info = []
        for friend in tweepy.Cursor(self.api.friends, screen_name = self.username).items(10):
            username = friend.screen_name
            name = friend.name
            followers = friend.followers_count
            friends = friend.friends_count
            info.append([name, username, followers, friends])
        return info

    def get_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in tweepy.Cursor(self.api.home_timeline, screen_name=self.username).items(num_tweets):
            tweets.append(tweet.text)
        return tweets

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in tweepy.Cursor(self.api.user_timeline, id=self.username).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_tweets_with_keywords(self, num_tweets, keywords):
        tweets = []
        query = str(keywords)
        # query = ' '.join(keywords)
        # query = str(query)
        # '#hathras -#shameonuppolice -@narendramodi'
        # print(query)
        for i, status in enumerate(tweepy.Cursor(self.api.search, q=query).items(num_tweets)):
            tweets.append({'s_no':i, 'tweet':status.text, 'author':status.author.screen_name, 'name':status.author.name})
        return tweets

class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.auth = Authenticator().authenticate()

    def stream_tweets(self, filename, tag_list):
        listener = TwitterListener(filename)
        stream = tweepy.Stream(self.auth, listener)

        stream.filter(track=tag_list)

class TwitterListener(TwitterStreamer):
    """
    This prints receaved tweets
    """
    def __init__(self, filename):
        self.filename = filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print(f"Error on_data {e}")
        return True

    def on_error(self, status):
        if status == 420:
            # rate limit
            return False
        print(status)

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
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    

# def create_figure(u_name):
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     info = Client(u_name)
#     friends = info.get_friends()
#     # xs = range(100)
#     # ys = [random.randint(1, 50) for x in xs]
#     axis.bar(friends.name, friends.friends)
#     return fig

# time_likes = pd.Series(data=df['len'].values, index=df['date'])
# time_likes.plot(figsize=(16, 4), color='r')
# plt.show()

class visualize(Client, TweetAnalyzer):
    """
    To visualize the data of tweets
    """
    
    def __init__(self, u_name=None, keywords=None):
        # self.user = Client(u_name)
        self.tweets = Client().api.user_timeline(screen_name=u_name, count=10)
        self.tweets_for_keywords = Client().api.search(q=keywords, count=10)

    # def visualize_likes(self):
    #     fig = Figure()
    #     axis = fig.add_subplot(1,1,1)
    #     df = self.tweets_to_df(self.tweets)
    #     time_likes = pd.Series(data=df['len'].values, index=df['date'])
    #     axis.plot(time_likes, color='r')
    #     plt.xticks(rotation=45)
    #     return fig

    # def visualize_retweets(self):
    #     plt.figure()
    #     plt.plot([1, 2])
    #     plt.title("test")
    #     buf = io.BytesIO()
    #     plt.savefig(buf, format='png')
    #     buf.seek(0)
    #     im = Image.open(buf)
    #     im.show()
    #     buf.close()


    def visualize_likes(self):
        plt.figure(figsize=(20,10))
        df = self.tweets_to_df(self.tweets)
        time_likes = pd.Series(data=df['likes'].values, index=df['date'])
        plt.plot(time_likes, color='r')
        plt.title('test')
        plt.xticks(rotation=25)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def visualize_retweets(self):
        plt.figure(figsize=(20,10))
        df = self.tweets_to_df(self.tweets)
        time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
        plt.plot(time_retweets, color='r')
        plt.title('test')
        plt.xticks(rotation=25)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def visualize_like_retweets(self):
        plt.figure(figsize=(20,10))
        df = self.tweets_to_df(self.tweets)
        time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
        time_likes = pd.Series(data=df['likes'].values, index=df['date'])
        plt.plot(time_retweets, color='b', label='retweets')
        plt.legend()
        plt.plot(time_likes, color='r', label='likes')
        plt.legend()
        plt.title('test')
        plt.xticks(rotation=25)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf


    def visualize_sentiments(self):
        plt.figure(figsize=(20,10))
        df = self.tweets_to_df(self.tweets)
        df['sentiment'] = np.array([self.analyze_sentiment(tweet) for tweet in df['tweets']])
        time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
        plt.hist(time_sentiment, color='r')
        plt.title('test')
        plt.xticks([-1,0,1], labels=['Negative', 'Neutral', 'Positive'])
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def visualize_keyword_sentiments(self):
        plt.figure(figsize=(20,10))
        df = self.tweets_to_df(self.tweets_for_keywords)
        df['sentiment'] = np.array([self.analyze_sentiment(tweet) for tweet in df['tweets']])
        time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
        plt.hist(time_sentiment, color='r')
        plt.title('test')
        plt.xticks([-1,0,1], labels=['Negative', 'Neutral', 'Positive'])
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf




if __name__ == "__main__":
                
    client = Client()
    tweet_analyzer = TweetAnalyzer()

    api = client.api

    tweets = api.user_timeline(screen_name='realDonaldTrump', count=10)

    df = tweet_analyzer.tweets_to_df(tweets)

    # print(np.mean(df['len']))

    # print(df[df['likes'] == np.max(df['likes'])])

    # print( df[df['retweets'] == np.min(df['retweets'])])

    # print(df.head())
    # time_retweets = pd.DataFrame(df[['retweets', 'tweets']].values, index=df['date'])

    # print(time_retweets)
