from cryptography.fernet import Fernet
import os

# Carica la chiave da variabile d'ambiente
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()

def encrypt_data(data: str) -> str:
    return Fernet(ENCRYPTION_KEY).encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    return Fernet(ENCRYPTION_KEY).decrypt(encrypted_data.encode()).decode()