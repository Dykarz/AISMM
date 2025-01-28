from flask_cors import CORS
from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# *** CODICE AGGIUNTO PER TEST SEMPLICE ***
@app.route('/')
def index():
    return "Ciao! Il backend Flask funziona!"
# *** FINE CODICE AGGIUNTO PER TEST SEMPLICE ***

# Configura la tua chiave API di Google AI
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = "YOUR_GOOGLE_AI_API_KEY"  # **Sostituisci con la tua chiave API! (Solo per test locale)**
    print("Attenzione: Chiave API Google AI non trovata nelle variabili d'ambiente. Usando la chiave hardcoded (solo per test locale).")
genai.configure(api_key=GOOGLE_API_KEY)

# Seleziona il modello Gemini Pro
model = genai.GenerativeModel('gemini-pro')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Messaggio mancante"}), 400

    try:
        # Inizia una chat (per mantenere la cronologia della conversazione)
        chat_session = model.start_chat(history=[]) # Inizia una nuova sessione di chat ogni volta per questo esempio semplice

        # Ottieni la risposta da Gemini
        response = chat_session.send_message(user_message)

        ai_response = response.text
        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"Errore API Gemini: {e}")  # Logga l'errore per debug
        return jsonify({"error": "Errore nella comunicazione con l'IA Gemini"}), 500

if __name__ == '__main__':
    app.run(debug=True) # debug=True SOLO per sviluppo locale, disabilita in produzione!