from flask import Flask, render_template, request, Response
from project import Client, visualize
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import json
import io
import random

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile', methods=['GET','POST'])
def get_profile():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        info = Client(u_name)
        profile = info.get_user_info()
        # response = json.dumps(profile, indent=4)
        return render_template('response.html', dict=profile)

@app.route('/followers', methods=['GET','POST'])
def get_followers():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        info = Client(u_name)
        followers = info.get_followers()
        # response = json.dumps(profile, indent=4)
        return render_template('response.html', list=followers, dict=None)

@app.route('/friends', methods=['GET','POST'])
def get_friends():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        info = Client(u_name)
        friends = info.get_friends()
        # response = json.dumps(profile, indent=4)
        return render_template('response.html', list=friends, dict=None)

@app.route('/likes.png', methods=['GET','POST'])
def plot_likes():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        client = visualize(u_name)
        # fig = create_figure(u_name)
        output = client.visualize_likes()
        # output = io.BytesIO()
        # FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

@app.route('/tweets', methods=['GET','POST'])
def get_tweets():
    if request.method == 'GET':
        return render_template('form.html', keyword=True)
    else:
        # u_name = request.form.get('username')
        keyword = request.form.get('keyword')
        print(keyword)
        client = Client()
        tweets = client.get_tweets_with_keywords(10, keyword)
        # response = json.dumps(profile, indent=4)
        return render_template('response.html', tweets=tweets, dict=None, list=None)
    


@app.route('/retweets.png', methods=['GET','POST'])
def plot_retweets():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        client = visualize(u_name)
        # fig = create_figure(u_name)
        output = client.visualize_retweets()
        # output = io.BytesIO()
        # FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

@app.route('/like-retweets.png', methods=['GET','POST'])
def plot_like_retweets():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        client = visualize(u_name)
        # fig = create_figure(u_name)
        output = client.visualize_like_retweets()
        # output = io.BytesIO()
        # FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

@app.route('/sentiment.png', methods=['GET','POST'])
def plot_sentiment():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        u_name = request.form.get('username')
        client = visualize(u_name)
        # fig = create_figure(u_name)
        output = client.visualize_sentiments()
        # output = io.BytesIO()
        # FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')


@app.route('/sentiment_keyword.png', methods=['GET','POST'])
def plot_keyword_sentiment():
    if request.method == 'GET':
        return render_template('form.html', keyword=True)
    else:
        # u_name = request.form.get('username')
        keyword = request.form.get('keyword')
        client = visualize(keywords=keyword)
        # fig = create_figure(u_name)
        output = client.visualize_keyword_sentiments()
        # output = io.BytesIO()
        # FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

# @app.route('/plot.png', methods=['GET','POST'])
# def plot_png():
#     if request.method == 'GET':
#         return render_template('form.html')
#     else:
#         u_name = request.form.get('username')
#         client = visualize(u_name)
#         # fig = create_figure(u_name)
#         fig = client.visualize_likes()
#         output = io.BytesIO()
#         FigureCanvas(fig).print_png(output)
        # return Response(output.getvalue(), mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)