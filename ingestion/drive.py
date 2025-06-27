# app/ingestion/drive_ingestion.py

import os
import io
import pdfplumber
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from app.faissmanager import get_sources_for_domain  # 
# from app.config import SCOPES  

SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/gmail.readonly',
]

def authenticate_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client.json', SCOPES)
            creds = flow.run_local_server(host='127.0.0.1', port=8000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def download_pdf_as_text(file_id, creds):
    drive_service = build('drive', 'v3', credentials=creds)
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()

    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    fh.seek(0)

    try:
        with pdfplumber.open(fh) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() or ""
            return full_text.strip()
    except Exception as e:
        print(f" Error reading PDF: {e}")
        return ""

def get_drive():
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    # 
    existing_ids = set(get_sources_for_domain("drive"))

    results = service.files().list(
        q="mimeType='application/pdf'",
        pageSize=50,
        fields="files(id, name, mimeType)"
    ).execute()

    files = results.get('files', [])
    all_texts = []
    all_ids = []

    for file in files:
        file_id = file['id']
        if file_id in existing_ids:
            print(f" Skipping already indexed: {file['name']}")
            continue

        print(f" Processing new PDF: {file['name']}")
        text = download_pdf_as_text(file_id, creds)
        if text:
            all_texts.append(text)
            all_ids.append(file_id)
        else:
            print(f"Skipped or empty: {file['name']}")

    return all_texts, all_ids  
