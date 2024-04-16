from flask import Flask, request, jsonify
from os import environ
from flasgger import Swagger
from flask_cors import CORS
import boto3
import requests
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

app=Flask(__name__)
CORS(app)

AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")

app.config["SWAGGER"] = {
    "title": "CreateAuction microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Allows interaction with the CreateAuction complex microservice",
}

Swagger=Swagger(app)

@app.route('/s3/create', methods=['POST'])
def s3create():
    """
    Create a image link
    ---
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        file:
                            type: file
                            description: The file to be uploaded (cannot be tested from swagger)
        responses:
            201:
                description: Auction created
            400:
                description: Bad request
    """

    uploaded_file = request.files['file'] # name from the front end 
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket = 'watchauctionimages'

    # Generate a unique key using uuid
    key = str(uuid.uuid4())

    s3.Bucket(bucket).put_object(Body=uploaded_file, Key=key)
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=604800)

    return {"file_key": key, "url": url}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5102, debug=True)