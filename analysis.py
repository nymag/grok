from pymongo import MongoClient
from bs4 import BeautifulSoup
from textblob import TextBlob

client = MongoClient('mongo01.qa.nymetro.com', 27017)
db = client.articles
articles = db.articles

def strip_html(html):
    return ''.join(BeautifulSoup(html).findAll(text=True))

def get_article_body(article):
    #some articles don't have bodies 
    if 'body' not in article:
        return ''
    #body is an array and entry and entryText exist within it
    for text in article['body']:
       if 'entry' in text:
        #lowercase dictionary: some articles use either entryText or entrytext
        lowercase_dict = {}
        for key, value in text['entry'].iteritems(): 
                lowercase_dict[key.lower()] = value            
        return lowercase_dict['entrytext']
    return ''

for entry in articles.find():
    #some articles don't have titles
    #ignore errors even if the printed title string isn't proper UTF-8 or has broken marker bytes
    title =  entry.get('entryTitle', 'no entry title found').encode('utf-8', 'ignore')
    body = get_article_body(entry)
    blob = TextBlob(body)

    #if there's no body in the article, the loop continues 
    if not body:
        continue

    polarity_of_each_sentence = [sentence.sentiment.polarity for sentence in blob.sentences]

    average_polarity = sum(polarity_of_each_sentence) / len(blob.sentences)
    average_polarity *= 100

    if average_polarity > 0:
        print title, ': positive ({0}% sure) '.format(abs(average_polarity))
    elif average_polarity < 0:
        print title, ': negative ({0}% sure)'.format(abs(average_polarity))
    else: 
        print title, ": Can't tell"
