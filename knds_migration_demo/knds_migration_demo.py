
# Author: Pete Chisamba 22.02.2026

import os
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

PG_CONN = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    dbname=os.getenv("PG_DB"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
)

CONF_BASE_URL = os.getenv("CONF_BASE_URL")
CONF_EMAIL = os.getenv("CONF_EMAIL")
CONF_API_TOKEN = os.getenv("CONF_API_TOKEN")
CONF_SPACE_KEY = os.getenv("CONF_SPACE_KEY")

auth = (CONF_EMAIL, CONF_API_TOKEN)


def create_page(title, body_html, parent_id=None):
    url = f"{CONF_BASE_URL}/rest/api/content"
    data = {
        "type": "page",
        "title": title,
        "space": {"key": CONF_SPACE_KEY},
        "body": {
            "storage": {
                "value": body_html,
                "representation": "storage"
            }
        }
    }
    if parent_id:
        data["ancestors"] = [{"id": str(parent_id)}]

    resp = requests.post(url, json=data, auth=auth)
    resp.raise_for_status()
    return resp.json()["id"]
def append_attachment_link_to_page(page_id, filename):
    """
    INPUT:
        page_id (str)  -> Confluence page ID
        filename (str) -> Name of uploaded file

    PROCESS:
        - Fetch current page content + version
        - Append HTML link pointing to attachment overview
        - Increment version
        - Update page

    OUTPUT:
        None (Raises exception if update fails)
    """

    # Get current page content + version
    get_url = f"{CONF_BASE_URL}/rest/api/content/{page_id}?expand=body.storage,version"
    resp = requests.get(get_url, auth=auth)
    resp.raise_for_status()

    page_data = resp.json()
    current_version = page_data["version"]["number"]
    current_body = page_data["body"]["storage"]["value"]
    title = page_data["title"]

    # Build link HTML
    attachment_url = f"{CONF_BASE_URL}/pages/viewpageattachments.action?pageID={page_id}"

    link_html = f"""
    <p>
        <strong>Attachment:</strong>
        <a href="{attachment_url}" target="_blank">{filename}</a>
    </p>
    """

    updated_body = current_body + link_html

    # Update page with incremented version
    update_payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "version": {"number": current_version + 1},
        "body": {
            "storage": {
                "value": updated_body,
                "representation": "storage"
            }
        }
    }

    update_url = f"{CONF_BASE_URL}/rest/api/content/{page_id}"
    update_resp = requests.put(update_url, json=update_payload, auth=auth)
    update_resp.raise_for_status()

def upload_attachment(page_id, file_path):
    """
    INPUT:
        page_id (str)  -> Confluence page ID
        file_path (str)-> Local file path to upload

    PROCESS:
        - Upload file as attachment to given page

    OUTPUT:
        filename (str) -> Name of uploaded file
    """

    url = f"{CONF_BASE_URL}/rest/api/content/{page_id}/child/attachment"
    filename = os.path.basename(file_path)

    headers = {
        "X-Atlassian-Token": "no-check"
    }

    with open(file_path, "rb") as f:
        files = {
            "file": (filename, f, "application/octet-stream")
        }

        resp = requests.post(
            url,
            headers=headers,
            files=files,
            auth=auth
        )

    resp.raise_for_status()

    return filename

def fetch_documents():
    cur = PG_CONN.cursor()
    cur.execute("""
        SELECT id, customer_name, project_code, document_type, version, file_path
        FROM documents
        ORDER BY customer_name, project_code, id
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def fetch_metadata(doc_id):
    cur = PG_CONN.cursor()
    cur.execute("""
        SELECT meta_key, meta_value
        FROM document_metadata
        WHERE document_id = %s
    """, (doc_id,))
    rows = cur.fetchall()
    cur.close()
    return dict(rows)


def main():
    customer_pages = {}
    project_pages = {}

    for doc_id, customer, project, doc_type, version, file_path in fetch_documents():

        # Customer page
        if customer not in customer_pages:
            customer_pages[customer] = create_page(customer, f"<p>{customer}</p>")
        customer_page_id = customer_pages[customer]

        # Project page
        proj_key = (customer, project)
        if proj_key not in project_pages:
            title = f"{project} – Project Overview"
            project_pages[proj_key] = create_page(title, f"<p>{project}</p>", parent_id=customer_page_id)
        project_page_id = project_pages[proj_key]

        # Document page
        metadata = fetch_metadata(doc_id)
        meta_html = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in metadata.items())
        meta_table = f"<table><tbody>{meta_html}</tbody></table>"

        body = f"""
        <p>Document ID: {doc_id}</p>
        <p>Customer: {customer}</p>
        <p>Project: {project}</p>
        <p>Type: {doc_type}</p>
        <p>Version: {version}</p>
        <h2>Metadata</h2>
        {meta_table}
        """

        doc_page_id = create_page(f"{doc_type} v{version}", body, parent_id=project_page_id)

        # Attachment
        if os.path.exists(file_path):
            print(f"Uploading attachment for document {doc_id} from {file_path}")
            #upload_attachment(doc_page_id, file_path)
            filename = upload_attachment(doc_page_id, file_path)
            append_attachment_link_to_page(doc_page_id, filename)
        else:
            print(f"Warning: File {file_path} not found for document {doc_id}")

        print(f"Migrated document {doc_id} → page {doc_page_id}")

    print("Migration completed.")


if __name__ == "__main__":
    main()

