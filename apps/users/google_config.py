from dotenv import load_dotenv
import os

load_dotenv()

# Get environment variables with validation
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Validate that required environment variables are set
if not CLIENT_ID:
    raise ValueError("CLIENT_ID environment variable is not set. Please check your .env file.")
    
if not CLIENT_SECRET:
    raise ValueError("CLIENT_SECRET environment variable is not set. Please check your .env file.")

config = {
  "web": {
    "client_id": CLIENT_ID,
    "project_id": "thapar-nightpass",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": CLIENT_SECRET,
    "javascript_origins": ["http://localhost:8000", "http://127.0.0.1:8000"]
  }
}
