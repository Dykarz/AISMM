# Chat IA Gemini Semplice - Sito Web con Chatbot IA

Questo progetto è un sito web semplice che integra una chat IA basata sul modello linguistico Gemini Pro di Google AI.  Permette agli utenti di interagire con un chatbot IA direttamente tramite un'interfaccia web user-friendly.

**Stato del Progetto:** Funzionante! La chat IA Gemini è completamente funzionante online. Gli utenti possono inviare messaggi tramite l'interfaccia web e ricevere risposte generate dal modello Gemini Pro.

**Tecnologie Utilizzate:**

* **Frontend:**
    * HTML, CSS, JavaScript - per la struttura, lo stile e l'interattività del sito web.
* **Backend:**
    * Python - Linguaggio di programmazione per il backend.
    * Flask - Microframework web Python per creare l'API backend.
    * `google-generativeai` (libreria Python) - Per interagire con l'API Gemini Pro di Google AI.
    * `flask-cors` (libreria Python) - Per abilitare CORS (Cross-Origin Resource Sharing) e permettere al frontend su GitHub Pages di comunicare con il backend su Codespaces.
    * gunicorn - Server WSGI Python per servire l'applicazione Flask (per il deployment su Heroku, se si desidera).
* **Hosting:**
    * **Frontend:** [GitHub Pages](https://pages.github.com/) - Hosting gratuito per siti web statici direttamente da repository GitHub.
    * **Backend:** [GitHub Codespaces](https://github.com/features/codespaces) - Ambiente di sviluppo online (usato per eseguire il backend Flask in questo progetto).  *Nota: Per un deployment più permanente, si consiglia di considerare piattaforme di hosting dedicate come Heroku.*

**Struttura del Progetto:**
Use code with caution.
Markdown
gemini-chat-ia/ (Cartella principale del progetto)
├── backend/ (Cartella per il codice backend Python)
│ └── app.py (File principale dell'applicazione Flask backend)
├── index.html (File HTML principale del frontend - ora nella root per GitHub Pages)
├── style.css (File CSS per lo stile del frontend - opzionale, ora nella root)
├── script.js (File JavaScript per l'interattività del frontend - opzionale, ora nella root)
├── requirements.txt (File per le dipendenze Python)
└── Procfile (File per Heroku - per specificare come avviare l'app)
└── README.md (Questo file - Documentazione del progetto)

**Codici Principali:**

**1. Backend (Python Flask) - `backend/app.py`:**

```python
from flask_cors import CORS
from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Ciao! Il backend Flask funziona!"

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
Use code with caution.
Nota Importante: Nel codice backend, ricorda di sostituire "YOUR_GOOGLE_AI_API_KEY" con la tua vera chiave API di Google AI se vuoi testare il backend localmente (anche se per il deployment su Codespaces/Heroku è consigliabile usare variabili d'ambiente).

2. Frontend (HTML, CSS, JavaScript) - index.html:

<!DOCTYPE html>
<html>
<head>
    <title>Chat IA Gemini Semplice</title>
    <style>
        /* Stile CSS base (puoi migliorarlo!) */
        body { font-family: sans-serif; }
        #chat-area { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        #input-area { display: flex; }
        #message-input { flex-grow: 1; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        #send-button { padding: 8px 15px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .user-message { text-align: right; margin-bottom: 5px; color: blue; }
        .ai-message { text-align: left; margin-bottom: 5px; color: green; }
        .error-message { color: red; }
    </style>
</head>
<body>
    <h1>Chat IA Gemini Semplice</h1>

    <div id="chat-area">
        <!-- Qui verranno visualizzati i messaggi della chat -->
    </div>

    <div id="input-area">
        <input type="text" id="message-input" placeholder="Scrivi il tuo messaggio...">
        <button id="send-button">Invia</button>
    </div>

    <script>
        const chatArea = document.getElementById('chat-area');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');

        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', function(event) { // Invia anche con Enter
            if (event.key === "Enter") {
                sendMessage();
            }
        });

        function sendMessage() {
            const message = messageInput.value.trim();
            if (message) {
                appendMessage('user-message', message, 'Utente'); // Mostra il messaggio dell'utente nella chat
                messageInput.value = ''; // Pulisci l'input

                // Invia il messaggio al backend API
                fetch('YOUR_CODESPACES_PUBLIC_URL/api/chat', { // **SOSTITUISCI "YOUR_CODESPACES_PUBLIC_URL" CON IL TUO URL PUBBLICO REALE DI CODESPACES!**
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.response) {
                        appendMessage('ai-message', data.response, 'IA Gemini'); // Mostra la risposta dell'IA nella chat
                    } else if (data.error) {
                        appendMessage('error-message', `Errore IA: ${data.error}`, 'Errore'); // Mostra un messaggio di errore
                    }
                })
                .catch(error => {
                    console.error('Errore Fetch API:', error);
                    appendMessage('error-message', 'Errore di comunicazione con il server.', 'Errore');
                });
            }
        }

        function appendMessage(messageClass, text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add(messageClass); // Aggiungi la classe CSS per lo stile
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`; // Usa innerHTML per il tag <strong>
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight; // Scroll automatico in basso
        }
    </script>
</body>
</html>

Html

Nota Importante: Nel codice frontend index.html, ricorda di sostituire "YOUR_CODESPACES_PUBLIC_URL" con il tuo vero URL Pubblico di Codespaces (porta 5000) per far funzionare la comunicazione con il backend.

3. File delle Dipendenze Python - requirements.txt:

flask
google-generativeai
gunicorn
flask-cors
Use code with caution.
4. File Procfile (per Heroku) - Procfile:

web: gunicorn backend.app:app
Use code with caution.
Come Avviare il Progetto (per sviluppo locale o in Codespaces):

Assicurati di avere Python 3 installato.

Crea un ambiente virtuale Python (consigliato): python -m venv venv (e attivalo: source venv/bin/activate o venv\Scripts\activate).

Installa le dipendenze Python: pip install -r requirements.txt.

Imposta la variabile d'ambiente GOOGLE_API_KEY: (Es. export GOOGLE_API_KEY="YOUR_API_KEY" in Linux/macOS o set GOOGLE_API_KEY=YOUR_API_KEY in Windows).

Esegui il backend Flask: python backend/app.py.

Apri il file frontend/index.html nel tuo browser (per test frontend statico, ma per la chat funzionante devi usare l'URL di GitHub Pages o un server web che serva index.html e che punti al backend).

Per testare la chat completa (frontend + backend):

Assicurati che il backend Flask sia in esecuzione (punto 5).

Apri l'URL del sito web frontend ospitato su GitHub Pages (es. https://<your-username>.github.io/<your-repository-name>/) nel tuo browser.

Prossimi Passi e Sviluppi Futuri:

Migliorare l'interfaccia utente (frontend) con CSS e JavaScript più avanzati.

Implementare la cronologia della conversazione per un'esperienza chat più contestuale.

Aggiungere gestione degli errori più robusta e feedback visivo per l'utente.

Esplorare le opzioni di personalizzazione dell'API Gemini Pro.

Considerare il deployment del backend su una piattaforma di hosting più permanente come Heroku.

Licenza:

[Aggiungi qui la licenza che preferisci per il tuo progetto, ad esempio MIT License, Apache 2.0, o specifica "Nessuna licenza" se non vuoi applicarne una specifica.]

Autore:

[Il tuo nome o nickname]

Data:

[Data di creazione del progetto o ultima modifica]