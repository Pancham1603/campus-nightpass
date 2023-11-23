from dotenv import load_dotenv
import os

load_dotenv()
config = {
  "web": {
    "client_id": str(os.getenv('CLIENT_ID')),
    "project_id": "thapar-nightpass",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": str(os.getenv('CLIENT_SECRET')),
    "redirect_uris": [
      "http://127.0.0.1:8000/accounts/google/login/callback/",
      "http://localhost:8000/accounts/google/login/callback/",
    ],
    "javascript_origins": ["http://localhost:8000", "http://127.0.0.1:8000"]
  }
}
