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