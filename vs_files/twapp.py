##########################################################################################
################################### Importing Packages ####################################
##########################################################################################

from flask import Flask, render_template, request, Response
from project import Client, Visualize
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import json
import io
import random
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def home():
    '''
    Home Page
    '''
    return render_template('home.html')


@app.route('/profile', methods=['GET','POST'])
def get_profile():
    '''
    Profile Info
    '''
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        info = Client(u_name)
        profile = info.get_user_info()
        return render_template('response.html', dict=profile)

@app.route('/followers', methods=['GET','POST'])
def get_followers():
    '''
    Information about followers
    '''
    if request.method == 'GET':
        return render_template('form.html', maxmin=True)
    else:
        u_name = request.form.get('username')
        minfollowers = int(request.form.get('minfollowers'))
        minfriends = int(request.form.get('minfriends'))
        info = Client(u_name)
        followers = info.get_followers(minfollower=minfollowers, minfriend=minfriends)
        return render_template('response.html', list=followers, dict=None)

@app.route('/friends', methods=['GET','POST'])
def get_friends():
    '''
    Information about friends
    '''
    if request.method == 'GET':
        return render_template('form.html', maxmin=True)
    else:
        u_name = request.form.get('username')
        minfollowers = int(request.form.get('minfollowers'))
        minfriends = int(request.form.get('minfriends'))
        info = Client(u_name)
        friends = info.get_friends(minfollower=minfollowers, minfriend=minfriends)
        return render_template('response.html', list=friends, dict=None)

@app.route('/tweets', methods=['GET','POST'])
def get_tweets():
    '''
    Fetch tweets from timeline
    '''
    if request.method == 'GET':
        return render_template('form.html',nummin=True)
    else:
        numtweets = request.form.get('numtweets')
        minlikes = request.form.get('minlikes')
        client = Client()
        tweets = client.get_timeline_tweets(num_tweets=numtweets, min_likes=minlikes)
        return render_template('response.html', tweets=tweets, dict=None, list=None)

@app.route('/tweet_timeline.png', methods=['GET','POST'])
def plot_tweet_timeline():
    '''
    Plot data about tweets from timeline
    '''
    if request.method == 'GET':
        return render_template('form.html',nummin=True)
    else:
        numtweets = request.form.get('numtweets')
        minlikes = request.form.get('minlikes')
        viz = Visualize()
        output = viz.visualize_timeline_tweets(num_tweets=numtweets, min_likes=minlikes)
        return Response(output.getvalue(), mimetype='image/png')


@app.route('/tweets_with_keyword', methods=['GET','POST'])
def get_tweets_with_keyword():
    '''
    Fetch tweets with certain keywords
    '''
    if request.method == 'GET':
        return render_template('form.html', keyword=True)
    else:
        keyword = request.form.get('keyword')
        print(keyword)
        client = Client()
        tweets = client.get_tweets_with_keywords(10, keyword)
        return render_template('response.html', tweets=tweets, dict=None, list=None)
    

@app.route('/likes.png', methods=['GET','POST'])
def plot_likes():
    '''
    Plot Likes on tweets of home page
    '''
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        client = Visualize(username=u_name)
        output = client.visualize_likes()
        return Response(output.getvalue(), mimetype='image/png')


@app.route('/retweets.png', methods=['GET','POST'])
def plot_retweets():
    '''
    Plot Retweets on tweets of home page
    '''
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        client = Visualize(username=u_name)
        output = client.visualize_retweets()
        return Response(output.getvalue(), mimetype='image/png')

@app.route('/like-retweets.png', methods=['GET','POST'])
def plot_like_retweets():
    '''
    Plot Likes and retweets on tweets of home page
    '''
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        client = Visualize(username=u_name)
        output = client.visualize_like_retweets()
        return Response(output.getvalue(), mimetype='image/png')

@app.route('/sentiment.png', methods=['GET','POST'])
def plot_sentiment():
    '''
    Plot sentiments on tweets of home page
    '''
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        client = Visualize(username=u_name)
        output = client.visualize_sentiments()
        return Response(output.getvalue(), mimetype='image/png')


@app.route('/sentiment_keyword.png', methods=['GET','POST'])
def plot_keyword_sentiment():
    '''
    Plot Likes on tweets with certain keywords
    '''
    if request.method == 'GET':
        return render_template('form.html', keyword=True)
    else:
        keyword = request.form.get('keyword')
        client = Visualize()
        output = client.visualize_keyword_sentiments(keywords=keyword)
        return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)

##########################################################################################
#################################### Code Ends Here ######################################
##########################################################################################