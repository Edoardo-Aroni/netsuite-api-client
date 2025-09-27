import os
import time
from urllib.parse import urlparse, parse_qs, quote, unquote
import requests
from . import config
from .utils import debug, generate_state


class AuthManager:
    def __init__(self, session):
        self.session = session
        self.access_token = None
        self.refresh_token = os.getenv("NS_REFRESH_TOKEN")
        self.token_expiry = None
        self.current_state = None

    def get_authorize_url(self, scope="rest_webservices restlets"):
        self.current_state = generate_state()
        return (f"https://{config.ACCOUNT_ID}.app.netsuite.com/app/login/oauth2/authorize.nl"
                f"?response_type=code&client_id={config.CLIENT_ID}"
                f"&redirect_uri={quote(config.REDIRECT_URI)}"
                f"&scope={quote(scope)}&state={quote(self.current_state)}")

    def handle_callback(self, callback_url):
        params = parse_qs(urlparse(callback_url).query)
        if "error" in params:
            debug(f"OAuth error: {params['error'][0]}")
            return None
        state = unquote(params.get("state", [""])[0])
        if state != self.current_state:
            debug("❌ State mismatch")
            return None
        return params.get("code", [None])[0]

    def _request_token(self, data):
        try:
            resp = self.session.post(
                config.TOKEN_URL,
                auth=(config.CLIENT_ID, config.CLIENT_SECRET),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=data, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            debug(f"Token request failed: {e}")
            if hasattr(e, 'response') and e.response:
                debug(f"HTTP {e.response.status_code}: {e.response.text}")
            return None

    def get_access_token(self, auth_code=None):
        if self.access_token and time.time() < (self.token_expiry or 0):
            return self.access_token

        if self.refresh_token:
            data = {"grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "redirect_uri": config.REDIRECT_URI}
        elif auth_code:
            data = {"grant_type": "authorization_code",
                    "code": auth_code,
                    "redirect_uri": config.REDIRECT_URI}
        else:
            return None

        token_data = self._request_token(data)
        if not token_data or "access_token" not in token_data:
            return None

        self.access_token = token_data["access_token"]
        expires_in = int(token_data.get("expires_in", 3600)) - 300
        self.token_expiry = time.time() + expires_in

        if "refresh_token" in token_data:
            self.refresh_token = token_data["refresh_token"]
            with open(".refresh_token", "w") as f:
                f.write(self.refresh_token)

        return self.access_token

    def load_refresh_token(self):
        if os.path.exists(".refresh_token"):
            with open(".refresh_token") as f:
                self.refresh_token = f.read().strip()
