# 🔒 Privacy-Preserving AI Firewall

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/Built%20with-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![FAISS](https://img.shields.io/badge/Vector%20Search-FAISS-7e57c2.svg)](https://github.com/facebookresearch/faiss)

> 🔐 An intelligent AI firewall to **detect**, **block**, and **log** sensitive data access attempts by AI agents using regex + semantic search.

---

## 🧠 Overview

This project creates a firewall that prevents AI agents from exfiltrating user-sensitive data like:
- Aadhaar numbers
- Phone numbers
- Personal file metadata
- Semantically similar document content

It **intercepts queries** sent to AI agents, checks them against **domain-specific and private vector indexes**, and blocks if privacy is violated.

---

## 🚀 Features

- ✅ Ingests from Gmail, Drive, Docs, Bookmarks, History
- 🤖 Embeds content using sentence-transformers (384-dim)
- 🧠 Vector similarity with FAISS
- 🧾 Regex + semantic privacy detection
- 📊 SQLite database for logs & metadata
- ⚠️ MITRE ATT&CK tactic tagging (e.g., Exfiltration)

---

## ⚙️ Setup

### 🔧 Install Dependencies

```bash
git clone https://github.com/yourname/privacy-firewall.git
cd privacy-firewall
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
