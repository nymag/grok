import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

# the file with the OAuth 2.0 Client details for authentication and authorization.
CLIENT_SECRETS = 'client_secrets.json'

# the Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
  scope='https://www.googleapis.com/auth/analytics.readonly',
  message='%s is missing' % CLIENT_SECRETS
)

# a file to store the access token
TOKEN_FILE_NAME = 'token.dat'


def prepare_credentials():
  # retrieve existing credendials
    storage = Storage(TOKEN_FILE_NAME)
    credentials = storage.get()

  # if existing credentials are invalid and Run Auth flow
  # the run method will store any new credentials
    if credentials is None or credentials.invalid:
        credentials = run(FLOW, storage)  # run Auth Flow and store credentials

    return credentials


def initialize_service():
    # create an http object
    http = httplib2.Http()

    credentials = prepare_credentials()  # retrieve stored creds. if not found, run Auth Flow
    http = credentials.authorize(http)  # authorize the http object

    # build the Analytics Service Object with the authorized http object
    return build('analytics', 'v3', http=http)
