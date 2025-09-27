from . import config
from .utils import debug
from .auth import AuthManager


class NetSuiteClient:
    def __init__(self, session):
        self.session = session
        self.auth = AuthManager(session)

    def _request(self, method, endpoint, **kwargs):
        token = self.auth.get_access_token()
        if not token:
            debug("❌ No valid token")
            return None
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        url = f"{config.BASE_URL}/{endpoint}"
        try:
            resp = self.session.request(method, url, headers=headers, timeout=30, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            debug(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response:
                debug(f"HTTP {e.response.status_code}: {e.response.text}")
            return None

    def get_employee(self, employee_id):
        return self._request("GET", f"employee/{employee_id}")

    def test_connection(self, auth_code=None):
        return bool(self.auth.get_access_token(auth_code))
