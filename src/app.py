import streamlit as st
import pandas as pd
import plotly.express as px
from utils import encrypt_data, decrypt_data
from auth.firebase import email_auth, get_user_id
from auth.api_auth import api_key_auth
from database.crud import (
    save_profile_to_db,
    get_user_profiles,
    delete_profile
)

# Configurazione pagina
st.set_page_config(
    page_title="Social Media Manager Pro",
    page_icon="📱",
    layout="wide"
)

# --- Gestione Autenticazione ---
if 'authenticated' not in st.session_state:
    st.session_state.update({
        'authenticated': False,
        'user_id': None,
        'current_profile': None
    })

if not st.session_state.authenticated:
    st.title("🔑 Accesso Social Media Manager")
    
    auth_method = st.radio("Metodo di accesso:", 
        ("Email/Password", "API Key"), horizontal=True)
    
    # Login con Email/Password
    if auth_method == "Email/Password":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Accedi"):
            if email_auth(email, password):
                st.session_state.authenticated = True
                st.session_state.user_id = get_user_id(email)
                st.rerun()
            else:
                st.error("Credenziali non valide")
    
    # Login con API Key
    else:
        api_key = st.text_input("API Key", type="password")
        
        if st.button("Accedi con API Key"):
            user = api_key_auth(api_key)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_id = user.id
                st.rerun()
            else:
                st.error("API Key non valida")
    
    # Opzione registrazione nuovo utente
    with st.expander("Non hai un account? Registrati"):
        new_email = st.text_input("Nuova Email")
        new_password = st.text_input("Nuova Password", type="password")
        
        if st.button("Crea Account"):
            # Implementa la creazione utente
            st.success("Account creato! Ora puoi accedere")
    
    st.stop()

# --- Interfaccia Principale ---
st.sidebar.title("Menu")
page = st.sidebar.radio("Scegli una sezione:", [
    "Dashboard",
    "Pianificazione Contenuti",
    "Analisi",
    "Gestione Profili",
    "Impostazioni Account"
])

# Selezione profilo nella sidebar
profiles = get_user_profiles(st.session_state.user_id)
if profiles:
    profile_names = [p['profile_name'] for p in profiles]
    selected_profile = st.sidebar.selectbox(
        "Seleziona Profilo",
        profile_names,
        index=0
    )
    st.session_state.current_profile = next(
        p for p in profiles if p['profile_name'] == selected_profile
    )

# --- Pagine ---
# Pagina: Dashboard
if page == "Dashboard":
    st.title("📊 Dashboard")
    
    if not profiles:
        st.warning("Aggiungi almeno un profilo per iniziare")
        st.stop()
    
    # Metriche
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Post Programmati", "3")
    with col2:
        st.metric("Engagement Medio", "8.2%")
    with col3:
        st.metric("Nuovi Follower", "+124")
    
    # Calendario
    st.subheader("Calendario Contenuti")
    sample_posts = pd.DataFrame({
        "Data": ["2023-10-01", "2023-10-05", "2023-10-10"],
        "Piattaforma": ["Instagram", "Twitter", "Facebook"],
        "Contenuto": ["Post su prodotto nuovo", "Annuncio evento", "Sondaggio"],
        "Stato": ["Programmato", "Pubblicato", "Bozza"]
    })
    st.dataframe(sample_posts)

# Pagina: Pianificazione Contenuti
elif page == "Pianificazione Contenuti":
    st.title("🗓 Pianificazione Contenuti")
    
    with st.form("nuovo_post"):
        piattaforma = st.selectbox("Piattaforma", 
            ["Instagram", "Twitter", "Facebook", "LinkedIn"])
        data_pubblicazione = st.date_input("Data pubblicazione")
        contenuto = st.text_area("Testo del post")
        media = st.file_uploader("Allega media (immagine/video)")
        
        if st.form_submit_button("Programma Post"):
            st.success("Post programmato con successo!")

# Pagina: Analisi
elif page == "Analisi":
    st.title("📈 Analisi")
    
    df_analytics = pd.DataFrame({
        "Giorno": pd.date_range(start="2023-10-01", periods=7),
        "Engagement": [45, 52, 48, 62, 55, 68, 70]
    })
    fig = px.line(df_analytics, x="Giorno", y="Engagement", 
                 title="Engagement Ultimi 7 Giorni")
    st.plotly_chart(fig)

# Pagina: Gestione Profili
elif page == "Gestione Profili":
    st.title("👥 Gestione Profili")
    
    tab1, tab2 = st.tabs(["Aggiungi Profilo", "Profili Esistenti"])
    
    with tab1:
        with st.form("nuovo_profilo"):
            profile_name = st.text_input("Nome Profilo")
            platform = st.selectbox("Piattaforma", 
                ["Twitter", "Instagram", "Facebook", "LinkedIn"])
            api_key = st.text_input(f"{platform} API Key", type="password")
            api_secret = st.text_input(f"{platform} API Secret", type="password")
            
            if st.form_submit_button("Salva Profilo"):
                # Crittografa le credenziali prima di salvare
                encrypted_data = {
                    "api_key": encrypt_data(api_key),
                    "api_secret": encrypt_data(api_secret)
                }
                save_profile_to_db(
                    user_id=st.session_state.user_id,
                    profile_name=profile_name,
                    platform=platform,
                    credentials=encrypted_data
                )
                st.success("Profilo salvato correttamente!")
    
    with tab2:
        for profile in profiles:
            with st.expander(profile['profile_name']):
                # Decrittografa per visualizzazione
                decrypted_data = {
                    "api_key": decrypt_data(profile['social_connections']['api_key']),
                    "api_secret": decrypt_data(profile['social_connections']['api_secret'])
                }
                st.write(f"**Piattaforma:** {profile['platform']}")
                st.json(decrypted_data)
                if st.button(f"Elimina {profile['profile_name']}", key=profile['id']):
                    delete_profile(profile['id'])
                    st.rerun()

# Pagina: Impostazioni Account
elif page == "Impostazioni Account":
    st.title("⚙️ Impostazioni Account")
    st.write("Modifica le tue credenziali di accesso")
    
    with st.form("modifica_credenziali"):
        new_password = st.text_input("Nuova Password", type="password")
        confirm_password = st.text_input("Conferma Password", type="password")
        
        if st.form_submit_button("Aggiorna Password"):
            if new_password == confirm_password:
                # Implementa l'aggiornamento password
                st.success("Password aggiornata con successo!")
            else:
                st.error("Le password non coincidono")