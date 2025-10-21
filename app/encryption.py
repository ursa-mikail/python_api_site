import os
import base64
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

class DataEncryptor:
    def __init__(self):
        self.passcode = os.environ.get('LOCAL_PASSCODE_FOR_SITE_DATA')
        if not self.passcode:
            raise ValueError("LOCAL_PASSCODE_FOR_SITE_DATA environment variable not set")
        
    def _derive_key(self, salt=None):
        """Derive encryption key from passcode using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(self.passcode.encode('utf-8'))
        return key, salt
    
    def encrypt_data(self, plaintext):
        """Encrypt data using AES-GCM"""
        if isinstance(plaintext, dict):
            plaintext = json.dumps(plaintext)
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
            
        key, salt = self._derive_key()
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        return base64.b64encode(salt + nonce + ciphertext).decode('utf-8')
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data using AES-GCM"""
        encrypted_bytes = base64.b64decode(encrypted_data)
        salt = encrypted_bytes[:16]
        nonce = encrypted_bytes[16:28]
        ciphertext = encrypted_bytes[28:]
        
        key, _ = self._derive_key(salt)
        aesgcm = AESGCM(key)
        
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Try to parse as JSON, return string if it fails
        try:
            return json.loads(plaintext.decode('utf-8'))
        except:
            return plaintext.decode('utf-8')
    
    def encrypt_file(self, input_path, output_path):
        """Encrypt a file and save to output path"""
        with open(input_path, 'r') as f:
            plaintext = f.read()
        
        encrypted_data = self.encrypt_data(plaintext)
        
        with open(output_path, 'w') as f:
            f.write(encrypted_data)
    
    def decrypt_file(self, input_path):
        """Decrypt a file and return contents"""
        with open(input_path, 'r') as f:
            encrypted_data = f.read()
        
        return self.decrypt_data(encrypted_data)
