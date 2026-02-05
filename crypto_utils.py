import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def privacy_amplification(shared_key):
    key_string = "".join(map(str, shared_key))
    return hashlib.sha256(key_string.encode()).hexdigest()

def encrypt_message(message, hex_key):
    key_bytes = bytes.fromhex(hex_key)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return iv + ciphertext

def decrypt_message(encrypted_data, hex_key):
    key_bytes = bytes.fromhex(hex_key)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode()