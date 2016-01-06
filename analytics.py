import argparse
from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools


def get_service(api_name, api_version, scope, client_secrets_path):
    """Get a service that communicates to a Google API.

    Args:
      api_name: string The name of the api to connect to.
      api_version: string The api version to connect to.
      scope: A list of strings representing the auth scopes to authorize for the
        connection.
      client_secrets_path: string A path to a valid client secrets file.

    Returns:
      A service that is connected to the specified API.
    """
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
        client_secrets_path, scope=scope,
        message=tools.message_if_missing(client_secrets_path))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage(api_name + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service


def get_results(service, profile_id):
    """Queries Google Analytics views

    Args:
      service: Service object built by the Google API Python client library
      profile_id: string The ID of the profile view

    Returns:
      Query results
    """
      # Use the Analytics Service Object to query the Core Reporting API
      # for the number of pageviews in the past month.
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date='30daysAgo',
        end_date='today',
        metrics='ga:pageviews',
        dimensions='ga:pageTitle,ga:pagePath',
        filters='ga:pagePath=~^/2015/12/[\w-]+.html$').execute()


def print_results(results):
    # Print data nicely for the user.
    if results:
        print 'Vulture articles and corresponding pageviews: %s' % results.get('rows')
    #print 'Total Sessions: %s' % results.get('rows')

    else:
        print 'No results found'


def main():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, 'client_secrets.json')
    # Vulture's profile ID
    profile_id = '107545746'
    print_results(get_results(service, profile_id))


if __name__ == '__main__':
    main()
