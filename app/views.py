from pymongo import MongoClient
from app import app
#from analysis import strip_html, get_article_body
from flask import render_template
#from textblob import TextBlob


client = MongoClient('mongo01.prd.nymetro.com', 27017)
db = client.articles
articles = db.articles


@app.route('/')
@app.route('/index')
def index():
    for entry_text in articles.find():
        #some articles don't have titles
        #ignore errors even if the printed title string isn't proper UTF-8 or has broken marker bytes
        #strip html from title
        title = strip_html(entry_text.get('entryTitle', 'no entryTitle found')).encode('UTF-8', 'ignore')
        url = entry_text.get('canonicalUrl', 'no url found')
        vulture_url = 'http://www.vulture.com/2015/12/'

    return render_template('index.html', entry_text=entry_text, title=title, url=url, vulture_url=vulture_url)
