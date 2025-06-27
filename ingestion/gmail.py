# app/ingestion/gmail_ingestion.py

from googleapiclient.discovery import build
from .drive import authenticate_google_drive  # Reuse auth
from app.faissmanager import get_sources_for_domain

def fetch_gmail_messages():
    creds = authenticate_google_drive()
    service = build('gmail', 'v1', credentials=creds)

    existing_ids = set(get_sources_for_domain("gmail"))

    results = service.users().messages().list(userId='me', maxResults=50).execute()
    messages = results.get('messages', [])
    texts = []
    sources = []

    for msg in messages:
        msg_id = msg['id']
        if msg_id in existing_ids:
            print(f"✅ Skipping already indexed email: {msg_id}")
            continue

        msg_data = service.users().messages().get(userId='me', id=msg_id).execute()
        snippet = msg_data.get('snippet', '')
        subject = ''
        for header in msg_data['payload'].get('headers', []):
            if header['name'].lower() == 'subject':
                subject = header['value']
                break

        content = f"{subject} {snippet}".strip()
        if content:
            texts.append(content)
            sources.append(msg_id)
        else:
            print(f"⚠️ Empty content for email: {msg_id}")

    return texts, sources
