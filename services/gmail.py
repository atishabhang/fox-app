import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from constants import constants
from models.email import Email

USER_TOKEN = 'token.json'


def authenticate():
    creds = None
    try:
        # Add mech to load token from file instead of every time getting from web.
        if os.path.exists(USER_TOKEN):
            creds = Credentials.from_authorized_user_file(USER_TOKEN, constants.SCOPES)
            creds.refresh(Request())

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(constants.CLIENT_SECRET_FILE, constants.SCOPES)
                    creds = flow.run_local_server(port=8085)
                    with open(USER_TOKEN, 'w') as token:
                        token.write(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(constants.CLIENT_SECRET_FILE, constants.SCOPES)
            creds = flow.run_local_server(port=8085)
            with open(USER_TOKEN, 'w') as token:
                token.write(creds.to_json())
        # return creds
    except Exception as inst:
        print("ERROR=", inst)
        pass

    return creds


# flow = InstalledAppFlow.from_client_secrets_file(constants.CLIENT_SECRET_FILE, constants.SCOPES)
# creds = flow.run_local_server(port=0)


def fetch_emails(creds):
    service = build(constants.API_SERVICE_NAME, constants.API_VERSION, credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    msgs = results.get('messages')
    emails = []
    for msg in msgs:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        try:
            _id = txt['id']
            _received_at = txt['internalDate']
            _payload = txt['payload']
            _sender = ""
            _subject = ""
            headers = _payload['headers']

            for d in headers:
                if d['name'] == 'Subject':
                    _subject = d['value']
                if d['name'] == 'From':
                    _sender = d['value']

            # parts = _payload.get('parts')[0]
            # data = parts['body']['data']
            # data = data.replace("-", "+").replace("_", "/")
            # decoded_data = base64.b64decode(data)

            # soup = BeautifulSoup(decoded_data, "lxml")
            # body = soup.body()

            email_obj = Email(id=_id, sender=_sender, subject=_subject, received_at=datetime.fromtimestamp(int(_received_at) / 1000))
            emails.append(email_obj)

        except Exception as inst:
            print(inst)
            pass

    return emails
