import os
from dotenv import load_dotenv
import streamlit as st
import requests
#from requests.auth import HTTPBasicAuth
#import json
from datetime import datetime

load_dotenv()
API_URL = os.getenv("MY_API_URL")

# Funzione per ottenere il contenuto dell'issue da Jira
def get_js_issue(issue_key):
            
    end_point = f"{API_URL}/js/issue/{issue_key}"
    
    try:
        response = requests.get(url=end_point)
        #response.raise_for_status()  # Verifica se la richiesta ha avuto successo
        issue_data = response.json()
        return issue_data
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta: {e}")
        return None

def create_jc_issue(x_api_key, item):

    end_point = f"{API_URL}/jc/issue"
    
    try:

        payload = {
            "project_key": "BDA",#{"key": project_key}, RIMAPPARE I PROGETTI/COMPONENTI
            "summary": item['fields']['summary'],
            "description": item['fields']['description'],
            "issue_type": item['fields']['issuetype']['name'],
            "fix_version": item['fields']['fixVersions'][0]['name'] if item['fields']['fixVersions'] else "",
            "priority": item['fields']['priority']['name'] if item['fields']['priority'] else "",
            "original_estimate": item['fields'].get('timetracking', {}).get('originalEstimate', ""),

            "status": item['fields']['status']['name'],
            "reporter": item['fields']['reporter']['emailAddress'] if item['fields']['reporter'] else "",
            "assignee": item['fields']['assignee']['emailAddress'] if item['fields']['assignee'] else "",
            "created": item['fields']['created'],
            "updated": item['fields']['updated'],
            "issue_key": item['key'],
            "issue_link": (f"{os.getenv("JIRA_SERVER_URL")}/browse/{item['key']}"),
        }

        print(f"Payload: {payload}")
        
        response = requests.post(url=end_point, json=payload, headers={"x-api-key": x_api_key})
        #response.raise_for_status()  # Verifica se la richiesta ha avuto successo

        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)
        
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta: {e}")
        return None
    
def create_jc_issue_comment(x_api_key, issue_key, item):

    end_point = f"{API_URL}/jc/issue/{issue_key}/comment"
    
    try:

        payload = {
            "text": item['body'],
            "author": item['author']['emailAddress'],
            "created": item['created'],
            "updated": item['updated']
        }

        print(f"Payload: {payload}")

        response = requests.post(url=end_point, json=payload, headers={"x-api-key": x_api_key})
        #response.raise_for_status()  # Verifica se la richiesta ha avuto successo

        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)
        
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta: {e}")
        return None

def create_jc_issue_attachment(x_api_key, issue_key, item):

    end_point = f"{API_URL}/jc/issue/{issue_key}/attachment"
    
    try:

        print(f"Item: {item}")
        
        response = requests.post(url=end_point, files=item, headers={"x-api-key": x_api_key})
        #response.raise_for_status()  # Verifica se la richiesta ha avuto successo

        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)
        
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta: {e}")
        return None
    
