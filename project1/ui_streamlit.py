import streamlit as st
import requests

API = st.sidebar.text_input("API URL", "http://localhost:8001")

st.title("Project1 — Stateful Chat UI")

session_id = st.sidebar.text_input("Session ID (leave empty to create)")

if st.sidebar.button("Create Session") or not session_id:
    r = requests.post(f"{API}/session")
    session_id = r.json()["session_id"]
    st.sidebar.success(f"Created {session_id}")

st.write(f"Session: {session_id}")

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("msg"):
    txt = st.text_area("Message", height=120)
    submitted = st.form_submit_button("Send")
    if submitted and txt.strip():
        payload = {"session_id": session_id, "message": txt}
        r = requests.post(f"{API}/chat", json=payload)
        data = r.json()
        st.session_state.history.append(("user", txt))
        st.session_state.history.append(("assistant", data.get("response", "")))

for role, text in st.session_state.history:
    if role == "user":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Bot:** {text}")
