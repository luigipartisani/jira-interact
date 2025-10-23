import streamlit as st
import requests

st.title("Issue copy")

API_URL = "http://localhost:8000"

#st.title("🚀 App Streamlit + FastAPI")

#if st.button("Ping backend"):
#    st.json(res.json())
#    res = requests.get(f"{API_URL}/ping")

#st.subheader("Invia un item")
name = st.text_input("Nome", "prodotto")
value = st.number_input("Valore", 0.0)

if st.button("Elabora"):
    payload = {"name": name, "value": value}
    res = requests.post(f"{API_URL}/process", json=payload)
    st.json(res.json())