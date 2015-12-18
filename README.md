# grok

Welcome to NYmag's first dose of data analytics!

Grok /ˈɡrɒk/ is a term that roughly means "to understand profoundly/have knowledge of". It was coined by Robert Heinlein in his science-fiction novel *Stranger in a Strange Land*.

Grok uses sentiment analysis techniques to characterize the sentiment of text units. In this case, Grok parses through NYmag's article content and expresses articles as having positive, negative, or neutral sentiment. It then matches them against article pageviews, e.g. "Article 2007/07/the_entourage_guiltpleasure_in_3.html has 100 pageviews and rates as 90% positive".

# Installation

First ensure that Python 2.7.9 or later is installed. Then install the following libraries using pip:

[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

```
pip install BeautifulSoup4
```

[PyMongo](https://api.mongodb.org/python/current/)

```
pip install pymongo
```

[TextBlob](http://textblob.readthedocs.org/en/dev/)

```
pip install -U textblob
```
```
python -m textblob.download_corpora
```

[Httplib2](https://github.com/jcgregorio/httplib2)

```
pip install httplib2
```

# Generate OAuth Credentials

Grok requires OAuth credentials in order to run. See [here](https://developers.google.com/api-client-library/python/guide/aaa_client_secrets) about generating a client_secrets.json file.

# Running Grok

```
python analytics.py
```
