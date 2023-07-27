from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

class googleDrive:
    def __init__(self):
        self.creds = None
        
    def authentication(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            return
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                    return
                except(e):
                    return
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials/credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)
                except(e):
                    print(e)
                    return
                   
                return
            with open('token.json', 'w') as token:
                try:
                    token.write(self.creds.to_json())
                    return
                except(e):
                    return

        # try:
        #     service = build('drive', 'v3', credentials=creds)
        #     results = service.files().list(
        #         pageSize=10, fields="nextPageToken, files(id, name)").execute()
        #     items = results.get('files', [])
        #     if not items:
        #         print('No files found.')
        #         return
        #     print('Files:')
        #     for item in items:
        #         print(u'{0} ({1})'.format(item['name'], item['id']))
        # except HttpError as error:
        #     # TODO(developer) - Handle errors from drive API.
        #     print(f'An error occurred: {error}')
