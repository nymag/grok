from pymongo import MongoClient
from app import app
from flask import render_template
from analysis import get_article_entry, get_article_title
from textblob import TextBlob
from analytics import get_service, get_results
from datetime import datetime

client = MongoClient('mongo01.prd.nymetro.com', 27017)
db = client.articles
articles = db.articles


@app.route('/')
@app.route('/index')
def index():
    start = datetime(2016, 1, 1)
    end = datetime(2016, 2, 1)
    query = {'status': 'published', 'blogName': 'Vulture', 'publishDate': {'$gte': start, '$lt': end}}
    entry_query = {'body.entry': 1, 'shorterHeadline': 1, 'canonicalUrl': 1}
    max_num = 1062
    article_entries = articles.find(query, entry_query).limit(max_num)
    article_count = articles.find(query).count()
    items = [[get_article_entry(item), get_article_title(item)] for item in article_entries]
    result = []

    for body, title in items:
        body = TextBlob(body)

        if len(body.sentences) > 0:
            polarity_of_each_sentence = [sentence.sentiment.polarity for sentence in body.sentences]

            average_polarity = sum(polarity_of_each_sentence) / len(body.sentences)
            average_polarity *= 100

        if average_polarity > 0:
            body = title + ' (positive: {0}% sure)'.format(abs(round(average_polarity, 1)))
        elif average_polarity < 0:
            body = title + ' (negative: {0}% sure)'.format(abs(round(average_polarity, 1)))
        result.append(body)

    return render_template('index.html', result=result, article_count=article_count, max_num=max_num)


@app.route('/analytics')
def google():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']
    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, 'client_secrets.json')
    # Vulture's profile ID
    profile_id = '107545746'
    items = get_results(service, profile_id)
    article_count = items.get('totalResults')
    rows = items.get('rows')
    result = []

    for row in rows:
        result.append(row)

    return render_template('analytics.html', result=result, article_count=article_count)
