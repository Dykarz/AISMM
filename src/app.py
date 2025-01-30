import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione pagina
st.set_page_config(
    page_title="Social Media Manager",
    page_icon="📱",
    layout="wide"
)

# Sidebar per navigazione
st.sidebar.title("Menu")
page = st.sidebar.radio("Scegli una sezione:", [
    "Dashboard",
    "Pianificazione Contenuti",
    "Analisi",
    "Impostazioni Account"
])

# Mock dati per esempio
sample_posts = pd.DataFrame({
    "Data": ["2023-10-01", "2023-10-05", "2023-10-10"],
    "Piattaforma": ["Instagram", "Twitter", "Facebook"],
    "Contenuto": ["Post su prodotto nuovo", "Annuncio evento", "Sondaggio"],
    "Stato": ["Programmato", "Pubblicato", "Bozza"]
})

# Pagina: Dashboard
if page == "Dashboard":
    st.title("📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Post Programmati", "3")
    with col2:
        st.metric("Engagement Medio", "8.2%")
    with col3:
        st.metric("Nuovi Follower", "+124")
    
    st.subheader("Calendario Contenuti")
    st.dataframe(sample_posts)

# Pagina: Pianificazione Contenuti
elif page == "Pianificazione Contenuti":
    st.title("🗓 Pianificazione Contenuti")
    
    with st.form("nuovo_post"):
        piattaforma = st.selectbox("Piattaforma", ["Instagram", "Twitter", "Facebook"])
        data_pubblicazione = st.date_input("Data pubblicazione")
        contenuto = st.text_area("Testo del post")
        media = st.file_uploader("Allega media (immagine/video)")
        
        if st.form_submit_button("Programma Post"):
            # Qui aggiungeremo la logica di salvataggio
            st.success("Post programmato con successo!")

# Pagina: Analisi
elif page == "Analisi":
    st.title("📈 Analisi")
    
    # Mock grafico
    df_analytics = pd.DataFrame({
        "Giorno": pd.date_range(start="2023-10-01", periods=7),
        "Engagement": [45, 52, 48, 62, 55, 68, 70]
    })
    fig = px.line(df_analytics, x="Giorno", y="Engagement", title="Engagement Ultimi 7 Giorni")
    st.plotly_chart(fig)

# Pagina: Impostazioni Account
elif page == "Impostazioni Account":
    st.title("⚙️ Impostazioni Account")
    st.write("Configurazione account social collegati (da implementare)")