from get_auth import initialize_service


def get_analytics(service, profile_id):
    # we want to grab pageview analytics data for each article
    ids = 'ga:' + profile_id
    data = service.data().ga().get(
        ids=ids,
        start_date='yesterday',
        end_date='today',
        dimensions='ga:pageTitle,ga:pagePath,ga:hostname',
        metrics='ga:pageviews',
        # only return articles from thecut and daily on nymag host
        filters='ga:hostname==nymag.com,ga:pagePath=~^/thecut|^/daily.*',
        sort='-ga:pageTitle',
        max_results=100
        ).execute()
    return data

if __name__ == '__main__':
    profile_id = '54903727'
    service = initialize_service()
    results = get_analytics(service, profile_id)
    print results
