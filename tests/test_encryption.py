import unittest
import os
import sys
import json

# Add the parent directory to Python path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.encryption import DataEncryptor

class TestEncryption(unittest.TestCase):
    def setUp(self):
        os.environ['LOCAL_PASSCODE_FOR_SITE_DATA'] = 'test_passcode_123'
        self.encryptor = DataEncryptor()

    def test_encrypt_decrypt_string(self):
        original = "Hello, World!"
        encrypted = self.encryptor.encrypt_data(original)
        decrypted = self.encryptor.decrypt_data(encrypted)
        self.assertEqual(original, decrypted)

    def test_encrypt_decrypt_dict(self):
        original = {"key": "value", "number": 42, "list": [1, 2, 3]}
        encrypted = self.encryptor.encrypt_data(original)
        decrypted = self.encryptor.decrypt_data(encrypted)
        self.assertEqual(original, decrypted)

    def test_encrypt_decrypt_file(self):
        # Create test input file
        test_data = {"test": "data", "secret": "password123"}
        with open('test_input.json', 'w') as f:
            json.dump(test_data, f)
        
        # Encrypt to file
        self.encryptor.encrypt_file('test_input.json', 'test_encrypted.enc')
        
        # Decrypt from file
        decrypted = self.encryptor.decrypt_file('test_encrypted.enc')
        
        self.assertEqual(test_data, decrypted)
        
        # Cleanup
        if os.path.exists('test_input.json'):
            os.remove('test_input.json')
        if os.path.exists('test_encrypted.enc'):
            os.remove('test_encrypted.enc')

    def tearDown(self):
        # Clean up environment variable
        if 'LOCAL_PASSCODE_FOR_SITE_DATA' in os.environ:
            del os.environ['LOCAL_PASSCODE_FOR_SITE_DATA']

if __name__ == '__main__':
    unittest.main()

    