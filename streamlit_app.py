import streamlit as st

read_issue = st.Page(
    page="views/read_issue.py",
    title="Leggi issue",
    icon=":material/file_open:",
    default=True
)

issue_copy_page = st.Page(
    page="views/issue_copy.py",
    title="Issue copy",
    icon=":material/file_copy:"
)

pg = st.navigation(
    {
        "Jira Server": [read_issue],
        "API": [issue_copy_page]
    }
)

pg.run()