from __future__ import print_function
from datetime import datetime, timedelta
import io
import json
import os.path
import shutil
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
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
                pageSize=100, 
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
    def get_folder(self,id):
        try:
            service = build('drive', 'v3', credentials=self.creds)
            results = service.files().list(
                q=f"'{id}' in parents",  # Add this line to filter by parent folder ID
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType)"
            ).execute()

            items = results.get('files', [])
            if not items:
                print('No files or folders found.')
            else:
                print('Files and folders:')
                for item in items:
                    name = item.get('name', 'Unknown')
                    item_type = item.get('mimeType', 'Unknown')
            return items
        except HttpError as error:
            print("ee")
    def document_automation(self,DOCUMENT_ID,FILE_PATH):
        print(DOCUMENT_ID)
        for document in DOCUMENT_ID:
            print(document["id"])
            self.service = build('drive', 'v3', credentials=self.creds,static_discovery=False)
            data = self.service.files().get(fileId=document["id"]).execute()['mimeType']
            exportedMimeType = None
            outputType = None
            if(data == "application/vnd.google-apps.document"):
                exportedMimeType = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                outputType = "docx"
                self.request = self.service.files().export(fileId=document["id"],mimeType=exportedMimeType)
            elif(data == "application/vnd.google-apps.spreadsheet"):
                exportedMimeType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                outputType = "xlsx"
                self.request = self.service.files().export(fileId=document["id"],mimeType=exportedMimeType)
            elif(data == "application/vnd.openxmlformats-officedocument.presentationml.presentation"):
                exportedMimeType = "application/pdf"
                outputType = "pptx"
                self.request = self.service.files().get_media(fileId=document["id"])
            else:
                exportedMimeType = "file"
                outputType = ""
                self.request = self.service.files().get_media(fileId=document["id"])
            
            self.fh = io.BytesIO()
            self.downloader = MediaIoBaseDownload(self.fh, self.request)
            done = False
            while done is False:
                status, done = self.downloader.next_chunk()
                print("Download %d%%" % int(status.progress() * 100))
            self.fh.seek(0)
            dt_string = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            for path in FILE_PATH:
                filename = f"{path}{document['name']}{dt_string}.{outputType}"
                with open(filename , 'wb+') as f:
                    shutil.copyfileobj(self.fh, f, length=131072)
    def get_about_info(self):
        drive_service = build('drive', 'v3', credentials=self.creds)
        about_info = drive_service.about().get(fields="user,storageQuota").execute()
        return about_info




