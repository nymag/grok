from pymongo import MongoClient
from app import app
from flask import render_template
from analysis import get_article_entry
from textblob import TextBlob

client = MongoClient('mongo01.prd.nymetro.com', 27017)
db = client.articles
articles = db.articles


@app.route('/')
@app.route('/index')
def index():
    query = {'status': 'published', 'blogName': 'Vulture'}
    entry_query = {'body.entry': 1, 'entryTitle': 1, 'canonicalUrl': 1}
    max_num = 100
    article_entries = articles.find(query, entry_query).limit(max_num)
    article_count = articles.find(query).count()
    items = ([get_article_entry(item) for item in article_entries])
    results = []

    for blob in items:
        blob = TextBlob(blob)

        if len(blob.sentences) > 0:
            polarity_of_each_sentence = [sentence.sentiment.polarity for sentence in blob.sentences]

            average_polarity = sum(polarity_of_each_sentence) / len(blob.sentences)
            average_polarity *= 100

        if average_polarity > 0:
            blob = blob + ': positive ({0}% sure) '.format(abs(average_polarity))
        elif average_polarity < 0:
            blob = blob + ': negative ({0}% sure)'.format(abs(average_polarity))
        results.append(blob)

    return render_template('index.html', results=results, article_count=article_count, max_num=max_num)
