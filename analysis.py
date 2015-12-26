from bs4 import BeautifulSoup


def strip_html(html):
    return ''.join(BeautifulSoup(html, 'html.parser').findAll(text=True))


def get_article_body(article):
    #grab all entry fields from article body
    entry_text = ''
    for text in article.get('body', []):
        keys = text.keys()
        if len(keys) > 0 and 'entry' in keys[0]:
            entry = text[keys[0]]
            #unicode handling
            if isinstance(entry, basestring):
                return entry
            entry_text = entry.get('entrytext', 'no entrytext found')
        #strip html from entry
        return strip_html(entry_text)
    return ''

''' for entry_text in articles.find():
    #some articles don't have titles
    #ignore errors even if the printed title string isn't proper UTF-8 or has broken marker bytes
    #strip html from title
    title = strip_html(entry_text.get('entryTitle', 'no entryTitle found')).encode('UTF-8', 'ignore')
    url = entry_text.get('canonicalUrl', 'no url found')
    vulture_url = 'http://www.vulture.com/2015/12/'
    blob = TextBlob(get_article_body(entry_text))

    #ensure that blob has sentences
    if len(blob.sentences) > 0:
        polarity_of_each_sentence = [sentence.sentiment.polarity for sentence in blob.sentences]

        average_polarity = sum(polarity_of_each_sentence) / len(blob.sentences)
        average_polarity *= 100

    if average_polarity > 0 and url.startswith(vultureUrl):
        print url, title, ': positive ({0}% sure) '.format(abs(average_polarity))
    elif average_polarity < 0 and url.startswith(vultureUrl):
        print url, title, ': negative ({0}% sure)'.format(abs(average_polarity)) '''
