from __future__ import print_function
import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError
import requests

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',"https://www.googleapis.com/auth/drive"]

class googleDrive:
    def __init__(self):
        self.creds = None
        
    def authentication(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)    
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
    def get_files(self):
        try:
            service = build('drive', 'v3', credentials=self.creds)
            results = service.files().list(
                pageSize=1000, 
                fields="nextPageToken, files(id, name, mimeType)").execute()
            items = results.get('files', [])
            if not items:
                print('No files or folders found.')
            else:
                print('Files and folders:')
                for item in items:
                    name = item.get('name', 'Unknown')
                    item_type = item.get('mimeType', 'Unknown')
                    if item_type == 'application/vnd.google-apps.folder':
                        print(f'Folder: {name}')
                    else:
                        print(f'File: {name}')
            return items
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
    def get_about_info(self):
        drive_service = build('drive', 'v3', credentials=self.creds)
        about_info = drive_service.about().get(fields="user,storageQuota").execute()
        print(about_info)
        return about_info




