import os
import json
from .encryption import DataEncryptor

class SiteManager:
    def __init__(self):
        self.encryptor = DataEncryptor()
        self.data_dir = 'site/data'
    
    def build_site_data(self):
        """Build and encrypt site data - for your existing demo"""
        site_data = {
            "site_config": {
                "name": "Encrypted Site",
                "version": "1.0.0",
                "description": "A site with encrypted data storage"
            },
            "content_data": {
                "home": {
                    "title": "Welcome to Our Secure Site",
                    "description": "All data is encrypted for security",
                    "features": ["Secure Data", "Encrypted Storage", "Privacy Focused"]
                },
                "about": {
                    "title": "About Us", 
                    "content": "We believe in data privacy and security."
                }
            },
            "secrets": {
                "api_keys": {
                    "service_1": "encrypted_api_key_123",
                    "service_2": "encrypted_secret_456"
                },
                "config": {
                    "database_url": "encrypted_db_url",
                    "admin_email": "encrypted_admin@example.com"
                }
            }
        }
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Encrypt and save different data types
        self._save_encrypted_data('site_config.json', site_data["site_config"])
        self._save_encrypted_data('content_data.json', site_data["content_data"])
        self._save_encrypted_data('secrets.json', site_data["secrets"])
        
        # Create a manifest file
        manifest = {
            "encrypted_files": [
                "site_config.json.enc",
                "content_data.json.enc", 
                "secrets.json.enc"
            ],
            "encryption_method": "AES-GCM",
            "key_derivation": "PBKDF2-HMAC-SHA256"
        }
        
        with open(f'{self.data_dir}/manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print("✅ Site data built and encrypted successfully!")
        print(f"📁 Encrypted files saved to: {self.data_dir}/")
    
    def _save_encrypted_data(self, filename, data):
        """Encrypt data and save to file"""
        encrypted = self.encryptor.encrypt_data(data)
        encrypted_filename = filename.replace('.json', '.json.enc')
        
        with open(f'{self.data_dir}/{encrypted_filename}', 'w') as f:
            f.write(encrypted)
    
    def load_site_data(self):
        """Load and decrypt all site data"""
        try:
            with open(f'{self.data_dir}/manifest.json', 'r') as f:
                manifest = json.load(f)
            
            decrypted_data = {}
            for enc_file in manifest["encrypted_files"]:
                file_key = enc_file.replace('.json.enc', '')
                decrypted_data[file_key] = self.encryptor.decrypt_file(
                    f'{self.data_dir}/{enc_file}'
                )
            
            return decrypted_data
        
        except FileNotFoundError:
            print("❌ No encrypted data found. Run build_site_data() first.")
            return None
    
    def view_decrypted_data(self):
        """View decrypted data (for verification)"""
        data = self.load_site_data()
        if data:
            print("🔓 Decrypted Site Data:")
            print(json.dumps(data, indent=2))
        return data

    # NEW METHODS FOR FLASK API
    def store_site_data(self, data_id, data, notes=None):
        """Store encrypted site data with notes - for Flask API"""
        site_data = {
            "data": data,
            "notes": notes,
            "timestamp": os.times().elapsed
        }
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Encrypt and save
        encrypted_data = self.encryptor.encrypt_data(site_data)
        filename = f"{data_id}.enc"
        
        with open(f'{self.data_dir}/{filename}', 'w') as f:
            f.write(encrypted_data)
        
        return {"message": f"Data stored as {filename}", "id": data_id}
    
    def retrieve_site_data(self, data_id):
        """Retrieve and decrypt site data - for Flask API"""
        filename = f"{data_id}.enc"
        filepath = f'{self.data_dir}/{filename}'
        
        if not os.path.exists(filepath):
            return {"error": f"Data with ID '{data_id}' not found"}
        
        with open(filepath, 'r') as f:
            encrypted_data = f.read()
        
        decrypted_data = self.encryptor.decrypt_data(encrypted_data)
        return decrypted_data
    
    def list_all_data(self):
        """List all stored encrypted data files - for Flask API"""
        if not os.path.exists(self.data_dir):
            return []
        
        files = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.enc') and not filename.endswith('.json.enc'):
                data_id = filename.replace('.enc', '')
                files.append({
                    "id": data_id,
                    "filename": filename,
                    "path": f"{self.data_dir}/{filename}"
                })
        
        return files
    
    def delete_site_data(self, data_id):
        """Delete encrypted site data - for Flask API"""
        filename = f"{data_id}.enc"
        filepath = f'{self.data_dir}/{filename}'
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return {"message": f"Data '{data_id}' deleted"}
        else:
            return {"error": f"Data with ID '{data_id}' not found"}
    
    def decrypt_file(self, filepath):
        """Helper method to decrypt a file"""
        with open(filepath, 'r') as f:
            encrypted_data = f.read()
        return self.encryptor.decrypt_data(encrypted_data)