const chatArea = document.getElementById('chat-area');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const sidebarToggle = document.getElementById('sidebar-toggle'); // Ottieni riferimento al pulsante toggle sidebar
const sidebar = document.getElementById('sidebar'); // Ottieni riferimento alla sidebar

sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', function(event) { // Invia anche con Enter
    if (event.key === "Enter") {
        sendMessage();
    }
});

sidebarToggle.addEventListener('click', toggleSidebar); // Aggiungi event listener per il toggle sidebar

function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        appendMessage('user-message', message, 'Utente'); // Mostra il messaggio dell'utente nella chat
        messageInput.value = ''; // Pulisci l'input

        // Invia il messaggio al backend API
        fetch('https://miniature-space-enigma-699xww7v6pq9crpw7-5000.app.github.dev/api/chat', { // **SOSTITUISCI "YOUR_CODESPACES_PUBLIC_URL" CON IL TUO URL PUBBLICO REALE DI CODESPACES!**
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                appendMessage('ai-message', data.response, 'Gemini'); // Mostra la risposta dell'IA nella chat
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

function toggleSidebar() { // Funzione per aprire/chiudere la sidebar
    sidebar.classList.toggle('sidebar-open'); // Aggiungi/rimuovi la classe 'sidebar-open' per mostrare/nascondere la sidebar
}