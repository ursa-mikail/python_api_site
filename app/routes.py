from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
import os

from .encryption import DataEncryptor
from .site_manager import SiteManager

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

encryptor = DataEncryptor()
site_manager = SiteManager()

class EncryptData(Resource):
    def post(self):
        """
        Encrypt data using AES-GCM
        ---
        tags:
        - Encryption
        parameters:
            - in: body
              name: body
              required: true
              schema:
                id: EncryptionRequest
                required:
                  - data
                properties:
                  data:
                    type: string
                    description: The data to encrypt
        responses:
            200:
                description: Successfully encrypted data
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                encrypted_data:
                                    type: string
                                    description: The encrypted data
                                original_data:
                                    type: string
                                    description: The original data
            400:
                description: Bad request if data is missing
        """
        data = request.json

        if not data:
            return {"error": "Request body must be in JSON format."}, 400

        data_to_encrypt = data.get('data')
        if not data_to_encrypt:
            return {"error": "Data field is required."}, 400
        
        encrypted_data = encryptor.encrypt_data(data_to_encrypt)
        
        return {
            "encrypted_data": encrypted_data,
            "original_data": data_to_encrypt
        }, 200

class DecryptData(Resource):
    def post(self):
        """
        Decrypt data using AES-GCM
        ---
        tags:
        - Encryption
        parameters:
            - in: body
              name: body
              required: true
              schema:
                id: DecryptionRequest
                required:
                  - encrypted_data
                properties:
                  encrypted_data:
                    type: string
                    description: The encrypted data to decrypt
        responses:
            200:
                description: Successfully decrypted data
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                decrypted_data:
                                    type: string
                                    description: The decrypted data
                                encrypted_data:
                                    type: string
                                    description: The original encrypted data
            400:
                description: Bad request if encrypted_data is missing
        """
        data = request.json

        if not data:
            return {"error": "Request body must be in JSON format."}, 400

        encrypted_data = data.get('encrypted_data')
        if not encrypted_data:
            return {"error": "encrypted_data field is required."}, 400
        
        try:
            decrypted_data = encryptor.decrypt_data(encrypted_data)
            
            return {
                "decrypted_data": decrypted_data,
                "encrypted_data": encrypted_data
            }, 200
        except Exception as e:
            return {"error": f"Decryption failed: {str(e)}"}, 400

class StoreSiteData(Resource):
    def post(self):
        """
        Store encrypted site data with notes
        ---
        tags:
        - Site Data
        parameters:
            - in: body
              name: body
              required: true
              schema:
                id: StoreSiteDataRequest
                required:
                  - data_id
                  - data
                properties:
                  data_id:
                    type: string
                    description: Unique identifier for the data
                  data:
                    type: string
                    description: The data to encrypt and store
                  notes:
                    type: string
                    description: Optional notes about the data
        responses:
            200:
                description: Successfully stored encrypted data
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
                                    description: Success message
                                id:
                                    type: string
                                    description: The data ID
            400:
                description: Bad request if required fields are missing
        """
        data = request.json

        if not data:
            return {"error": "Request body must be in JSON format."}, 400

        data_id = data.get('data_id')
        data_to_store = data.get('data')
        notes = data.get('notes')

        if not data_id or not data_to_store:
            return {"error": "Both 'data_id' and 'data' fields are required."}, 400
        
        result = site_manager.store_site_data(data_id, data_to_store, notes)
        return result, 200

class RetrieveSiteData(Resource):
    def get(self, data_id):
        """
        Retrieve and decrypt site data
        ---
        tags:
        - Site Data
        parameters:
            - name: data_id
              in: path
              type: string
              required: true
              description: The ID of the data to retrieve
        responses:
            200:
                description: Successfully retrieved decrypted data
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                data:
                                    type: string
                                    description: The decrypted data
                                notes:
                                    type: string
                                    description: The stored notes
                                timestamp:
                                    type: number
                                    description: When the data was stored
            404:
                description: Data not found
        """
        result = site_manager.retrieve_site_data(data_id)
        if 'error' in result:
            return result, 404
        return result, 200

class ListSiteData(Resource):
    def get(self):
        """
        List all stored encrypted data files
        ---
        tags:
        - Site Data
        responses:
            200:
                description: List of all encrypted data files
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: string
                                        description: The data ID
                                    filename:
                                        type: string
                                        description: The encrypted filename
                                    path:
                                        type: string
                                        description: The file path
        """
        files = site_manager.list_all_data()
        return files, 200

class DeleteSiteData(Resource):
    def delete(self, data_id):
        """
        Delete encrypted site data
        ---
        tags:
        - Site Data
        parameters:
            - name: data_id
              in: path
              type: string
              required: true
              description: The ID of the data to delete
        responses:
            200:
                description: Successfully deleted data
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
                                    description: Success message
            404:
                description: Data not found
        """
        result = site_manager.delete_site_data(data_id)
        if 'error' in result:
            return result, 404
        return result, 200

# Register all routes
api.add_resource(EncryptData, "/encrypt")
api.add_resource(DecryptData, "/decrypt")
api.add_resource(StoreSiteData, "/site-data")
api.add_resource(RetrieveSiteData, "/site-data/<string:data_id>")
api.add_resource(ListSiteData, "/site-data")
api.add_resource(DeleteSiteData, "/site-data/<string:data_id>")

@app.route('/')
def home():
    return """
    <h1>Encrypted Site Data API</h1>
    <p>Visit <a href="/apidocs">/apidocs</a> for Swagger documentation</p>
    <p>Endpoints:</p>
    <ul>
        <li>POST /encrypt - Encrypt data</li>
        <li>POST /decrypt - Decrypt data</li>
        <li>POST /site-data - Store encrypted site data</li>
        <li>GET /site-data - List all stored data</li>
        <li>GET /site-data/{id} - Retrieve specific data</li>
        <li>DELETE /site-data/{id} - Delete data</li>
    </ul>
    """

if __name__ == "__main__":
    app.run(debug=True)
    