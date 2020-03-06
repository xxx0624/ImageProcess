from __future__ import print_function
import pickle
import os.path
import cv2
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def init_drive_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_image(service, file_path):
    img = MediaFileUpload(file_path, mimetype='image/jpeg')
    file_metadata = {'name': file_path.split('/')[-1]}
    file = service.files().create(body=file_metadata,
                                        media_body=img,
                                        fields='id').execute()
    print ('File ID: %s' % file.get('id'))
    return file.get('id')

# def main():
#     service = init_drive_service()
#     upload_image(service)
    # file_metadata = {'name': 'testuploadphoto.jpg'}
    # media = MediaFileUpload('/Users/xxx0624/Downloads/testWriteimage.png', mimetype='image/jpeg')
    # file = service.files().create(body=file_metadata,
    #                                     media_body=media,
    #                                     fields='id').execute()
    # print ('File ID: %s' % file.get('id'))

if __name__ == '__main__':
    main()
