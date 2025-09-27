import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.getenv("NS_ACCOUNT_ID")
CLIENT_ID = os.getenv("NS_CLIENT_ID")
CLIENT_SECRET = os.getenv("NS_CLIENT_SECRET")
REDIRECT_URI = os.getenv("NS_REDIRECT_URI")

TOKEN_URL = f"https://{ACCOUNT_ID}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"
BASE_URL = f"https://{ACCOUNT_ID}.suitetalk.api.netsuite.com/services/rest/record/v1"
