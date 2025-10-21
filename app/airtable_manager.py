import os
from pyairtable import Api  
from .encryption import DataEncryptor

class AirtableManager:
    def __init__(self):
        self.api_key = os.environ.get('AIRTABLE_KEY')
        self.base_id = os.environ.get('AIRTABLE_BASE_ID')
        #https://airtable.com/appML0B7u16CqUuk1/pagHObhsuSP8nLfRx/preview?app_preview=true
        #self.base_id = 'appML0B7u16CqUuk1'
        self.table_id = 'pagHObhsuSP8nLfRx'

        if not self.api_key or not self.base_id:
            raise ValueError("AIRTABLE_KEY and AIRTABLE_BASE_ID environment variables must be set")
        
        #self.api = Api(self.api_key)  # ← CREATES AIRTABLE API CLIENT
        #self.table = self.api.table(self.base_id, 'site_data')  # ← ACCESSES YOUR TABLE
        #self.table = self.api.table(self.base_id, self.table_id)
        # self.encryptor = DataEncryptor()


       # Check if Airtable credentials are set
        if not self.api_key or not self.base_id:
            self.demo_mode = True
            print("⚠️  Airtable credentials not set - running in demo mode")
            self.demo_data = {}
            return
        
        try:
            self.api = Api(self.api_key)
            self.table = self.api.table(self.base_id, 'site_data')
            self.demo_mode = False
            print("✅ Airtable connected successfully")
        except Exception as e:
            print(f"❌ Airtable connection failed: {e}")
            self.demo_mode = True
            self.demo_data = {}
        
        self.encryptor = DataEncryptor()

    
    def store_data(self, key, data, data_type='content'):
        """Store encrypted data in Airtable"""
        encrypted_value = self.encryptor.encrypt_data(data)
        
        # Check if record exists
        existing_records = self.table.all(formula=f"{{key}} = '{key}'")  # ← USES pyairtable
        
        if existing_records:
            # Update existing record
            record_id = existing_records[0]['id']
            self.table.update(record_id, {  # ← USES pyairtable
                'encrypted_value': encrypted_value,
                'data_type': data_type
            })
        else:
            # Create new record
            self.table.create({  # ← USES pyairtable
                'key': key,
                'encrypted_value': encrypted_value,
                'data_type': data_type
            })
    
    def get_data(self, key):
        """Retrieve and decrypt data from Airtable"""
        records = self.table.all(formula=f"{{key}} = '{key}'")  # ← USES pyairtable
        
        if not records:
            return None
        
        encrypted_value = records[0]['fields']['encrypted_value']
        return self.encryptor.decrypt_data(encrypted_value)
    
    def get_all_data(self):
        """Retrieve all data from Airtable"""
        records = self.table.all()  # ← USES pyairtable
        result = {}
        
        for record in records:
            key = record['fields']['key']
            encrypted_value = record['fields']['encrypted_value']
            result[key] = {
                'data': self.encryptor.decrypt_data(encrypted_value),
                'type': record['fields'].get('data_type', 'content'),
                'created': record['fields'].get('created_time'),
                'modified': record['fields'].get('last_modified_time')
            }
        
        return result
    
    def delete_data(self, key):
        """Delete data from Airtable"""
        records = self.table.all(formula=f"{{key}} = '{key}'")  # ← USES pyairtable
        
        if records:
            self.table.delete(records[0]['id'])  # ← USES pyairtable
            return True
        return False



    
    def list_all_data(self):
        """List all stored data"""
        try:
            if self.demo_mode:
                files = []
                for key in self.demo_data.keys():
                    files.append({
                        "id": key,
                        "filename": f"{key}.enc",
                        "path": f"demo:{key}"
                    })
                return files
            else:
                records = self.table.all()
                files = []
                
                for record in records:
                    files.append({
                        "id": record['fields']['key'],
                        "filename": f"{record['fields']['key']}.enc", 
                        "path": f"airtable:{record['fields']['key']}"
                    })
                
                return files
        except Exception as e:
            print(f"Error listing data: {e}")
            return []