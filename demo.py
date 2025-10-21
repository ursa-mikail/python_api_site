#!/usr/bin/env python3
"""
Demo script showing encrypted site data usage via Flask API
"""
import os
import sys
import requests
import json
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🔐 Encrypted Site Data API Demo")
    print("=" * 50)
    
    # Check if passcode is set
    if not os.environ.get('LOCAL_PASSCODE_FOR_SITE_DATA'):
        print("❌ Please set LOCAL_PASSCODE_FOR_SITE_DATA environment variable")
        print("   Add to ~/.zshrc: export LOCAL_PASSCODE_FOR_SITE_DATA='your_passcode'")
        print("   Then run: source ~/.zshrc")
        return
    
    # API base URL
    BASE_URL = "http://localhost:5000"
    
    # Test API connection
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Flask API is not running. Start it with: python run.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Flask API is not running. Start it with: python run.py")
        return
    
    print("✅ Flask API is running")
    
    # Demo data to store
    demo_data = [
        {
            "data_id": "site_config",
            "data": json.dumps({
                "name": "Encrypted Demo Site",
                "version": "2.0.0",
                "description": "A demo site with encrypted data storage via API"
            }),
            "notes": "Site configuration settings"
        },
        {
            "data_id": "homepage_content",
            "data": json.dumps({
                "title": "Welcome to Our Secure Demo Site",
                "description": "All data is encrypted and managed via API",
                "features": ["API Encryption", "Secure Storage", "RESTful Endpoints"]
            }),
            "notes": "Homepage content and features"
        },
        {
            "data_id": "user_data",
            "data": json.dumps({
                "preferences": {"theme": "dark", "notifications": True},
                "profile": {"name": "Demo User", "role": "admin"}
            }),
            "notes": "User preferences and profile data"
        },
        {
            "data_id": "api_secrets",
            "data": json.dumps({
                "stripe_key": "sk_test_demo_123456",
                "sendgrid_key": "SG.demo_abc123",
                "database_url": "postgresql://user:pass@localhost/demo_db"
            }),
            "notes": "Encrypted API keys and secrets"
        }
    ]
    
    print("\n1. 📤 Storing encrypted data via API...")
    stored_ids = []
    
    for item in demo_data:
        response = requests.post(
            f"{BASE_URL}/site-data",
            json=item,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Stored: {item['data_id']} - {result['message']}")
            stored_ids.append(item['data_id'])
        else:
            print(f"   ❌ Failed to store {item['data_id']}: {response.json()}")
    
    print(f"\n   📊 Total items stored: {len(stored_ids)}")
    
    # Wait a moment for processing
    time.sleep(1)
    
    print("\n2. 📋 Listing all stored data via API...")
    response = requests.get(f"{BASE_URL}/site-data")
    
    if response.status_code == 200:
        all_data = response.json()
        print(f"   📁 Found {len(all_data)} encrypted files:")
        for item in all_data:
            print(f"      • {item['id']} -> {item['filename']}")
    else:
        print("   ❌ Failed to list data")
        return
    
    print("\n3. 🔍 Retrieving and displaying decrypted data...")
    for data_id in stored_ids:
        response = requests.get(f"{BASE_URL}/site-data/{data_id}")
        
        if response.status_code == 200:
            decrypted_data = response.json()
            print(f"\n   📄 {data_id}:")
            print(f"      Data: {decrypted_data['data']}")
            print(f"      Notes: {decrypted_data['notes']}")
            print(f"      Timestamp: {decrypted_data['timestamp']}")
        else:
            print(f"   ❌ Failed to retrieve {data_id}: {response.json()}")
    
    print("\n4. 🔐 Testing encryption/decryption endpoints...")
    
    # Test encryption
    test_text = "This is a secret message for encryption demo"
    encrypt_response = requests.post(
        f"{BASE_URL}/encrypt",
        json={"data": test_text},
        headers={"Content-Type": "application/json"}
    )
    
    if encrypt_response.status_code == 200:
        encrypt_result = encrypt_response.json()
        encrypted_data = encrypt_result['encrypted_data']
        print(f"   ✅ Encrypted: '{test_text}'")
        print(f"   📦 Encrypted data length: {len(encrypted_data)} characters")
        
        # Test decryption
        decrypt_response = requests.post(
            f"{BASE_URL}/decrypt",
            json={"encrypted_data": encrypted_data},
            headers={"Content-Type": "application/json"}
        )
        
        if decrypt_response.status_code == 200:
            decrypt_result = decrypt_response.json()
            print(f"   ✅ Decrypted: '{decrypt_result['decrypted_data']}'")
            print(f"   🔄 Match: {test_text == decrypt_result['decrypted_data']}")
        else:
            print(f"   ❌ Decryption failed: {decrypt_response.json()}")
    else:
        print(f"   ❌ Encryption failed: {encrypt_response.json()}")
    
    print("\n5. 🗑️  Cleaning up demo data...")
    for data_id in stored_ids:
        response = requests.delete(f"{BASE_URL}/site-data/{data_id}")
        
        if response.status_code == 200:
            print(f"   ✅ Deleted: {data_id} - {response.json()['message']}")
        else:
            print(f"   ❌ Failed to delete {data_id}: {response.json()}")
    
    # Final verification
    print("\n6. ✅ Final verification...")
    response = requests.get(f"{BASE_URL}/site-data")
    if response.status_code == 200:
        remaining_data = response.json()
        print(f"   📊 Remaining encrypted files: {len(remaining_data)}")
        
        if len(remaining_data) == 0:
            print("   🎉 Demo completed successfully! All data cleaned up.")
        else:
            print("   ⚠️  Some data remains (may be from previous runs)")
    
    print("\n" + "=" * 50)
    print("📚 API Endpoints demonstrated:")
    print("   POST /site-data     - Store encrypted data")
    print("   GET  /site-data     - List all data")
    print("   GET  /site-data/:id - Retrieve specific data") 
    print("   DELETE /site-data/:id - Delete data")
    print("   POST /encrypt       - Encrypt data")
    print("   POST /decrypt       - Decrypt data")
    print(f"\n🌐 Visit http://localhost:5000/apidocs for Swagger documentation")

if __name__ == '__main__':
    main()

"""
% python3 demo.py 
🔐 Encrypted Site Data API Demo
==================================================
✅ Flask API is running

1. 📤 Storing encrypted data via API...
   ✅ Stored: site_config - Data stored as site_config.enc
   ✅ Stored: homepage_content - Data stored as homepage_content.enc
   ✅ Stored: user_data - Data stored as user_data.enc
   ✅ Stored: api_secrets - Data stored as api_secrets.enc

   📊 Total items stored: 4

2. 📋 Listing all stored data via API...
   📁 Found 6 encrypted files:
      • user_preferences -> user_preferences.enc
      • site_config -> site_config.enc
      • homepage_content -> homepage_content.enc
      • api_keys -> api_keys.enc
      • api_secrets -> api_secrets.enc
      • user_data -> user_data.enc

3. 🔍 Retrieving and displaying decrypted data...

   📄 site_config:
      Data: {"name": "Encrypted Demo Site", "version": "2.0.0", "description": "A demo site with encrypted data storage via API"}
      Notes: Site configuration settings
      Timestamp: 1761019785.58

   📄 homepage_content:
      Data: {"title": "Welcome to Our Secure Demo Site", "description": "All data is encrypted and managed via API", "features": ["API Encryption", "Secure Storage", "RESTful Endpoints"]}
      Notes: Homepage content and features
      Timestamp: 1761019785.62

   📄 user_data:
      Data: {"preferences": {"theme": "dark", "notifications": true}, "profile": {"name": "Demo User", "role": "admin"}}
      Notes: User preferences and profile data
      Timestamp: 1761019785.65

   📄 api_secrets:
      Data: {"stripe_key": "sk_test_demo_123456", "sendgrid_key": "SG.demo_abc123", "database_url": "postgresql://user:pass@localhost/demo_db"}
      Notes: Encrypted API keys and secrets
      Timestamp: 1761019785.67

4. 🔐 Testing encryption/decryption endpoints...
   ✅ Encrypted: 'This is a secret message for encryption demo'
   📦 Encrypted data length: 120 characters
   ✅ Decrypted: 'This is a secret message for encryption demo'
   🔄 Match: True

5. 🗑️  Cleaning up demo data...
   ✅ Deleted: site_config - Data 'site_config' deleted
   ✅ Deleted: homepage_content - Data 'homepage_content' deleted
   ✅ Deleted: user_data - Data 'user_data' deleted
   ✅ Deleted: api_secrets - Data 'api_secrets' deleted

6. ✅ Final verification...
   📊 Remaining encrypted files: 2
   ⚠️  Some data remains (may be from previous runs)

==================================================
📚 API Endpoints demonstrated:
   POST /site-data     - Store encrypted data
   GET  /site-data     - List all data
   GET  /site-data/:id - Retrieve specific data
   DELETE /site-data/:id - Delete data
   POST /encrypt       - Encrypt data
   POST /decrypt       - Decrypt data

🌐 Visit http://localhost:5000/apidocs for Swagger documentation
"""    