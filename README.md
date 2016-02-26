# Introduction

Grok /ˈɡrɒk/ is a term that roughly means "to understand profoundly/have knowledge of". It was coined by Robert Heinlein in his science-fiction novel *Stranger in a Strange Land*.

Grok uses sentiment analysis techniques to characterize the sentiment of text units. In this case, Grok parses through NYmag's article content and expresses articles as having positive, negative, or neutral sentiment. It then matches them against article pageviews, e.g. "Article 2007/07/the_entourage_guiltpleasure_in_3.html has 100 pageviews and rates as 90% positive".

# Installation

First ensure that Python 3.0 or later is installed. Build the required docs in your local env, from the project directory:

```
pip3 install -r requirements.txt
```

# Generate OAuth Credentials

Grok requires OAuth credentials in order to generate Google Analytics data. See [here](https://developers.google.com/api-client-library/python/guide/aaa_client_secrets) about generating a client_secrets.json file.

# Running Grok

```
python3 manage.py runserver
```
