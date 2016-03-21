from app import app
from flask import render_template, make_response
from pymongo import MongoClient
from textblob import TextBlob
import numpy as np
from io import BytesIO
from datetime import datetime

from analysis import get_article_date, get_article_title
from analytics import get_service, get_results

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


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
    print(result)

    return render_template('index.html', result=result)


@app.route("/articles/duration.png")
def positive_sentiment_graph():
    sentiment()
    # Create a new dict with items that have two values for xaxis and yaxis data points
    items = {k: v for k, v in result.items() if len(v) == 2}
    fig = Figure((40, 30))
    plt = fig.add_subplot(1, 1, 1)
    # Generate data points from xaxis and yaxis values
    x = [item[0] for item in items.values()]
    y = [item[1] for item in items.values()]
    N = len(x)
    colors = np.random.rand(N)
    area = np.pi * (15)**2
    plt.scatter(x, y, s=area, alpha=0.5)
    vals = plt.get_yticks()
    plt.set_ylim(ymin=1, ymax=10000)
    plt.set_xlim(xmin=0, xmax=31)
    plt.tick_params(axis='both', labelsize=20)
    plt.set_xlabel('Publish Date (Day)', fontsize=25)
    plt.set_ylabel('Pageviews', fontsize=25)
    fig.suptitle('New York Magazine: January 2016 \n Total Articles: {0}'.format(len(items)), fontsize=30)
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


@app.route('/articles/query')
def index():
    # Adjust date based on analytics timeframe so count matches
    query = {'status': 'published', 'blogName': 'Vulture'}
    entry_query = {'body.entry': 1, 'shorterHeadline': 1, 'publishDate': 1}
    # Adjust limit based on analytics limit so count matches
    limit = 5000
    article_entries = articles.find(query, entry_query).limit(limit)
    article_count = articles.find(query).count()
    items = [[get_article_date(item), get_article_title(item)] for item in article_entries]
    for date, title in items:
        sentiment_result.update({title: date})

    return render_template('sentiment.html', sentiment_result=sentiment_result, article_count=article_count, limit=limit)
