from pymongo import MongoClient
from app import app
from flask import render_template
from textblob import TextBlob
from analysis import strip_html, get_article_body

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
    items = [item for item in article_entries]

    return render_template('index.html', article_count=article_count, items=items)
