from http.client import HTTPException
import os
import requests
from dotenv import load_dotenv
from backend.requestDto import CreateIssueRequest, CreateCommentRequest

#HEADERS = {'Content-Type':'application/json', 'User-Agent':'bnx-auto'}

load_dotenv()

# Mappatura progetti
#PROJECT_MAP = {
#    "WCO": "AD"
#}

# Mappatura componenti
#COMPONENT_MAP = {
#    "WCO": "WebComposer"
#}

def get_issue(jira_type, issue_key):

    try:

        print(f"Get issue {issue_key} from Jira {jira_type}...")
        
        if jira_type == "Server":
            JIRA_URL = os.getenv("JIRA_SERVER_URL")
            JIRA_AUTH = (os.getenv("JIRA_SERVER_USER"), os.getenv("JIRA_SERVER_PASS"))
        elif jira_type == "Cloud":
            JIRA_URL = os.getenv("JIRA_CLOUD_URL")
            JIRA_AUTH = (os.getenv("JIRA_CLOUD_EMAIL"), os.getenv("JIRA_CLOUD_API_TOKEN"))

        end_point = f"{JIRA_URL}/rest/api/2/issue/{issue_key}"
        response = requests.get(url = end_point, auth = JIRA_AUTH)#, headers = HEADERS)

        if response.ok:
            return response.json()
        elif response.status_code == 404:
            raise Exception("Issue non trovata")
        else:
            raise Exception(response.text)
            
    except Exception as e:
        raise e

def create_issue(jira_type, item: CreateIssueRequest):
    
    try:

        print(f"Create issue in Jira {jira_type}...")

        if jira_type == "Server":
            JIRA_URL = os.getenv("JIRA_SERVER_URL")
            JIRA_AUTH = (os.getenv("JIRA_SERVER_USER"), os.getenv("JIRA_SERVER_PASS"))
        elif jira_type == "Cloud":
            JIRA_URL = os.getenv("JIRA_CLOUD_URL")
            JIRA_AUTH = (os.getenv("JIRA_CLOUD_EMAIL"), os.getenv("JIRA_CLOUD_API_TOKEN"))

        payload = {
            "fields": {
                "project": {"key": item.project_key},
                "summary": item.summary,
                "description": ("-" * 50) + "\nORIGINAL DETAILS\n" + ("-" * 50) + "\nIssue key: " + item.issue_key + "\nIssue link: " + item.issue_link + "\nStatus: " + item.status + "\nReporter: " + item.reporter + "\nAssignee: " + item.assignee + "\nCreated: " + "item.created" + "\nUpdated: " + "item.updated" "\n" + ("-" * 50) + "\n\n" + item.description,
                "issuetype": {"name": item.issue_type},
                "fixVersions": [{"name": item.fix_version}],
                #"reporter": {"emailAddress": issue_data.reporter},
                "assignee": {"emailAddress": item.assignee},
                "priority": {"name": item.priority},
                "timetracking": {"originalEstimate": item.original_estimate}
            }
        }

        #print(f"Payload: {payload}")
        end_point = f"{JIRA_URL}/rest/api/2/issue"
        response = requests.post(url = end_point, auth = JIRA_AUTH, json=payload)#, headers = HEADERS)
        #response.raise_for_status()
        
        if response.ok:
            return response.json()["key"]
        else:
            raise Exception(response.text)
            
    except Exception as e:
        raise e
    
def create_comment(jira_type, issue_key, item: CreateCommentRequest):
    
    try:

        print(f"Create issue comment in Jira {jira_type}...")

        if jira_type == "Server":
            JIRA_URL = os.getenv("JIRA_SERVER_URL")
            JIRA_AUTH = (os.getenv("JIRA_SERVER_USER"), os.getenv("JIRA_SERVER_PASS"))
        elif jira_type == "Cloud":
            JIRA_URL = os.getenv("JIRA_CLOUD_URL")
            JIRA_AUTH = (os.getenv("JIRA_CLOUD_EMAIL"), os.getenv("JIRA_CLOUD_API_TOKEN"))

        #adf_content = convert_jira_markup_to_adf(item.text)
        #print(f"adf_content : {adf_content}")

        # convert the ADF string returned by convert_jira_markup_to_adf into a JSON list
        #try:
        #    adf_list = json.loads(adf_content)
        #except Exception as e :
        #    print(f"Conversion to ADF failed: {e}")
        #    # if conversion fails, fall back to a simple paragraph containing the raw text
        #    adf_list = [
        #       {
        #            "type": "paragraph___",
        #            #"content": [{"type": "text", "text": item.text}]
        #        }
        #    ]

        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                #"content": adf_list
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": ("-" * 50) + "\nORIGINAL DETAILS\n" + ("-" * 50) + "\nAuthor: " + item.author + "\nCreated: " + item.created + "\nUpdated: " + item.updated + "\n" + ("-" * 50) + "\n\n" + item.text
                            }
                        ]
                    }
                ]
            }
        }
        
        #print(f"Payload: {payload}")
        end_point = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/comment"
        response = requests.post(url = end_point, auth = JIRA_AUTH, json=payload)#, headers = HEADERS)
        #response.raise_for_status()
        
        if response.ok:
            return ""
        else:
            raise Exception(response.text)
            
    except Exception as e:
        raise e
    
