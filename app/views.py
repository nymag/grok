from pymongo import MongoClient
from app import app
from flask import render_template
from textblob import TextBlob
from analysis import get_article_entry

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
    items = [get_article_entry(item) for item in article_entries]
    entries = [TextBlob(entry_text) for entry_text in items]

    for entry_text in entries:

        if len(entry_text.sentences) > 0:
            polarity_of_each_sentence = [sentence.sentiment.polarity for sentence in entry_text.sentences]

            average_polarity = sum(polarity_of_each_sentence) / len(entry_text.sentences)
            average_polarity *= 100

        if average_polarity > 0:
            entry_text = entry_text + ': positive ({0}% sure) '.format(abs(average_polarity))
        elif average_polarity < 0:
            entry_text = entry_text + ': negative ({0}% sure)'.format(abs(average_polarity))

    return render_template('index.html', article_count=article_count, items=items, entries=entries, entry_text=entry_text)
