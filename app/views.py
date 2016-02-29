from app import app
from flask import render_template
from pymongo import MongoClient
from textblob import TextBlob
from analysis import get_article_entry, get_article_title
from analytics import get_service, get_results
from datetime import datetime


client = MongoClient('mongo01.prd.nymetro.com', 27017)
db = client.articles
articles = db.articles

start = datetime(2016, 1, 1)
end = datetime(2016, 2, 1)
query = {'status': 'published', 'blogName': 'Vulture', 'publishDate': {'$gte': start, '$lt': end}}
entry_query = {'body.entry': 1, 'shorterHeadline': 1, 'canonicalUrl': 1}
max_num = 1062
sentiment_result = {}

article_entries = articles.find(query, entry_query).limit(max_num)
article_count = articles.find(query).count()
items = [[get_article_entry(item), get_article_title(item)] for item in article_entries]
scope = ['https://www.googleapis.com/auth/analytics.readonly']
service = get_service('analytics', 'v3', scope, 'client_secrets.json')
profile_id = '107545746'
analytics_items = get_results(service, profile_id)
analytics_article_count = analytics_items.get('totalResults')
rows = analytics_items.get('rows')
analytics_result = {}


@app.route('/')
@app.route('/index')
def sentiment():
    index()
    analytics()
    result = {}
    for d in sentiment_result, analytics_result:
        for k, v in d.items():
            result.setdefault(k, []).append(v)

    return render_template('index.html', result=result)


@app.route('/analytics')
def analytics():
    for title, pageviews in rows:
        remove = (-len('-- Vulture') - 1)
        title = title[:remove]
        analytics_result.update({title: pageviews})

    return render_template('analytics.html', analytics_result=analytics_result, analytics_article_count=analytics_article_count)


@app.route('/sentiment')
def index():
    for body, title in items:
        body = TextBlob(body)

        if len(body.sentences) > 0:
            polarity_of_each_sentence = [sentence.sentiment.polarity for sentence in body.sentences]

            average_polarity = sum(polarity_of_each_sentence) / len(body.sentences)
            average_polarity *= 100

        if average_polarity > 0:
            sentiment = 'positive ({}% sure)'.format(abs(round(average_polarity, 0)))
        elif average_polarity < 0:
            sentiment = 'negative ({}% sure)'.format(abs(round(average_polarity, 0)))

        sentiment_result.update({title: sentiment})

    return render_template('sentiment.html', sentiment_result=sentiment_result, article_count=article_count, max_num=max_num)
