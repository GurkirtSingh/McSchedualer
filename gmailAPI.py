from __future__ import print_function
from http import server
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
import constant
SCOPES = constant.SCOPES

def gmailAccess():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # query the new schedule message
    latestMessageList = service.users().messages().list(userId='me', maxResults=1, q='mcd13687@ext.mcdonalds.com').execute()
    messageID = latestMessageList['messages'][0]['id']
    # get the email with id
    message = service.users().messages().get(userId='me', id=messageID, format='raw').execute()

    if not message:
        print('no message found')
    else:
        return message['raw']
