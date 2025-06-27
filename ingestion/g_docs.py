# app/ingestion/docs_ingestion.py

from googleapiclient.discovery import build
from .drive import authenticate_google_drive  
from app.faissmanager import get_sources_for_domain

def extract_google_doc_text(doc_id, docs_service):
    try:
        doc = docs_service.documents().get(documentId=doc_id).execute()
        text = ''
        for content in doc.get('body', {}).get('content', []):
            for element in content.get('paragraph', {}).get('elements', []):
                if 'textRun' in element and 'content' in element['textRun']:
                    text += element['textRun']['content']
        return text.strip()
    except Exception as e:
        print(f" Failed to extract doc {doc_id}: {e}")
        return ""

def fetch_google_docs():
    creds = authenticate_google_drive()
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)

    existing_ids = set(get_sources_for_domain("docs"))

    results = drive_service.files().list(
        q="mimeType='application/vnd.google-apps.document'",
        pageSize=50, fields="files(id, name)").execute()

    texts, sources = [], []

    for file in results.get('files', []):
        doc_id = file['id']
        if doc_id in existing_ids:
            print(f"Skipping already indexed doc: {file['name']}")
            continue

        print(f" Processing Google Doc: {file['name']}")
        text = extract_google_doc_text(doc_id, docs_service)
        if text:
            texts.append(text)
            sources.append(doc_id)
        else:
            print(f" Empty content: {file['name']}")

    return texts, sources