def create_attachment(jira_type, issue_key, file): #item: CreateAttachmentRequest):
    
    try:

        print(f"Create issue attachment in Jira {jira_type}...")

        HEADERS = {"X-Atlassian-Token": "no-check"}

        if jira_type == "Server":
            JIRA_URL = os.getenv("JIRA_SERVER_URL")
            JIRA_AUTH = (os.getenv("JIRA_SERVER_USER"), os.getenv("JIRA_SERVER_PASS"))
        elif jira_type == "Cloud":
            JIRA_URL = os.getenv("JIRA_CLOUD_URL")
            JIRA_AUTH = (os.getenv("JIRA_CLOUD_EMAIL"), os.getenv("JIRA_CLOUD_API_TOKEN"))

        print(f"Files: {file}")

        files = {"file": (file.filename, file.file, file.content_type)}
        

        end_point = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/attachments"
        response = requests.post(url=end_point, auth=JIRA_AUTH, files=files, headers = HEADERS)
        #response.raise_for_status()
        
        if response.ok:
            return ""
        else:
            raise Exception(response.text)
            
    except Exception as e:
        raise e
    

import re
import json

def convert_jira_markup_to_adf(jira_markup):
    # Funzione per convertire il testo in formato Jira Wiki Markup in ADF
    def parse_heading(m):
        """Converte i titoli H1, H2, H3, etc."""
        level = len(m.group(1))  # il numero di "=" definisce il livello del titolo
        return json.dumps({
            "type": "heading",
            "attrs": {"level": level},
            "content": [{"type": "text", "text": m.group(2)}]
        })

    def parse_bold(m):
        """Converte il grassetto ('''''text''''' -> **text**)"""
        return json.dumps({
            "type": "text",
            "text": m.group(1),
            "marks": [{"type": "strong"}]
        })

    def parse_italic(m):
        """Converte il corsivo (''text'' -> _text_)"""
        return json.dumps({
            "type": "text",
            "text": m.group(1),
            "marks": [{"type": "em"}]
        })

    def parse_bullet_list(m):
        """Converte gli elenchi puntati (/* item */ -> [item])"""
        return json.dumps({
            "type": "bulletList",
            "content": [{"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": m.group(1)}]}]}]
        })

    def parse_numbered_list(m):
        """Converte gli elenchi numerati (/# item #/ -> [item])"""
        return json.dumps({
            "type": "orderedList",
            "content": [{"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": m.group(1)}]}]}]
        })

    def parse_paragraph(m):
        """Converte i paragrafi normali"""
        return json.dumps({
            "type": "paragraph",
            "content": [{"type": "text", "text": m.group(1)}]
        })

    def parse_link(m):
        """Converte i link (URL)"""
        return json.dumps({
            "type": "text",
            "text": m.group(1),
            "marks": [{"type": "link", "attrs": {"href": m.group(2)}}]
        })
    
    def parse_image(m):
        """Converte le immagini (URL immagini)"""
        return json.dumps({
            "type": "image",
            "attrs": {"src": m.group(1)}
        })

    def parse_table(m):
        """Converte le tabelle Jira (| colonna1 | colonna2 | -> tabella ADF)"""
        # Separiamo le righe della tabella
        rows = m.group(1).strip().split('\n')
        table_content = []
        
        # Separiamo le celle per ogni riga
        for row in rows:
            cells = row.strip().split('|')[1:-1]  # Rimuoviamo i bordi della tabella (|...|)
            table_content.append({
                "type": "tableRow",
                "content": [{"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": cell.strip()}]}]} for cell in cells]
            })

        return json.dumps({
            "type": "table",
            "content": table_content
        })

    # Rimuove gli spazi extra prima e dopo la stringa
    jira_markup = jira_markup.strip()

    # Conversione dei titoli
    jira_markup = re.sub(r"^=+(.*?)=+$", parse_heading, jira_markup, flags=re.M)

    # Conversione di grassetto ('''''text''''' -> **text**)
    jira_markup = re.sub(r"''''(.*?)''''", parse_bold, jira_markup)

    # Conversione di corsivo (''text'' -> _text_)
    jira_markup = re.sub(r"''(.*?)''", parse_italic, jira_markup)

    # Conversione degli elenchi puntati (/* item */ -> [item])
    jira_markup = re.sub(r"^\* (.+)$", parse_bullet_list, jira_markup, flags=re.M)

    # Conversione degli elenchi numerati (/# item #/ -> [item])
    jira_markup = re.sub(r"^\# (.+)$", parse_numbered_list, jira_markup, flags=re.M)

    # Conversione dei paragrafi normali
    jira_markup = re.sub(r"^(?!\*|\#|=+)(.+)$", parse_paragraph, jira_markup, flags=re.M)

    # Conversione dei link (URL)
    jira_markup = re.sub(r"\[([^\]]+)\|([^\]]+)\]", parse_link, jira_markup)

    # Conversione delle immagini (URL immagini)
    jira_markup = re.sub(r"!\[.*?\|([^\]]+)\]", parse_image, jira_markup)

    # Conversione delle tabelle (| col1 | col2 | ...)
    jira_markup = re.sub(r"(\|.*?\|(?:\n\|.*?\|)*)", parse_table, jira_markup)

    # Ritorna il risultato finale come una lista di oggetti JSON ADF
    # Utilizziamo "eval" per interpretare le stringhe JSON formattate
    return f"[{', '.join(jira_markup.splitlines())}]"