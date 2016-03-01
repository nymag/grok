from app import app
from flask import render_template, make_response
from pymongo import MongoClient
from textblob import TextBlob
from analysis import get_article_entry, get_article_title
from analytics import get_service, get_results
from datetime import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from io import BytesIO

client = MongoClient('mongo01.prd.nymetro.com', 27017)
db = client.articles
articles = db.articles

#Articles with google analytics pageviews
analytics_result = {}
#Articles expressing positive and/or negative sentiment
sentiment_result = {}
#Articles expressing positive and/or negative sentiment against pageviews
result = {}


@app.route('/')
@app.route('/index')
def sentiment():
    index()
    analytics()
    for d in sentiment_result, analytics_result:
        for k, v in d.items():
            result.setdefault(k, []).append(v)

    return render_template('index.html', result=result)


@app.route("/articles/sentiment.png")
def positive_sentiment_graph():
    sentiment()
    # Create a new dict with items that have two values for xaxis and yaxis data points
    items = {k: v for k, v in result.items() if len(v) == 2}
    fig = Figure((10, 10))
    plt = fig.add_subplot(1, 1, 1)
    # Generate data points from xaxis and yaxis values
    x = [item[1] for item in items.values()]
    y = [item[0] for item in items.values()]
    N = len(x)
    colors = np.random.rand(N)
    area = np.pi * (15 * np.random.rand(N))**2
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    vals = plt.get_yticks()
    plt.yaxis.set_major_formatter(
        FuncFormatter(lambda y, pos: ('{0:.2f}'.format(y*1)).rstrip('0').rstrip('.')+'%'))
    plt.set_ylim(ymin=1)
    plt.set_xlim(xmin=0)
    plt.set_xlabel('Pageviews', fontsize=14)
    plt.set_ylabel('Positive Sentiment', fontsize=14)
    fig.suptitle('New York Magazine: January 2016 Articles', fontsize=18)
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/articles/analytics')
def analytics():
    # Define the auth scopes to request
    scope = ['https://www.googleapis.com/auth/analytics.readonly']
    # Authenticate and construct service
    service = get_service('analytics', 'v3', scope, 'client_secrets.json')
    profile_id = '107545746'
    analytics_items = get_results(service, profile_id)
    analytics_article_count = analytics_items.get('totalResults')
    rows = analytics_items.get('rows')
    # Clean up analytics keys so they match sentiment dict keys
    for title, pageviews in rows:
        remove = (-len('-- Vulture') - 1)
        title = title[:remove]
        analytics_result.update({title: pageviews})

    return render_template('analytics.html', analytics_result=analytics_result, analytics_article_count=analytics_article_count)


@app.route('/articles/sentiment')
def index():
    # Adjust date based on analytics timeframe so count matches
    start = datetime(2016, 1, 1)
    end = datetime(2016, 2, 1)
    query = {'status': 'published', 'blogName': 'Vulture', 'publishDate': {'$gte': start, '$lt': end}}
    entry_query = {'body.entry': 1, 'shorterHeadline': 1}
    # Adjust limit based on analytics limit so count matches
    limit = 1062
    article_entries = articles.find(query, entry_query).limit(limit)
    article_count = articles.find(query).count()
    items = [[get_article_entry(item), get_article_title(item)] for item in article_entries]
    for body, title in items:
        body = TextBlob(body)

        if len(body.sentences) > 0:
            polarity_of_each_sentence = [sentence.sentiment.polarity for sentence in body.sentences]

            average_polarity = sum(polarity_of_each_sentence) / len(body.sentences)
            average_polarity *= 100

        if average_polarity > 0:
            sentiment = '{}'.format(abs(round(average_polarity, 0)))
        #elif average_polarity < 0:
            #sentiment = 'negative ({}% sure)'.format(abs(round(average_polarity, 0)))

            sentiment_result.update({title: sentiment})

    return render_template('sentiment.html', sentiment_result=sentiment_result, article_count=article_count, limit=limit)
