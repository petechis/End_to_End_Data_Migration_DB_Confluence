# 📦 Document Migration Demo

### PostgreSQL → Confluence Cloud (Raw REST API)

**Simulation of a Documentum → Confluence Migration (Metadata + Files)**

## 🇬🇧 English Version

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Relational%20DB-blue)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![psycopg2](https://img.shields.io/badge/psycopg2-DB%20Connector-lightgrey)
![Requests](https://img.shields.io/badge/Requests-HTTP%20Client-green)
![Confluence](https://img.shields.io/badge/Confluence-Cloud-blue)
![REST API](https://img.shields.io/badge/API-REST-orange)
![Migration Strategy](https://img.shields.io/badge/Migration-Raw%20SQL%20%2B%20REST-red)

[English](README.md) | [German](./translations/DE/README.md)

---

## 🎯 Project Purpose

This project demonstrates a **structured data migration process** from a local PostgreSQL database (simulating an OpenText Documentum system) to Confluence Cloud.

It migrates:

* 📄 Documents (files from local file system)
* 🏷 Metadata (key/value pairs)
* 🏗 Logical hierarchy (Customer → Project → Document)

⚡ No special migration tools were used.
Only:

* Raw SQL (PostgreSQL)
* Python
* Raw Confluence REST API

This serves as a **baseline migration architecture** for interviews and portfolio demonstration.

---

## 🏗 Architecture Overview

```
┌──────────────────────────┐
│ PostgreSQL (localhost)   │
│ documents + metadata     │
└──────────────┬───────────┘
               │
               ▼
        Python Script
   (psycopg2 + requests)
               │
               ▼
    Confluence REST API
               │
               ▼
        Confluence Cloud
```

---

## 📂 Target Structure in Confluence

Space: `DOCMIG`

```
DOCMIG
 ├── BMW AG
 │     └── PRJ-001 – Project Overview
 │            ├── SOW v1
 │            └── Invoice v1
 └── Siemens Healthineers
        └── PRJ-002 – Project Overview
               └── Spec v3
```

Each document page contains:

* Metadata table
* Document details
* Attached file (PDF/DOCX)

---

## ⚙️ Technology Stack

| Layer         | Technology                  |
| ------------- | --------------------------- |
| Database      | PostgreSQL (localhost:5432) |
| Backend       | Python 3                    |
| DB Connector  | psycopg2                    |
| HTTP Client   | requests                    |
| Target System | Confluence Cloud            |
| Auth          | API Token (Basic Auth)      |

---

## 🚀 Setup

### 1️⃣ Python Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install psycopg2-binary requests python-dotenv
```

---

### 2️⃣ Environment Variables (.env)

```
PG_HOST=localhost
PG_DB=documentum_demo
PG_USER=postgres
PG_PASSWORD=postgres

CONF_BASE_URL=https://your-domain.atlassian.net/wiki
CONF_EMAIL=your-email@example.com
CONF_API_TOKEN=your-api-token
CONF_SPACE_KEY=DOCMIG
```

---

## 🧠 Core Migration Logic (Important Excerpts)

### Create Confluence Page

```python
def create_page(title, body_html, parent_id=None):
    url = f"{CONF_BASE_URL}/rest/api/content"
    data = {
        "type": "page",
        "title": title,
        "space": {"key": CONF_SPACE_KEY},
        "body": {
            "storage": {
                "value": body_html,
                "representation": "storage",
            }
        },
    }
    if parent_id:
        data["ancestors"] = [{"id": str(parent_id)}]

    resp = requests.post(url, json=data, auth=auth)
    resp.raise_for_status()
    return resp.json()["id"]
```

---

### Upload Attachment

```python
def upload_attachment(page_id, file_path):
    url = f"{CONF_BASE_URL}/rest/api/content/{page_id}/child/attachment"
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        resp = requests.post(url, files=files, auth=auth)
    resp.raise_for_status()
```

---

## 🔎 Validation

After running:

```bash
python migrate_raw.py
```

Check in Confluence:

* Space exists
* Customer pages created
* Project hierarchy correct
* Metadata tables rendered
* Attachments uploaded

---

## 🛠 Troubleshooting

| Error               | Cause             | Solution                 |
| ------------------- | ----------------- | ------------------------ |
| 401 Unauthorized    | Invalid API token | Generate new token       |
| 403 Forbidden       | Missing access    | Check Confluence license |
| 404 Space not found | Wrong Space Key   | Verify Space Key         |
| KeyError "id"       | API failure       | Print response body      |

---

## ⭐ Best Practices Demonstrated

* Structured hierarchy mapping
* Clean separation of concerns
* Idempotent page caching (no duplicates)
* REST-based integration
* Environment-based credential handling
* Reproducible local execution

---

## 🎥 5-Minute Video Walkthrough

👉 **Presentation:**

[Loom-Video:](https://www.loom.com/share/3d1526ff3d034ed38cf41c0343816173)

---

## 🧑‍💼 Elevator Pitch

> “I implemented an automated migration from PostgreSQL to Confluence using raw SQL and the Confluence REST API. The script extracts documents and metadata, dynamically builds a hierarchical structure (Customer → Project → Document), and uploads attachments. The process is fully reproducible, API-driven, and tool-independent.”

---

## 👤 Author

**Pete Chisamba**
Munich, Germany
BI | Data | DMS | Confluence Administration

---
