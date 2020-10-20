from project import (Client,
                    TweetAnalyzer,
                    visualize)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# info = Client('ajeetsparmar')
# friends, _ = info.get_timeline_tweets(2)
# print(friends)

client = Client()
tweet_analyzer = TweetAnalyzer()

api = client.api

# tweets = api.user_timeline(screen_name='realDonaldTrump', count=10)

# df = tweet_analyzer.tweets_to_df(tweets)

# ct = tweet_analyzer.clean_tweet(tweets)
# print(ct)
keyword = input('Enter')
tweet = client.get_tweets_with_keywords(10, keyword)
print(tweet)
# dir(api.search)

# print(np.mean(df['len']))

# print(df[df['likes'] == np.max(df['likes'])])

# print( df[df['retweets'] == np.min(df['retweets'])])

# print(df.head())

# # Time Series
# time_likes = pd.Series(data=df['len'].values, index=df['date'])
# time_likes.plot(figsize=(16, 4), color='r')
# plt.show()

# time_favs = pd.Series(data=df['likes'].values, index=df['date'])
# time_favs.plot(figsize=(16, 4), color='r')
# plt.show()


# time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
# time_retweets.plot(figsize=(16, 4), color='r')
# plt.show()


# # Layered Time Series:
# time_likes = pd.Series(data=df['likes'].values, index=df['date'])
# time_likes.plot(figsize=(16, 4), label="likes", legend=True)

# time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
# time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
# plt.show()

# df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

# print(df.head())

# info = visualize('ajeetsparmar')
# fig = info.visualize_likes()
# plt.show()