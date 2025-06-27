import os
import json
import sqlite3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ✅ Configuration
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/documents.readonly'

]
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
FAISS_DIMENSION = 384
FAISS_NLIST = 5

# ✅ Initialize embedding model + FAISS index
model = SentenceTransformer(EMBEDDING_MODEL_NAME)
index = faiss.IndexFlatL2(FAISS_DIMENSION)
# index = faiss.IndexIVFFlat(quantizer, FAISS_DIMENSION, FAISS_NLIST)
# index = faiss.IndexFlatL2(dimension)
# index.add(embeddings_np)
trained = False

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print("validates with existing token")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client.json', SCOPES)
            creds = flow.run_local_server(host='127.0.0.1', port=8000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            print("without")
    return creds

def extract_google_docs_text(docs_service, doc_id):
    doc = docs_service.documents().get(documentId=doc_id).execute()
    # print(f"the initial doc is {doc}")
    text = ''
    for content in doc.get('body', {}).get('content', []):
        # print(f"content in doc: {content}")
        for element in content.get('paragraph', {}).get('elements', []):
            # print(f"element in content{element}")
            if 'textRun' in element and 'content' in element['textRun']:
                text += element['textRun']['content']
    # print(f"final output of the google docs{text.strip()}")           
    return text.strip()

def list_google_drive_docs(drive_service):
    results = drive_service.files().list(
        q="mimeType='application/vnd.google-apps.document'",
        pageSize=20, fields="files(id, name)").execute()
    return results.get('files', [])

def extract_bookmarks(bookmarks_file_path):
    with open(bookmarks_file_path, 'r') as file:
        bookmarks_json = json.load(file)
    bookmarks = []

    def traverse(node):
        if 'children' in node:
            for child in node['children']:
                traverse(child)
        elif node.get('type') == 'url':
            bookmarks.append(f"{node.get('name', '')} {node.get('url', '')}")

    traverse(bookmarks_json.get('roots', {}))
    return bookmarks

def extract_browsing_history(chrome_history_path):
    con = sqlite3.connect(chrome_history_path)
    cursor = con.cursor()
    cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 50;")
    rows = cursor.fetchall()
    con.close()
    print( [f"{title} {url}".strip() for url, title in rows if title])
    return [f"{title} {url}".strip() for url, title in rows if title]

def generate_embedding(text):
    return model.encode([text]).astype('float32')

def add_embeddings(embeddings_list):
    global trained
    if not trained:
        index.train(np.vstack(embeddings_list))
        trained = True
    index.add(np.vstack(embeddings_list))

def main():
    embeddings = []

    #gdrive
    creds = authenticate_google()
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    for file in list_google_drive_docs(drive_service):
        text = extract_google_docs_text(docs_service, file['id'])
        if text:
            embeddings.append(generate_embedding(text))

    #bookmarks of chrome
    bookmarks_path = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")  # Adjust path as needed
    if os.path.exists(bookmarks_path):
        for text in extract_bookmarks(bookmarks_path):
            embeddings.append(generate_embedding(text))

    #chrome history
    history_path = os.path.expanduser("~/.config/google-chrome/Default/History")  # path to chrome history file
    if os.path.exists(history_path):
        for text in extract_browsing_history(history_path):
            embeddings.append(generate_embedding(text))

    # embeddings
    if embeddings:
        add_embeddings(embeddings)
        print(f"Total embeddings added to FAISS: {index.ntotal}")
    else:
        print(" No embeddings were added. Check data sources.")

    # 
    incoming_text = "Show me confidential emails from last week"
    incoming_embedding = generate_embedding(incoming_text)
    distances, indices = index.search(incoming_embedding, k=5)
    print("Distances:", distances)
    print("Indices:", indices[0][1].values())

if __name__ == '__main__':
    main()
