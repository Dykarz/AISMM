import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Configurazione Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["FIREBASE_CONFIG"])
    firebase_admin.initialize_app(cred)

def email_auth(email, password):
    try:
        user = auth.get_user_by_email(email)
        return True
    except:
        return False