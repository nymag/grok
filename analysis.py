from bs4 import BeautifulSoup
from datetime import datetime


def strip_html(html):
    return ''.join(BeautifulSoup(html, 'html.parser').findAll(text=True))


def get_article_date(item):
    article_date = item.get('publishDate')
    return article_date.day
      

def get_article_title(item):
    article_title = item.get('shorterHeadline', [])
    return strip_html(article_title)