# Funzione principale dell'app Streamlit
def main():

    #load_dotenv()

    st.title("Issue da Jira Server")
    st.set_page_config( layout="wide")

    # Input dell'utente
    api_key = st.text_input(key="input_api_key", label="API ey", value="gg")
    issue_key = st.text_input(key="input_issue_key", label="Issue key (es: PROJ-123)")

    if st.button("Carica"):
        if not issue_key:
            st.error("Indicare 'issue key'")
        else:
            issue_data = get_js_issue(issue_key)
            if issue_data:
                # Visualizza i dettagli dell'issue
                st.header(f"{issue_key}".upper())
                st.subheader(f"**{issue_data['fields']['summary']}**")

                #st.write("**Etichette**:", ", ".join(issue_data['fields']['labels']) if issue_data['fields']['labels'] else "Nessuna")

                # Utilizzo di colonne per impaginare i dati in modo gradevole
                col1, col2 = st.columns(2)

                with col1:
                    
                    st.write("**Issue Type:**", issue_data['fields']['issuetype']['name'])
                    st.write("**Status:**", issue_data['fields']['status']['name'])
                    affected_versions = issue_data['fields'].get('versions', [])
                    if affected_versions:
                        affected_versions_names = ", ".join([v['name'] for v in affected_versions])
                    else:
                        affected_versions_names = ""
                    st.write("**Affected Version:**", affected_versions_names)
                    fix_versions = issue_data['fields'].get('fixVersions', [])
                    if fix_versions:
                        fix_version_names = ", ".join([v['name'] for v in fix_versions])
                    else:
                        fix_version_names = ""
                    st.write("**Fix Version:**", fix_version_names)
                    st.write("**Priority:**", issue_data['fields']['priority']['name'])

                with col2:
                    st.write("**Assignee:**", issue_data['fields']['assignee']['emailAddress'] if issue_data['fields']['assignee'] else "")
                    st.write("**Reporter:**", issue_data['fields']['reporter']['emailAddress'] if issue_data['fields']['reporter'] else "")
                    st.write("**Created:**", issue_data['fields']['created'])
                    st.write("**Updated:**", issue_data['fields']['updated'])
                    st.write("**Original Estimate:**", issue_data['fields'].get('timetracking', {}).get('originalEstimate', ""))

                # Descrizione della issue
                st.subheader("Description")
                st.write(issue_data['fields']['description'])

                # Crea un pannello collassabile chiamato "Allegati"
                attachments = issue_data['fields'].get('attachment', [])
                with st.expander(f"Attachments ({len(attachments)})"):
                    if attachments:
                        col_attach1, col_attach2, col_attach3 = st.columns(3)
                        col_attach1, col_attach2, col_attach3 = st.columns([3,1,1])
                        for att in attachments:
                            with col_attach1:
                                st.write(f"{att['content']}")
                            with col_attach2:
                                st.write(f"{att['size']}")
                            with col_attach3:
                                st.write(f"{att['created']}")
                    else:
                        st.write("Nessun allegato presente.")

                # Crea un pannello collassabile chiamato "Commenti"
                comments = issue_data['fields'].get('comment', []).get('comments', [])
                with st.expander(f"Comments ({len(comments)})"):
                    if comments:
                        for cmm in comments:
                            with st.expander(f"{cmm['author']['emailAddress']} - {cmm['created']}"):
                                st.write(f"{cmm['body']}")
                    else:
                        st.write("Nessun allegato presente.")
            else:
                st.error("???")
                    

    # Aggiungere un bottone per eventualmente modificare o aggiornare i dati (opzionale)
    st.write("")
    if st.button("Copia in Jira Cloud"):
        if not issue_key:
            st.error("Indicare 'issue key'")
        else:
            issue_data = get_js_issue(issue_key)
            if issue_data:
                try:
                    new_issue_key = "BDA-15"
                    #new_issue_key = create_jc_issue(api_key, issue_data)
                    #st.info(f"{os.getenv("JIRA_CLOUD_URL")}/browse/{new_issue_key}")

                    comments = issue_data['fields'].get('comment', []).get('comments', [])
                    if comments:
                        for comment in comments:
                            create_jc_issue_comment(api_key, new_issue_key, comment)
                                        
                    #attachments = issue_data['fields'].get('attachment', [])
                    #if attachments:
                    #    for attachment in attachments:
                    #        js_auth = (os.getenv("JIRA_SERVER_USER"), os.getenv("JIRA_SERVER_PASS"))
                    #        content = requests.get(attachment['content'], auth=js_auth).content
                    #        files = {'file': (attachment['filename'], content)}       
                    #        create_jc_issue_attachment(api_key, new_issue_key, files)

                except Exception as e:
                    st.error(e)
            else:
                st.error("???")
        #st.write("Funzionalità di modifica non implementata.")



if __name__ == "__main__":
    main()
