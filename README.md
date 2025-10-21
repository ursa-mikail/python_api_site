# Encrypted Site Data Manager

A simple system for managing encrypted site data using AES-GCM encryption.

## Features

- 🔐 AES-GCM encryption for site data
- 📁 Organized site/data structure
- 🔑 Key derivation using PBKDF2
- 🧪 Comprehensive testing
- 🚀 Easy deployment

## Quick Start

```
project/
├── app/
│   ├── __init__.py
│   ├── routes.py          # Main Flask app with Swagger
│   ├── encryption.py      # AES-GCM encryption
│   └── book_review.py     # Your original Airtable code
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_encryption.py
├── site/
│   └── data/              # Encrypted files
├── requirements.txt
├── runtime.txt
├── .env.example
├── .gitignore
└── README.md
```

1. **Set environment variable:**
   ```bash
   echo 'export LOCAL_PASSCODE_FOR_SITE_DATA="your_secure_passcode_here"' >> ~/.zshrc
   source ~/.zshrc

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Build encrypted site data:

```
python build.py
```

4. Verify encryption:

```
python -c "from app.site_manager import SiteManager; sm = SiteManager(); sm.view_decrypted_data()"
```

5. Testing

```
% python -m unittest discover tests
...✅ Site data built and encrypted successfully!
📁 Encrypted files saved to: site/data/
.
----------------------------------------------------------------------
Ran 4 tests in 0.331s

OK
```

6. Run demo

```
% python3 demo.py
🔐 Encrypted Site Data Demo
========================================

1. Building encrypted site data...
✅ Site data built and encrypted successfully!
📁 Encrypted files saved to: site/data/

2. Displaying decrypted data...
🔓 Decrypted Site Data:
{
  "site_config": {
    "name": "Encrypted Site",
    "version": "1.0.0",
    "description": "A site with encrypted data storage"
  },
  "content_data": {
    "home": {
      "title": "Welcome to Our Secure Site",
      "description": "All data is encrypted for security",
      "features": [
        "Secure Data",
        "Encrypted Storage",
        "Privacy Focused"
      ]
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

3. Demo completed successfully! 🎉
   Site Name: Encrypted Site
   Version: 1.0.0
   Home Title: Welcome to Our Secure Site
   Features: Secure Data, Encrypted Storage, Privacy Focused
   Secrets: 2 API keys encrypted

```

7. Curl

```
# Encrypt data
curl -X POST http://localhost:5000/encrypt \
  -H "Content-Type: application/json" \
  -d '{"data": "My secret site data"}'

# Store encrypted site data  
curl -X POST http://localhost:5000/site-data \
  -H "Content-Type: application/json" \
  -d '{"data_id": "homepage_content", "data": "Welcome to my site", "notes": "Main page content"}'

# List all stored data
curl http://localhost:5000/site-data

# Retrieve specific data
curl http://localhost:5000/site-data/homepage_content
```

```
% # Step 1: Encrypt
ENCRYPTED=$(curl -s -X POST "http://localhost:5000/encrypt" \
  -H "Content-Type: application/json" \
  -d '{"data": "My secret website content - by ursa"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['encrypted_data'])")

echo "Encrypted data: $ENCRYPTED"

# Step 2: Decrypt
 % curl -X POST "http://localhost:5000/decrypt" \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_data\": \"$ENCRYPTED\"}"
{
    "decrypted_data": "My secret website content",
    "encrypted_data": "h2Y8AJZBB1tzTndzTpbMHUIgMXGyY7zBpNZe4iXU392M5gFQ/SNAeYdJKHKuQKUa2MnQ1gCPyJa/JBzpRny5jvZ5QDbd"
}


```

4. List Before and After Delete

```
# List all data first
curl "http://localhost:5000/site-data"

# Delete one
curl -X DELETE "http://localhost:5000/site-data/homepage_content"

# List again to confirm it's gone
curl "http://localhost:5000/site-data"
```

5. Complete Cleanup Example

```
# Delete all test data
curl -X DELETE "http://localhost:5000/site-data/homepage_content"
curl -X DELETE "http://localhost:5000/site-data/site_config" 
curl -X DELETE "http://localhost:5000/site-data/user_data"
curl -X DELETE "http://localhost:5000/site-data/secret_keys"

# Verify everything is deleted
curl "http://localhost:5000/site-data"
```

Add Data and List
1. Add Multiple Site Data Entries

```
# Add homepage content
curl -X POST "http://localhost:5000/site-data" \
  -H "Content-Type: application/json" \
  -d '{
    "data_id": "homepage_content",
    "data": "Welcome to My Encrypted Website! This is the main content.",
    "notes": "Homepage hero section content"
  }'

# Add site configuration
curl -X POST "http://localhost:5000/site-data" \
  -H "Content-Type: application/json" \
  -d '{
    "data_id": "site_config", 
    "data": "{\"theme\": \"dark\", \"language\": \"en\", \"features\": [\"encryption\", \"secure\"]}",
    "notes": "Site configuration settings"
  }'

# Add user data
curl -X POST "http://localhost:5000/site-data" \
  -H "Content-Type: application/json" \
  -d '{
    "data_id": "user_preferences",
    "data": "{\"notifications\": true, \"privacy_level\": \"high\", \"auto_backup\": false}",
    "notes": "User preference settings"
  }'

# Add API keys (encrypted)
curl -X POST "http://localhost:5000/site-data" \
  -H "Content-Type: application/json" \
  -d '{
    "data_id": "api_keys",
    "data": "{\"stripe\": \"sk_test_123456\", \"sendgrid\": \"SG.abc123\", \"aws\": \"AKIAIOSFODNN7EXAMPLE\"}",
    "notes": "Encrypted API keys for services"
  }'
```

2. List All Stored Data
```
curl "http://localhost:5000/site-data"
```

3. Retrieve Specific Data to Verify

```
# Get homepage content
curl "http://localhost:5000/site-data/homepage_content"

# Get site config
curl "http://localhost:5000/site-data/site_config"

# Get API keys
curl "http://localhost:5000/site-data/api_keys"
```


# AIRTABLE_KEY

```
https://airtable.com/create/tokens/new

data.records:read
See the data in records

data.records:write
Create, edit, and delete records

add base:

My First Workspace
Encrypted Site Data

```
```
Click "Add a base" → "Start from scratch"

Name it: Encrypted Site Data

Click "Create base"

2. Set up Your Table Structure
You need ONE table. Here's how to create it:

In your Airtable base:

Table name: site_data (rename the default "Table 1")

Add these fields:

Field Name  Field Type  Description
key   Single line text  Unique identifier for each data entry
encrypted_value   Long text   The encrypted data (this will store your ciphered data)
data_type   Single select  Type: config, content, secrets, user_data
created_time   Created time   (Auto-generated - don't need to create)
last_modified  Last modified time   (Auto-generated - don't need to create)
To add fields:

Click "+" next to existing fields

Choose field type

Name the field

For data_type, set options: config, content, secrets, user_data
```


# RENDER

```
https://dashboard.render.com/
```
